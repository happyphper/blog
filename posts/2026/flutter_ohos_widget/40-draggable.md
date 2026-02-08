# Flutter for OpenHarmony 实战之基础组件：第四十篇 Draggable 与 DragTarget — 实现直观的拖拽数据交互

## 前言

在移动端应用中，除了点击和滑动，最能体现交互深度的就是“拖拽”（Drag and Drop）。无论是将商品拖入购物车、整理文件位置，还是在拼图游戏中移动碎片，拖拽交互都能为用户提供极其直观的操作反馈感。

在 **Flutter for OpenHarmony** 开发中，内置的 `Draggable` 和 `DragTarget` 是一对完美的搭档。它们能让你轻松实现跨区域的数据搬运，且能完美自动适配鸿蒙多窗口、多分屏下的触控手势。本文将详解这对组合的机制及高级实战技巧。

---

## 一、拖拽三部曲：数据搬运的底层机制

拖拽交互涉及三个核心组件：

1.  **Draggable**：被拖动的源组件，负责携带数据（Data）。
2.  **DragTarget**：接收数据的目标区域，负责处理数据接收逻辑（Accept/Reject）。
3.  **LongPressDraggable**（可选）：仅在长按后才触发拖动的变体，常用于避免与列表滑动手势冲突。

---

## 二、Draggable：赋予组件“漂浮”的能力

`Draggable` 不仅能携带数据，还能定义拖动中、拖动后的不同外观。

### 1.1 基础实现
```dart
Draggable<String>(
  data: '这是被传递的包裹', // 核心：传递的数据
  child: _buildItem('拖动我'), // 处于原始位置时的样子
  feedback: _buildItem('我飞起来了', isFeeback: true), // 拖动过程中悬浮在手指底下的样子
  childWhenDragging: _buildPlaceholder(), // 拖走后留在原地的占位样子
)
```

### 1.2 跨页面传递
💡 **提示**：只要 `Draggable` 发送的数据类型与 `DragTarget` 接收的类型一致，哪怕它们不在同一个父容器下，也能完成交互。

---

## 三、DragTarget：数据的港湾

`DragTarget` 实时感知上方是否有 `Draggable` 经过，并决定是否“开门迎接”。

### 2.1 接收逻辑控制
```dart
DragTarget<String>(
  // 实时回调：当有东西从上方滑过
  onWillAccept: (data) => data != null, 
  // 核心回调：当用户在上方松手
  onAccept: (data) {
    setState(() {
      _receivedData = data;
    });
  },
  builder: (context, candidateData, rejectedData) {
    return Container(
      width: 200, height: 200,
      color: candidateData.isNotEmpty ? Colors.blue[100] : Colors.grey[200],
      child: const Center(child: Text("放这里")),
    );
  },
)
```

<!-- IMAGE_PLACEHOLDER: 组件拖动中与目标区域高亮反馈在鸿蒙设备上的展示效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 四、实战：构建一个简单的“分类分发系统”

假设我们要将不同的“功能模块”拖入“我的工具箱”：

```dart
Row(
  mainAxisAlignment: MainAxisAlignment.spaceAround,
  children: [
    Draggable<String>(data: '扫一扫', feedback: _p(Icons.qr_code_scanner), child: _p(Icons.qr_code_scanner)),
    Draggable<String>(data: '付款码', feedback: _p(Icons.payment), child: _p(Icons.payment)),
    
    DragTarget<String>(
      onAccept: (v) => _showResult(v),
      builder: (c, list, _) => Container(
         width: 100, height: 100, 
         child: Icon(Icons.shopping_cart, color: list.isNotEmpty ? Colors.red : Colors.grey),
      ),
    ),
  ],
)
```

<!-- IMAGE_PLACEHOLDER: 拖动组件进入购物车的成功反馈效果动图 -->
<!-- 类型: GIF -->
<!-- 设备: 鸿蒙模拟器 -->

---

## 五、OpenHarmony 平台适配建议

### 5.1 触控手势冲突处理
在鸿蒙系统上，全局侧滑返回或页面上下滚动可能会打断拖拽手势。

✅ **推荐方案**：
对于列表中的拖拽项，务必使用 `LongPressDraggable`。这样用户只有在长按确认后才开始拖动，正常滑动则作为列表滚动处理，这完全符合鸿蒙系统的交互逻辑。

### 5.2 窗口缩放与坐标平移
鸿蒙应用支持自由缩放窗口。

💡 **调优建议**：
在 `feedback` 节点设计时，尽量不使用固定像素（Px）的位置偏移，而是依靠 `Material` 包装，并确保拖动过程中外层有 `Overlay` 支持（Flutter 自动处理，但要注意 Z-Index）。

### 5.3 震动马达反馈 (HapticFeedback)
拖拽开始、进入目标区域、放置成功，这三个节点应给予用户明确的触感。

```dart
import 'package:flutter/services.dart';

// 开始拖动
onDragStarted: () => HapticFeedback.heavyImpact(),
// 成功放置
onAccept: (v) => HapticFeedback.vibrate(),
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙平板分屏状态下跨窗口（应用内）拖拽演示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 六、完整示例代码

以下代码演示了一个带有“垃圾桶回收”功能的拖拽排序/清理示例。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: DragDropDemo()));

class DragDropDemo extends StatefulWidget {
  const DragDropDemo({super.key});

  @override
  State<DragDropDemo> createState() => _DragDropDemoState();
}

class _DragDropDemoState extends State<DragDropDemo> {
  final List<String> _tools = ["相机", "日历", "备忘录", "计算器"];
  bool _isHovering = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 拖拽交互实战')),
      body: Column(
        children: [
          const SizedBox(height: 50),
          // 1. 可拖拽项目区
          Wrap(
            spacing: 20,
            children: _tools.map((t) => Draggable<String>(
              data: t,
              feedback: _buildToolItem(t, elevation: 10),
              childWhenDragging: Opacity(opacity: 0.3, child: _buildToolItem(t)),
              child: _buildToolItem(t),
            )).toList(),
          ),
          
          const Spacer(),
          
          // 2. 垃圾桶目标区
          DragTarget<String>(
            onWillAccept: (_) {
              setState(() => _isHovering = true);
              return true;
            },
            onLeave: (_) => setState(() => _isHovering = false),
            onAccept: (data) {
              setState(() {
                _tools.remove(data);
                _isHovering = false;
              });
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("$data 已被移除")));
            },
            builder: (context, data, _) {
              return Container(
                width: double.infinity,
                height: 150,
                color: _isHovering ? Colors.red[100] : Colors.grey[100],
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      _isHovering ? Icons.delete_forever : Icons.delete_outline,
                      size: 64,
                      color: _isHovering ? Colors.red : Colors.grey,
                    ),
                    const SizedBox(height: 8),
                    Text(_isHovering ? "松手即销毁" : "将图标拖到这里删除",
                        style: TextStyle(color: _isHovering ? Colors.red : Colors.black54)),
                  ],
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildToolItem(String label, {double elevation = 0}) {
    return Material(
      elevation: elevation,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        decoration: BoxDecoration(color: Colors.blue, borderRadius: BorderRadius.circular(12)),
        child: Text(label, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
    );
  }
}
```

---

## 七、总结

在 Flutter for OpenHarmony 开发中，拖拽交互能让你的应用从“能用”跨越到“好用”。

1.  **Draggable-DragTarget**：是一对数据搬运的“发送端”与“接收端”。
2.  **LongPressDraggable**：是处理手机端复杂叠加手势冲突的良药。
3.  **反馈体系**：利用 Z-Index（feedback）和物理震感（HapticFeedback），给用户建立起一种虚拟物体的真实操作感。

通过这对组件，你可以实现极为丰富的卡片排序、文件管理等系统级深度交互。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

