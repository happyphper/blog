![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第十一篇 BottomNavigationBar 与 TabBar 多页切换

> **摘要**：一个复杂的 App 通常包含多个功能模块。本文将深入讲解 Flutter 中最核心的两种多页切换模式：底部导航 (BottomNavigationBar) 和顶部选项卡 (TabBar)。我们将探讨 Material 3 风格的新组件 NavigationBar，解决页面切换时的状态丢失问题，并适配鸿蒙系统的底部手势条。

## 前言

打开你手机里的微信、淘宝或抖音，你会发现它们都有一个共同的架构：底部有 4-5 个图标，点击切换不同的主页面；顶部可能还有“关注/推荐/热榜”这样的分类切换。

这就是移动端最经典的 **“底 Tab + 顶 Tab”** 双导航架构。

**本文你将学到**：
- `BottomNavigationBar` (经典) 与 `NavigationBar` (Material 3) 的区别
- `TabBar` + `TabBarView` 实现滑动切换
- **核心难点**：如何让页面在切换后不重置？(AutomaticKeepAliveClientMixin)
- **鸿蒙适配**：底部导航栏如何避开系统手势条 (Home Indicator)

---

## 一、底部导航：App 的根基

Flutter 提供了两种主流的底部导航组件。

### 1.1 经典款：BottomNavigationBar

这是最传统、兼容性最好的组件。

```dart
class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _currentIndex = 0;
  
  // 页面列表
  final List<Widget> _pages = [
    const HomePage(),
    const CategoryPage(),
    const ProfilePage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_currentIndex], // 根据下标显示对应页面
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        type: BottomNavigationBarType.fixed, // 超过3个item必须设置fixed
        selectedItemColor: Colors.blue,
        unselectedItemColor: Colors.grey,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: '首页'),
          BottomNavigationBarItem(icon: Icon(Icons.category), label: '分类'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: '我的'),
        ],
      ),
    );
  }
}
```

### 1.2 新潮款：NavigationBar (M3)

Material 3 引入了更高、更圆润的 `NavigationBar`。它自带点击涟漪和胶囊状的指示器，视觉效果更好。

```dart
NavigationBar(
  selectedIndex: _currentIndex,
  onDestinationSelected: (index) => setState(() => _currentIndex = index),
  destinations: const [
    NavigationDestination(
      icon: Icon(Icons.home_outlined),
      selectedIcon: Icon(Icons.home),
      label: '首页',
    ),
    NavigationDestination(
      icon: Icon(Icons.explore_outlined),
      selectedIcon: Icon(Icons.explore),
      label: '发现',
    ),
    // ...
  ],
)
```

---

## 二、顶部选项卡：TabBar

`TabBar` 通常用于在同一个主栏目下，切换不同的子分类（如新闻 App 的频道）。它必须配合 `TabController` 使用。

### 2.1 DefaultTabController (推荐)

最简单的方法是在父级包裹一个 `DefaultTabController`，这样我们就不用手动管理 Controller 了。

```dart
class NewsPage extends StatelessWidget {
  const NewsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3, // Tab 数量
      child: Scaffold(
        appBar: AppBar(
          title: const Text('资讯'),
          bottom: const TabBar(
            tabs: [
              Tab(text: '推荐'),
              Tab(text: '科技'),
              Tab(text: '体育'),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            Center(child: Text('推荐内容列表')),
            Center(child: Text('科技内容列表')),
            Center(child: Text('体育内容列表')),
          ],
        ),
      ),
    );
  }
}
```

![Flutter 多级导航架构概念图 (中文版)](./images/flutter_navigation_tabs_concept_cn.png)

---

## 三、核心难点：页面状态保持

默认情况下，当你从“首页”切换到“我的”，再切回“首页”时，**首页会被重建**（列表滚动位置丢失，输入框清空）。这是因为 `Scaffold.body` 直接替换了 Widget。

### 3.1 解决方案：IndexedStack

如果你希望所有页面在初始化后一直存在，可以使用 `IndexedStack`。它会一次性加载所有页面（**注意内存消耗**）。

```dart
// 修改 Scaffold body
body: IndexedStack(
  index: _currentIndex,
  children: _pages, // 所有页面都会被保留在 Widget 树中，只是不可见
),
```

### 3.2 解决方案：AutomaticKeepAliveClientMixin

如果你使用的是 `PageView` 或 `TabBarView`，更推荐让**子页面**自己决定是否保持状态。

```dart
class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

// 1. 混入 AutomaticKeepAliveClientMixin
class _HomePageState extends State<HomePage> with AutomaticKeepAliveClientMixin {
  
  // 2. 重写 wantKeepAlive 返回 true
  @override
  bool get wantKeepAlive => true; 

  @override
  Widget build(BuildContext context) {
    super.build(context); // 3. 必须调用 super.build
    return ListView.builder(
      itemCount: 100,
      itemBuilder: (c, i) => ListTile(title: Text('Item $i')),
    );
  }
}
```

---

## 四、OpenHarmony 鸿蒙适配专题

### 4.1 底部导航栏与手势条

现在的鸿蒙手机（如 Mate 60）默认开启全面屏手势，底部有一条“黑条”或“白条” (Home Indicator)。

如果你的 `BottomNavigationBar` 高度写死，或者没有适配 `SafeArea`，底部的图标可能会被这个手势条遮挡。

Flutter 的 `Scaffold` + `BottomNavigationBar` 默认已经处理了 `SafeArea`。但如果你使用了自定义的底部栏（比如 Stack 里的 Positioned），**务必**包裹 `SafeArea` 并设置 `bottom: true`。

```dart
Align(
  alignment: Alignment.bottomCenter,
  child: SafeArea(
    child: Container(
      height: 60,
      color: Colors.white,
      child: Row(...),
    ),
  ),
)
```

---

## 五、总结

搭建一个 App 的骨架，核心就是“一底一顶”。

### 核心要点
1.  **底部导航**：推荐使用 M3 风格的 `NavigationBar`，视觉更现代。
2.  **顶部 Tab**：使用 `DefaultTabController` 配合 `TabBarView` 最省事。
3.  **状态保持**：不想每次切换都重加载？请记住 `IndexedStack` (简单粗暴) 或 `AutomaticKeepAliveClientMixin` (精细控制)。
4.  **鸿蒙适配**：时刻留意底部的安全区域，不要让按钮贴底太近。

### 下一篇预告
基本的页面结构都有了，但是我们现在的布局还是太“循规蹈矩”了（一行一列）。如果我要做一个 Pinterest 那样的瀑布流，或者像相册一样的网格呢？
**《Flutter for OpenHarmony 实战之基础组件：第十二篇 GridView 网格布局详解》**
我们将突破线性布局的限制，探索二维空间的布局艺术。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/11-navigation-tabs)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/11-navigation-tabs)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
