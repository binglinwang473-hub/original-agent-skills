#!/usr/bin/env python3
"""Generate a short VoxCPM2 high-fidelity voice-clone audition."""

from __future__ import annotations

import argparse
from pathlib import Path

import soundfile as sf
from voxcpm import VoxCPM


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-audio", required=True, type=Path)
    parser.add_argument("--prompt-text", required=True, type=Path)
    parser.add_argument("--reference-audio", required=True, type=Path)
    parser.add_argument("--model-id", default="openbmb/VoxCPM2")
    parser.add_argument("--text", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--device", default="mps")
    parser.add_argument("--inference-timesteps", type=int, default=10)
    parser.add_argument("--cfg-value", type=float, default=2.0)
    parser.add_argument("--no-optimize", action="store_true")
    args = parser.parse_args()

    prompt_text = args.prompt_text.read_text(encoding="utf-8").strip()
    model = VoxCPM.from_pretrained(
        args.model_id,
        device=args.device,
        optimize=not args.no_optimize,
        load_denoiser=False,
    )
    print("生成高保真短试听…", flush=True)
    generation_args = dict(
        text=args.text,
        prompt_wav_path=str(args.prompt_audio),
        prompt_text=prompt_text,
        cfg_value=args.cfg_value,
        inference_timesteps=args.inference_timesteps,
        normalize=False,
        retry_badcase=True,
    )
    if "VoxCPM2" in args.model_id:
        generation_args["reference_wav_path"] = str(args.reference_audio)
    wav = model.generate(**generation_args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(args.output, wav, model.tts_model.sample_rate)
    print(f"试听已生成：{args.output} ({len(wav) / model.tts_model.sample_rate:.2f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
