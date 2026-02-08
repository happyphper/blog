![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第九篇 Scaffold 页面骨架与导航栏

> **摘要**：Scaffold 是 Flutter 页面开发的“脚手架”。本文将详细介绍如何使用 Scaffold 构建标准 App 页面，涵盖 AppBar 标题栏、BottomNavigationBar 底部导航、Drawer 侧边栏等核心模块，并深入探讨在 OpenHarmony 平台上如何进行沉浸式状态栏与沉浸式导航适配。

## 前言

在之前的文章中，我们学习了按钮、文本、图片等局部组件。但一个真正的 App 页面是由这些组件在“脚手架”上堆叠而成的。

`Scaffold` 组件就是这个脚手架。它实现了 Material Design 的基本视觉结构。如果没有它，你需要手动处理状态栏高度、屏幕安全区域、各个部件的定位逻辑，这会非常痛苦。

**本文你将学到**：
- Scaffold 的 5 大核心区域
- AppBar 的动作按钮 (Actions) 与自定义图标
- 手把手实现底部导航栏页签切换
- Drawer 侧边栏的结构与交互
- 鸿蒙设备上的沉浸式布局（SafeArea）实战

---

## 一、Scaffold 核心结构

一个典型的 `Scaffold` 页面由以下几部分组成：

```dart
Scaffold(
  appBar: AppBar(title: const Text('页面标题')),
  body: const Center(child: Text('主体内容')),
  floatingActionButton: FloatingActionButton(onPressed: () {}),
  drawer: const Drawer(child: Text('侧边栏')),
  bottomNavigationBar: BottomNavigationBar(items: [...]),
)
```

<!-- IMAGE_PLACEHOLDER: Scaffold 各区域分布图 -->
<!-- 类型: 示意图 -->
<!-- 内容: 标注 AppBar, Body, FAB, Drawer, BottomNav 的位置 -->

---

## 二、AppBar：页面的门面

`AppBar` 通常位于页面顶部，包含标题和常用的操作按钮。

```dart
AppBar(
  leading: IconButton(
    icon: const Icon(Icons.menu),
    onPressed: () => _scaffoldKey.currentState?.openDrawer(),
  ),
  title: const Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text('首页', style: TextStyle(fontSize: 18)),
      Text('OpenHarmony 开发者社区', style: TextStyle(fontSize: 12)),
    ],
  ),
  centerTitle: false, // 鸿蒙/Android 风格标题通常居左
  actions: [
    IconButton(icon: const Icon(Icons.search), onPressed: () {}),
    IconButton(icon: const Icon(Icons.notifications_none), onPressed: () {}),
  ],
  backgroundColor: Colors.blue,
  elevation: 0, // 去掉阴影，实现扁平化设计
)
```

---

## 三、BottomNavigationBar：多页切换

这是现代主流 App 最常用的导航方式。

```dart
class MainScaffold extends StatefulWidget {
  const MainScaffold({super.key});

  @override
  State<MainScaffold> createState() => _MainScaffoldState();
}

class _MainScaffoldState extends State<MainScaffold> {
  int _currentIndex = 0;

  final List<Widget> _pages = const [
    HomePage(),
    SquarePage(),
    MessagePage(),
    ProfilePage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_currentIndex], // 配合第四篇讲的 IndexedStack 更好
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() => _currentIndex = index);
        },
        type: BottomNavigationBarType.fixed, // 超过 3 个建议设为 fixed
        selectedItemColor: Colors.blue,
        unselectedItemColor: Colors.grey,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: '首页'),
          BottomNavigationBarItem(icon: Icon(Icons.explore), label: '广场'),
          BottomNavigationBarItem(icon: Icon(Icons.message), label: '消息'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: '我的'),
        ],
      ),
    );
  }
}
```

---

## 四、Drawer：扩展功能的藏宝库

如果导航栏放不下，或者是一些设置、关于页面，通常会放在侧边栏。

```dart
drawer: Drawer(
  child: ListView(
    padding: EdgeInsets.zero,
    children: [
      // 头部背景
      UserAccountsDrawerHeader(
        accountName: const Text('王码码'),
        accountEmail: const Text('wangmama@example.com'),
        currentAccountPicture: const CircleAvatar(
          backgroundImage: NetworkImage('...'),
        ),
        decoration: BoxDecoration(color: Colors.blue[600]),
      ),
      ListTile(
        leading: const Icon(Icons.settings),
        title: const Text('系统设置'),
        onTap: () {},
      ),
      ListTile(
        leading: const Icon(Icons.color_lens),
        title: const Text('主题切换'),
        onTap: () {},
      ),
      const Divider(),
      ListTile(
        leading: const Icon(Icons.exit_to_app),
        title: const Text('退出登录'),
        onTap: () {},
      ),
    ],
  ),
)
```

---

## 五、鸿蒙适配：沉浸式与 SafeArea

在 OpenHarmony 设备中，如 Mate 60/70 的“灵动岛”或挖孔屏，如果不做适配，内容会被摄像头遮挡。

### 5.1 使用 SafeArea

`SafeArea` 会自动查询屏幕的 `padding`（刘海、挖孔、底部导航条高度），并为子组件添加内边距。

```dart
Scaffold(
  // 💡 提示：如果不想 body 延伸到刘海区
  body: SafeArea(
    child: YourContent(),
  ),
);
```

### 5.2 沉浸式设计

如果你希望图片延伸到状态栏下方（沉浸式效果）：

```dart
Scaffold(
  // 禁止调整 Body 尺寸以避开键盘，实现全屏背景
  extendBodyBehindAppBar: true, 
  appBar: AppBar(
    backgroundColor: Colors.transparent, // 背景透明
    elevation: 0,
  ),
  body: Container(
    decoration: const BoxDecoration(
      image: DecorationImage(image: AssetImage('bg.png'), fit: BoxFit.cover),
    ),
  ),
)
```

---

## 六、实战：构建一个标准的“底部导航+悬浮球”页面

```dart
class AppShell extends StatelessWidget {
  const AppShell({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('鸿蒙实战应用'),
        elevation: 0,
      ),
      body: const Center(child: Text('核心业务区域')),
      
      // 底部工具栏
      bottomNavigationBar: BottomAppBar(
        shape: const CircularNotchedRectangle(), // 缺口形状
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            IconButton(icon: const Icon(Icons.home), onPressed: () {}),
            IconButton(icon: const Icon(Icons.search), onPressed: () {}),
            const SizedBox(width: 40), // 为 FAB 留出的空位
            IconButton(icon: const Icon(Icons.message), onPressed: () {}),
            IconButton(icon: const Icon(Icons.person), onPressed: () {}),
          ],
        ),
      ),
      
      // 悬浮按钮位置：停靠在底部栏中间
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        backgroundColor: Colors.orange,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 底部切口导航栏效果图 -->
<!-- 类型: 鸿蒙设备截图 -->
<!-- 内容: 展示中间有圆型切口的底部导航栏与悬浮按钮 -->

---

## 七、总结

`Scaffold` 组件是我们将基础元素粘合成“页面”的胶水。

### 核心知识点：
1. **地基作用**：必须先有 Scaffold，才能方便地使用 AppBar、Drawer 等 Material 部件。
2. **多页签**：结合 `BottomNavigationBar` 和 `IndexedStack` 是主流 App 的标配。
3. **安全第一**：在各种挖孔屏盛行的鸿蒙设备上，永远记得包裹一层 `SafeArea`。
4. **沉浸式控制**：利用 `extendBodyBehindAppBar` 打造高颜值的全屏 UI。

### 下一篇预告
当用户点击了页面的按钮，我们需要给他们反馈。
**《Flutter for OpenHarmony 实战之基础组件：第十篇 弹窗交互与反馈体系》**
我们将深入探讨 Dialog、SnackBar 和 BottomSheet 的使用技巧。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/9-scaffold-nav)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/9-scaffold-nav)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
