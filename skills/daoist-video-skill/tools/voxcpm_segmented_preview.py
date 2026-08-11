#!/usr/bin/env python3
"""Generate a pronunciation-controlled VoxCPM preview sentence by sentence."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
from voxcpm import VoxCPM


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--segments", required=True, type=Path)
    parser.add_argument("--reference-audio", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--device", default="mps")
    parser.add_argument("--pause-ms", type=int, default=260)
    parser.add_argument("--inference-timesteps", type=int, default=4)
    parser.add_argument("--cfg-value", type=float, default=2.0)
    args = parser.parse_args()

    segments = [x.strip() for x in args.segments.read_text(encoding="utf-8").split("\n\n") if x.strip()]
    model = VoxCPM.from_pretrained(
        "openbmb/VoxCPM2",
        device=args.device,
        optimize=False,
        load_denoiser=False,
    )
    silence = np.zeros(int(model.tts_model.sample_rate * args.pause_ms / 1000), dtype=np.float32)
    chunks = []
    for index, segment in enumerate(segments, start=1):
        print(f"生成第 {index}/{len(segments)} 句", flush=True)
        wav = model.generate(
            text=segment,
            reference_wav_path=str(args.reference_audio),
            cfg_value=args.cfg_value,
            inference_timesteps=args.inference_timesteps,
            normalize=False,
            retry_badcase=True,
        )
        chunks.append(np.asarray(wav, dtype=np.float32))
        if index != len(segments):
            chunks.append(silence)
    audio = np.concatenate(chunks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(args.output, audio, model.tts_model.sample_rate)
    print(f"试听已生成：{args.output} ({len(audio) / model.tts_model.sample_rate:.2f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
