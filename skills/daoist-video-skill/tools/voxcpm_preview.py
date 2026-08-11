#!/usr/bin/env python3
"""Generate a local VoxCPM audition file for human pacing/pronunciation review."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local VoxCPM voice preview")
    parser.add_argument("--text", required=True, type=Path, help="Text file passed to VoxCPM")
    parser.add_argument("--output", required=True, type=Path, help="Output WAV path")
    parser.add_argument("--device", default="auto", choices=["auto", "mps", "cpu", "cuda"])
    parser.add_argument("--reference-audio", type=Path, help="Optional reference audio for cloning")
    parser.add_argument("--no-optimize", action="store_true", help="Disable torch.compile-style optimization")
    args = parser.parse_args()

    if not args.text.exists():
        print(f"文本不存在：{args.text}", file=sys.stderr)
        return 2
    voxcpm_bin = shutil.which("voxcpm") or str(Path(sys.executable).with_name("voxcpm"))
    if not Path(voxcpm_bin).exists():
        print("未找到 voxcpm。请先在独立 Python 3.10–3.12 环境安装 VoxCPM。", file=sys.stderr)
        print("官方安装：pip install voxcpm", file=sys.stderr)
        return 3
    if args.reference_audio and not args.reference_audio.exists():
        print(f"参考音频不存在：{args.reference_audio}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    text = args.text.read_text(encoding="utf-8").strip()
    if args.reference_audio:
        command = [
            voxcpm_bin, "clone", "--text", text,
            "--reference-audio", str(args.reference_audio),
            "--output", str(args.output), "--device", args.device,
        ]
    else:
        command = [
            voxcpm_bin, "design", "--text", text,
            "--output", str(args.output), "--device", args.device,
        ]
    if args.no_optimize:
        command.append("--no-optimize")

    print("运行：", " ".join(command[:4]), "…")
    subprocess.run(command, check=True)
    print(f"试听已生成：{args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
