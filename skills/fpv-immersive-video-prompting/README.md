<div align="center">

# FPV 运镜导演.skill

> *把 AI 视频提示词，从“画面描述”升级成“行动轨迹设计”。*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Runtime](https://img.shields.io/badge/Runtime-Hermes%20·%20Claude%20·%20Codex%20·%20Cursor-blueviolet)](#安装)
[![AI Video](https://img.shields.io/badge/AI%20Video-Seedance%20·%20Kling%20·%20Runway%20·%20Veo-ff69b4)](#适合什么场景)

<br>

**一个专门为 FPV / image-to-video 设计的 AI 视频提示词 Skill。**

它不只帮你写“电影感、浅景深、光影高级”。
它会先设计镜头是谁，从哪里出发，按什么顺序经过哪些人，怎么绕过障碍物，最后停在哪里。

<br>

[看效果](#效果示例) · [安装](#安装) · [它解决什么](#它解决什么) · [工作原理](#工作原理) · [资产包](#gpt-image-资产包) · [English](README_EN.md)

</div>

---

## 效果示例

### 咖啡厅猫咪视角

用户输入：

```text
帮我做一个咖啡厅里 3 个人依次互动的 FPV 视频提示词，15 秒，猫咪视角
```

Skill 会先判断这不是红线路径场景，而是近距离人物互动。它会生成一套完整资产包，而不是只给一张首帧图。

```text
图片 1：咖啡厅猫咪低机位首帧，带 1、2、3 小编号停靠点
图片 2：靠窗女生独立人物参考图
图片 3：吧台咖啡师独立人物参考图
图片 4：角落圆桌男生独立人物参考图
图片 5：干净版首帧，去掉编号，用作真正视频首帧
```

然后输出视频 prompt：

```text
观众是一只在咖啡厅里自由走动的猫咪，镜头保持接近地面的低机位，
从咖啡厅入口旁的地垫开始，严格按编号顺序移动：
入口地垫 → 1 靠窗座位的女生 → 2 吧台前的咖啡师 → 3 角落圆桌旁的男生 → 窗边阳光下停住。

全片包含 exactly 3 个主要人物，不要增加或减少主目标。
镜头运动必须符合猫咪的身体限制，能看到桌腿、椅腿、地面纹理、人的鞋子，
可以短暂停顿、好奇转头、绕开障碍物，但不能飞，不能跳上吧台，不能穿过桌椅和人腿。
```

这类提示词的重点不是“咖啡厅很漂亮”，而是让视频模型知道猫到底怎么走。

---

### 世界地图飞行

用户输入：

```text
我想做一个 Seedance 2.0 的世界地图飞行，从雪原穿过峡谷、王城，最后到火山。
```

Skill 会切换到红线路径控制模式。

```text
图片 1：16:9 奇幻大陆航拍路线规划图，一条连续红线从雪原出发，经过峡谷和王城，抵达火山口
图片 2：可选干净世界参考图，去掉红线
```

视频 prompt 会明确说明：

```text
红色路线只作为摄像机路径控制，不是最终画面内容。
最终视频不要出现红线、箭头、地图标注、文字标签、UI 或俯视地图感。
镜头必须严格沿红线几何飞行，有自然 banking、贴近地形掠过、穿越地标时的前景视差和稳定地平线。
```

同样是 FPV，一个是猫在咖啡厅里走，一个是无人机穿越大陆。两种场景不能用同一套提示词。

---

## 它解决什么

很多 AI 视频 prompt 看起来很完整，实际一生成就翻车。

常见问题是：

- 镜头突然瞬移，空间断了
- 人物数量一会儿多一会儿少
- 首帧里的编号、红线、箭头残留在成片里
- 说是猫咪视角，结果变成无人机视角
- 说是一镜到底，结果中间跳切
- 室内路线穿过桌子、椅子、墙和人腿
- 多人物互动里，角色脸和衣服互相漂移

原因通常不是缺少风格词，而是缺少行动轨迹。

FPV 视频要写清楚的不是一张图，而是一段运动：谁在看，怎么走，经过谁，在哪里停，什么东西不能变。

---

## 适合什么场景

- 咖啡厅、客厅、展厅、庭院、宫殿等室内一镜到底
- 3 到 8 个角色依次互动的短视频
- 猫、狗、机器人吸尘器、无人机、鸟、幽灵、车辆等非人类 POV
- GPT Image / GPT-Image-2 首帧和人物参考图资产包
- Seedance、Kling、Runway、Veo 等 image-to-video 工作流
- 红线路径控制、世界地图飞行、城市到地标、峡谷穿越、赛车线路
- 想把提示词从“视觉描述”变成“镜头调度”的创作者

---

## 工作原理

这个 Skill 会把一个 FPV 视频拆成 8 个问题。

```text
1. 摄像机是谁
2. 从哪里开始
3. exactly 有多少个主要人物或目标
4. 按什么顺序经过它们
5. 每一段路线是否物理可达
6. 每个停靠点发生什么互动
7. 哪些身份、服装、位置必须保持一致
8. 哪些东西绝对不能出现在最终画面里
```

然后它会选择两种路线模式之一。

### 编号停靠点

适合近距离人物互动、室内空间、咖啡厅、客厅、派对、展厅。

这类场景里不要默认画红线。红线很容易穿过桌椅、墙面和人腿，也容易残留在视频里。

更稳定的做法是，在首帧里放小编号 1、2、3，把角色顺序标清楚。真正的移动路线交给视频 prompt 约束。

### 红线路径控制

适合大世界路线、航拍地图、城市飞行、峡谷穿越、赛车线路、Seedance 2.0 path control。

这类场景的核心是路线几何。红线可以作为路径控制，但最终视频里必须完全消失。

---

## GPT Image 资产包

如果场景里有 N 个主要人物，Skill 默认生成完整资产包。

```text
1 张带编号首帧图
N 张人物独立参考图
1 张可选干净首帧图
```

以 3 人咖啡厅为例：

```text
图片 1：咖啡厅猫咪视角首帧，带编号 1、2、3
图片 2：靠窗女生参考图
图片 3：咖啡师参考图
图片 4：角落男生参考图
图片 5：干净版首帧，去掉编号和所有标记
```

这样做的目的很简单：首帧管空间，人物参考管身份，干净首帧管最终输入。

如果只给一张图，视频模型很容易把路线、角色和画面标记混在一起。

---

## 安装

### 方式一：安装到 Hermes

```bash
git clone https://github.com/binglinwang473-hub/original-agent-skills.git \
  ~/.hermes/skills/creative/original-agent-skills
```

重启 Hermes，或开启新会话后即可使用：

```text
skills/fpv-immersive-video-prompting/SKILL.md
```

### 方式二：作为通用 Skill 使用

如果你不使用 Hermes，也可以直接把 `SKILL.md` 放进 Claude、Codex、Cursor、OpenCode 或其他支持 Skill / long prompt 的 Agent 环境里。

### 方式三：只当提示词方法论参考

直接阅读：

```text
SKILL.md
skill/references/gpt-image-asset-packs.md
skill/references/session-patterns.md
```

---

## 使用方式

你可以这样说：

```text
帮我做一个咖啡厅里 3 个人依次互动的 FPV 视频提示词，15 秒，猫咪视角
```

```text
做一个宫殿庭院 FPV，一镜到底经过 5 个角色，最后到池塘边
```

```text
我有一张世界地图，想让镜头沿红线从雪原飞到火山，帮我写 Seedance 2.0 prompt
```

```text
给我一套 GPT Image 生图 prompt，要包含首帧图、人物参考图和干净版首帧
```

---

## 仓库结构

```text
.
├── README.md
├── README_EN.md
├── SKILL.md
├── skill/
│   ├── SKILL.md
│   └── references/
│       ├── gpt-image-asset-packs.md
│       ├── liyue-ai-redline-fpv-case.md
│       ├── mayz-seedance-world-route-case.md
│       ├── public-article-angle.md
│       └── session-patterns.md
├── examples/
│   ├── numbered-stop-example.md
│   └── redline-route-example.md
└── LICENSE
```

---

## 设计理念

FPV 提示词不是把一张图说得更美。

它更像在设计一个小关卡：入口在哪里，路线怎么走，角色站在哪里，镜头能不能绕过去，最后有没有一个让观众理解空间的停顿。

只要运动没设计清楚，模型就会替你设计。它设计出来的结果，通常就是瞬移、穿墙、换脸和跳切。

这个 Skill 的价值，是把这套判断流程固定下来，让每次生成 FPV 视频前都先过一遍空间、路线、角色和物理限制。

---

## English

For English documentation, see [README_EN.md](README_EN.md).

---

## License

MIT License.
