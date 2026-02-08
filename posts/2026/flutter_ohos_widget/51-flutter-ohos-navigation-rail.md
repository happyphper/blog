# Flutter for OpenHarmony 实战之基础组件：第五十一篇 NavigationRail — 适配平板与折叠屏的侧边导航

## 前言

随着移动设备形态的多样化，特别是鸿蒙平板（MatePad）和华为 Mate X 系列折叠屏的普及，传统的底部导航栏在横屏模式下往往会造成竖向空间的浪费，且在大屏上点击不便。

在 **Flutter for OpenHarmony** 开发中，`NavigationRail`（侧边导航轨）是专为宽屏设计的导航组件。它能常驻在屏幕左侧，提供极致的左右手持握交互体验。本文将详解 `NavigationRail` 的实现及如何根据屏幕宽度动态切换导航模式。

---

## 一、NavigationRail 核心结构

`NavigationRail` 通常作为 `Row` 的第一个元素，紧邻主内容区域展示。

### 1.1 基础实现代码
```dart
NavigationRail(
  selectedIndex: _selectedIndex,
  onDestinationSelected: (int index) {
    setState(() => _selectedIndex = index);
  },
  labelType: NavigationRailLabelType.selected, // 仅选中时显示文字
  destinations: const <NavigationRailDestination>[
    NavigationRailDestination(icon: Icon(Icons.favorite_border), selectedIcon: Icon(Icons.favorite), label: Text('收藏')),
    NavigationRailDestination(icon: Icon(Icons.bookmark_border), selectedIcon: Icon(Icons.bookmark), label: Text('书签')),
    NavigationRailDestination(icon: Icon(Icons.star_border), selectedIcon: Icon(Icons.star), label: Text('星标')),
  ],
)
```

### 1.2 扩展性：添加 Leading 与 Trailing
你可以像原生鸿蒙应用一样，在侧边栏顶部放置头像，底部放置设置图标。

```dart
NavigationRail(
  leading: const CircleAvatar(child: Text('OH')),
  trailing: IconButton(icon: const Icon(Icons.settings), onPressed: () {}),
  //...
)
```

<!-- IMAGE_PLACEHOLDER: NavigationRail 在鸿蒙平板上的横屏展示效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 二、响应式切换：底部 vs 侧边

💡 **实战技巧**：在鸿蒙开发中，我们应该根据屏幕宽度自动选择最合适的导航方式。

```dart
LayoutBuilder(
  builder: (context, constraints) {
    bool isWide = constraints.maxWidth > 600; // 宽屏判断逻辑
    return Scaffold(
      bottomNavigationBar: isWide ? null : _buildBottomBar(), // 手机端用底部导航
      body: Row(
        children: [
          if (isWide) _buildNavRail(), // 宽屏/平板用侧边导航
          const VerticalDivider(thickness: 1, width: 1), 
          const Expanded(child: Center(child: Text("页面内容"))),
        ],
      ),
    );
  },
)
```

---

## 三、进阶：标签模式与浮动效果

在鸿蒙的高级 UI 规范中，侧边栏往往具有一定的通透感或背景悬浮效果。

### 3.1 展开式侧边栏 (Extended)
如果你希望侧边栏能够像桌面应用一样展开显示完整文字，可以设置 `extended` 属性。

```dart
NavigationRail(
  extended: _isExtended, // 通过按钮切换展开/收起
  minExtendedWidth: 200,
  //...
)
```

<!-- IMAGE_PLACEHOLDER: NavigationRail 在折叠屏展开模式下自动由图标变为图标+文字的动效 -->
<!-- 类型: GIF -->
<!-- 设备: 鸿蒙模拟器 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 手势区避让 (Sidebar Gestures)
鸿蒙系统支持侧边滑动返回手势。如果 `NavigationRail` 设置得太宽，可能会干扰用户的系统手势操作。

✅ **推荐方案**：
保留默认的 `minWidth: 72`。如果需要扩展宽度，建议在 `NavigationRail` 外层包裹一层 `SafeArea`，确保其不会遮挡鸿蒙系统的核心交互边距。

### 4.2 适配平行视界 (Multiplier Window)
鸿蒙系统的“平行视界”会将一个应用拆分为左右两屏。

💡 **调优建议**：
在平行视界下，由于单屏宽度变窄，应用可能会错误地将 `NavigationRail` 切换为底部导航。建议在判断 `isWide` 时，结合 `MediaQuery.of(context).orientation`。只有在物理横屏且宽度确实足够时才启用侧边导航，避免在分屏状态下导致布局过度拥挤。

### 4.3 视觉细节与马达反馈
点击侧边项时，图标应具有明显的缩放或颜色填充反馈。

✅ **最佳实践**：
- 为选中的 `NavigationRailDestination` 设置 `selectedIcon`。
- 点击时调用 `HapticFeedback.selectionClick()`。

<!-- IMAGE_PLACEHOLDER: 鸿蒙平板分屏状态下导航栏样式的自适应调整演示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 五、完整示例代码

以下代码演示了一个可以根据窗口大小自动在“底部导航”与“侧边导航”之间切换的专业主页框架。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: ResponsiveNavPage()));

class ResponsiveNavPage extends StatefulWidget {
  const ResponsiveNavPage({super.key});

  @override
  State<ResponsiveNavPage> createState() => _ResponsiveNavPageState();
}

class _ResponsiveNavPageState extends State<ResponsiveNavPage> {
  int _idx = 0;

  @override
  Widget build(BuildContext context) {
    // 1. 获取屏幕宽度
    final double screenWidth = MediaQuery.of(context).size.width;
    final bool isWide = screenWidth > 700;

    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 响应式导航实战')),
      // 2. 手机端显示底部导航
      bottomNavigationBar: isWide ? null : NavigationBar(
        selectedIndex: _idx,
        onDestinationSelected: (i) => setState(() => _idx = i),
        destinations: _buildNavDestinations(),
      ),
      body: Row(
        children: [
          // 3. 宽屏/平板显示侧边导航
          if (isWide) NavigationRail(
            selectedIndex: _idx,
            labelType: NavigationRailLabelType.all,
            onDestinationSelected: (i) => setState(() => _idx = i),
            destinations: _buildRailDestinations(),
            leading: const Padding(padding: EdgeInsets.all(16), child: CircleAvatar(child: Icon(Icons.person))),
          ),
          const VerticalDivider(thickness: 1, width: 1),
          Expanded(
            child: Center(
              child: Text("正在浏览页面 ${_idx + 1}", style: const TextStyle(fontSize: 24)),
            ),
          ),
        ],
      ),
    );
  }

  // 辅助构建函数
  List<NavigationDestination> _buildNavDestinations() {
    return const [
      NavigationDestination(icon: Icon(Icons.home_outlined), label: "主页"),
      NavigationDestination(icon: Icon(Icons.settings_outlined), label: "设置"),
    ];
  }

  List<NavigationRailDestination> _buildRailDestinations() {
    return const [
      NavigationRailDestination(icon: Icon(Icons.home_outlined), label: Text("主页")),
      NavigationRailDestination(icon: Icon(Icons.settings_outlined), label: Text("设置")),
    ];
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的大屏适配之路上，`NavigationRail` 是不可或缺的利器。

1.  **形态选择**：宽屏用 Rail，竖屏用 Bar。
2.  **空间利用**：Rail 能有效释放纵向空间，在大屏阅读类应用中体验极佳。
3.  **细节打磨**：关注鸿蒙端的分屏适配与手势避让，让你的应用在平板和折叠屏上展现出真正的“原生感”。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

