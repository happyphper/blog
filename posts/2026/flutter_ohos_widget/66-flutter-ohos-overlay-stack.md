# Flutter for OpenHarmony 实战之基础组件：第六十六篇 Overlay — 实现全局悬浮窗与自由分层 UI

## 前言

在进行一些工具类或社交类应用开发时，我们经常需要这种视觉元素：一个常驻在屏幕右侧的“悬浮球”，或者是一个能跨越所有导航页面、直接弹出的“全局通知通知栏”。这些元素不属于任何一个具体的页面路由，而是漂浮在整个应用的最顶层。

在 **Flutter for OpenHarmony** 开发中，`Overlay` 是管理这些“插队” UI 元素的终极容器。它允许你直接向 `Navigator` 的叠加层中插入自定义 Widget。本文将详解如何利用 `Overlay` 打造一个鸿蒙风格的全局悬浮组件及弹窗管理系统。

---

## 一、Overlay 的核心概念

`Overlay` 是一个 Stack 结构的组件，它自动存在于每个 `MaterialApp` 中。
- **OverlayEntry**：叠加层中的一个子项。每个条目都可以独立显示、隐藏或调整位置。
- **Overlay.of(context)**：获取当前树中的 Overlay 状态对象。

---

## 二、实战：构建一个全局拖拽悬浮球

我们将实现一个不随页面跳转而消失，始终吸附在鸿蒙侧边的悬浮球。

### 2.1 创建并插入条目
```dart
OverlayEntry? _entry;

void _showFloatingBall() {
  _entry = OverlayEntry(
    builder: (context) => Positioned(
      top: 100,
      right: 20,
      child: GestureDetector(
        onPanUpdate: (details) {
          // 这里可以实现拖拽逻辑并调用 _entry?.markNeedsBuild()
        },
        child: const CircleAvatar(child: Icon(Icons.flash_on)),
      ),
    ),
  );
  
  // 插入到全局 Overlay 中
  Overlay.of(context).insert(_entry!);
}
```

---

## 三、进阶：局部弹窗避让与显隐动画

💡 **交互技巧**：使用 `Overlay` 弹出自定义弹窗时，通常需要一个半透明的遮罩层（Scrim）。

```dart
_entry = OverlayEntry(
  builder: (context) => Stack(
    children: [
       // 1. 半透明遮罩
       GestureDetector(onTap: () => _remove(), child: Container(color: Colors.black26)),
       // 2. 居中内容的弹窗
       Center(child: MyCustomDialog()),
    ],
  ),
);
```

<!-- IMAGE_PLACEHOLDER: 通过 Overlay 实现的全局悬浮球在鸿蒙多页面跳转间依然保持显示的动效 -->
<!-- 类型: GIF -->
<!-- 设备: 鸿蒙手机 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 悬浮窗与鸿蒙手势导航的冲突
鸿蒙系统大量依赖侧边滑动返回和底部上拉回桌面。

✅ **推荐方案**：
对于悬浮球类组件，建议限制其在 Y 轴的移动范围，不要让其紧贴底部的“手势线”区域。在鸿蒙端，建议给悬浮球设置一个吸附逻辑：当用户松开手后，悬浮球应自动平滑移动到最近的左右边缘，并保留 5-10 像素的间距，防止干扰系统的侧滑手势。

### 4.2 设置页面级别的 Overlay
如果不需要全局显示。

💡 **调优建议**：
在鸿蒙端，如果你的 Overlay 仅服务于当前页面，记得在 `dispose` 中一定要调用 `_entry?.remove()`。否则，当用户退出该页面时，这个叠加层依然会顽固地漂浮在其它页面之上，导致 UI 逻辑错误和内存泄漏。

### 4.3 宽屏/平行视界下的层级管理
针对鸿蒙平板多窗口。

✅ **最佳实践**：
在分屏模式下，`Overlay` 仅在当前应用所属的窗口内有效。当你从悬浮条点击触发一个大弹窗时，建议检查当前屏幕可用宽度。如果是宽屏，可以将弹窗偏向一侧显示，而不是暴力地遮盖全屏，这符合鸿蒙平行视界的设计美学。

<!-- IMAGE_PLACEHOLDER: 鸿蒙平板折叠屏下，悬浮控制台自动吸附与避让逻辑的视觉效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 五、完整示例代码

以下代码演示了一个简单的全局悬浮操作球控制系统。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: OverlayHome()));

class OverlayHome extends StatefulWidget {
  const OverlayHome({super.key});

  @override
  State<OverlayHome> createState() => _OverlayHomeState();
}

class _OverlayHomeState extends State<OverlayHome> {
  OverlayEntry? _overlayEntry;

  void _toggleOverlay() {
    if (_overlayEntry == null) {
      _overlayEntry = _createOverlayEntry();
      Overlay.of(context).insert(_overlayEntry!);
    } else {
      _overlayEntry?.remove();
      _overlayEntry = null;
    }
  }

  OverlayEntry _createOverlayEntry() {
    return OverlayEntry(
      builder: (context) => Positioned(
        bottom: 100,
        right: 20,
        child: Material(
          color: Colors.transparent,
          child: FloatingActionButton(
            onPressed: () => print("悬浮操作被触发"),
            child: const Icon(Icons.rocket_launch),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 全局叠加层实战')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(onPressed: _toggleOverlay, child: const Text("切换悬浮球显示")),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SecondPage())),
              child: const Text("跳转到下一页 (观察悬浮球是否消失)")
            ),
          ],
        ),
      ),
    );
  }
}

class SecondPage extends StatelessWidget {
  const SecondPage({super.key});
  @override
  Widget build(BuildContext context) => Scaffold(appBar: AppBar(title: const Text("第二页")));
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的设计进阶中，`Overlay` 是你操作路由栈以外空间的唯一钥匙。

1.  **分层思维**：将应用分为“路由层”和“全局叠加层”。
2.  **生命周期**：手动管理 `OverlayEntry` 的插入与移除是防止内存泄漏的必修课。
3.  **鸿蒙适配**：在这一层上，务必考虑与系统手势、多窗口环境的物理一致性，让悬浮组件既能快速直达，又不干扰系统的核心交互。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

