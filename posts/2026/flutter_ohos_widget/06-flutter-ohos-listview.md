![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第六篇 ListView 列表组件详解

> **摘要**：几乎每个 App 都有列表界面。本文深入剖析 Flutter 中 ListView 的三种构建方式，重点讲解高性能列表 ListView.builder 的使用技巧，并结合 ScrollController 实现下拉刷新、上拉加载更多及“回到顶部”等经典交互场景。

## 前言

在 Flutter 中，`ListView` 是最常用的滚动组件。初学者常犯的错误是：直接把所有数据塞进一个 `Column` 里放进 `SingleChildScrollView`，或者在数据量很大时使用默认的 `ListView()` 构造函数。

这些做法在数据少时没问题，一旦数据超过 100 条，性能就会急剧下降，甚至导致 App 卡顿（Jank）。

**本文你将学到**：
- ListView、ListView.builder、ListView.separated 的选择策略
- 如何实现各种各样的分割线
- 下拉刷新 (Pull to Refresh) 的原生实现
- 监听滚动位置与“一键回到顶部”
- 列表性能优化的 3 个关键点

![Flutter ListView on OpenHarmony 概念图 (中文版)](./images/flutter_ohos_listview_concept_cn.png)

---

## 一、ListView 的三种构建方式

### 1.1 默认构造函数 (少量静态数据)

适用于数据量少且确定的场景（如设置页面）。

```dart
ListView(
  padding: const EdgeInsets.all(16),
  children: const [
    ListTile(title: Text('设置')),
    ListTile(title: Text('关于')),
    ListTile(title: Text('退出登录')),
  ],
)
```

**缺点**：它会一次性创建所有子组件，数据多了会导致内存暴涨。

### 1.2 ListView.builder (大量/动态数据)

**强烈推荐**。它采用“懒加载”机制，只有当子组件滚动到屏幕可见区域时才会被创建，滑出屏幕后会被回收。

```dart
ListView.builder(
  itemCount: 1000, // 列表总数
  itemBuilder: (context, index) {
    // 回调函数：返回第 index 个位置的组件
    return ListTile(
      leading: CircleAvatar(child: Text('${index + 1}')),
      title: Text('第 $index 条数据'),
      subtitle: Text('这是动态生成的超长列表'),
    );
  },
)
```

### 1.3 ListView.separated (带分割线)

需要在每个列表项之间添加分割线时使用，比在 builder 里手动判断 index 更优雅。

```dart
ListView.separated(
  itemCount: 20,
  // 列表项构建器
  itemBuilder: (context, index) => ListTile(title: Text('Item $index')),
  // 分割线构建器
  separatorBuilder: (context, index) {
    // 每隔 5 项显示一个广告，否则显示普通分割线
    if ((index + 1) % 5 == 0) {
      return Container(
        height: 60,
        color: Colors.blue[50],
        alignment: Alignment.center,
        child: const Text('--- 广告位 ---'),
      );
    }
    return const Divider(height: 1, indent: 16);
  },
)
```

---

## 二、滚动控制与监听

想要获取滑动的距离，或者控制列表滚动，需要使用 `ScrollController`。

### 2.1 监听滚动 (实现“回到顶部”按钮)

```dart
class ScrollToTopDemo extends StatefulWidget {
  const ScrollToTopDemo({super.key});

  @override
  State<ScrollToTopDemo> createState() => _ScrollToTopDemoState();
}

class _ScrollToTopDemoState extends State<ScrollToTopDemo> {
  // 1. 创建 Controller
  final ScrollController _controller = ScrollController();
  bool _showBackTop = false;

  @override
  void initState() {
    super.initState();
    // 2. 添加监听器
    _controller.addListener(() {
      // 当滑动距离 > 200 时显示按钮
      if (_controller.offset > 200 && !_showBackTop) {
        setState(() => _showBackTop = true);
      } else if (_controller.offset <= 200 && _showBackTop) {
        setState(() => _showBackTop = false);
      }
    });
  }

  @override
  void dispose() {
    // 3. 销毁 Controller
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        controller: _controller, // 4. 绑定 Controller
        itemCount: 50,
        itemBuilder: (_, i) => ListTile(title: Text('Item $i')),
      ),
      floatingActionButton: _showBackTop
          ? FloatingActionButton(
              child: const Icon(Icons.arrow_upward),
              onPressed: () {
                // 5. 控制滚动
                _controller.animateTo(
                  0, // 回到顶部
                  duration: const Duration(milliseconds: 500),
                  curve: Curves.easeInOut,
                );
              },
            )
          : null,
    );
  }
}
```

---

## 三、实战：下拉刷新与上拉加载

这是最常用的列表业务场景。

- **下拉刷新**：使用自带的 `RefreshIndicator`。
- **上拉加载**：通常通过监听 `ScrollController` 是否滑动到底部来实现。

```dart
class NewsList extends StatefulWidget {
  const NewsList({super.key});

  @override
  State<NewsList> createState() => _NewsListState();
}

class _NewsListState extends State<NewsList> {
  final List<String> _data = List.generate(15, (i) => '初始新闻标题 $i');
  final ScrollController _scrollController = ScrollController();
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
  }

  void _onScroll() {
    // 判断是否滑动到底部
    if (_scrollController.position.pixels == 
        _scrollController.position.maxScrollExtent) {
      _loadMore();
    }
  }

  // 模拟上拉加载
  Future<void> _loadMore() async {
    if (_isLoading) return;
    setState(() => _isLoading = true);
    
    await Future.delayed(const Duration(seconds: 2)); // 模拟网络请求
    
    setState(() {
      _data.addAll(List.generate(5, (i) => '新增新闻 ${DateTime.now().second} - $i'));
      _isLoading = false;
    });
  }

  // 模拟下拉刷新
  Future<void> _onRefresh() async {
    await Future.delayed(const Duration(seconds: 1));
    setState(() {
      _data.clear();
      _data.addAll(List.generate(15, (i) => '刷新后的新闻 $i'));
    });
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _onRefresh, // 绑定下拉刷新事件
      child: ListView.builder(
        controller: _scrollController,
        itemCount: _data.length + 1, // 多一项用于显示 Loading
        itemBuilder: (context, index) {
          // 如果是最后一项，显示加载指示器
          if (index == _data.length) {
            return _isLoading
                ? const Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Center(child: CircularProgressIndicator()),
                  )
                : const SizedBox(); // 没在加载时不显示
          }
          
          return ListTile(
            leading: const Icon(Icons.newspaper),
            title: Text(_data[index]),
            subtitle: const Text('2026-05-20'),
          );
        },
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 下拉刷新交互动图 -->
<!-- 类型: 鸿蒙设备录屏 -->
<!-- 内容: 展示下拉出现 Loading 圈，以及上拉到底部自动加载新数据 -->

---

## 四、鸿蒙开发性能优化技巧

在 OpenHarmony 这样可能运行在不同性能水平设备上的平台，列表优化尤为重要。

### 4.1 固定高度优化 (itemExtent)

如果你的列表项高度是固定的（例如都是 50px），**务必**设置 `itemExtent`。
这会让 Flutter 跳过高度计算过程，大幅提升长列表滚动的流畅度。

```dart
ListView.builder(
  itemExtent: 50.0, // 强制指定每个 item 高度为 50
  itemCount: 10000,
  itemBuilder: (ctx, index) => Container(alignment: Alignment.center, child: Text('$index')),
)
```

### 4.2 避免过度绘制 (RepaintBoundary)

如果列表项非常复杂（例如包含复杂的 Stack、Canvas 绘图），可以给 Item 包裹一个 `RepaintBoundary`，这样该 Item 的重绘不会影响其他 Item。

### 4.3 保持状态 (AutomaticKeepAlive)

如果列表项中包含 TextField 输入框或者 TabView，滑动出屏幕后状态会丢失。
解决方案：让 Item 的 State 混入 `AutomaticKeepAliveClientMixin`。

```dart
class MyListItem extends StatefulWidget {
  // ...
}

class _MyListItemState extends State<MyListItem> with AutomaticKeepAliveClientMixin {
  @override
  bool get wantKeepAlive => true; // 保持存活，不被回收

  @override
  Widget build(BuildContext context) {
    super.build(context); // 必须调用
    return TextField();
  }
}
```

---

## 五、总结

ListView 是处理流式内容的核心。

### 核心要点
1.  **选对构造器**：数据多了一定要用 `builder` 或 `separated`。
2.  **交互三剑客**：`RefreshIndicator` (下拉) + `ScrollController` (监听) + `CircularProgressIndicator` (上拉加载)。
3.  **性能第一**：固定高度用 `itemExtent`，复杂 Item 用 `RepaintBoundary`。

### 下一篇预告
列表中的内容需要用户去点击、长按甚至拖拽。
**《Flutter for OpenHarmony 实战之基础组件：第七篇 Button 按钮与手势交互》**
我们将学习各种 Button (点击)、InkWell (水波纹) 以及 GestureDetector (全能手势) 的使用。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/6-listview)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/6-listview)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
