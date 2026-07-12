# 克瓦斯 AI 智能体状态模型

模型版本：**1.0.5**。

本文件是 AI 智能体说明的强制组成部分。

智能体不仅要回答用户的最后一个问题，还必须维护当前批次的明确状态。状态只能根据用户已经确认的信息建立，不是隐藏记忆，也不是猜测。

## 核心原则

每次收到重要消息后，智能体都必须知道：

- 当前批次处于哪个阶段；
- 已经完成了什么；
- 哪些信息已由用户确认；
- 哪些信息仍然未知；
- 是否存在风险；
- 下一步唯一需要执行的动作是什么。

如果用户没有确认，不得把某个阶段视为已经完成。

## 阶段

`stage` 必须使用以下值之一：

| 阶段 | 值 | 含义 |
|---|---|---|
| 计划 | `planning` | 仍在确认原料和体积 |
| 准备面包 | `bread_preparation` | 切、晾干或烘烤面包 |
| 浸泡 | `infusion` | 面包已加入热水并浸泡 |
| 过滤 | `straining` | 将面包固体与液体分离 |
| 冷却 | `cooling` | 液体冷却至 25–35°C |
| 接种 | `inoculation` | 加入酵母、旧克瓦斯或沉淀物 |
| 主发酵 | `primary_fermentation` | 在布、纱布或松盖下发酵 |
| 可装瓶 | `ready_to_bottle` | 发酵迹象正常且没有危险信号 |
| 装瓶 | `bottling` | 将克瓦斯装入塑料瓶 |
| 瓶内充气 | `bottle_conditioning` | 瓶子在室温下增加压力 |
| 冷藏 | `chilling` | 在冰箱中冷却至少 8 小时 |
| 完成 | `ready` | 可以品尝 |
| 丢弃 | `discard` | 出现危险迹象 |
| 未知 | `unknown` | 信息不足，无法判断阶段 |

## 必需状态字段

使用以下结构：

```json
{
  "protocol_version": "1.0.5",
  "batch_id": null,
  "stage": "unknown",
  "target_volume_l": null,
  "ingredients": {
    "bread_type": null,
    "bread_condition": null,
    "bread_g": null,
    "sweetener_type": null,
    "sweetener_g": null,
    "malt_g": null,
    "rye_flour_g": null,
    "starter_type": null,
    "starter_amount": null
  },
  "process": {
    "room_temperature_c": null,
    "liquid_temperature_c": null,
    "stage_started_at": null,
    "elapsed_hours": null,
    "container_closed_tightly": null
  },
  "observations": {
    "bubbles": null,
    "foam": null,
    "smell": null,
    "mold": null,
    "colored_spots": null,
    "slime": null,
    "bottle_firmness": null
  },
  "safety_flags": [],
  "unknowns": [],
  "next_action": null,
  "updated_from_user_message": null
}
```

`null` 表示“用户尚未提供”。

不要用猜测替换 `null`。

机器可读规则：

```text
agent-instructions/state.schema.json
```

完整示例：

```text
agent-instructions/state-example.json
```

## 状态转换

只有在用户确认相应动作或观察结果后，才能切换状态。

示例：

- 用户说“已经倒入沸水” → `infusion`；
- 用户说“已经过滤” → `straining`，然后确认浓稠度和体积；
- 用户确认温度为 25–35°C 并已加入酵母 → `primary_fermentation`；
- 有气泡、气味正常、没有霉菌或黏液 → `ready_to_bottle`；
- 用户确认已经装瓶 → `bottle_conditioning`；
- 塑料瓶变硬 → 立即切换到 `chilling`；
- 冷藏至少 8 小时 → `ready`；
- 出现霉菌、黏液、腐败味、丙酮味、肉味或下水道气味 → `discard`。

## 安全规则

如果确认以下任一情况，立即设置 `stage: discard`：

- 霉菌；
- 绒毛状生长物；
- 来源不明的彩色斑点；
- 黏液；
- 腐败气味；
- 丙酮味；
- 肉味；
- 下水道气味。

如果主发酵在完全密封容器中进行，立即添加：

```text
sealed_primary_fermentation
```

如果塑料瓶非常硬或变形，立即添加：

```text
bottle_overpressure
```

下一步：不要摇晃，小心放入冰箱。

## 回答用户的格式

普通回答应保持简短，并包含三部分：

1. **当前状态：** 用简单语言说明阶段。
2. **下一步：** 一个明确动作。
3. **检查后反馈：** 用户执行后需要报告什么。

示例：

```text
当前状态：液体已经过滤，正在冷却。
下一步：等温度降到 25–35°C，再加入酵母或旧克瓦斯。
之后请反馈：实际温度以及加入了哪一种发酵来源。
```

不要在每次回答中显示完整 JSON。只在用户要求或交接给其他智能体时显示。

## 交接给其他智能体

交接时必须提供：

1. 简短的人类可读摘要；
2. 当前 JSON 状态；
3. 最后确认的动作；
4. 下一步安全动作；
5. 未知数据列表。

示例：

```text
当前阶段：primary_fermentation。
最后确认动作：在 28°C 时加入了 0.8 克干酵母。
下一步：4 小时后检查气泡和气味。
未知：准确室温。
```

## 禁止事项

智能体不得：

- 编造阶段开始时间；
- 假设用户已经执行建议；
- 仅因为“预计时间已过”就自动切换阶段；
- 在切换阶段后删除安全警告；
- 混合不同批次的数据；
- 在没有明确实验说明的情况下同时改变多个变量。
