# Daoist Video Skill（第一版）

这是一个面向中文短视频的、可恢复的原创东方哲思内容生产流水线。

第一版目标不是无人值守批量发布，而是把一条视频拆成有记录的阶段，并在三个节点停下来等待人工确认：

1. 计划确认
2. 分镜图确认
3. 声音确认

## 当前默认规格

- 账号方向：东方哲思 / 道家启发 / 日常关系与情绪
- 画幅：1080 × 1920，9:16
- 时长：30–60 秒
- 结构：开头钩子 + 观点展开 + 结尾留白
- 画面：5 个镜头，保持同一套人设和视觉基调
- 输出：视频、逐字字幕、封面、标题、发布文案

## 目录

```text
daoist-video-skill/
├── account_bible.md          # 账号人设、禁区、视觉规范
├── pipeline.py                # 状态机与任务记录 CLI
├── pipeline_config.json       # 输出规格和阶段配置
├── content/
│   └── 2026-08-09-first-video/
│       ├── brief.md           # 选题简报
│       ├── script.md          # 原创口播稿
│       ├── storyboard.md      # 五镜头分镜
│       └── publish.md         # 发布文案
└── state/
    └── 2026-08-09-first-video.json
```

## 使用

在本目录运行：

```bash
python3 pipeline.py status
python3 pipeline.py approve plan
python3 pipeline.py approve storyboard
python3 pipeline.py approve voice
python3 pipeline.py set-artifact script content/2026-08-09-first-video/script.md
python3 pipeline.py set-artifact storyboard content/2026-08-09-first-video/storyboard.md
python3 pipeline.py status
```

`pipeline.py` 会把每个阶段的状态、输入输出、任务 ID、费用和重试次数写入 `state/`。重复执行不会重新提交已经完成的阶段；外部付费任务的 ID 可以用 `set-remote-task` 写入，方便中断后继续。

## 后续接入

- 配音：可接 `narrator-ai-cli` 或其他 TTS 服务
- 生图：接入图像生成服务，先生成五张分镜图并停在 `storyboard` 确认点
- 合成：使用 FFmpeg，把配音、图片、字幕和 BGM 合成 MP4
- 发布：第一阶段只生成发布包，不自动操作平台账号

任何付费任务都应先执行预算检查并等待人工确认。
