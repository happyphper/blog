![封面图](images/109-cover.png)

# Flutter for OpenHarmony 实战之殿堂：第一百零九篇 鸿蒙智慧屏 (TV) 实战 — 系统级画中画 (PiP) 与多窗协同

## 前言

电视的大屏优势如果不利用起来就是浪费。在 **HarmonyOS TV** 场景中，有一种极其高级的体验：**画中画 (Picture-in-Picture)**。用户可以在一边看球赛直播的同时，通过角落的小窗口监控家门口的摄像头，或者在悬浮窗里回复消息。

作为 **Flutter for OpenHarmony** 开发者，如何打通这种跨窗口的渲染？如何实现窗口间的通信？本篇将带你跨越窗口边界。

---

## 一、鸿蒙端画中画 (PiP) 的实现机制

在鸿蒙系统中，画中画不是简单的层级叠加，而是涉及到了物理窗口（Window）的拆分：
- **主窗口**：承载完整的 Flutter 应用。
- **浮窗 (Float Window)**：一个受系统托管的、具备独立渲染表面（Surface）的小型窗口。

---

## 二、实战：将 Flutter 全屏视频实时推送到系统浮窗

### 2.1 启动 PiP 模式
利用鸿蒙原生的 `PiPController` 模块。

```typescript
// 💡 原理：在原生侧声明画中画权限并启动
import pip from '@ohos.pip';

async function enterPipMode() {
  let pipController = await pip.create({
    context: this.context,
    templateType: pip.PiPTemplateType.VIDEO_PLAY,
    // 📌 指向包含视频流的原生节点
    contentNode: this.videoXComponent
  });
  pipController.start();
}
```

### 2.2 在 Flutter 侧同步浮窗状态
当手机/电视进入 PiP 模式时，Flutter 层需要动态隐藏非核心 UI（如评论区、侧边栏），并调整布局。

```dart
// 📌 监听窗口模式变更模式变更
void onWindowModeChanged(WindowMode mode) {
  if (mode == WindowMode.pip) {
    setState(() => _isPipMode = true);
  }
}
```

<!-- IMAGE_PLACEHOLDER: 华为智慧屏大背景播放电影，右下角悬浮窗实时展示 Flutter 编写的智能家居摄像监控画面的实拍图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示多窗口协作的科技感 -->

---

## 三、进阶：双窗间的数据实时隧道

如果用户在浮窗里点击了“关灯”，主窗口的状态也需要同步更新。

### 3.1 跨窗口通信
- ✅ **方案**：利用鸿蒙原生的 **Emitter** 机制或我们的老朋友分布式数据对象（Distributed Data Object）。
- ✅ **Flutter 侧**：两个窗口虽然共享一份 AOT 资产，但可能运行在不同的 Engine 实例中。因此，统一的 `MethodChannel` 回调监听是保证同步的关键。

---

## 四、OpenHarmony 平台适配要点：资源抢占

在 TV 端开启 PiP 意味着设备同时开启了两个视频解码流。
- ⚠️ **风险**：低端智慧屏可能会因 VPU 压力过大而崩溃。
- ✅ **建议**：在进入 PiP 前，通过原生插件查询系统剩余显存。如果显存不足，自动将主窗口的视频流分辨率从 4K 压制到 1080P，为浮窗腾出硬件解码空间。

---

## 五、总结

画中画是“多模态”开发的进阶：
1.  **窗口意识**：学会管理非全屏状态下的 Flutter 表现。
2.  **分片渲染**：利用 `contentNode` 将视频纹理路由到不同的窗口。
3.  **平滑过渡**：入窗和出窗的动画必须连贯。

在这一篇的加持下，你的 TV 应用将不再是一个死板的矩形，而是一个可以随处安放、灵活互动的“智慧体”。

第一百一十篇，我们将为 TV 专栏收官，探讨 **鸿蒙智慧屏应用的自动化云端多机型性能评测**。

---

> 📦 **画中画专用适配组件 (Ohos-PiP-Helper)**：[open-harmony-examples/tv-pip-toolkit](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/tv-pip-toolkit)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
