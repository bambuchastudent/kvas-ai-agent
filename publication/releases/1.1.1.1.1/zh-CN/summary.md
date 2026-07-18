---
lang: zh-CN
doc_type: summary
title: KVASSISTENT — 用户快速指南
subtitle: 家庭 Zhizha 克瓦斯、高温、阳光和酒精边界
version: 1.1.1.1.1
---

<!-- section:overview -->
## 项目简介

**KVASSISTENT** 帮助人制作家庭 Zhizha 克瓦斯，并为 AI 智能体提供独立的状态协议。1.1.1.1.1 版本增加了 28°C 发酵、直射阳光和酒精估算的研究规则。

<!-- section:baseline -->
## 3 升基础配方

- 水 — 3 升；
- 完全干燥面包干 — 180–220 克；
- 推荐 150 克白面包干 + 50–70 克黑麦或 Borodinsky；
- 白糖或 panela — 100–120 克；
- 麦芽 — 20–30 克或黑麦粉 — 10–20 克；
- 第一批：0.5–1 克干酵母或 2–3 克鲜酵母；
- 后续批次：500 毫升旧克瓦斯或 3–5 汤匙沉淀物。

<!-- section:process -->
## 简短流程

1. 将面包烤至深金黄色。
2. 加入沸水浸泡 4–8 小时。
3. 过滤，只保留液体。
4. 加糖并冷却至 25–35°C。
5. 加入发酵来源，用布、纱布或松盖覆盖。
6. 发酵 8–12 小时；28°C 时 4–6 小时开始检查。
7. 气味正常并有气泡后装入塑料瓶。
8. 室温充气 2–6 小时，瓶体变硬后冷藏。

<!-- section:heat -->
## 28°C 高温和阳光

28°C **阴凉处**可以使用，但速度很快。不要把玻璃罐放在直射阳光下：液体温度可能远高于空气。移到阴凉处，测量液体温度并频繁检查。

温度区间：18–24°C 稳定；25–27°C 快速；28–30°C 高温，4 小时开始检查；31–34°C 移到凉处；35°C 以上冷却并停止家庭流程。

<!-- section:alcohol -->
## 两周会达到 8% 吗？

不会自动达到。3 升中加入 100–120 克糖，仅由这些糖产生的理论上限约为 2.2–2.6% ABV。理论 8% 需要约 370 克可发酵糖，实际需要更多。准确酒精度需要初始/最终比重或实验室检测。

28°C 放置两周已经不是快速克瓦斯，而是更不可预测的长期酒精和酸性发酵。

<!-- section:sweeteners -->
## 白糖、panela、麦芽糖和麦芽

Panela 可约 1:1 替代白糖。麦芽糖可以发酵，但不能替代麦芽风味和酶。麦芽提取物更适合增加麦芽香气。

<!-- section:state -->
## 批次状态

AI 智能体记录空气和液体温度、最高温度、直射阳光、暴露时间、封闭方式、观察结果和酒精估算。未知值保持 `null`。

<!-- section:safety -->
## 安全

主发酵不能完全密封。立即把罐子移出阳光。出现霉菌、绒毛、彩色斑点、黏液、腐败味、丙酮味、肉味或下水道气味时丢弃。

<!-- section:links -->
## 资源

- 研究：`docs/research-fermentation-heat.md`
- 智能体：`agent-instructions/kvas-agent.zh-CN.md`
- 状态：`agent-instructions/state-model.zh-CN.md`
- Schema：`agent-instructions/state.schema.json`
- 仓库：https://github.com/bambuchastudent/kvas-ai-agent
