# Flutter for OpenHarmony 实战之基础组件：第四十九篇 CustomPaint — 释放像素级的创意绘制力

## 前言

虽然 Flutter 提供了极其丰富的预置组件，但在追求独特视觉风格或处理动态数据可视化（如自定义图表、复杂的路径动画）时，传统的组件堆砌往往显得力不从心。这时，我们就需要掌握 Flutter 绘图系统的核心——`CustomPaint`。

在 **Flutter for OpenHarmony** 平台上，利用 Skia 引擎（或 Impeller）的强大性能，我们可以通过 `CustomPaint` 直接在画布（Canvas）上指挥每一个像素。本文将带大家从零开始，实战绘制几何形状与一个基础的动态饼图，开启鸿蒙应用的原生图形开发之旅。

---

## 一、CustomPaint 与 CustomPainter：画家与画板

- **CustomPaint**：是 Widget，它在组件树中占据位置，类似于一块“画板”。
- **CustomPainter**：是逻辑类，你在这里编写具体的绘图指令（画线、画圆等），它是真正的“画家”。

---

## 二、实战演练：绘制一个基础几何画板

### 2.1 定义 Painter
我们需要重写两个核心方法：
- `paint`: 获取 `Canvas` 和 `Size`，进行具体绘制。
- `shouldRepaint`: 决定何时需要重新重绘（通常与数据变化联动）。

```dart
class MyPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    // 1. 定义画笔
    final paint = Paint()
      ..color = Colors.blue
      ..strokeWidth = 4.0
      ..style = PaintingStyle.stroke; // 描边模式

    // 2. 绘制圆形
    canvas.drawCircle(Offset(size.width / 2, size.height / 2), 50, paint);
    
    // 3. 绘制线段
    canvas.drawLine(Offset.zero, Offset(size.width, size.height), paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}
```

### 2.2 在组件中使用
```dart
CustomPaint(
  size: const Size(200, 200), // 指定画布大小
  painter: MyPainter(),
)
```

<!-- IMAGE_PLACEHOLDER: CustomPaint 绘制的基本几何图形在鸿蒙端渲染预览 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、进阶：构建动态进度饼图

数据可视化是 `CustomPaint` 的主战场。

### 3.1 扇形绘制逻辑
```dart
void paint(Canvas canvas, Size size) {
  final rect = Rect.fromLTWH(0, 0, size.width, size.height);
  final paint = Paint()
    ..style = PaintingStyle.fill
    ..isAntiAlias = true;

  // 绘制蓝色扇形 (代表 70%)
  paint.color = Colors.blue;
  canvas.drawArc(rect, 0, 3.14 * 2 * 0.7, true, paint);
  
  // 绘制灰色背景
  paint.color = Colors.grey[200]!;
  canvas.drawArc(rect, 3.14 * 2 * 0.7, 3.14 * 2 * 0.3, true, paint);
}
```

<!-- IMAGE_PLACEHOLDER: 动态饼图在鸿蒙平板统计报表页面的应用效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 抗锯齿与分辨率适配
鸿蒙设备屏幕像素密度极高（DPI）。

✅ **推荐方案**：
在创建 `Paint` 时，务必设置 `isAntiAlias = true`。如果不开启抗锯齿，在鸿蒙的高清缩放屏幕下，曲线和圆形的边缘会有明显的颗粒感，影响界面的“高级感”。

### 4.2 性能监控与重绘控制
`CustomPaint` 如果在动画中频繁执行，会造成 CPU 压力。

💡 **调优建议**：
在 `shouldRepaint` 中进行精细化判断。只有当外部传入的“数据百分比”或“颜色配置”确实发生变化时才返回 `true`。对于不需要交互的复杂静态背景，建议使用 `RepaintBoundary` 进行包裹，强制 Flutter 对该层进行位图缓存，避免冗余重绘。

### 4.3 触控坐标转换
在鸿蒙应用的自定义图表中，用户点击了某个扇区。

✅ **最佳实践**：
由于 `CustomPainter` 本身不具备事件监听能力。你需要将其嵌套在 `GestureDetector` 中，通过 `onPanDown` 获取到屏幕绝对坐标后，利用组件的 `RenderBox` 转换为 Canvas 内部的相对坐标，再进行碰撞检测逻辑判定（如计算点击点与圆心的距离）。

<!-- IMAGE_PLACEHOLDER: 鸿蒙应用导航轨迹绘制动效预览 -->
<!-- 类型: 截图 -->
<!-- 设备: 模拟器 -->

---

## 五、完整示例代码

以下代码演示了一个可以根据滑块实时改变填充比例的“动态百分比仪表盘”。

```dart
import 'package:flutter/material.dart';
import 'dart:math' as math;

void main() => runApp(const MaterialApp(home: CustomChartPage()));

class CustomChartPage extends StatefulWidget {
  const CustomChartPage({super.key});

  @override
  State<CustomChartPage> createState() => _CustomChartPageState();
}

class _CustomChartPageState extends State<CustomChartPage> {
  double _percent = 0.5;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 自定义图形实战')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CustomPaint(
              size: const Size(200, 200),
              painter: ProgressPainter(_percent),
            ),
            const SizedBox(height: 50),
            Slider(
              value: _percent,
              onChanged: (v) => setState(() => _percent = v),
            ),
            Text("当前下载进度: ${(_percent * 100).toInt()}%"),
          ],
        ),
      ),
    );
  }
}

class ProgressPainter extends CustomPainter {
  final double percentage;
  ProgressPainter(this.percentage);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;
    
    // 1. 绘制背景暗色圆环
    final bgPaint = Paint()
      ..color = Colors.grey[300]!
      ..style = PaintingStyle.stroke
      ..strokeWidth = 15;
    canvas.drawCircle(center, radius, bgPaint);
    
    // 2. 绘制进度彩色圆弧
    final progressPaint = Paint()
      ..color = Colors.blue[800]!
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round
      ..strokeWidth = 15;
    
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -math.pi / 2, // 从正上方开始
      math.pi * 2 * percentage, 
      false, 
      progressPaint
    );
  }

  @override
  bool shouldRepaint(covariant ProgressPainter oldDelegate) {
    return oldDelegate.percentage != percentage;
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的视觉无人区探索中，`CustomPaint` 是你最后的底牌。

1.  **无限自由度**：只要 Path 能够到达的地方，画面就能呈现。
2.  **性能优先**：在大屏鸿蒙设备上通过 `RepaintBoundary` 进行分层存储是必修课。
3.  **万物皆可绘**：从简单的进度环到复杂的股票 K 线图，掌握了坐标系与画笔，就掌握了 UI 设计的终极话语权。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

