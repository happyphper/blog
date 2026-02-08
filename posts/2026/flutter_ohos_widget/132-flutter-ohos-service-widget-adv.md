![封面图](images/132-cover.png)

# Flutter for OpenHarmony 实战之殿堂：第一百三十二篇 鸿蒙万能卡片 (Service Widget) 进阶 — 实时刷新与双向通信

## 前言

我们在 131 篇了解了元服务的基本概念。本篇我们要更进一步：探讨 **鸿蒙万能卡片 (Service Widget)** 的生命周期与数据更新机制。一张“死”的图片卡片是没有生命力的，用户希望看到的是实时滚动的股票行情、实时跳动的心率步数。

作为 Flutter 开发者，如何让鸿蒙桌面的 ArkUI 卡片与后台的 Flutter 逻辑层实现毫秒级的数据互通？我们将利用鸿蒙核心的 **FormManager (卡片管理器)** 揭晓答案。

---

## 一、鸿蒙卡片的驱动模型

鸿蒙万能卡片的刷新并不是由卡片自己发起的，而是受 **FormManager** 统一调度的：
- **定时刷新**：系统根据设定的固定周期（如每 4 小时）唤醒 Provider。
- **主动刷新 (Push)**：应用后台由于业务变化（如收到推送），主动调用系统 API 更新卡片。
- **动态交互**：用户在卡片上的点击按钮（Action），触发 Provider 回调。

---

## 二、实战：构建一个“实时步数”动态卡片

### 2.1 原生侧：注册 FormExtensionAbilityExtensionAbility
这是卡片的后台大脑，负责接收 Flutter 侧的数据并推给桌面。

```typescript
// 💡 原理：在 onCreateForm 时建立数据通路数据通路
import formBindingData from '@ohos.app.form.formBindingData';

onUpdateForm(formId) {
  // 📌 核心逻辑：封装要更新给卡片的 JSON 数据数据
  let formData = { "steps": this.currentSteps, "calories": 450 };
  let bindingData = formBindingData.createFormBindingData(formData);
  // ⚡️ 物理分发：告诉桌面更新对应的卡片 UI对应的卡片 UI
  formProvider.updateForm(formId, bindingData);
}
```

### 2.2 Flutter 侧：实时计算并推送至卡片推送至卡片
当 Flutter 应用运行在后台时（例如正在计步），需要将数据同步给卡片。

```dart
// ⚡️ 架构思路：利用 MethodChannel 触发原生侧的 updateForm
void updateDesktopCard(int steps) async {
  await _channel.invokeMethod('pushDataToCard', {
    'formId': _savedFormId,
    'steps': steps
  });
}
```

<!-- IMAGE_PLACEHOLDER: 用户在手机上跑步，鸿蒙桌面上的 Flutter 风格万能卡片数字实时跳动，且伴随精美进度条填充动效的实拍图 -->
<!-- 类型: 动图 -->
<!-- 内容: 展示卡片异步刷新的丝滑感 -->

---

## 三、进阶：集成系统级“卡片代理刷新加载”

为了省电，鸿蒙支持在手机息屏时挂起应用，由系统代理刷新卡片。
- ✅ **方案**：配置 `scheduled_update_time`。
- ✅ **结果**：即便 Flutter 进程被系统回收，鸿蒙系统也会在特定时间点通过 ArkTS 微内核自动抓取数据并刷新卡片，保证用户醒来时看到的是最新信息。

---

## 四、OpenHarmony 平台适配要点：卡片交互限制

鸿蒙卡片（尤其是 2 * 2 尺寸）严禁复杂的滑动列表（Scrollable）。
- ⚠️ **规则**：所有交互必须基于 **Action**（点击事件）。
- ✅ **建议**：如果你的卡片需要展示多条新闻，建议使用“翻页按钮（Next/Prev）”。点击按钮时，Flutter 通过原生管道计算出下一页数据并调用 `updateForm` 刷新，这比直接在卡片上滑动的性能开销低 80%。

---

## 五、总结

卡片开发是“数据与视图的极致解耦”：
1.  **卡片不渲染 Flutter**：卡片是 ArkUI 写的，Flutter 只负责提供业务逻辑与数据。
2.  **Manager 为桥**：通过 FormManager 实现进程间的通信与生命周期对齐。
3.  **电量优先**：设计合理的刷新频率，是元服务能被用户长期留在桌面上的前提。

第一百三十三篇，我们将探讨元服务的一个极致场景——**鸿蒙负一屏服务直达与 Flutter 动态卡片的热部署实战**。

---

> 📦 **动态卡片开发脚手架 (Ohos-Card-Master)**：[open-harmony-examples/service-widget-kit](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/service-widget-kit)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
