# Flutter for OpenHarmony 实战之基础组件：第二十八篇 LayoutBuilder 与 OrientationBuilder — 构建响应式鸿蒙应用

## 前言

身处鸿蒙生态（OpenHarmony），开发者面临的是一个“极度多样化”的硬件环境：从窄屏手机到宽大的 MatePad 平板，从方正的折叠屏到车载大屏。如果依然使用硬编码的宽高来设计 UI，应用必将在不同设备上显得格格不入。

响应式布局是跨平台开发的灵魂。在 **Flutter for OpenHarmony** 中，`LayoutBuilder` 和 `OrientationBuilder` 是我们应对尺寸变化的终极利器。本文将深入讲解这两个组件的实战用法，教你如何编写一套代码，优雅适配所有鸿蒙终端。

---

## 一、LayoutBuilder：感知父容器的约束

`LayoutBuilder` 是最强大的布局感知组件。它的回调函数会提供 `BoxConstraints`，告诉你父组件允许你占据的最大和最小宽高。

### 1.1 核心逻辑
与 `MediaQuery`（感知屏幕尺寸）不同，`LayoutBuilder` **感知的是它的父容器**。这意味着哪怕是在一个小卡片内部，你也能根据剩余空间动态调整布局。

### 1.2 基础实战代码
```dart
LayoutBuilder(
  builder: (BuildContext context, BoxConstraints constraints) {
    if (constraints.maxWidth > 600) {
      // 空间充足：水平排列
      return Row(
        children: [
          Expanded(child: _buildBanner()),
          Expanded(child: _buildInfo()),
        ],
      );
    } else {
      // 空间狭窄：垂直排列
      return Column(
        children: [
          _buildBanner(),
          _buildInfo(),
        ],
      );
    }
  },
)
```

<!-- IMAGE_PLACEHOLDER: LayoutBuilder 在手机和平板上的不同展现效果对比 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机/平板 -->

---

## 二、OrientationBuilder：应对屏幕旋转

在鸿蒙设备上，屏幕旋转（从竖屏变为横屏）是一个非常常见的动作。`OrientationBuilder` 专门用于捕捉并响应方向变化。

### 2.1 捕获方向状态
`OrientationBuilder` 会告诉你当前是 `portrait`（竖屏）还是 `landscape`（横屏）。

```dart
OrientationBuilder(
  builder: (context, orientation) {
    return GridView.count(
      // 竖屏两列，横屏四列
      crossAxisCount: orientation == Orientation.portrait ? 2 : 4,
      children: List.generate(20, (i) => Card(child: Center(child: Text('Item $i')))),
    );
  },
)
```

💡 **技巧**：虽然 `MediaQuery.of(context).orientation` 也能获取方向，但 `OrientationBuilder` 具有更好的局部刷新性能，且逻辑更聚合。

---

## 三、进阶：构建通用的 Responsive 容器

在鸿蒙应用开发中，为了提高代码复用性，我们可以封装一个通用的 `ResponsiveLayout` 组件。

```dart
class ResponsiveLayout extends StatelessWidget {
  final Widget mobile;
  final Widget? tablet;
  final Widget desktop;

  const ResponsiveLayout({
    required this.mobile,
    this.tablet,
    required this.desktop,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth < 600) {
          return mobile;
        } else if (constraints.maxWidth < 1200) {
          return tablet ?? desktop; // 如果没有定义平板视图，则回退到桌面视图
        } else {
          return desktop;
        }
      },
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 基于自定义布局组件在折叠屏手机展开前后的变化 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙折叠屏 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 折叠屏适配 (Flex Mode)
鸿蒙折叠屏手机在半折叠状态下，应用会进入“平行视界”或分屏模式。

✅ **推荐方案**：
通过 `LayoutBuilder` 实时监控宽度变化。当宽度发生突变时（如折叠屏展开），UI 应该平滑过渡，建议配合 `AnimatedContainer` 使用，避免布局闪烁。

### 4.2 平板分屏与多窗口
在鸿蒙系统中，用户可以自由调整应用窗口大小。

⚠️ **注意事项**：
不要在 `initState` 中缓存屏幕宽高，因为窗口尺寸可能会在运行时被用户拉伸。必须在 `build` 方法中依赖 `LayoutBuilder` 或 `MediaQuery` 的实时数据。

### 4.3 字体缩放适配
鸿蒙系统支持全局字体大小调节。

✅ **最佳实践**：
在 `LayoutBuilder` 计算间距时，如果涉及到文本容器，尽量使用比例（Percentage）或灵活的 `Flex` 布局，不要使用固定的 `height`，防止大号字体导致内容被裁剪。

---

## 五、完整示例代码

以下提供一个完整的“多端适配 Dashboard”示例，可直接在鸿蒙模拟器中通过调整窗口大小查看效果。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: AdaptiveDashboard()));

class AdaptiveDashboard extends StatelessWidget {
  const AdaptiveDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 响应式布局实战')),
      body: LayoutBuilder(
        builder: (context, constraints) {
          // 根据宽度决定显示模式
          if (constraints.maxWidth > 900) {
            return _buildWideLayout();
          } else if (constraints.maxWidth > 600) {
            return _buildMediumLayout();
          } else {
            return _buildMobileLayout();
          }
        },
      ),
    );
  }

  // 大屏布局：左侧导航 + 中间内容 + 右侧详情
  Widget _buildWideLayout() {
    return Row(
      children: [
        Container(width: 250, color: Colors.blue[50], child: const _Sidebar()),
        const Expanded(flex: 3, child: _MainContent()),
        Container(width: 300, color: Colors.grey[100], child: const _DetailsPanel()),
      ],
    );
  }

  // 中屏布局（平板）：左侧导航 + 核心内容
  Widget _buildMediumLayout() {
    return Row(
      children: [
        Container(width: 80, color: Colors.blue[50], child: const _MiniSidebar()),
        const Expanded(child: _MainContent()),
      ],
    );
  }

  // 窄屏布局（手机）：仅展示核心内容
  Widget _buildMobileLayout() {
    return const _MainContent();
  }
}

class _Sidebar extends StatelessWidget {
  const _Sidebar();
  @override
  Widget build(BuildContext context) => const Center(child: Text("完整导航栏"));
}

class _MiniSidebar extends StatelessWidget {
  const _MiniSidebar();
  @override
  Widget build(BuildContext context) => const Center(child: Icon(Icons.menu));
}

class _MainContent extends StatelessWidget {
  const _MainContent();
  @override
  Widget build(BuildContext context) {
    return OrientationBuilder(
      builder: (context, orientation) {
        return GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: orientation == Orientation.portrait ? 1 : 2,
            childAspectRatio: 2.5,
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
          ),
          itemCount: 8,
          itemBuilder: (context, index) => Card(
            color: Colors.blue[100 * (index % 5 + 1)],
            child: Center(child: Text("数据卡片 $index")),
          ),
        );
      },
    );
  }
}

class _DetailsPanel extends StatelessWidget {
  const _DetailsPanel();
  @override
  Widget build(BuildContext context) => const Center(child: Text("详情展示区"));
}
```

---

## 六、总结

在构建 Flutter for OpenHarmony 应用时，响应式设计不再是可选配置，而是生存必备。

1.  **LayoutBuilder**：用于局部灵活性，根据父容器分配的空间改变组件形状。
2.  **OrientationBuilder**：用于处理物理世界的方向切换。
3.  **核心理念**：放弃对像素（Pixel）的绝对控制，转向对比例（Ratio）和约束（Constraints）的逻辑管理。

通过这两个组件的灵活搭配，你的应用将能够真正做到“一套代码，全端覆盖”，在鸿蒙世界的各种屏幕上都能提供一流的视觉体验。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

