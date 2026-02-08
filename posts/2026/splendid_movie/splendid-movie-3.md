---
title: "Flutter for OpenHarmony：沉浸式 HeroSection 与联动标签 — 复杂首页布局艺术"
date: 2026-02-02
tags: ["Flutter", "OpenHarmony", "UI布局", "Slivers"]
categories: ["Flutter for OpenHarmony 实战"]
---

# Flutter for OpenHarmony：沉浸式 HeroSection 与联动标签 — 复杂首页布局艺术

## 前言

在 [上一篇](https://blog.csdn.net/your-link) 中，我们通过玻璃拟态（Glassmorphism）为 Splendid Movie 奠定了视觉基调。今天，我们将聚焦于 App 的“门面”——**首页（Home Screen）**。

一个好的电影应用首页，不仅要能展示海报，更要处理好复杂的滚动逻辑、分类筛选以及沉浸式的视觉体验。本文将剖析如何使用 `Stack` 布局、`CustomScrollView` 和状态管理，构建一个既美观又高性能的首页。

<!-- IMAGE_PLACEHOLDER: 首页整体动态演示 -->
<!-- 类型: GIF -->
<!-- 设备: 鸿蒙设备 -->
<!-- 内容: 上下滑动浏览，点击 Category 切换内容，顶部的 Hero 大图随之视差滚动 -->

---

## 一、 沉浸式 Hero Section：让海报“破框”而出

传统的 App 顶部通常是一个 AppBar，但在 Splendid Movie 中，我们希望电影海报能延伸到屏幕的最顶端（状态栏下方），创造出沉浸感。

### 1.1 Stack + Gradient Overlay

要实现这个效果，核心在于使用 `Stack` 将图片置于底层，并在其上叠加一层**渐变遮罩**，保证顶部的状态栏文字和底部的电影标题清晰可见。

```dart
// lib/widgets/hero_banner.dart

class HeroBanner extends StatelessWidget {
  final Movie movie;

  const HeroBanner({required this.movie});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // 1. 底层大图
        Positioned.fill(
          child: Image.network(
            movie.posterUrl,
            fit: BoxFit.cover,
            // 💡 技巧：使用 ShaderMask 给图片边缘增加柔和过渡
            color: Colors.black.withOpacity(0.3),
            colorBlendMode: BlendMode.darken,
          ),
        ),
        
        // 2. 底部渐变遮罩 (防止文字看不清)
        Positioned(
          bottom: 0,
          left: 0,
          right: 0,
          height: 200, // 遮罩高度
          child: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.transparent,
                  // 这里的背景色与 App 背景色一致，实现无缝衔接
                  const Color(0xFF09090F).withOpacity(0.8), 
                  const Color(0xFF09090F),
                ],
              ),
            ),
          ),
        ),

        // 3. 电影信息内容
        Positioned(
          bottom: 20,
          left: 20,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(movie.title, style: AppTheme.h1),
              Row(children: [...]), // 评分星星等
            ],
          ),
        )
      ],
    );
  }
}
```

### 1.2 OpenHarmony 适配要点

在鸿蒙设备上，状态栏的高度因机型而异。为了防止图片内容被刘海屏遮挡，我们需要结合 `MediaQuery` 获取精确的 `padding.top`。

```dart
// 适配刘海屏
final topPadding = MediaQuery.of(context).padding.top;

// 顶部搜索栏位置
Positioned(
  top: topPadding + 10, 
  left: 20, 
  right: 20,
  child: SearchBar(),
)
```

---

## 二、 联动分类标签 (Category Tabs)

在 Hero Section 下方，我们需要一个可以横向滚动的分类标签栏。点击不同标签时，下方的电影列表应随之刷新。

### 2.1 状态管理与布局

这里我们利用 `DisplayFeature` 或简单的 `State` 来控制选中的 `selectedIndex`。

```dart
// lib/screens/home_screen.dart (片段)

int _selectedIndex = 0;
final categories = ["All", "Action", "Drama", "Sci-Fi", "Thriller"];

Widget _buildCategoryTabs() {
  return SizedBox(
    height: 50,
    child: ListView.builder(
      scrollDirection: Axis.horizontal,
      itemCount: categories.length,
      padding: const EdgeInsets.symmetric(horizontal: 20),
      itemBuilder: (context, index) {
        final isSelected = _selectedIndex == index;
        return GestureDetector(
          onTap: () {
            setState(() => _selectedIndex = index);
            // TODO: 触发下方列表数据更新
          },
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            margin: const EdgeInsets.only(right: 16),
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
            decoration: BoxDecoration(
              // 选中态使用霓虹渐变色
              gradient: isSelected 
                  ? const LinearGradient(colors: [Color(0xFF7B61FF), Color(0xFFFF5A5F)])
                  : null,
              color: isSelected ? null : Colors.white10,
              borderRadius: BorderRadius.circular(25),
              border: isSelected ? null : Border.all(color: Colors.white24),
            ),
            child: Center(
              child: Text(
                categories[index],
                style: TextStyle(
                  color: isSelected ? Colors.white : Colors.white60,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ),
          ),
        );
      },
    ),
  );
}
```

<!-- IMAGE_PLACEHOLDER: 标签切换动效 -->
<!-- 类型: GIF -->
<!-- 内容: 点击 "Action" 标签，背景色平滑过渡为渐变红，且有轻微的缩放动画 -->

---

## 三、 高性能横向列表 (Horizontal Movie List)

首页的主体由多个横向滚动的电影列表组成（如“正在热映”、“Top 10”）。

### 3.1 嵌套滚动的性能隐忧

如果直接在 `Column` 中放入多个 `ListView`，可能会遇到高度计算错误或滚动冲突。最佳实践是确定好每个 Section 的高度。

```dart
Widget _buildMovieSection(String title, List<Movie> movies) {
  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      // 标题栏
      Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        child: Text(title, style: AppTheme.h2),
      ),
      
      // 横向滚动列表
      SizedBox(
        height: 280, // 🔒 固定高度，避免布局计算开销
        child: ListView.separated(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 20),
          itemCount: movies.length,
          separatorBuilder: (_, __) => const SizedBox(width: 16),
          itemBuilder: (context, index) {
            return MovieCard(
              movie: movies[index],
              width: 160, // 卡片固定宽度
            );
          },
        ),
      ),
    ],
  );
}
```

### 3.2 鸿蒙下的手势冲突处理

在鸿蒙系统（OpenHarmony）中，侧滑返回手势（Swipe Back）可能会与横向滚动的列表（Horizontal ListView）发生冲突。用户想滑回上一页，却误触了列表滚动。

**✅ 解决方案**：
1.  **增加边距**：确保列表左侧有足够的 `padding`（如 20dp），让用户从屏幕极边缘滑动时能触发系统返回。
2.  **以及**：对于全屏横向轮播图，建议配合 `WillPopScope` 或 `PopScope` 进行手势拦截判定（虽然首页通常不需要返回，但在二级页面非常重要）。

---

## 四、 总结

通过本篇的实战，我们完成了 Splendid Movie 首页的核心构建：
*   利用 `Stack` + `Gradient` 实现了沉浸式的 Hero 头部。
*   构建了响应式的 `CategoryTabs` 筛选器。
*   解决了横向列表在移动端的布局难题与手势适配。

至此，我们的 App 已经看起来像一个像样的产品了。但它还缺那一点“灵魂”——动效。下一篇，我们将进入全系列最精彩的部分：**【播放篇】视频播放器深度定制与弹幕系统实战**。我们将手写一个弹幕引擎，并在鸿蒙设备上流畅运行视频。

---

> 📦 **完整代码已上传至 AtomGit**：[splendid_movie](https://atomgit.com/jiang_style/splendid_movie)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
