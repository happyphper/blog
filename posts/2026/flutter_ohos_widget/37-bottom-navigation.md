# Flutter for OpenHarmony 实战之基础组件：第三十七篇 NavigationBar 与 BottomNavigationBar — 现代应用导航栏解析

## 前言

底部导航栏（Bottom Navigation）是移动应用最核心的“交通枢纽”。它让用户能够通过单手快速在 3 到 5个主要页面之间来回切换。随着 Material 3 规范的普及，传统的 `BottomNavigationBar` 正在逐渐演变为更加视觉现代化的 `NavigationBar`。

在 **Flutter for OpenHarmony** 平台上，构建稳定且流畅的导航系统不仅涉及 UI 组件的选择，还涉及状态管理与平台视觉特性的适配。本文将对比两代导航组件，带大家跑通鸿蒙应用中最通用的主页框架。

---

## 一、两代导航栏的对比

### 1.1 BottomNavigationBar (Legacy)
传统的底部导航栏，具有背景着色、选中项放大等经典效果。

```dart
BottomNavigationBar(
  currentIndex: _selectedIndex,
  selectedItemColor: Colors.blue[800],
  unselectedItemColor: Colors.grey,
  type: BottomNavigationBarType.fixed, // 超过3个项时建议固定类型
  onTap: _onItemTapped,
  items: const <BottomNavigationBarItem>[
    BottomNavigationBarItem(icon: Icon(Icons.home), label: '首页'),
    BottomNavigationBarItem(icon: Icon(Icons.business), label: '业务'),
    BottomNavigationBarItem(icon: Icon(Icons.school), label: '学院'),
  ],
)
```

### 1.2 NavigationBar (Material 3 - 推荐)
现代化的导航栏，取消了文字标题的强制显示（可选），采用胶囊形选中背景，更加符合桌面/端侧融合的审美。

```dart
NavigationBar(
  selectedIndex: _selectedIndex,
  onDestinationSelected: (int index) {
    setState(() => _selectedIndex = index);
  },
  destinations: const <Widget>[
    NavigationDestination(icon: Icon(Icons.explore), label: '探索'),
    NavigationDestination(icon: Icon(Icons.commute), label: '通勤'),
    NavigationDestination(selectedIcon: Icon(Icons.bookmark), icon: Icon(Icons.bookmark_border), label: '收藏'),
  ],
)
```

<!-- IMAGE_PLACEHOLDER: BottomNavigationBar 与 NavigationBar 在鸿蒙设备上的视觉差异对比 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 二、进阶实战：联动 PageView 实现平滑切换

单纯的导航栏切换只是改变状态，如果想让左右滑动也能切换页面，需要将 `NavigationBar` 与 `PageView` 深度联动。

```dart
class MainScaffold extends StatefulWidget {
  @override
  _MainScaffoldState createState() => _MainScaffoldState();
}

class _MainScaffoldState extends State<MainScaffold> {
  int _idx = 0;
  final PageController _pageController = PageController();

  void _onNavTap(int index) {
    setState(() => _idx = index);
    _pageController.animateToPage(index, duration: Duration(milliseconds: 300), curve: Curves.ease);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: PageView(
        controller: _pageController,
        onPageChanged: (v) => setState(() => _idx = v),
        children: [HomePage(), DiscoverPage(), SettingPage()],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _idx,
        onDestinationSelected: _onNavTap,
        destinations: [...],
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 导航栏联动翻页在大屏鸿蒙平板上的多任务展示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 三、定制化外观：打造高阶 UI

在鸿蒙系统中，我们有时需要底部导航栏具有悬浮感或是特殊的阴影。

```dart
Container(
  decoration: BoxDecoration(
    color: Colors.white,
    boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 10, spreadRadius: 1)],
    borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
  ),
  child: NavigationBar(
    elevation: 0, // 去掉内置阴影，使用 Container 的阴影
    backgroundColor: Colors.transparent,
    selectedIndex: _idx,
    onDestinationSelected: (idx) => setState(() => _idx = idx),
    destinations: [...],
  ),
)
```

---

## 四、OpenHarmony 平台适配建议

### 4.1 底部手势栏避让
鸿蒙设备的手势控制条通常位于屏幕最底部。如果导航栏文字贴得太死，极易引起误操作。

✅ **推荐方案**：
导航栏组件内部通常会自动应用 `SafeArea`，但在自定义导航容器时，必须手动包裹。

```dart
bottomNavigationBar: SafeArea(
  child: MyCustomNavBar(),
)
```

### 4.2 路由树与持久化导航
在鸿蒙系统上，用户点击“系统返回”手势时。

💡 **调优思路**：
如果页面切换是通过 `PageView` 而非路由跳转实现的，直接返回可能会退出应用。建议通过 `PopScope` 拦截，若当前导航索引不为 0，则先切回主页索引。

### 4.3 触控反馈适配
导航项点击时触发鸿蒙系统的触感反馈，能让物理感更强。

```dart
import 'package:flutter/services.dart';

onDestinationSelected: (v) {
  HapticFeedback.selectionClick(); // 针对选中变更的特定震动
  setState(() => _selectedIndex = v);
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙手机处于横屏/分屏状态时底部导航栏的自动伸缩预览 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 五、完整示例代码

以下代码演示了一个标准的“底部导航 + 多页面系统”框架。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: AppMainFrame()));

class AppMainFrame extends StatefulWidget {
  const AppMainFrame({super.key});

  @override
  State<AppMainFrame> createState() => _AppMainFrameState();
}

class _AppMainFrameState extends State<AppMainFrame> {
  int _currentIndex = 0;
  final List<Widget> _pages = [
    const _DummyPage(title: "首页", color: Colors.blue),
    const _DummyPage(title: "探索", color: Colors.green),
    const _DummyPage(title: "动态", color: Colors.orange),
    const _DummyPage(title: "我的", color: Colors.purple),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 使用 IndexedStack 可以保留各个页面的滚动状态
      body: IndexedStack(
        index: _currentIndex,
        children: _pages,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        indicatorColor: Colors.blue.withAlpha(50),
        onDestinationSelected: (index) {
          setState(() => _currentIndex = index);
        },
        destinations: const [
          NavigationDestination(
            selectedIcon: Icon(Icons.home, color: Colors.blue),
            icon: Icon(Icons.home_outlined),
            label: '首页',
          ),
          NavigationDestination(
            selectedIcon: Icon(Icons.explore, color: Colors.blue),
            icon: Icon(Icons.explore_outlined),
            label: '探索',
          ),
          NavigationDestination(
            selectedIcon: Icon(Icons.notifications, color: Colors.blue),
            icon: Icon(Icons.notifications_none),
            label: '动态',
          ),
          NavigationDestination(
            selectedIcon: Icon(Icons.person, color: Colors.blue),
            icon: Icon(Icons.person_outline),
            label: '我的',
          ),
        ],
      ),
    );
  }
}

class _DummyPage extends StatelessWidget {
  final String title;
  final Color color;
  const _DummyPage({required this.title, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: color.withAlpha(10),
      child: Center(
        child: Text(title, style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: color)),
      ),
    );
  }
}
```

---

## 六、总结

底部导航栏是鸿蒙应用体验的基石。

1.  **首选新一代**：为了更好的未来适配性（包含大屏和平板），建议优先使用 Material 3 规范的 `NavigationBar`。
2.  **状态保留**：如果希望页面切换时不重新加载，使用 `IndexedStack` 指引 `body`。
3.  **用户感知**：在鸿蒙平台上，利用好安全区域避让和触控反馈（HapticFeedback），是区分开发者专业度的关键细节。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

