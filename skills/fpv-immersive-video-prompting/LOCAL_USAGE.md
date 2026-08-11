# 本地使用说明

这个仓库是一个 AI 视频提示词 Skill，不是视频生成软件。

它的用途是：当你要做 FPV、一镜到底、猫/狗/无人机/机器人视角、红线路径飞行、多人依次互动视频时，让 Codex/Claude/Cursor 根据 `SKILL.md` 生成更稳定的视频提示词和 GPT Image 资产包提示词。

## 最简单用法

把需求直接发给 Codex，并明确说使用这个 skill：

```text
使用 `skills/fpv-immersive-video-prompting/SKILL.md` 的方法，
帮我做一个咖啡厅里 3 个人依次互动的 FPV 视频提示词，15 秒，猫咪视角。
```

Codex 应输出：

1. GPT Image 资产包 prompt
2. 图片数量说明
3. 视频生成 prompt
4. negative prompt / 避免项
5. 使用步骤

## 推荐输入格式

```text
使用 FPV 运镜导演 skill。

场景：
时长：
比例：
POV 视角：
主要人物/目标数量：
路线：
最终停在哪里：
使用的视频模型：
是否需要 GPT Image 首帧/参考图：
风格：
必须避免：
```

## 两种模式

### 1. 编号停靠点模式

适合：

- 咖啡厅、客厅、展厅、庭院、宫殿等室内场景
- 多个人物依次互动
- 猫、狗、机器人吸尘器、人类访客等近距离 POV

核心做法：

- 首帧图里只放小编号 1、2、3
- 不画红线
- 视频 prompt 里要求镜头按编号顺序移动
- 最终视频禁止出现编号、箭头、文字、路线

### 2. 红线路径控制模式

适合：

- 世界地图飞行
- 城市到地标穿越
- 峡谷/赛车/无人机路线
- Seedance 2.0 path control

核心做法：

- 先生成一张带红线的路线规划图
- 红线只作为摄像机路径控制
- 视频 prompt 里明确要求最终画面去掉红线、箭头、地图标注

## 常用示例

```text
使用 FPV 运镜导演 skill，帮我做一个现代客厅里 5 个人依次互动的 FPV 视频提示词，15 秒，像客人走进房间一样。需要 GPT Image 首帧和人物参考图。
```

```text
使用 FPV 运镜导演 skill，做一个 Seedance 2.0 世界地图飞行，从雪原穿过峡谷、王城，最后到火山。需要红线路径控制图 prompt 和视频 prompt。
```

```text
使用 FPV 运镜导演 skill，做一个机器人吸尘器视角的咖啡厅短片，12 秒，经过 3 个顾客和 1 个吧台咖啡师，最后停在窗边阳光里。
```

## 仓库关键文件

```text
SKILL.md
```

主 skill。给 agent 读取。

```text
examples/numbered-stop-example.md
```

室内、多人物、编号停靠点示例。

```text
examples/redline-route-example.md
```

世界地图、红线路径控制示例。

```text
skill/references/gpt-image-asset-packs.md
```

GPT Image 首帧图、角色参考图、干净首帧图的资产包方法。

```text
skill/references/session-patterns.md
```

常见失败原因和修正模式。

## 判断它有没有用

有用，但它只负责提示词设计。

你还需要：

- 用 GPT Image / GPT-Image-2 生成首帧图和角色参考图
- 把图片和视频 prompt 放进 Seedance / Kling / Runway / Veo 等视频模型
- 多试几次，挑稳定结果

它能显著改善的是：镜头路线、目标数量、POV 物理限制、角色一致性、红线/编号残留控制。
