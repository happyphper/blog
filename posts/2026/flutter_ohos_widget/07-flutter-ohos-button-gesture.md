![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第七篇 Button 按钮与手势交互

> **摘要**：一个好的 App 不仅要“好看”，还要“好用”。本文全面解析 Flutter 中的按钮组件体系（Elevated/Text/Outlined），深入对比 InkWell 与 GestureDetector 的使用场景，并手把手教你在 OpenHarmony 上实现全功能的“可拖拽悬浮球”交互。

## 前言

用户与 App 最直接的交流方式就是**点击**和**触摸**。

Flutter 提供了两套交互体系：
1. **封装好的按钮组件**：直接能用，符合 Material Design 规范。
2. **底层手势系统**：`GestureDetector`，可以把任何组件变成可交互的，并支持复杂的拖拽、缩放逻辑。

**本文你将学到**：
- Material 3 风格按钮全家桶的使用与样式定制
- InkWell 水波纹效果的实现原理
- GestureDetector 捕获点击、长按、双击、拖拽
- 实战：打造一个系统级的可拖拽悬浮球
- 解决手势冲突 (GestureArena) 的基本思路

![Flutter 按钮与手势交互概念图 (中文版)](./images/flutter_ohos_button_gesture_concept_cn.png)

---

## 一、Flutter 按钮全家桶

在 Flutter 2.0+ 之后，官方推荐使用新一代的按钮组件。

### 1.1 三大基础按钮

| 组件 | 场景 | 特点 |
|---|---|---|
| **ElevatedButton** | 主要操作 | 有阴影、有背景色，立体感强 |
| **OutlinedButton** | 次要操作 | 无背景、有边框，清爽 |
| **TextButton** | 辅助/低频操作 | 无背景、无边框，仅文字，常用于 Dialog |

```dart
Column(
  children: [
    // 1. 实心按钮 (原 RaisedButton)
    ElevatedButton(
      onPressed: () => print('点击提交'),
      child: const Text('提交订单'),
    ),
    
    // 2. 边框按钮
    OutlinedButton(
      onPressed: () {},
      child: const Text('取消'),
    ),
    
    // 3. 文本按钮 (原 FlatButton)
    TextButton(
      onPressed: () {},
      child: const Text('了解更多'),
    ),
  ],
)
```

### 1.2 样式定制 (ButtonStyle)

不喜欢默认的蓝色？没问题，`style` 属性可以完全自定义。

```dart
ElevatedButton(
  onPressed: () {},
  style: ElevatedButton.styleFrom(
    backgroundColor: Colors.purple, // 背景色
    foregroundColor: Colors.white,  // 文字/图标色
    elevation: 8,                   // 阴影高度
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(20), // 圆角
    ),
    padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
  ),
  child: const Text('自定义按钮'),
)
```

### 1.3 IconButton 与 FAB

- **IconButton**: 纯图标按钮，常用于 AppBar。
- **FloatingActionButton (FAB)**: 页面右下角的悬浮按钮。

```dart
// 图标按钮
IconButton(
  icon: const Icon(Icons.thumb_up),
  color: Colors.blue,
  onPressed: () {},
)

// 悬浮按钮
FloatingActionButton(
  onPressed: () {},
  child: const Icon(Icons.add),
)
```

---

## 二、InkWell vs GestureDetector

如果我想让一个普通的 `Container` 或者 `Image` 也能被点击，该怎么办？

### 2.1 InkWell (带水波纹)

如果你希望点击时有 Material Design 风格的水波纹扩散效果，**必须**使用 `InkWell`。

⚠️ **注意**：`InkWell` 必须放在 `Material` 组件内部，或者父级有 Material 属性，否则水波纹无法显示（因为水波纹是在 Material 层上绘制的）。

```dart
Material(
  color: Colors.transparent, // 必须透明，否则挡住下面的内容
  child: InkWell(
    onTap: () {},
    borderRadius: BorderRadius.circular(8),
    splashColor: Colors.blue.withOpacity(0.3), // 波纹颜色
    child: Container(
      padding: const EdgeInsets.all(12),
      child: const Text('带水波纹的点击区域'),
    ),
  ),
)
```

### 2.2 GestureDetector (全能王)

如果你不需要水波纹，或者需要监听更复杂的手势（拖拽、缩放），就用它。它没有任何视觉效果，纯粹处理逻辑。

```dart
GestureDetector(
  onTap: () => print('单击'),
  onDoubleTap: () => print('双击666'),
  onLongPress: () => print('长按触发'),
  child: Container(
    color: Colors.blue[100],
    padding: const EdgeInsets.all(20),
    child: const Text('全能手势识别区'),
  ),
)
```

---

## 三、实战：可拖拽悬浮球 (Draggable FAB)

在鸿蒙大屏设备上，固定位置的悬浮按钮可能会挡住内容。我们来实现一个可以随手指拖拽，松手后吸附到屏幕边缘的悬浮球。

```dart
class DraggableFloatingBall extends StatefulWidget {
  const DraggableFloatingBall({super.key});

  @override
  State<DraggableFloatingBall> createState() => _DraggableFloatingBallState();
}

class _DraggableFloatingBallState extends State<DraggableFloatingBall> {
  // 初始位置
  Offset _offset = const Offset(300, 500);

  @override
  Widget build(BuildContext context) {
    // 使用 Stack 进行定位
    return Stack(
      children: [
        Positioned(
          left: _offset.dx,
          top: _offset.dy,
          child: GestureDetector(
            // 1. 监听拖拽更新
            onPanUpdate: (details) {
              setState(() {
                // 累加手指滑动的偏移量
                _offset += details.delta;
              });
            },
            // 2. 监听拖拽结束 (松手吸附逻辑)
            onPanEnd: (details) {
              final screenWidth = MediaQuery.of(context).size.width;
              double targetX;
              
              // 判断靠左还是靠右
              if (_offset.dx + 25 < screenWidth / 2) {
                targetX = 16; // 靠左边距
              } else {
                targetX = screenWidth - 66; // 靠右边距 (Size 50 + Margin 16)
              }
              
              setState(() {
                // 只改变 X 轴吸附，Y 轴保持不动
                _offset = Offset(targetX, _offset.dy);
              });
            },
            child: Container(
              width: 50,
              height: 50,
              decoration: BoxDecoration(
                color: Colors.blue,
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.3),
                    blurRadius: 8,
                    offset: const Offset(0, 4),
                  )
                ],
              ),
              child: const Icon(Icons.apps, color: Colors.white),
            ),
          ),
        ),
      ],
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 悬浮球拖拽动图 -->
<!-- 类型: 鸿蒙设备录屏 -->
<!-- 内容: 演示手指拖动悬浮球，松手后自动吸附到屏幕边缘 -->

---

## 四、手势竞技场 (Gesture Arena)

当多个手势组件嵌套时（例如：水平滑动的列表里有一个可以点击的按钮），谁来响应手势？Flutter 有一套竞技场机制。

**原则**：
1. 父组件和子组件竞争，通常子组件优先。
2. 只有胜出者才会获得后续的事件流。

**常见问题**：
`ListView` 里的 Item 无法横向滑动删除？
**解决**：这是典型的冲突。如果在 `ListView` 里使用横向手势，需要确保手势方向准确，或者使用 `Listener` 直接监听原始指针事件。

---

## 五、总结

交互是 App 的灵魂。

### 核心要点
1.  **按钮选型**：首选 `ElevatedButton`，次选 `Outlined/TextButton`。
2.  **视觉反馈**：哪怕是自定义点击区域，也尽量加上 `InkWell` 水波纹，让用户知道“我点到了”。
3.  **手势控制**：简单的点击用 `onTap`，复杂的拖拽用 `onPanUpdate`。
4.  **鸿蒙特性**：在大屏设备上，可拖拽的悬浮操作（如上的实战）能显著提升单手操作体验。

### 下一篇预告
到目前为止，我们已经能展示内容（Text/Image/List）并响应用户的点击（Button）。但是如何让用户**输入内容**呢？
**《Flutter for OpenHarmony 实战之基础组件：第八篇 TextField 输入框与表单》**
这将是基础组件系列的**最终篇**。我们将学习如何处理文本输入、表单校验、键盘遮挡处理以及自定义输入框样式。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/7-button-gesture)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/7-button-gesture)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
