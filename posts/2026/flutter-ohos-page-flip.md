![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战：手把手教你实现 3D 仿真翻书动画

> **摘要**：在阅读类应用中，翻页动画是个极其提升质感的功能。本文将深入探讨如何在 Flutter for OpenHarmony 平台上，通过 Matrix4 矩阵变换和 AnimationController 打造一个高性能的 3D 仿真翻书动画，并适配鸿蒙折叠屏设备的交互。

## 前言

随着鸿蒙生态的快速发展，开发者对 UI 的追求已经从“能用”转向了“精致”。翻书动画（Page Flip）由于涉及复杂的 3D 变换和手势数学计算，往往被视为 UI 开发的高级门槛。

在 Flutter 的原生渲染引擎支持下，我们无需依赖三方库，仅通过内置的 `Transform` 组件即可实现丝滑的翻页效果。

**本文你将学到**：
- Matrix4 透视矩阵的核心原理（setEntry 详解）
- 如何平衡 3D 转换中的正面与反面层级
- 手势滑动量与动画弧度的映射逻辑
- 针对鸿蒙折叠屏（Mate X 系列）的适配优化

---

## 一、数学基础：Matrix4 3D 变换

要在 2D 屏幕上模拟 3D 翻页，我们需要用到**矩阵变换**。

```dart
// 在透视矩阵中，第3行第2列的值决定了透视感
final matrix = Matrix4.identity()
  ..setEntry(3, 2, 0.001) // 值越大，近大远小的透视效果越强烈
  ..rotateY(_animation.value); // 围绕 Y 轴旋转
```

如果没有 `setEntry(3, 2, 0.001)`，旋转看起来只是宽度在缩放（正交投影），而没有空间感。

<!-- IMAGE_PLACEHOLDER: 透视与正交投影对比 -->
<!-- 类型: 示例图 -->
<!-- 内容: 展示 setEntry 开启前后的旋转效果差异 -->

---

## 二、核心组件：FlipPage 结构

一个完整的翻页动作由三部分组成：
1. **Static Page (底页)**：当前页面的后续内容。
2. **Foreground (翻转页正面)**：正在翻转的当前页面。
3. **Background (翻转页反面)**：翻页后露出的下一页背面。

### 2.1 状态管理

```dart
class BookFlipWidget extends StatefulWidget {
  final Widget front; // 当前页
  final Widget back;  // 下一页内容

  const BookFlipWidget({super.key, required this.front, required this.back});

  @override
  State<BookFlipWidget> createState() => _BookFlipWidgetState();
}

class _BookFlipWidgetState extends State<BookFlipWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  
  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    );
  }
}
```

---

## 三、代码实现：翻页动画

### 3.1 核心构建逻辑

为了让翻页看起来更自然，我们需要根据旋转角度（0 到 π）来动态切换显示正面还是反面。

```dart
Widget _buildFlipAnimation() {
  return AnimatedBuilder(
    animation: _controller,
    builder: (context, child) {
      // 弧度计算：从 0 (未翻开) 到 -pi (完全向左翻转)
      double rotateValue = -_controller.value * pi;
      bool isFront = rotateValue > -pi / 2; // 是否旋转未过半

      return Transform(
        transform: Matrix4.identity()
          ..setEntry(3, 2, 0.001)
          ..rotateY(rotateValue),
        alignment: Alignment.centerLeft, // 以左侧为轴
        child: isFront 
          ? widget.front // 显示正面
          : Transform(
              // 当翻转过半时，需要垂直翻转反面内容，否则字是反的
              transform: Matrix4.identity()..rotateY(pi),
              alignment: Alignment.center,
              child: widget.back, // 显示反面内容
            ),
      );
    },
  );
}
```

### 3.2 完整代码封装

```dart
import 'dart:math';
import 'package:flutter/material.dart';

class PageFlipAnimation extends StatefulWidget {
  const PageFlipAnimation({super.key});

  @override
  State<PageFlipAnimation> createState() => _PageFlipAnimationState();
}

class _PageFlipAnimationState extends State<PageFlipAnimation> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  bool _isFlipped = false;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
  }

  void _togglePage() {
    if (_isFlipped) {
      _controller.reverse();
    } else {
      _controller.forward();
    }
    _isFlipped = !_isFlipped;
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _togglePage,
      child: Center(
        child: Stack(
          children: [
            // 底页：下一页的内容
            _buildPaper(Colors.white, "这是下一页的内容..."),
            
            // 动画层：正在翻转的页
            AnimatedBuilder(
              animation: _controller,
              builder: (context, child) {
                double angle = _controller.value * pi;
                return Transform(
                  alignment: Alignment.centerLeft,
                  transform: Matrix4.identity()
                    ..setEntry(3, 2, 0.0015)
                    ..rotateY(-angle),
                  child: angle < pi / 2
                      ? _buildPaper(Colors.blue[50]!, "当前页封面\n点击翻页")
                      : Transform(
                          alignment: Alignment.center,
                          transform: Matrix4.identity()..rotateY(pi),
                          child: _buildPaper(Colors.grey[100]!, "下一页的背面样式"),
                        ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPaper(Color color, String text) {
    return Container(
      width: 300,
      height: 450,
      decoration: BoxDecoration(
        color: color,
        borderRadius: const BorderRadius.only(
          topRight: Radius.circular(12),
          bottomRight: Radius.circular(12),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(5, 5),
          )
        ],
      ),
      padding: const EdgeInsets.all(24),
      child: Center(
        child: Text(
          text,
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 20, color: Colors.blueGrey),
        ),
      ),
    );
  }
  
  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
```

---

## 四、鸿蒙适配：响应式翻页

在 OpenHarmony 平台上，特别是像 **华为 Mate X6** 这样的折叠屏设备中，展开后屏幕变为类似 Pad 的大屏，这时单张“翻书”可能显得过小。

### 4.1 适配方案：双栏翻页

我们可以利用 `MediaQuery` 判断屏幕宽度，如果是大屏，则切换为“双栏翻书”模式。

```dart
Widget build(BuildContext context) {
  final width = MediaQuery.of(context).size.width;
  bool isFoldableExpanded = width > 600;

  return isFoldableExpanded 
    ? Row(
        // 在折叠屏展开态，左右两页对称布局
        children: [
           LeftPage(),
           RightPageFlipAnimation(),
        ],
      )
    : NormalFlipAnimation();
}
```

---

## 五、进阶：添加阴影与纸张卷曲感

为了增加真实感，翻页过程中光影应该随角度变化：

1. **阴影**：在反面（下一页背面）叠加一个半透明蒙层，角度越大，蒙层越淡。
2. **边缘卷曲**：通过 `LinearGradient` 模拟纸张边缘的受光面和背光面。

```dart
// 模拟翻页阴影效果
Container(
  decoration: BoxDecoration(
    gradient: LinearGradient(
      colors: [
        Colors.black.withOpacity(0.3 * (1 - _controller.value)),
        Colors.transparent,
      ],
      begin: Alignment.centerLeft,
      end: Alignment.centerRight,
    ),
  ),
)
```

---

## 六、总结

通过本文的实战，我们成功在 Flutter for OpenHarmony 上实现了一个具有 3D 透视感的仿真翻书动画。

### 关键要点：
1. **Matrix4** 是实现 3D 效果的灵魂。
2. **层级控制**：翻转过半（90度）时是视觉切换的关键点。
3. **平台适配**：针对鸿蒙折叠屏设计响应式体验。

这样的动画效果不仅可以用于电子书阅读器，还可以用于精美的产品图册展现或具有仪式感的信封开启交互。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: feature/book-flip-animation)](https://atomgit.com/dragonbady/open-harmony-example/tree/feature/book-flip-animation)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
