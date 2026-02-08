---
title: "Flutter for OpenHarmony：全栈业务页构建 — 从电影商城到个人中心"
date: 2026-02-02
tags: ["Flutter", "OpenHarmony", "GridView", "Sliver"]
categories: ["Flutter for OpenHarmony 实战"]
---

# Flutter for OpenHarmony：全栈业务页构建 — 从电影商城到个人中心

## 前言

前面的文章中，我们攻克了首页和播放器这两个技术高地。今天，我们将视角转向 App 的商业化与用户体系——**电影商城 (Store)** 和 **个人中心 (Profile)**。

这两个页面看似常规，但要做出“高级感”并不容易。本篇将详细讲解如何利用 `Sliver` 家族构建弹性滚动的个人页头，以及在鸿蒙设备上完美适配的网格布局系统。

<!-- IMAGE_PLACEHOLDER: 个人中心与商城双页展示 -->
<!-- 类型: 截图 -->
<!-- 内容: 左侧为个人中心（头像+毛玻璃背景），右侧为商城网格卡片 -->

---

## 一、 电影商城：响应式网格系统 (Store Screen)

商城的通常布局是：顶部有横向推荐，下方是密集的商品网格。

### 1.1 使用 SliverGrid 构建复杂列表

为了让页面滚动更自然，我们放弃简单的 `Column`，转而使用 `CustomScrollView` + `SliverGrid`。

```dart
// lib/screens/store_screen.dart

Widget build(BuildContext context) {
  return Scaffold(
    body: CustomScrollView(
      slivers: [
        // 1. 顶部标题栏
        SliverAppBar(
          title: Text("Movie Store"),
          backgroundColor: AppColors.background,
          floating: true, // 向下滚动时隐藏，向上滚动立即出现
        ),

        // 2. 热门推荐 (横向)
        SliverToBoxAdapter(
          child: _buildFeaturedSection(),
        ),

        // 3. 电影网格
        SliverPadding(
          padding: const EdgeInsets.all(16),
          sliver: SliverGrid(
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,       // 双列布局
              childAspectRatio: 0.7,   // 宽高比，适合电影海报
              mainAxisSpacing: 16,
              crossAxisSpacing: 16,
            ),
            delegate: SliverChildBuilderDelegate(
              (context, index) => _buildStoreItem(movies[index]),
              childCount: movies.length,
            ),
          ),
        ),
      ],
    ),
  );
}
```

### 1.2 鸿蒙大屏适配技巧

OpenHarmony 设备不仅有手机，还有平板和折叠屏。固定的 `crossAxisCount: 2` 在大屏上会显得非常稀疏。我们应该根据屏幕宽度动态调整列数。

```dart
// 动态获取列数
final width = MediaQuery.of(context).size.width;
int columns = 2;
if (width > 600) columns = 3;  // 折叠屏展开/平板
if (width > 900) columns = 4;  // PC/大屏

SliverGridDelegateWithFixedCrossAxisCount(
  crossAxisCount: columns,
  // ...
)
```

---

## 二、 个人中心：视差滚动与模糊背景 (Profile Screen)

个人中心是展示用户个性的地方。我们采用“头像居中 + 背景模糊”的经典设计，并配合视差滚动效果。

### 2.1 整体布局结构

```dart
Stack(
  children: [
    // 1. 全屏背景图
    Positioned.fill(
      child: Image.asset("assets/bg_profile.jpg", fit: BoxFit.cover),
    ),
    
    // 2. 全屏高斯模糊遮罩
    Positioned.fill(
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
        child: Container(color: Colors.black54),
      ),
    ),

    // 3. 内容区域
    SafeArea(
      child: Column(
        children: [
          _buildUserInfo(), // 头像、昵称
          _buildStatsRow(), // 粉丝数、关注数
          Expanded(child: _buildMenuOptions()), // 底部菜单列表
        ],
      ),
    ),
  ]
)
```

### 2.2 性能与美学的平衡

在 `ProfileScreen` 中，我们大量使用了 `GlassContainer` 作为菜单项的背景。

```dart
Widget _buildMenuOptions() {
  return Container(
    margin: const EdgeInsets.only(top: 20),
    padding: const EdgeInsets.symmetric(horizontal: 20),
    child: ListView(
      children: [
        _buildGlassMenuItem(Icons.history, "播放历史"),
        _buildGlassMenuItem(Icons.favorite, "我的收藏"),
        _buildGlassMenuItem(Icons.settings, "设置"),
      ],
    ),
  );
}
```

这种设计使得个人中心看起来像悬浮在虚空之中，非常符合我们 "Neon Night" 的主题。

---

## 三、 表单交互：登录页 (Login Screen)

登录页虽然简单，但它是用户体验的第一道门槛。我们需要处理好软键盘弹出时的布局适应。

### 3.1 键盘避让

在鸿蒙设备上，软键盘弹出高度各异。使用 `SingleChildScrollView` 或 `resizeToAvoidBottomInset: true` 是标准做法。

但在 Splendid Movie 中，我们希望背景图保持不动，只有输入框上移。

```dart
Scaffold(
  resizeToAvoidBottomInset: false, // 🚫 禁止背景变形
  body: Stack(
    children: [
      // 背景图
      Positioned.fill(child: Image.asset(...)),
      
      // 内容层：使用 AnimatedPadding 或 Center 配合键盘高度
      Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.only(
             // 💡 关键：底部 Padding 设为键盘高度，把内容顶上去
             bottom: MediaQuery.of(context).viewInsets.bottom
          ),
          child: _buildLoginForm(),
        ),
      ),
    ],
  ),
);
```

---

## 四、 总结

这一篇我们完善了 Splendid Movie 的业务拼图：
*   使用 `SliverGrid` 搭建了高性能的瀑布流商城。
*   利用 `Stack` + `BackdropFilter` 打造了高级感的个人中心。
*   通过 `MediaQuery` 巧妙处理了登录页的键盘遮挡问题。

至此，我们的 App 功能开发阶段基本结束。接下来的文章将转向**“工程化与发布”**。下一篇 **【品牌篇】App 图标定制与沉浸式启动页 (Splash) 方案** 将教你如何给 App 穿上这一身帅气的行头，打破“默认 Flutter 图标”的魔咒。

---

> 📦 **完整代码已上传至 AtomGit**：[splendid_movie](https://atomgit.com/jiang_style/splendid_movie)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
