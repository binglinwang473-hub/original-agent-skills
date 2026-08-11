#!/usr/bin/env python3
"""Small, dependency-free state machine for the Daoist Video Skill MVP."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / "state"
CONFIG_PATH = ROOT / "pipeline_config.json"
VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def validate_video_id(video_id: str) -> str:
    """Allow only portable task IDs that cannot escape the state directory."""
    if not isinstance(video_id, str) or not VIDEO_ID_PATTERN.fullmatch(video_id):
        raise ValueError(
            "video_id must start with a letter or digit and contain only "
            "letters, digits, '.', '_' or '-' (max 128 characters)"
        )
    return video_id


def state_path(video_id: str) -> Path:
    return STATE_DIR / f"{validate_video_id(video_id)}.json"


def load_state(video_id: str) -> dict:
    path = state_path(video_id)
    if not path.exists():
        raise SystemExit(f"找不到任务：{video_id}。先运行 init {video_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = state_path(state["video_id"])
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def stage_record(status: str = "pending") -> dict:
    return {
        "status": status,
        "started_at": None,
        "completed_at": None,
        "attempts": 0,
        "remote_task_id": None,
        "cost_points": 0,
        "artifacts": [],
        "error": None,
    }


def init_task(video_id: str) -> None:
    path = state_path(video_id)
    if path.exists():
        raise SystemExit(f"任务已存在：{video_id}")
    config = load_config()
    stages = {name: stage_record() for name in config["stages"]}
    stages["brief"]["status"] = "ready"
    state = {
        "video_id": video_id,
        "created_at": now(),
        "updated_at": now(),
        "current_stage": "brief",
        "stages": stages,
        "global": {
            "account": config["project_name"],
            "input_hash": None,
            "notes": [],
        },
    }
    save_state(state)
    print(f"已创建任务：{video_id}")
    print(f"状态文件：{path}")


def stage_index(config: dict, name: str) -> int:
    try:
        return config["stages"].index(name)
    except ValueError:
        raise SystemExit(f"未知阶段：{name}")


def advance_to(state: dict, target: str) -> None:
    config = load_config()
    stages = config["stages"]
    target_i = stage_index(config, target)
    current_i = stage_index(config, state["current_stage"])
    if target_i < current_i:
        raise SystemExit(f"不能回退阶段：{state['current_stage']} → {target}")
    for name in stages[:target_i]:
        if state["stages"][name]["status"] not in {"done", "approved", "ready"}:
            raise SystemExit(f"阶段 {name} 尚未完成，不能进入 {target}")
    state["current_stage"] = target
    state["stages"][target]["status"] = "running"
    state["stages"][target]["started_at"] = state["stages"][target]["started_at"] or now()


def approve(video_id: str, checkpoint: str) -> None:
    state = load_state(video_id)
    mapping = {
        "plan": ("plan_review", "script"),
        "storyboard": ("storyboard_review", "voice_preview"),
        "voice-preview": ("voice_review", "voice_lock"),
        "voice": ("voice_review", "voice_lock"),
    }
    if checkpoint not in mapping:
        raise SystemExit("确认点必须是 plan、storyboard、voice-preview 或 voice")
    current, next_stage = mapping[checkpoint]
    if state["current_stage"] != current:
        raise SystemExit(f"当前阶段是 {state['current_stage']}，不是 {current}")
    state["stages"][current]["status"] = "approved"
    state["stages"][current]["completed_at"] = now()
    if next_stage != current:
        advance_to(state, next_stage)
    state["updated_at"] = now()
    save_state(state)
    print(f"已确认 {checkpoint}，进入 {next_stage}")


def set_artifact(video_id: str, stage: str, artifact: str) -> None:
    set_artifact_with_options(video_id, stage, artifact, allow_external=False)


def set_artifact_with_options(
    video_id: str,
    stage: str,
    artifact: str,
    *,
    allow_external: bool,
) -> None:
    state = load_state(video_id)
    path = Path(artifact).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    else:
        path = path.resolve()
    if not path.is_file():
        raise SystemExit(f"文件不存在：{path}")
    if not allow_external:
        try:
            path.relative_to(ROOT)
        except ValueError as exc:
            raise ValueError(
                "artifact must be inside the skill directory by default; "
                "pass --allow-external-path only after checking the file"
            ) from exc
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rec = state["stages"].get(stage)
    if rec is None:
        raise SystemExit(f"未知阶段：{stage}")
    item = {"path": str(path), "sha256": digest, "recorded_at": now()}
    def normalized(item_path: str) -> str:
        candidate = Path(item_path).expanduser()
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        return str(candidate.resolve())
    rec["artifacts"] = [
        x for x in rec["artifacts"] if normalized(x["path"]) != str(path)
    ] + [item]
    rec["status"] = "done"
    rec["completed_at"] = now()
    config = load_config()
    if state["current_stage"] == stage:
        current_i = stage_index(config, stage)
        if current_i + 1 < len(config["stages"]):
            next_stage = config["stages"][current_i + 1]
            state["current_stage"] = next_stage
            state["stages"][next_stage]["status"] = "ready"
            state["stages"][next_stage]["started_at"] = now()
    state["updated_at"] = now()
    save_state(state)
    print(f"已记录产物：{stage} ← {path}")


def set_remote_task(video_id: str, stage: str, task_id: str, cost: float = 0) -> None:
    if not math.isfinite(cost) or cost < 0:
        raise ValueError("cost must be a finite non-negative number")
    state = load_state(video_id)
    rec = state["stages"].get(stage)
    if rec is None:
        raise SystemExit(f"未知阶段：{stage}")
    rec["remote_task_id"] = task_id
    rec["cost_points"] = cost
    rec["attempts"] += 1
    rec["status"] = "waiting_remote"
    state["updated_at"] = now()
    save_state(state)
    print(f"已记录远程任务：{stage} ← {task_id}")


def status(video_id: str) -> None:
    state = load_state(video_id)
    print(f"任务：{video_id}")
    print(f"当前阶段：{state['current_stage']}")
    print(f"更新时间：{state['updated_at']}")
    print()
    for name, rec in state["stages"].items():
        marker = "✓" if rec["status"] in {"done", "approved"} else "→" if name == state["current_stage"] else "·"
        extra = f"，产物 {len(rec['artifacts'])} 个" if rec["artifacts"] else ""
        if rec["remote_task_id"]:
            extra += f"，远程任务 {rec['remote_task_id']}"
        print(f"{marker} {name}: {rec['status']}{extra}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Daoist Video Skill pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("video_id")

    p = sub.add_parser("status")
    p.add_argument("video_id", nargs="?", default="2026-08-09-first-video")

    p = sub.add_parser("approve")
    p.add_argument("checkpoint", choices=["plan", "voice-preview", "voice", "storyboard"])
    p.add_argument("--video-id", default="2026-08-09-first-video")

    p = sub.add_parser("set-artifact")
    p.add_argument("stage")
    p.add_argument("artifact")
    p.add_argument("--video-id", default="2026-08-09-first-video")
    p.add_argument(
        "--allow-external-path",
        action="store_true",
        help="allow an artifact outside this skill directory after manual review",
    )

    p = sub.add_parser("set-remote-task")
    p.add_argument("stage")
    p.add_argument("task_id")
    p.add_argument("--cost", type=float, default=0)
    p.add_argument("--video-id", default="2026-08-09-first-video")

    args = parser.parse_args()
    if args.command == "init":
        init_task(args.video_id)
    elif args.command == "status":
        status(args.video_id)
    elif args.command == "approve":
        approve(args.video_id, args.checkpoint)
    elif args.command == "set-artifact":
        set_artifact_with_options(
            args.video_id,
            args.stage,
            args.artifact,
            allow_external=args.allow_external_path,
        )
    elif args.command == "set-remote-task":
        set_remote_task(args.video_id, args.stage, args.task_id, args.cost)


if __name__ == "__main__":
    main()
