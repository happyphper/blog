![封面图](images/133-cover.png)

# Flutter for OpenHarmony 实战之殿堂：第一百三十三篇 鸿蒙元服务 (Atomic Service) — 负一屏直达与小艺建议联动

## 前言

元服务的最强分发入口在哪里？答案是 **负一屏 (Minus One Screen)**。在 **HarmonyOS NEXT** 中，用户向右一滑，系统会根据时间、地点和用户行为，自动推荐最合适的元服务卡片。

如果你的 Flutter 应用是一个打车软件，而在周一早上 8:00 用户正准备上班，你的元服务卡片能精准出现在负一屏并显示“一键叫车”，那你的分发转化率将呈指数级增长。本篇将教你如何打通 **“小艺建议”** 的推荐逻辑。

---

## 一、负一屏与“小艺建议”的推荐算法

鸿蒙系统的 AI 引擎会根据以下维度进行卡片推荐：
- **时空特征**：用户在特定的时间点（如周一早晨）进入特定的位置（如家里的地库）。
- **设备状态**：连接了特定的车载蓝牙。
- **用户画像**：历史点击频次。

在 Flutter 侧，我们的任务是：**向系统申报意图（Intent）并提供高质量预览卡片。**

---

## 二、实战：将 Flutter 业务逻辑映射为系统推荐卡片

### 2.1 声明“意图卡片 (Action Card)”卡片)”
在 `form_config.json5` 中，我们需要声明卡片的属性。

```json
{
  "forms": [
    {
      "name": "CommuteCard",
      "description": "通勤打车助手",
      "src": "./js/CommuteCard/pages/index/index",
      "window": { "designWidth": 720, "autoDesignWidth": true },
      "isDefault": true,
      "supportDimensions": ["2*2"]
    }
  ]
}
```

### 2.2 触发系统级“意图推荐”推荐”
利用鸿蒙原生的 **ContextAware (情境感知)** 接口上报用户状态。

```typescript
// 💡 原理：通过原生 side 告知系统当前的业务状态业务状态
import sceneHelper from '@ohos.ai.sceneHelper';

function reportCommuteScene() {
  // 📌 核心逻辑：上报“准备通勤”的意图，触发系统在负一屏显示卡片卡片
  sceneHelper.updateScene(SceneType.COMMUTE, {
    "status": "PREPARING",
    "target": "Office"
  });
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙负一屏上，基于用户地理位置变化自动浮现的 Flutter 风格元服务卡片（显示排队进度）的动态呈现图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示元服务与系统 AI 引擎深度协同的魅力 -->

---

## 三、进阶：卡片侧的“轻量化预览”渲染

负一屏对滑动性能要求极高。
- ✅ **方案**：在卡片对应的 ArkUI 代码中，完全使用 **纯绘图指令 (Canvas)** 渲染。数据的源头来自于我们在 120 篇学过的全场景 IoT 管理平台的实时广播。
- ✅ **体验**：用户在负一屏看到的是预渲染好的快照，点击瞬间启动 Flutter 落地页，这种“视觉无缝”感是高端应用的标配。

---

## 四、OpenHarmony 平台适配要点：连接稳定性

负一屏的卡片在弱网下可能会显示失败。
- ✅ **推荐做法**：使用我们 119 篇学过的 **分布式数据快照存储**。当卡片由于网络原因无法获取最新 API 数据时，直接读取缓存在共享目录中的上一次成功获取的“语义快照”，并打上“5 分钟前更新”的标签，确保用户体验不中断。

---

## 五、总结

元服务的高级阶段是“意图化服务”：
1.  **卡片即服务**：不是为了广告，是为了高效解决具体场景问题。
2.  **AI 驱动分发**：利用小艺建议算法，让服务主动找到用户。
3.  **落地无缝化**：从 ArkUI 的极简预览到 Flutter 的全量逻辑，切换必须丝滑。

第一百三十四篇，我们将探讨元服务的终极方案——**鸿蒙元服务的热更新与动态化配置：无需发版即可改变卡片逻辑逻辑**。

---

> 📦 **服务直达集成工具 (Ohos-Direct-Kit)**：[open-harmony-examples/atomic-direct-integration](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/atomic-direct-integration)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
