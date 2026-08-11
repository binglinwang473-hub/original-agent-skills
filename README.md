# 我的原创 Agent Skills

这里集中保存原创的 Agent Skill 与可恢复内容生产工作流。

项目目前处于早期公开阶段，由创建者维护。仓库不声称拥有下载量或广泛采用数据；重点是把 Agent 指令、文件操作边界、人工确认和可恢复状态整理成可以检查、测试和继续维护的公开材料。

## 包含内容

### Daoist Video Skill

路径：`skills/daoist-video-skill/`

面向中文东方哲思短视频的可恢复生产流水线。它把一条视频拆成选题简报、脚本、分镜、声音预览、素材、合成、质检和发布准备等阶段，在计划、分镜和声音节点暂停等待人工确认，并用状态文件记录产物、重试次数、远程任务和费用。

## 原创范围

`daoist-video-skill/` 保留原创方法论、代码、示例内容和 Skill 指令；本仓库不包含本机虚拟环境、缓存音频或带本机绝对路径的状态文件。

## 开发检查

```bash
python3 -m unittest discover -s skills/daoist-video-skill/tests -v
python3 -m py_compile skills/daoist-video-skill/pipeline.py
```

提交 Skill 或脚本前，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [SECURITY.md](SECURITY.md)。
