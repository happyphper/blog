# Flutter for OpenHarmony 实战之基础组件：第四十二篇 Transform, RotatedBox 与 FittedBox — 空间变换与布局自适应

## 前言

在追求动感 UI 和精细适配的过程中，掌握组件的“次元变换”能力至关重要。你是否想过让一个图标旋转 45 度？或者让一个巨大的图片在极小的容器内保持比例缩放？甚至是实现 3D 翻转效果？

在 **Flutter for OpenHarmony** 平台上，`Transform`、`RotatedBox` 和 `FittedBox` 分别从矩阵变换、物理旋转和容器适配三个维度，赋予了开发者极强的空间控制力。本文将深度剖析这三者的差异及实战应用场景，让你的鸿蒙应用布局更加游刃有余。

---

## 一、Transform：强大的 4x4 矩阵变换

`Transform` 允许你在渲染阶对组件进行旋转、缩放、平移甚至三维形变。

### 1.1 基础变换类型
- **旋转 (Rotate)**：绕中心点旋转。
- **缩放 (Scale)**：按倍率放大缩小。
- **平移 (Translate)**：位置偏移。

### 1.2 3D 转换实战
这是 `Transform` 最迷人的地方，通过 `Matrix4` 改变 Z 轴视角。

```dart
Transform(
  transform: Matrix4.identity()
    ..setEntry(3, 2, 0.001) // 设置透视效果
    ..rotateY(0.5),        // 绕 Y 轴旋转，产生 3D 翻转感
  alignment: FractionalOffset.center,
  child: Container(
    width: 200, height: 100,
    color: Colors.blueAccent,
    child: const Center(child: Text("3D 翻转卡片", style: TextStyle(color: Colors.white))),
  ),
)
```

<!-- IMAGE_PLACEHOLDER: 3D 翻转效果在鸿蒙手机上的视觉展示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 二、RotatedBox：具有“物理体积”的旋转

尽管 `Transform.rotate` 也能旋转，但它属于**绘制阶段**的变换。而被旋转的组件在布局阶段依然占据旋转前的矩形空间。

### 2.1 核心区别
`RotatedBox` 会在**布局阶段**进行旋转。这意味着它会真实改变父容器的宽高计算，类似于我们在 Word 中旋转图片的操作。

```dart
RotatedBox(
  quarterTurns: 1, // 顺时针旋转 90 度 (1 quarter = 90 deg)
  child: const Text("我是被竖着放的标题"),
)
```

💡 **选型建议**：如果你需要旋转一个 Tab 标签并让其它组件正确排开，请选 `RotatedBox`；如果你只是想做一个旋转动画且不影响布局，请选 `Transform`。

---

## 三、FittedBox：内容适配的专家

当子组件的尺寸大于父组件分配的空间时，`FittedBox` 会根据指定的适配模式（Fit）自动对子组件进行缩放。

### 3.1 适配模式详解
- **BoxFit.contain**：缩放以确保内容完全显示（默认）。
- **BoxFit.cover**：缩放以填满容器，可能部分被裁剪。
- **BoxFit.fill**：拉伸以填满容器，不保证比例。

```dart
Container(
  width: 200, height: 100,
  color: Colors.grey[200],
  child: FittedBox(
    fit: BoxFit.contain, // 确保复杂的 Logo 不被挤压
    child: Row(
      children: [
        Icon(Icons.stars, color: Colors.blue),
        Text("这是一个很长很长的适配文案"),
      ],
    ),
  ),
)
```

<!-- IMAGE_PLACEHOLDER: 不同 BoxFit 模式在鸿蒙平板分屏窄窗口下的适配效果对比 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 动画性能优选
在鸿蒙高刷屏幕上，实现组件旋转动画。

✅ **推荐方案**：
避免直接在 `build` 方法里修改 `RotatedBox` 的参数来实现动画，因为这会触发昂贵的重新布局（Re-layout）。应结合 `Transform` 和 `AnimationController`，因为 `Transform` 的计算是在绘制层完成的，性能极佳。

### 4.2 响应式文本自适应
由于鸿蒙系统支持不同的字体缩放级别。

💡 **调优建议**：
在小卡片内部，如果怕长文字溢出（Overflow），可以使用 `FittedBox` 包裹 `Text`。这样当文字过长时，它会自动在容器内缩小字号显示，而不是粗鲁地截断。

### 4.3 刘海屏旋转避让
在鸿蒙手机从横屏转为竖屏时。

✅ **最佳实践**：
如果使用了 3D 变换的背景，注意在旋转过程中检查 `SafeArea`。因为变换后的组件边缘可能会超出安全区域，导致与鸿蒙系统的任务栏发生视觉冲突。

---

## 五、完整示例代码

以下代码演示了一个带有“3D 轮播感”、“自适应文字”和“物理旋转标签”的演示页面。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: TransformDemo()));

class TransformDemo extends StatefulWidget {
  const TransformDemo({super.key});

  @override
  State<TransformDemo> createState() => _TransformDemoState();
}

class _TransformDemoState extends State<TransformDemo> {
  double _sliderValue = 0.0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 变换与适配实战')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            // 1. 3D 变换展示
            const Text("1. Transform (3D 矩阵变换)"),
            const SizedBox(height: 20),
            Transform(
              transform: Matrix4.identity()
                ..setEntry(3, 2, 0.001)
                ..rotateX(_sliderValue), // 随滑动条动态旋转
              alignment: Alignment.center,
              child: Card(
                color: Colors.indigo,
                child: Container(width: 250, height: 120, child: const Center(child: Text("拖动滑块试试", style: TextStyle(color: Colors.white)))),
              ),
            ),
            Slider(value: _sliderValue, min: 0, max: 1.5, onChanged: (v) => setState(() => _sliderValue = v)),
            
            const SizedBox(height: 60),
            // 2. 物理旋转
            const Text("2. RotatedBox (90度物理布局)"),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const RotatedBox(quarterTurns: 3, child: FlutterLogo(size: 60)),
                const SizedBox(width: 20),
                const Text("我是被父容器\n重新计算过的布局"),
              ],
            ),
            
            const SizedBox(height: 60),
            // 3. 内容适配
            const Text("3. FittedBox (自适应缩放)"),
            const SizedBox(height: 20),
            Container(
              width: 150, height: 60,
              color: Colors.blue[50],
              child: const FittedBox(
                child: Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text("无论这段话多长，它都会在这个框里完整显示"),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 开发中，熟练利用这三个组件能让你的 UI 极具动态张力与环境韧性。

1.  **Transform**：追求酷炫动效与 3D 表现的首选，性能最优。
2.  **RotatedBox**：针对固定角度布局（如报表侧边的竖写文字）的最稳健方案。
3.  **FittedBox**：是解决长文案、大图标在小容器内“不体面”溢出的万能钥匙。

合理组合这三者，你的鸿蒙应用将不再局限于二维平面的堆切，而是呈现出一种富有弹性且深度的现代视觉质感。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

