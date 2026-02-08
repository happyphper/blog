![封面图](images/83-cover.png)

# Flutter for OpenHarmony 实战之进阶：第八十三篇 鸿蒙元服务（服务卡片）与 Flutter 的协同开发

## 前言

在 **HarmonyOS NEXT** 的产品定义中，**元服务 (Atomic Service)** 是极其重要的一环。它以“万能卡片”的形式常驻在负一屏或桌面，为用户提供“即用即走”的极速体验。很多开发者会问：Flutter 能不能用来写这些高频互动的“服务卡片”？

答案是：**核心逻辑复用，视觉原生承载**。本篇将为你详解 Flutter 应用如何与鸿蒙原生服务卡片进行高效协同。

---

## 一、元服务卡片的核心架构限制

在鸿蒙系统中，服务卡片（Form）并不是一个完整的 Ability，它运行在高度受限的 JS 环境中（通常使用 ArkTS 的声明式语法）。
- **空间受限**：卡片有固定的尺寸（1x2, 2x2, 2x4 等）。
- **能力受限**：不能直接运行 Flutter 渲染引擎（因为 Engine 太重，加载太慢）。
- **交互受限**：主要通过 `postCardAction` 与后台进行简单的异步通信。

因此，我们的架构方案是：**Flutter 应用负责复杂业务逻辑与完整页面；ArkTS 服务卡片负责轻量化呈现与拉起应用**。

---

## 二、实战：Flutter 逻辑驱动原生卡片刷新

### 2.1 数据的流转链路
1.  用户在 Flutter 应用内修改了数据（如设置了闹钟、更新了待办事项）。
2.  Flutter 通过 `MethodChannel` 通知鸿蒙原生侧。
3.  鸿蒙原生侧调用 `formProvider.updateForm` 更新卡片显示。

### 2.2 鸿蒙原生：定义卡片数据模型
在 ArkTS 中定义卡片的数据对象：

```typescript
// 💡 原理：定义可观测的卡片数据
class CardData {
  title: string = "我的待办";
  taskCount: number = 0;
}
```

### 2.3 Flutter：触发卡片更新
```dart
class OhosFormTool {
  static const _channel = MethodChannel('com.example/ohos_form');

  static Future<void> updateCardData(int count) async {
    // ⚡️ 将 Flutter 业务逻辑产生的结果，通过管道塞给原生卡片
    await _channel.invokeMethod('updateForm', {'count': count});
  }
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙桌面服务卡片与 Flutter 应用内部数据实时同步的动图演示 -->
<!-- 类型: GIF -->
<!-- 内容: 展示在应用内操作，桌面卡片瞬间数字变化的联调效果 -->

---

## 三、进阶：通过卡片精准点击，跳转 Flutter 特定页面

卡片最大的价值是“引流”。当用户点击卡片的某个模块时，我们需要直接进入 Flutter 应用的相应深层页面。

### 3.1 原生侧路由转换
在卡片点击动作中，携带特定的 `params`。

```typescript
postCardAction(this, {
  "action": "router",
  "abilityName": "EntryAbility",
  "params": {
    "pageRoute": "/task_detail",
    "taskId": 1001
  }
});
```

### 3.2 Flutter 侧捕获路由参数
在 `main.dart` 或 `AppObserver` 中处理从原生传递过来的启动参数。

```dart
void handleLaunchParams(Map params) {
  String? route = params['pageRoute'];
  if (route != null) {
    navigatorKey.currentState?.pushNamed(route, arguments: params['taskId']);
  }
}
```

---

## 四、OpenHarmony 平台适配挑战

### 4.1 卡片刷新频率限制
鸿蒙系统对卡片的主动刷新频率有严格限制（如每天 100 次以内）。
- ✅ **建议**：只在核心数据发生“状态级”变更时才同步。避免将卡片当成实时监控大屏使用。

### 4.2 保持视觉风格一致
鸿蒙服务卡片有严格的设计规范（Corner Radius, Margin）。
- ✅ **技巧**：在 Flutter 模拟卡片效果时，务必使用鸿蒙系统的资源文件（如 `ohos_common_dimens`）中定义的圆角值。

---

## 五、总结

元服务卡片是 Flutter 应用通往用户的“第二窗口”：
1.  **分工明确**：卡片负责“看”，Flutter 负责“做”。
2.  **数据桥接**：利用通信管道实现两端数据的最终一致性。
3.  **精准直达**：打通卡片跳转链路，实现“服务直达”的极致体验。

学会了这一篇，你的 Flutter 应用将不再是一个孤岛，而是深度嵌入鸿蒙桌面的明星产品。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/form-card-integration](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/form-card-integration)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
