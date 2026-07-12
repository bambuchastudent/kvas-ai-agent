---
lang: zh-CN
doc_type: summary
title: 克瓦斯 Zhizha - 摘要
subtitle: 适用于人和 AI 智能体的可复现家庭克瓦斯
version: 1.0.5
---

<!-- section:overview -->
## 项目简介

**Kvass** 是一个关于安全、可复现家庭克瓦斯的开放知识库。**Zhizha** 是项目品牌和个性。1.0.5 版本以五种语言提供结构一致的 PDF 和网页。

<!-- section:baseline -->
## 3 升基础配方

- 水 - 3 升；
- 完全干燥的面包干 - 180-220 克；
- 推荐 150 克白面包干 + 50-70 克黑麦或 Borodinsky 面包干；
- 白糖或 panela - 100-120 克；
- 麦芽 - 20-30 克，或黑麦粉 - 10-20 克；
- 鲜酵母 - 2-3 克，或干酵母 - 0.5-1 克。

后续批次可使用 500 毫升旧克瓦斯或 3-5 汤匙沉淀物。

<!-- section:process -->
## 简短流程

1. 将面包烤至深金黄色。
2. 倒入沸水并浸泡 4-8 小时。
3. 过滤，只保留液体。
4. 加入糖源并冷却至 25-35°C。
5. 加入发酵来源，在布或松盖下发酵 8-12 小时。
6. 气味正常并出现气泡后装入塑料瓶。
7. 室温充气 2-6 小时，瓶体变硬后立即冷藏。
8. 冷藏至少 8 小时。

<!-- section:sweeteners -->
## 白糖、panela、麦芽糖和麦芽

面包主要含淀粉，酵母不会自行把淀粉转化为糖。因此简单配方需要可控糖源。Panela 可按重量约 1:1 替代白糖，并带来糖蜜风味。麦芽糖可发酵，但不能替代麦芽风味和酶。为了麦芽香气，麦芽提取物通常比纯麦芽糖更合适。

<!-- section:state -->
## 批次状态

AI 智能体维护一个明确状态：`planning`、`bread_preparation`、`infusion`、`straining`、`cooling`、`inoculation`、`primary_fermentation`、`ready_to_bottle`、`bottling`、`bottle_conditioning`、`chilling`、`ready`、`discard` 或 `unknown`。未知值保持 `null`；只有用户确认后才能切换阶段。

<!-- section:safety -->
## 安全

主发酵不能完全密封。瓶内充气后，塑料瓶一旦变硬就应冷藏。出现霉菌、绒毛状生长物、彩色斑点、黏液、腐败味、丙酮味、肉味或下水道气味时，应丢弃整批。

<!-- section:links -->
## 资源

- AI 智能体说明：`agent-instructions/kvas-agent.zh-CN.md`
- 状态模型：`agent-instructions/state-model.zh-CN.md`
- JSON Schema：`agent-instructions/state.schema.json`
- 完整协议：`recipes/kvas-reproducible.md`
- 批次记录：`docs/batch-log-template.md`
- 仓库：https://github.com/bambuchastudent/kvas-ai-agent
