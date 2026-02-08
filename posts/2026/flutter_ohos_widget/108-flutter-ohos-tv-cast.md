![封面图](images/108-cover.png)

# Flutter for OpenHarmony 实战之殿堂：第一百零八篇 鸿蒙智慧屏 (TV) 交互 — 跨端投屏与多屏控制实战

## 前言

在鸿蒙生态中，**“设备孤岛”** 是不存在的。用户最常见的操作就是：在手机上选好想看的视频，然后“搜”一下投到电视上。或者，把手机当做电视的游戏手柄。

本篇将通过 **Flutter for OpenHarmony** 带你实战开发一套跨端协同系统。我们将深入研究鸿蒙原生的 **Cast Engine (投屏引擎)**，实现手机端与 TV 端的无缝交互。

---

## 一、鸿蒙多屏协同的技术底座

在鸿蒙系统中，多端交互不只是简单的无线显示：
- **Cast Engine**：专门负责音视频、图片及屏幕镜像的发现与传输。
- **分布式软总线**：负责控制指令（如遥控命令、游戏手势）的极速传递。

---

## 二、实战：开发一个 Flutter 投屏控制端

### 2.1 发现附近的智慧屏设备
利用鸿蒙原生的分布式设备发现能力。

```dart
// 💡 架构思路：通过插件调起鸿蒙系统级设备发现面板
static Future<void> startCastDiscovery() async {
  // ⚡️ 唤起鸿蒙 Cast Kit 的系统 UI，让用户选择投向哪台电视
  await _channel.invokeMethod('openCastPanel');
}
```

### 2.2 手机端控制 TV 播放
一旦链路建立，手机端 Flutter 应用就变成了遥控器。

```dart
// 📌 发送控制指令（暂停/播放/进度）
void sendControlCommand(String action, dynamic value) {
  // 通过分布式数据通信分发分发
  _distributedChannel.send({
    'type': 'CONTROL',
    'action': action,
    'value': value,
  });
}
```

<!-- IMAGE_PLACEHOLDER: 用户在华为手机上滑动 Flutter 进度条，华为智慧屏对应的视频画面实时无损同步变化的实景动态图 -->
<!-- 类型: 动图 -->
<!-- 内容: 展示鸿蒙系统级 Cast 协议的超低延迟响应 -->

---

## 三、进阶：反向投屏（镜像控制）

在某些交互游戏中，我们需要把电视的画面映射到手机上，或者在手机上控制电视上的 3D 模型。

### 3.1 共享屏幕纹理
- ✅ **方案**：利用鸿蒙底层的 `screenCapture` 模块。将 TV 端的渲染结果捕获为视频流，通过 H.265 压缩后，利用软总线的可靠传输发送给手机端。
- ✅ **Flutter 侧**：手机端利用我们在 107 篇学过的 `Texture()` 组件实时解码并渲染这个画面，从而实现“第二屏”交互。

---

## 四、OpenHarmony 平台适配要点：连接稳定性

多屏交互中最怕“断连”。
- ✅ **推荐做法**：在 Flutter 侧维护一个 `SyncState` 模型。每隔 500ms 进行一次两端心跳对齐。如果检测到 Wi-Fi 环境不稳定，自动将投屏质量从 4K 降级为 720P，以确保播放不卡顿。

---

## 五、总结

多屏协同是“让屏幕动起来”：
1.  **系统级发现**：充分利用鸿蒙 Cast Kit，不要手写协议。
2.  **指令流转**：利用软总线实现手机对 TV 的物理级控制。
3.  **体验统一**：确保手机端遥控 UI 与 TV 端反馈高度同步。

第一百零九篇，我们将探讨如何利用大屏优势进行 **鸿蒙 TV 端的全场景分布教育与会议系统开发**。

---

> 📦 **跨端投屏组件包 (OhosCastKit)**：[open-harmony-examples/multi-screen-cast](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/multi-screen-cast)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
