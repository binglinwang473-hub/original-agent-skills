# VoxCPM 本地试听

## 目的

先用本地 VoxCPM 产出试听稿，只确认：

1. 语速是否能落在约 38–42 秒。
2. 逗号、句号和换行形成的停顿是否自然。
3. “道家、知止、睡眠、精神”等词的读音是否准确。
4. 低沉、克制、略带古意的表演是否贴合原视频，而不是变成夸张古装腔。

## 试听文本

初版使用同目录的 `voice_preview_text.txt`。因 V3 吐字不准，修正版改用 `voice_preview_phonemes.txt`，逐句生成并显式控制拼音声调。

## 原视频参考人声

- 来源视频：`/Users/bl/Downloads/KERVYykQjbEKPVt2.mp4`
- 原始音轨提取：`assets/audio/reference/KERVYykQjbEKPVt2-voice-reference.wav`
- 人声分离参考：`assets/audio/reference/KERVYykQjbEKPVt2-vocals-reference.wav`
- 处理方式：先提取 AAC 音轨，再用 Demucs 分离 vocals；VoxCPM 优先使用分离后的人声参考

## 推荐初始参数

- VoxCPM 2
- `device=auto`；Apple Silicon 可优先尝试 MPS
- `inference_timesteps=10`
- `cfg_value=2.0`
- 先不做音频后处理，先听原始语速、停顿和发音

## 锁定规则

试听通过后，人工填写：

- 试听文件路径
- 实际时长
- 语速调整结论
- 需要改写或标注读音的词
- ChatCut 最终音色和真实 `voiceId`

## V1 试听产物

- 文件：`assets/audio/2026-08-09-first-video/voxcpm-preview-v1.wav`
- 时长：31.2 秒
- 状态：待人工试听确认

## 参考音色试听对比

- V2：`assets/audio/2026-08-09-first-video/voxcpm-preview-v2-reference.wav`，使用原始混合音轨参考，30.72 秒
- V3：`assets/audio/2026-08-09-first-video/voxcpm-preview-v3-vocals.wav`，使用分离后人声参考，30.56 秒，待人工确认
- V4：`assets/audio/2026-08-09-first-video/voxcpm-preview-v4-phonemes.wav`，逐句 + 拼音音素控制，32.22 秒，待人工确认

然后运行：

```bash
python3 pipeline.py set-artifact voice_preview <试听音频路径>
python3 pipeline.py approve voice --video-id 2026-08-09-first-video
python3 pipeline.py set-artifact voice_lock content/2026-08-09-first-video/voice_selection.md
```

没有完成试听复核前，不提交 ChatCut TTS。
