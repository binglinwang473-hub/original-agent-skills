<div align="center">

# FPV Camera Director.skill

> *Turn AI video prompts from visual description into action trajectory design.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Runtime](https://img.shields.io/badge/Runtime-Hermes%20·%20Claude%20·%20Codex%20·%20Cursor-blueviolet)](#install)
[![AI Video](https://img.shields.io/badge/AI%20Video-Seedance%20·%20Kling%20·%20Runway%20·%20Veo-ff69b4)](#use-cases)

<br>

**A route-first prompting skill for cinematic FPV image-to-video workflows.**

It does not only add words like cinematic, shallow depth of field, and beautiful lighting.
It designs who the camera is, where it starts, which targets it visits, how it moves around obstacles, and where the shot ends.

<br>

[Examples](#examples) · [Install](#install) · [What it solves](#what-it-solves) · [How it works](#how-it-works) · [Asset packs](#gpt-image-asset-packs) · [中文](README.md)

</div>

---

## Examples

### Cat POV in a cafe

User request:

```text
Create a 15-second FPV video prompt in a cafe where 3 people interact one by one. Cat POV.
```

The skill recognizes this as a close character-interaction scene, not a red-line route-control scene. It prepares a full image asset pack instead of stopping at a single first-frame prompt.

```text
Image 1: low-angle cafe first frame from cat POV, with small numbered stops 1, 2, 3
Image 2: independent reference image for the woman by the window
Image 3: independent reference image for the barista
Image 4: independent reference image for the man at the corner table
Image 5: optional clean first frame without numbers, used as the real image-to-video input
```

Then it produces a video prompt like this:

```text
The viewer is a cat freely moving through a cafe. The camera stays close to the floor.
Starting from the entrance mat, it moves strictly in numbered order:
entrance mat → 1 woman by the window → 2 barista at the counter → 3 man at the corner table → stops in a patch of sunlight by the window.

The video contains exactly 3 main people. Do not add or remove main targets.
The camera movement must obey cat-body physics: low height, small steps, short pauses, curious head turns, visible table legs, chair legs, floor texture, shoes, and occasional paw or tail edges.
The cat cannot fly, jump onto the counter, pass through furniture, pass through legs, or suddenly become human eye level.
```

The core is not making the cafe prettier. The core is making the model understand how the cat moves.

---

### World-map flythrough

User request:

```text
I want a Seedance 2.0 world-map flight, starting from a snowfield, crossing a canyon and royal city, and ending at a volcano.
```

The skill switches to red-line route-control mode.

```text
Image 1: 16:9 fantasy continent route-planning image, with one continuous red route from the snowfield through the canyon and city to the volcano
Image 2: optional clean world reference without the red line
```

The video prompt then states:

```text
The red route is only camera-path control, not final visual content.
The final video must not show red lines, arrows, map labels, text, UI, or a flat map-view look.
The camera must strictly follow the drawn route geometry, with natural banking, close terrain passes, foreground parallax through landmarks, and a stable horizon.
```

Both are FPV videos, but they require different route logic.

---

## What it solves

Many AI video prompts look complete and still fail.

Common failures:

- the camera teleports and breaks the space
- character count changes mid-shot
- numbers, red lines, arrows, or labels remain in the final video
- cat POV turns into drone POV
- one-shot video becomes jump cuts
- indoor movement passes through tables, chairs, walls, or people
- character faces and outfits drift between interactions

The problem is usually not a lack of style words. It is a missing action trajectory.

FPV prompting needs to describe motion, not only imagery: who is looking, how they move, whom they pass, where they pause, and what must stay consistent.

---

## Use cases

- one-shot FPV walkthroughs in cafes, living rooms, galleries, courtyards, palaces, and exhibitions
- short videos where 3 to 8 characters interact in sequence
- non-human POVs such as cats, dogs, robot vacuums, drones, birds, spirits, vehicles, or object cameras
- GPT Image / GPT-Image-2 first-frame and character-reference asset packs
- Seedance, Kling, Runway, Veo, and similar image-to-video workflows
- red-line route control, world-map flythroughs, city-to-landmark movement, canyon flights, racing lines
- creators who want camera choreography instead of generic visual prompting

---

## How it works

The skill breaks an FPV video into eight questions.

```text
1. Who or what is the camera?
2. Where does it start?
3. Exactly how many main characters or targets exist?
4. In what order should the camera visit them?
5. Can every movement segment physically happen?
6. What interaction happens at each stop?
7. Which identities, outfits, and positions must remain consistent?
8. What must never appear in the final video?
```

Then it chooses one of two route modes.

### Numbered stop markers

Best for close character interactions, interiors, cafes, living rooms, social scenes, and exhibitions.

In these scenes, a red line is often risky. It can cross furniture, walls, or people, and it can leak into the final video.

The safer pattern is to place small numbered markers near each target in the first frame, then use the video prompt to define the movement between stops.

### Red-line path control

Best for large-scale routes: aerial maps, city flythroughs, canyon flights, racing lines, fantasy continents, and Seedance-style path-control demos.

Here the route geometry is the main constraint. The red line can control the path, but it must disappear completely from the final video.

---

## GPT Image asset packs

When the scene contains N main characters, the skill defaults to a full asset pack.

```text
1 numbered first-frame image
N independent character reference images
1 optional clean first-frame image
```

For a three-person cafe scene:

```text
Image 1: cafe cat-POV first frame with numbered stops 1, 2, 3
Image 2: reference image for the woman by the window
Image 3: reference image for the barista
Image 4: reference image for the man at the corner table
Image 5: clean first frame without numbers or marks
```

The first frame controls space. The character references control identity. The clean first frame controls the actual video input.

A single image often mixes all three responsibilities and causes route marks, identity drift, or layout confusion.

---

## Install

### Option 1: Install into Hermes

```bash
git clone https://github.com/zhouwei713/fpv-immersive-video-prompting.git \
  ~/.hermes/skills/creative/fpv-immersive-video-prompting
```

Restart Hermes or open a new session. The skill will be available as:

```text
fpv-immersive-video-prompting
```

### Option 2: Use it in another agent runtime

If you do not use Hermes, copy `SKILL.md` into Claude, Codex, Cursor, OpenCode, or any agent environment that supports skills or long prompt instructions.

### Option 3: Read it as a prompting method

Start with:

```text
SKILL.md
skill/references/gpt-image-asset-packs.md
skill/references/session-patterns.md
```

---

## Usage

Try prompts like:

```text
Create a 15-second cat-POV FPV video in a cafe where 3 people interact one by one.
```

```text
Make a palace courtyard FPV shot that passes 5 characters in order and ends by a pond.
```

```text
I have a world map. Help me write a Seedance 2.0 prompt where the camera follows a red route from a snowfield to a volcano.
```

```text
Give me a GPT Image asset-pack prompt with a first frame, character references, and a clean first frame.
```

---

## Repository structure

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

## Design philosophy

FPV prompting is not about making one still image more beautiful.

It is closer to level design: where the entrance is, how the route moves, where the characters stand, whether the camera body can physically pass through the space, and whether the ending gives the viewer a coherent sense of the scene.

If motion is not designed, the model designs it for you. That usually means teleportation, wall-crossing, face drift, and jump cuts.

This skill makes the route, identity, and physics checks explicit and reusable.

---

## License

MIT License.
