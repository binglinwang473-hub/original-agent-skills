# Numbered Stop Marker Example

## User request

帮我做一个现代客厅里 5 个人依次互动的 FPV 视频提示词，15 秒，像客人走进房间一样。

## Why numbered stops

This is a close-interaction interior scene. A continuous red path can easily cross furniture, walls, or people, and the line may remain visible in the final video. Small numbered markers are safer because the prompt can define the movement between stops while the first frame only marks target order.

## Asset plan

1. First-frame image of a modern living room with exactly 5 small numbered stop markers near the 5 main characters.
2. Five separate character reference images, one for each main character.
3. Optional clean first frame without numbered markers for safer image-to-video input.

## Copy-ready video prompt

使用上传图片作为首帧、编号路线参考和 5 个角色外观参考，生成一段 16:9、15 秒、一镜到底的现代客厅客人视角 FPV 视频。首帧中的编号 1 到 5 只作为镜头停靠顺序参考，不要出现在最终画面里。最终视频不要出现数字、编号、路线、箭头、文字标签或 UI。

观众是一位刚进入房间的客人，从客厅入口出发，严格按编号顺序移动：入口 → 1 沙发旁的朋友 → 2 落地窗前的人 → 3 茶几旁的人 → 4 开放式吧台旁的人 → 5 阳台门口的人。全片包含 exactly 5 个主要人物，不要增加或减少主目标。角色脸、服装、位置和身份保持参考图一致。

镜头保持人类眼平高度，有轻微步行摆动、自然转头、真实加速减速和短暂停留。移动必须沿客厅地面和可通行空间完成，不能穿过沙发、茶几、墙面、玻璃、人物身体或其他障碍物。

时间轴：
0.00-2.00：从入口进入客厅，环境光从落地窗洒入，镜头建立空间方向。
2.00-4.50：移动到 1，沙发旁的朋友抬头微笑并举杯示意。
4.50-7.00：移动到 2，落地窗前的人转身看向镜头，窗帘轻微摆动。
7.00-9.50：移动到 3，茶几旁的人递出一本杂志，咖啡有轻微蒸汽。
9.50-12.00：移动到 4，吧台旁的人把杯子放下，吧台灯有温暖反光。
12.00-15.00：移动到 5，阳台门口的人拉开门，镜头停在室内外光线交界处并回望客厅层次。

避免：编号残留、路线线条、箭头、换脸、同脸、身份漂移、主目标数量变化、穿模、跳切、瞬移、错误 POV、过度抖动、场景漂移、低质、畸形、水印。
