# 克瓦斯（Kvass）

**Kvass** 是一个关于可复现家庭自制克瓦斯的开放知识库。

**项目品牌：Zhizha（Жижа）。**  
Kvass 是项目名称，Zhizha 是项目风格与个性。

**当前版本：1.0.6**

## 项目目标

帮助人和 AI 智能体使用明确的克数、时间、温度、状态和安全规则，稳定地复现家庭自制克瓦斯。

项目包括：

- 3 升基础配方；
- 面包、糖、粗糖、麦芽糖和麦芽的说明；
- 发酵安全检查；
- 批次记录模板；
- AI 智能体状态模型；
- 俄语、英语、西班牙语、德语和简体中文说明；
- 用于 Telegram 分享的页面。

## 3 升基础配方

### 原料

- 水：3 升；
- 完全干燥的面包干：180–220 克；
- 推荐：150 克白面包干 + 50–70 克黑麦或 Borodinsky 面包干；
- 如果面包只是变硬、没有完全干燥：250–300 克；
- 白糖或 panela 粗糖：100–120 克；
- 麦芽：20–30 克，可选；
- 或黑麦粉：10–20 克；
- 第一批：
  - 鲜酵母 2–3 克；
  - 或干酵母 0.5–1 克；
- 后续批次可改用：
  - 500 毫升旧克瓦斯或压滤液；
  - 或 3–5 汤匙沉淀物。

### 做法

1. 将面包烤至深金黄色，不要烧焦。
2. 倒入沸水。
3. 浸泡 4–8 小时。
4. 过滤。
5. 发酵的是液体，不是面包糊。
6. 加入 100–120 克白糖或 panela。
7. 冷却到 25–35°C。
8. 加入酵母、旧克瓦斯或沉淀物。
9. 用布、纱布或松盖覆盖，不要密封。
10. 发酵 8–12 小时；天气炎热时从第 6 小时开始检查。
11. 出现气泡并且气味正常后，装入塑料瓶。
12. 每 0.5 升加入 3 粒葡萄干或 1/2 茶匙糖。
13. 室温二次充气 2–6 小时。
14. 塑料瓶变硬后立即放入冰箱。
15. 冷藏至少 8 小时。

## 为什么通常需要加糖

面包中的碳水化合物主要是淀粉。酵母不会自行把面包淀粉转化成糖。

啤酒生产依靠麦芽酶和糖化过程，把谷物淀粉转化为可发酵糖。简单的面包克瓦斯通常没有完整糖化过程，因此额外加入糖能让发酵、气泡和味道更稳定。

- panela 可按重量约 1:1 替代白糖；
- 麦芽糖可以发酵，但不能提供完整的麦芽风味和酶作用；
- 麦芽提取物通常比纯麦芽糖更适合增加麦芽风味。

## AI 智能体状态

版本 1.0.6 要求 AI 智能体维护当前批次的明确状态。

允许的阶段：

```text
planning
bread_preparation
infusion
straining
cooling
inoculation
primary_fermentation
ready_to_bottle
bottling
bottle_conditioning
chilling
ready
discard
unknown
```

智能体必须：

- 只使用用户确认的数据更新状态；
- 不假设用户已经执行建议；
- 未知值保持为 `null`；
- 保存安全警告；
- 不混合不同批次的数据；
- 每次只建议一个明确的下一步；
- 在交接给其他智能体时传递 JSON 状态、最后确认动作、下一步和未知字段。

中文智能体说明：

- [`agent-instructions/kvas-agent.zh-CN.md`](agent-instructions/kvas-agent.zh-CN.md)
- [`agent-instructions/state-model.zh-CN.md`](agent-instructions/state-model.zh-CN.md)
- [`agent-instructions/state.schema.json`](agent-instructions/state.schema.json)

## 安全规则

以下情况立即将状态设为 `discard` 并丢弃整批：

- 霉菌；
- 绒毛状生长物；
- 异常彩色斑点；
- 黏液；
- 腐败气味；
- 丙酮味；
- 肉味或下水道气味。

主发酵不要使用完全密封容器。

瓶内充气建议使用塑料瓶。瓶体变硬后立即冷藏，不要摇晃。

## 链接

- 仓库：`https://github.com/bambuchastudent/kvas-ai-agent`
- Telegram 分享页：`https://kvassistent.pages.dev/v1.0.6/`
- 完整可复现协议：[`recipes/kvas-reproducible.md`](recipes/kvas-reproducible.md)
- 批次记录模板：[`docs/batch-log-template.md`](docs/batch-log-template.md)
