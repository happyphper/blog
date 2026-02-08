![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战：每日热点 App（三）— 深色模式适配与高级 UI 组件封装

> **摘要**：一个好的 App，颜值是第一生产力。本文将带你进入"每日热点"应用的视觉中心，讲解如何构建一套专业级的深色模式设计系统，封装具有高级感的 UI 组件，并手把手教你实现具有"呼吸感"的骨架屏动画。

## 前言

在[《逻辑篇》](https://blog.csdn.net/your_link_to_part2)中，我们打通了后端 API 的管道，让数据流进了应用。但如果直接用原生的 `ListView` 展示这些 JSON 数据，界面会显得苍白无力。

在鸿蒙（HarmonyOS）生态中，用户对界面的精致程度有着极高的期待。特别是深色模式（Dark Mode），不仅是为了护眼，更是一种审美的表达。本篇我们将利用 Flutter 强大的渲染能力，打造一个 Premium 感十足的聚合新闻界面。

---

## 一、设计系统：构建应用的主基调

在动手写 Widget 之前，我们需要先定义出一套严谨的设计规范。一个专业的 UI 不应该是随机取色的过程，而是系统性应用色彩、圆角和间距的结果。

### 1.1 全面拥抱 OLED 深色模式

为了让应用在鸿蒙设备的 OLED 屏幕上更省电、对比度更柔和，我们定义了一套基于黑灰色的层级系统。

```dart
class AppTheme {
  // 🟢 背景层级
  static const Color backgroundDark = Color(0xFF0A0A0B); // 纯净底色
  static const Color surfaceDark = Color(0xFF121214);    // 二级背景
  static const Color cardDark = Color(0xFF1A1A1D);       // 卡片背景

  // 🟢 品牌色：热点红 + 渐变
  static const Color primary = Color(0xFFDC2626);
  static const LinearGradient primaryGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFFDC2626), Color(0xFFB91C1C)],
  );

  // 🟢 统一圆角规范
  static const double radiusMd = 12.0;
  static const double radiusLg = 16.0;
}
```

💡 **设计心得**：在鸿蒙深色模式下，应避免使用纯黑色（#000000）作为卡片色，深灰色能提供更好的深度感和可交互感。

---

## 二、高级组件：热榜卡片 `HotItemCard` 的艺术

`HotItemCard` 是整个应用出现频率最高的 UI 单元。我们将为其注入细节，包括索引角标、平台配色标签和优雅的投影。

### 2.1 结构化布局方案

我们使用 `intrinsicHeight` 配合 `Row` 和 `Column` 来实现自适应高度。

```dart
Widget _buildCard(BuildContext context) {
  return Container(
    margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: AppTheme.cardDark,
      borderRadius: BorderRadius.circular(AppTheme.radiusMd),
      border: Border.all(color: AppTheme.border, width: 1), // 极细边框增加精致感
    ),
    child: Row(
      children: [
        // 1. 排名索引
        _buildIndex(item.index),
        const SizedBox(width: 16),
        // 2. 主体内容
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(item.title, style: AppTheme.titleStyle),
              const SizedBox(height: 8),
              _buildMetaInfo(),
            ],
          ),
        ),
      ],
    ),
  );
}
```

📌 **亮点分析**：我们在卡片周围加上了 `0.5px` 或 `1px` 的深灰色边框，这种“微分割”在深色模式下非常受大厂 UI 欢迎。

---

## 三、动效增强：打造“呼吸感”骨架屏

数据加载时的“白屏”或“转圈圈”会让用户感到焦虑。骨架屏（Skeleton Screen）通过模拟内容的占位，让加载过程不再死板。

### 3.1 呼吸动画的实现细节

我们通过 `AnimationController` 实现一个循环的透明度变化，让占位块像是在“呼吸”。

```dart
class LoadingSkeleton extends StatefulWidget {
  const LoadingSkeleton({super.key});

  @override
  State<LoadingSkeleton> createState() => _LoadingSkeletonState();
}

class _LoadingSkeletonState extends State<LoadingSkeleton> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    )..repeat(reverse: true); // 🔄 无限循环逆向播放
    
    _animation = Tween<double>(begin: 0.3, end: 0.8).animate(_controller);
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Opacity(
          opacity: _animation.value, // 核心：透明度随动画变化
          child: _buildPlaceholderList(),
        );
      },
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 骨架屏动画演示 GIF -->
<!-- 类型: GIF -->
<!-- 内容: 展示深色模式下，骨架屏渐隐渐显的丝滑效果 -->

---

## 四、鸿蒙化适配：针对不同设备的微调

HarmonyOS 设备的形态非常多样（直板手机、折叠屏、平板）。

### 4.1 响应式列布局

在鸿蒙平板上，如果列表还是占据全宽会显得间距过大。我们可以结合 `LayoutBuilder` 或 `MediaQuery` 进行优化：

```dart
Widget _buildResponsiveGrid(BuildContext context) {
  final width = MediaQuery.of(context).size.width;
  return ListView.builder(
    padding: EdgeInsets.symmetric(
      // 💡 亮点：大屏（如鸿蒙平板）增加侧边距，小屏保持标准
      horizontal: width > 600 ? width * 0.15 : 0, 
    ),
    itemBuilder: (context, index) => HotItemCard(item: _items[index]),
  );
}
```

### 4.2 文字渲染优化

鸿蒙系统默认使用 HarmonyOS Sans 字体，它的字间距和字重与 Android 系略有不同。我们在 `TextStyle` 中设置 `height: 1.5`，确保多行新闻标题在鸿蒙设备上不会显得拥挤。

---

## 五、下篇预告

本篇文章我们从 UI 设计系统的构建到高级自定义组件的封装，完成了“每日热点”应用最关键的视觉部分。我们的 App 现在不仅有“灵魂”（数据），也有了“完美的颜值”。

目前还有一个关键问题：当用户点击心仪的新闻标题时，如何跳转原平台阅读？当服务器出错时，如何展示友好的报错并支持重试？

在最终篇**【交互篇】**中，我们将处理“外部浏览器跳转 + 剪贴板兜底”的双保险跳转逻辑，并集成下拉刷新，完成应用的最后一块拼图。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-example (主分支)](https://atomgit.com/dragonbady/open-harmony-example/tree/main/examples/daily_hotspots)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
