# Flutter for OpenHarmony 实战之基础组件：第三十六篇 PageView — 流畅的整页滑动与轮播实现

## 前言

在移动端应用中，整页滑动（Swiping Pages）是除了垂直滚动之外最高频的交互方式。无论是引导页（Onboarding）、图片浏览器还是内容分类切换（如抖音的上下滑），底层都离不开 `PageView` 的身影。

在 **Flutter for OpenHarmony** 平台上，`PageView` 能够充分利用系统的极致流畅动效，配合鸿蒙设备自适应的刷新率周期，实现如丝般顺滑的翻页感。本文将深入讲解 `PageView` 的进阶用法，包括页面预加载、视口比例定制及复杂的滑动联动。

---

## 一、PageView 的核心成员

### 1.1 基础结构
`PageView` 的使用非常简单，类似于水平排列的 `ListView`，但它具有“磁力吸附”特性，即每次滑动都会停在某一页的中心。

```dart
PageView(
  children: [
    Container(color: Colors.red, child: Center(child: Text("第一页"))),
    Container(color: Colors.blue, child: Center(child: Text("第二页"))),
    Container(color: Colors.green, child: Center(child: Text("第三页"))),
  ],
)
```

### 1.2 PageController：页面的“遥控器”
如果你想通过代码控制翻页（例如点击按钮跳到下一页），或者是调整初始显示的页面、页面的显示比例，就必须用到 `PageController`。

```dart
final PageController _controller = PageController(
  initialPage: 0,
  viewportFraction: 0.8, // 核心：视口比例，设为 0.8 可看到左右两边页面的预览
);
```

---

## 二、高级进阶：自定义视口与无限轮播

### 2.1 视口比例（Viewport Fraction）
在设计精美的鸿蒙应用（如音乐专辑滚动）中，我们常需要中间页面最大，左右页面露出一小部分。

```dart
PageView.builder(
  controller: PageController(viewportFraction: 0.85),
  itemBuilder: (context, index) {
    return AnimatedPadding(
      duration: const Duration(milliseconds: 300),
      // 根据当前页码通过控制器算出的偏移进行缩放动画
      padding: EdgeInsets.symmetric(vertical: _currentPage == index ? 0 : 40, horizontal: 8),
      child: Card(elevation: 4, color: Colors.blue[300]),
    );
  },
)
```

<!-- IMAGE_PLACEHOLDER: 自定义视口比例在鸿蒙平板上的卡片轮播效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、常见应用场景：App 引导页

一个典型的 App 启动引导页实战代码：

```dart
class OnboardingScreen extends StatefulWidget {
  @override
  _OnboardingScreenState createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final _pageController = PageController();
  int _currentPage = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          PageView(
            controller: _pageController,
            onPageChanged: (idx) => setState(() => _currentPage = idx),
            children: [
              _buildPage("欢迎使用鸿蒙新视界", Icons.rocket_launch, Colors.blue),
              _buildPage("高效跨平台开发体验", Icons.code, Colors.indigo),
              _buildPage("即刻开启你的创意", Icons.brush, Colors.deepPurple),
            ],
          ),
          Positioned(
            bottom: 60,
            left: 0, right: 0,
            child: _buildIndicator(), // 页面指示器
          )
        ],
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 引导页页面指示器（Dots Indicator）在鸿蒙端的动态切换效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 模拟器 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 滑动阻尼与回弹效果
鸿蒙系统（如 HarmonyOS Next）的滑动曲线非常具有物理感。

✅ **推荐方案**：
对于 PageView，建议设置 `physics: const BouncingScrollPhysics()`。这种物理引擎在滑动到边缘时会产生自然的弹性效果，非常符合鸿蒙用户的触感预期。

### 4.2 功耗与性能管理
`PageView` 默认会预加载相邻的页面。

💡 **调优建议**：
如果每一页都是非常沉重的 Widget（如全屏高清视频），建议利用 `onPageChanged` 回调，结合状态管理仅渲染当前可见的页面，对不可见页面执行 `Pause` 或释放资源的操作。

### 4.3 多分辨率（折叠屏）适配
在鸿蒙折叠屏设备上，屏幕宽度会发生剧烈变化。

✅ **最佳实践**：
当屏幕宽度超过 800px 时，利用 `LayoutBuilder` 动态调整 `PageController` 的 `viewportFraction`。大屏设备上可以适当调小该值，一次展示更多的侧边内容。

```dart
LayoutBuilder(
  builder: (context, constraints) {
    final fraction = constraints.maxWidth > 600 ? 0.6 : 1.0;
    return PageView(controller: PageController(viewportFraction: fraction), ...);
  }
)
```

---

## 五、完整示例代码

以下代码演示了一个带有“同步指示器”和“按钮控制”的整页轮播组件。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: PageViewDemo()));

class PageViewDemo extends StatefulWidget {
  const PageViewDemo({super.key});

  @override
  State<PageViewDemo> createState() => _PageViewDemoState();
}

class _PageViewDemoState extends State<PageViewDemo> {
  final PageController _controller = PageController();
  int _currentIdx = 0;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 翻页容器实战')),
      body: Column(
        children: [
          // 核心翻页区域
          Expanded(
            child: PageView.builder(
              controller: _controller,
              onPageChanged: (v) => setState(() => _currentIdx = v),
              itemCount: 4,
              itemBuilder: (context, index) {
                return _buildPageContent(index);
              },
            ),
          ),
          
          // 底部控制与指示器
          _buildBottomBar(),
        ],
      ),
    );
  }

  Widget _buildPageContent(int index) {
    final colors = [Colors.blue, Colors.orange, Colors.green, Colors.purple];
    return Container(
      margin: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: colors[index % colors.length],
        borderRadius: BorderRadius.circular(24),
        boxShadow: [BoxShadow(color: Colors.black.withAlpha(20), blurRadius: 10, offset: const Offset(0, 5))],
      ),
      child: Center(
        child: Text("PAGE ${index + 1}", style: const TextStyle(color: Colors.white, fontSize: 40, fontWeight: FontWeight.bold)),
      ),
    );
  }

  Widget _buildBottomBar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // 页面指示器
          Row(
            children: List.generate(4, (i) => Container(
              width: _currentIdx == i ? 24 : 8,
              height: 8,
              margin: const EdgeInsets.only(right: 6),
              decoration: BoxDecoration(
                color: _currentIdx == i ? Colors.blue : Colors.grey[300],
                borderRadius: BorderRadius.circular(4),
              ),
            )),
          ),
          
          // 翻页按钮
          ElevatedButton(
            onPressed: () {
              _controller.nextPage(duration: const Duration(milliseconds: 400), curve: Curves.easeInOutQuart);
            },
            child: const Text("下一页"),
          )
        ],
      ),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 开发中，`PageView` 是构建沉浸式、交互式界面的首选布局工具。

1.  **PageController**：是灵魂，通过 `viewportFraction` 和 `nextPage` 控制翻页体验。
2.  **物理引擎**：在鸿蒙端首选 `BouncingScrollPhysics` 以获得最佳视觉感知。
3.  **多端适配**：利用 `LayoutBuilder` 实时监控宽度，让轮播图在手机和平板上都能展现出最合理的视口比例。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

