![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第九篇 Scaffold 与 AppBar 页面骨架

> **摘要**：一个标准的 App 页面往往由导航栏、内容区、侧边栏和悬浮按钮组成。本文将深入解析 Flutter 中页面骨架 Scaffold 的全方位用法，重点讲解 AppBar 的深度定制技巧，并针对 OpenHarmony 平台的沉浸式状态栏与刘海屏适配提供最佳实践方案。

## 前言

在之前的文章中，我们学习了 Container、Row、Column 等局部布局组件。但如果要构建一个完整的、符合 Material Design 规范的 App 页面，我们需要一个顶层容器来组织这些元素。

这就是 **Scaffold**（脚手架）。

它就像建筑工地上的脚手架一样，为你提供了页面所需的标准结构：顶部有 `AppBar`，中间是 `body`，底部有 `BottomNavigationBar`，侧边还有 `Drawer`。

**本文你将学到**：
- Scaffold 的五脏六腑：从顶到底的完整结构
- AppBar 的进阶定制：搜索栏、自定义高度与渐变色
- 沉浸式状态栏 (Immersive Status Bar) 的鸿蒙适配
- Drawer 侧滑菜单的实现
- 实战：搭建一个标准的“新闻客户端”首页骨架

---

## 一、Scaffold：页面的骨骼

`Scaffold` 是 Material 库中最重要的布局脚手架，它实现了基本的 Material Design 视觉布局结构。

### 1.1 核心属性概览

![Flutter Scaffold 页面骨架结构图 (中文版)](./images/flutter_scaffold_structure_concept_cn.png)

一个标准的 `Scaffold` 包含以下核心部分：

```dart
Scaffold(
  appBar: AppBar(title: Text('页面标题')), // 顶部导航栏
  body: Center(child: Text('内容区域')),   // 中间核心内容
  floatingActionButton: FloatingActionButton( // 悬浮按钮
    onPressed: () {},
    child: Icon(Icons.add),
  ),
  drawer: Drawer(), // 左侧滑菜单
  endDrawer: Drawer(), // 右侧滑菜单
  bottomNavigationBar: BottomNavigationBar(...), // 底部导航
  backgroundColor: Colors.white, // 页面背景色
)
```

### 1.2 浮动按钮的位置控制 (FAB Location)

通过 `floatingActionButtonLocation` 属性，我们可以将 FAB 玩出花样，比如嵌入到底部导航栏中间。

```dart
Scaffold(
  // 将 FAB 嵌入底部导航栏中心
  floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
  floatingActionButton: FloatingActionButton(
    shape: CircleBorder(), // 圆形
    onPressed: () {},
    child: Icon(Icons.add),
  ),
  bottomNavigationBar: BottomAppBar(
    shape: CircularNotchedRectangle(), // 配合 FAB 挖孔
    child: Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        IconButton(icon: Icon(Icons.home), onPressed: () {}),
        SizedBox(width: 48), // 中间留白给 FAB
        IconButton(icon: Icon(Icons.person), onPressed: () {}),
      ],
    ),
  ),
  // ...
)
```

---

## 二、AppBar：不仅仅是标题栏

`AppBar` 是页面的门面。除了显示标题，它还能承载搜索、菜单、标签栏等功能。

### 2.1 基础定制：左中右结构

AppBar 遵循经典的 leading (左) - title (中) - actions (右) 结构。

```dart
AppBar(
  // 1. 左侧图标 (默认是返回箭头或菜单三横杠)
  leading: IconButton(
    icon: Icon(Icons.menu),
    onPressed: () {},
  ),
  // 2. 中间标题
  title: Text('首页'),
  centerTitle: true, // 标题居中 (Android 默认靠左，iOS 默认居中)
  // 3. 右侧操作区
  actions: [
    IconButton(icon: Icon(Icons.search), onPressed: () {}),
    IconButton(icon: Icon(Icons.more_vert), onPressed: () {}),
  ],
  elevation: 0, // 去掉阴影
  backgroundColor: Colors.blueAccent,
)
```

### 2.2 进阶：渐变色 AppBar (PreferredSize)

如果我想让 AppBar 的背景是渐变色，或者放一张图片，单纯设置 `backgroundColor` 是不行的（它只支持纯色）。我们需要使用 `FlexibleSpace`。

```dart
AppBar(
  title: Text('渐变导航栏'),
  flexibleSpace: Container(
    decoration: BoxDecoration(
      gradient: LinearGradient(
        colors: [Colors.blue, Colors.purple],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
    ),
  ),
)
```

### 2.3 进阶：Bottom 区域 (TabBar)

AppBar 的底部通常用于放置 `TabBar`，实现分页切换。

```dart
AppBar(
  title: Text('新闻'),
  bottom: TabBar(
    controller: _tabController,
    tabs: [
      Tab(text: '推荐'),
      Tab(text: '热点'),
      Tab(text: '视频'),
    ],
  ),
)
```

---

## 三、OpenHarmony 鸿蒙适配专题

在鸿蒙设备（尤其是手机和平板）上开发时，处理“刘海屏”、“挖孔屏”以及“状态栏”是绕不开的话题。

### 3.1 沉浸式状态栏 (Immersive Status Bar)

默认情况下，Flutter 在鸿蒙上的状态栏可能是黑色的。为了实现沉浸式（即内容延伸到状态栏下方，或状态栏透明），我们需要使用 `SystemChrome`。

**依赖引入**：`import 'package:flutter/services.dart';`

```dart
void main() {
  // 1. 配置系统 UI 样式
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent, // 状态栏透明
    statusBarIconBrightness: Brightness.dark, // 图标黑色 (亮色背景时使用)
    // statusBarIconBrightness: Brightness.light, // 图标白色 (深色背景时使用)
  ));
  
  runApp(const MyApp());
}
```

💡 **鸿蒙特有注意事项**：
在 OpenHarmony API 11+ 中，窗口默认可能是全屏布局的。如果发现内容被状态栏遮挡，需要检查 `Scaffold` 的 `body` 是否正确处理了顶部偏移。

### 3.2 安全区域 (SafeArea)

现在的鸿蒙手机大多有前置摄像头挖孔。为了防止内容被遮挡，**务必**给 `body` 包裹一个 `SafeArea`。

```dart
Scaffold(
  body: SafeArea(
    // 💡 top: true (默认) 会自动避开状态栏
    // 💡 bottom: true (默认) 会自动避开底部 Home 条
    child: Column(
      children: [Text('这段文字绝对不会被刘海挡住')],
    ),
  ),
)
```

### 3.3 侧滑返回手势冲突

在鸿蒙系统上，从屏幕左边边缘右滑是“返回”手势。如果你的 App 中使用了 `Drawer` (侧滑菜单)，也是左边缘右滑触发。这会导致冲突。

✅ **最佳实践**：
- 如果页面有 `Drawer`，建议保留左上角的“汉堡菜单”图标，让用户点击触发打开，而不是依赖边缘手势。
- 或者将 `drawerEdgeDragWidth` 设置小一点，避免覆盖系统手势区域。

---

## 四、实战：通用页面骨架封装

为了在项目中复用，我们通常会封装一个 `BaseScaffold`。

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class BaseScaffold extends StatelessWidget {
  final String title;
  final Widget body;
  final List<Widget>? actions;
  final Widget? floatingActionButton;
  final bool showBack; // 是否显示返回键

  const BaseScaffold({
    super.key,
    required this.title,
    required this.body,
    this.actions,
    this.floatingActionButton,
    this.showBack = true,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 1. 统一的 AppBar 样式
      appBar: AppBar(
        title: Text(
          title, 
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        elevation: 0.5,
        backgroundColor: Colors.white,
        foregroundColor: Colors.black, // 标题和图标颜色
        actions: actions,
        leading: showBack 
            ? IconButton(
                icon: const Icon(Icons.arrow_back_ios_new),
                onPressed: () => Navigator.pop(context),
              ) 
            : null,
      ),
      // 2. 统一的安全区域处理
      body: SafeArea(
        child: body,
      ),
      floatingActionButton: floatingActionButton,
      backgroundColor: const Color(0xFFF5F5F5), // 统一灰底
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 实战运行效果截图 -->
<!-- 设备: 鸿蒙 Mate 60 -->
<!-- 内容: 展示基于 BaseScaffold 构建的简单页面，包含标题、白色背景 AppBar 和灰色背景 Body -->

---

## 五、总结

`Scaffold` 是 Flutter 页面的基石，掌握它就掌握了 App 的基本形态。

### 核心要点回顾
1.  **结构化**：`Scaffold` 提供了标准化的 UI 槽位 (AppBar, Body, FAB, Drawer)。
2.  **个性化**：`AppBar` 支持灵活的自定义，包括渐变背景和 TabBar 扩展。
3.  **适配性**：在鸿蒙开发中，时刻由 `SafeArea` 和 `SystemChrome` 保驾护航，确保界面不被物理开孔遮挡。

### 下一篇预告
页面骨架搭好了，如果我们需要在页面中弹出一个对话框提醒用户，或者从底部弹出一个选择菜单，该怎么做？
**《Flutter for OpenHarmony 实战之基础组件：第十篇 Dialog, SnackBar 与 BottomSheet 交互反馈》**
我们将学习如何优雅地与用户进行“对话”。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/9-scaffold-appbar)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/9-scaffold-appbar)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
