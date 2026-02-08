![Flutter for OpenHarmony 实战：ScrollController 与 Scrollbar](./images/17-scroll-controller.png)

# Flutter for OpenHarmony 实战之基础组件：第十七篇 滚动进阶 ScrollController 与 Scrollbar

> **摘要**：在前面的文章中，我们学习了如何使用 ListView 和 GridView 展示列表数据。但在实际开发中，我们往往需要更精细的控制：比如用户滑到一定高度时显示“回到顶部”按钮，或者在右侧展示一个符合鸿蒙系统风格的滚动条。本文将深入探讨滚动布局的“指挥官” —— `ScrollController`。

## 前言

滚动（Scrolling）是移动端应用中最频繁的交互操作之一。一个优秀的应用不仅要能显示长列表，还要能感知用户的滚动意图。

在 OpenHarmony 设备上，用户对滑动的流畅度和反馈感有较高的要求。通过 `ScrollController`，我们可以精确掌握滚动的每一个像素，从而实现：
- 动态显示/隐藏 UI 元素（如：向上滑动隐藏底部导航栏）。
- 加载更多逻辑（结合滚动到底部）。
- 跨组件同步滚动。
- 自定义滚动条风格。

**本文你将学到**：
- `ScrollController` 的核心属性与生命周期
- 监听滚动位置 (`offset`) 并触发动画
- 如何实现平滑的“回到顶部 (Back to Top)”功能
- 适配 OpenHarmony 的滚动条 (`Scrollbar`) 配置
- 实战：打造一个带搜索框动态缩放效果的列表页

---

## 一、ScrollController：滚动的灵魂

### 1.1 什么是 ScrollController
`ScrollController` 是一个控制器对象，它可以被关联到任何可滚动组件（如 `ListView`, `GridView`, `SingleChildScrollView`）上。

### 1.2 基本结构

```dart
class _MyListPageState extends State<MyListPage> {
  // 1. 定义控制器
  final ScrollController _controller = ScrollController();

  @override
  void initState() {
    super.initState();
    // 2. 绑定监听
    _controller.addListener(() {
      print('当前滚动偏移量: ${_controller.offset}');
    });
  }

  @override
  void dispose() {
    // 3. 💡 别忘了在页面销毁时释放内存
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: _controller, // 4. 关联到 ListView
      itemBuilder: (context, index) => ListTile(title: Text('Item $index')),
      itemCount: 100,
    );
  }
}
```

---

## 二、监听与控制

### 2.1 监听：感知“回到顶部”的时机

我们通常希望在用户向上滑动超过一定距离（例如 200 像素）后，显示一个悬浮按钮。

```dart
bool _showBackToTop = false;

void _scrollListener() {
  if (_controller.offset >= 200 && !_showBackToTop) {
    setState(() => _showBackToTop = true);
  } else if (_controller.offset < 200 && _showBackToTop) {
    setState(() => _showBackToTop = false);
  }
}
```

### 2.2 控制：一键回顶

`ScrollController` 提供了两个核心方法来改变位置：
- `jumpTo(double value)`：直接跳转，没有动画（瞬间移动）。
- `animateTo(double value, ...)`：带动画的平滑平移。

```dart
void _backToTop() {
  _controller.animateTo(
    0, 
    duration: const Duration(milliseconds: 500),
    curve: Curves.easeInOut, // 💡 使用缓动曲线让滑动更自然
  );
}
```

---

## 三、Scrollbar：适配鸿蒙视觉风格

在长列表中，滚动条能给用户明确的长度预期。

### 3.1 基础用法
将可滚动组件包裹在 `Scrollbar` 中即可。

```dart
Scrollbar(
  child: ListView(
    controller: _controller, // 💡 注意：如果要显式控制，两者必须关联同一个 controller
    children: [...],
  ),
)
```

### 3.2 鸿蒙风格适配
OpenHarmony 的滚动条通常比较细长，且在不滚动时会自动隐藏。我们可以通过属性进行精细化调整：

```dart
Scrollbar(
  controller: _controller,
  thumbVisibility: false,      // 是否始终显示滚动条轨道
  trackVisibility: false,      // 是否始终显示滚动条滑块
  thickness: 6.0,             // 💡 调整宽度，符合鸿蒙 2.0+ 的精致感
  radius: const Radius.circular(3), // 圆角
  child: ListView.builder(
    controller: _controller,
    itemCount: 100,
    itemBuilder: (context, index) => ListTile(title: Text('数据项 $index')),
  ),
)
```

---

## 四、OpenHarmony 实战：搜索栏动态缩放

这是一个常见的 UI 效果：当用户向上滑动列表时，顶部的搜索框逐渐缩小并变淡，为内容留出更多空间。

### 核心实现逻辑

```dart
class OhosDynamicHeader extends StatefulWidget {
  const OhosDynamicHeader({super.key});

  @override
  State<OhosDynamicHeader> createState() => _OhosDynamicHeaderState();
}

class _OhosDynamicHeaderState extends State<OhosDynamicHeader> {
  final ScrollController _scrollController = ScrollController();
  double _headerOpacity = 1.0;
  double _headerHeight = 100.0;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(() {
      // 💡 根据滚动偏移量计算头部透明度和高度
      double offset = _scrollController.offset;
      setState(() {
        _headerOpacity = (1 - offset / 100).clamp(0, 1);
        _headerHeight = (100 - offset).clamp(50, 100);
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // 动态头部
          Opacity(
            opacity: _headerOpacity,
            child: Container(
              height: _headerHeight,
              color: Colors.blue,
              alignment: Alignment.center,
              child: const Text('鸿蒙新闻', style: TextStyle(color: Colors.white, fontSize: 20)),
            ),
          ),
          // 列表
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              itemCount: 50,
              itemBuilder: (context, index) => ListTile(title: Text('新闻资讯条目 $index')),
            ),
          ),
        ],
      ),
    );
  }
}
```

![ScrollController 滚动联动效果演示](./images/17-scroll-controller.png)
> **图 1**：通过监听滚动位移，实现搜索框随列表滑动而动态缩放的交互动效。

---

## 五、注意事项

1. **共享 Controller 问题**：如果你在一个页面里有多个 `ListView`，不要共用同一个 `ScrollController` 实例，否则其中一个滚动时，另一个会同步跳动甚至报错。
2. **Dispose 释放**：`ScrollController` 内部包含 `ChangeNotifier`，如果忘记 `dispose()`，在复杂应用中会导致严重的内存泄漏。
3. **NotificationListener**：如果你只需要监听滚动，不想控制滚动，建议使用 `NotificationListener<ScrollNotification>`，它性能更好且不需要手动销毁。

---

## 六、总结

`ScrollController` 让我们拥有了操纵时间（滚动位置）的能力。

### 核心要点：
1. **监听位置**：通过 `offset` 获取当前位置。
2. **控制行为**：通过 `animateTo` 实现平滑的页面跳转。
3. **视觉增强**：使用 `Scrollbar` 提升长列表的交互体验。
4. **适配建议**：在鸿蒙大屏上，利用滚动反馈来动态调整侧边栏或顶栏的显示状态。

### 下一篇预告
当简单的 ListView 满足不了你，你想在一个页面里混合瀑布流、列表、吸顶头部，并让它们共享一个完美的滚动动效时，该请出 Flutter 布局的“终极杀器”了。
**《Flutter for OpenHarmony 实战之基础组件：第十八篇 布局终极者 CustomScrollView 与 Slivers》**
准备好进入 Flutter 布局的深水区了吗？

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/17-scroll-controller)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/17-scroll-controller)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
