# Flutter for OpenHarmony 实战之基础组件：第五十六篇 SliverPersistentHeader — 打造极致个性的吸顶交互头部

## 前言

在进行复杂的长列表开发时，我们经常需要实现这样的效果：当列表滑动到某个分类（例如“热门推荐”）时，该分类的标题会自动锁定并“吸附”在屏幕顶部，直到下一个分类把它顶走。普通的 `AppBar` 只能吸顶一个，而 `SliverPersistentHeader` 则是为了实现“多级联动吸顶”而生的重型武器。

在 **Flutter for OpenHarmony** 平台上，利用这个组件可以构建出极具动态美感的详情页或索引页。本文将详解如何通过自定义 `Delegate`，在鸿蒙应用中实现高度可定制的吸顶头部特效。

---

## 一、核心原理：SliverPersistentHeaderDelegate

不同于普通的 Widget，`SliverPersistentHeader` 必须接收一个实现了 `SliverPersistentHeaderDelegate` 的派生类。

### 1.1 你需要告诉系统四件事：
- **minExtent**：头部折叠后的最小高度。
- **maxExtent**：头部展开时的最大高度。
- **build**：如何根据当前的 `shrinkOffset`（收缩偏移量）渲染不同的 UI。
- **shouldRebuild**：何时需要刷新头部（性能优化的关键）。

---

## 二、实战演练：构建多级吸顶分类标题

### 2.1 编写自定义 Delegate
```dart
class MyHeaderDelegate extends SliverPersistentHeaderDelegate {
  final String title;
  MyHeaderDelegate(this.title);

  @override
  Widget build(BuildContext context, double shrinkOffset, bool overlapsContent) {
    // shrinkOffset 从 0 到 maxExtent 变化
    // 可以根据 shrinkOffset 实现渐变色、文字大小变化等动效
    return Container(
      color: shrinkOffset > 0 ? Colors.blue[800] : Colors.blue[100],
      alignment: Alignment.centerLeft,
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Text(title, style: TextStyle(
        color: shrinkOffset > 0 ? Colors.white : Colors.black87,
        fontWeight: FontWeight.bold
      )),
    );
  }

  @override
  double get maxExtent => 80.0; // 展开高度

  @override
  double get minExtent => 50.0; // 吸顶后的固定高度

  @override
  bool shouldRebuild(covariant SliverPersistentHeaderDelegate oldDelegate) => true;
}
```

### 2.2 在 CustomScrollView 中使用
```dart
CustomScrollView(
  slivers: [
    SliverPersistentHeader(
      pinned: true, // 核心：设为 true 才会吸顶
      delegate: MyHeaderDelegate("分类一：鸿蒙组件"),
    ),
    SliverList(...), // 对应的展示列表
    SliverPersistentHeader(
      pinned: true,
      delegate: MyHeaderDelegate("分类二：开发实战"),
    ),
    SliverList(...),
  ],
)
```

<!-- IMAGE_PLACEHOLDER: SliverPersistentHeader 实现的多级分类标题在滑过程中自动吸顶的效果演示 -->
<!-- 类型: GIF -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、进阶：打造视差翻转效果

由于我们在 `build` 中可以实时获取 `shrinkOffset`。

💡 **动效思路**：
你可以根据 `(maxExtent - shrinkOffset) / maxExtent` 计算出一个 0 到 1 的进度值。利用这个值来动态缩放背景图片、调整文字透明度或是改变图标的旋转角度。在鸿蒙端展现出一种“呼吸感”十足的折叠体验。

```dart
double progress = (maxExtent - shrinkOffset) / maxExtent;
return Stack(
  fit: StackFit.expand,
  children: [
    Opacity(opacity: progress, child: Image.network(...)),
    Center(child: Text("标题", style: TextStyle(fontSize: 16 + 10 * progress))),
  ],
);
```

<!-- IMAGE_PLACEHOLDER: 结合动画计算的视差头部在鸿蒙平板横屏模式下的流畅交互 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 滚动触感反馈适配
在鸿蒙系统上，当吸顶头部正好“贴”到顶端那一瞬间。

✅ **推荐方案**：
监听 `shrinkOffset`。当 `shrinkOffset == maxExtent - minExtent`（即刚达到完全折叠状态）时，可以触发一次极其微弱的 `HapticFeedback.lightImpact()`。这种精细的反馈能让鸿蒙用户感觉到界面元素“到位”了。

### 4.2 性能与 shouldRebuild
吸顶头部在滑动过程中每一帧都会调用 `build`。

💡 **调优建议**：
在鸿蒙端高刷屏幕（120Hz）上，确保 `build` 方法内部逻辑足够轻量。不要在 `build` 方法里初始化任何控制器或进行耗时运算。同时在 `shouldRebuild` 中通过判断关键参数（如 Title 是否改变）来决定是否真正重绘，减少不必要的 GPU 损耗。

### 4.3 状态栏颜色适配
鸿蒙系统的状态栏文字颜色（深色/浅色）会影响阅读体验。

✅ **最佳实践**：
既然吸顶头部在收缩后颜色往往会加深，建议在 `build` 方法中判断 `shrinkOffset`。当进入收缩状态时，通过 `SystemUiOverlayStyle` 动态将鸿蒙状态栏设置为浅色模式（白色文字），确保视觉上的连贯性和易读性。

<!-- IMAGE_PLACEHOLDER: 动态调整鸿蒙状态栏文字颜色以匹配吸顶头部底色的效果预览 -->
<!-- 类型: 截图 -->
<!-- 设备: 模拟器 -->

---

## 五、完整示例代码

以下代码演示了一个带有“颜色渐变”和“文字缩放”的专业吸顶头部实战示例。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: PersistentHeaderDemo()));

class PersistentHeaderDemo extends StatelessWidget {
  const PersistentHeaderDemo({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          _buildHeader("华为 HarmonyOS 实战系列"),
          SliverList(delegate: SliverChildBuilderDelegate((c, i) => ListTile(title: Text("基础课 #$i")), childCount: 15)),
          _buildHeader("Flutter 跨平台开发进阶"),
          SliverList(delegate: SliverChildBuilderDelegate((c, i) => ListTile(title: Text("高级课 #$i")), childCount: 15)),
        ],
      ),
    );
  }

  Widget _buildHeader(String title) {
    return SliverPersistentHeader(
      pinned: true,
      delegate: CustomHeaderDelegate(title),
    );
  }
}

class CustomHeaderDelegate extends SliverPersistentHeaderDelegate {
  final String title;
  CustomHeaderDelegate(this.title);

  @override
  Widget build(BuildContext context, double shrinkOffset, bool overlapsContent) {
    // 计算收缩比例（从 1.0 为全展开，0.0 为完全重叠/吸顶）
    final double visiblePercent = (maxExtent - shrinkOffset) / maxExtent;
    
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            Color.lerp(Colors.blue[100], Colors.blue[900], 1 - visiblePercent)!,
            Color.lerp(Colors.blue[200], Colors.blue[800], 1 - visiblePercent)!,
          ],
        ),
      ),
      child: Center(
        child: Text(
          title,
          style: TextStyle(
            fontSize: 16 + 8 * visiblePercent, // 文字从 24 缩放到 16
            color: visiblePercent < 0.5 ? Colors.white : Colors.blue[900],
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }

  @override
  double get maxExtent => 120.0;

  @override
  double get minExtent => 60.0;

  @override
  bool shouldRebuild(covariant CustomHeaderDelegate oldDelegate) {
    return oldDelegate.title != title;
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的复杂长页面设计中，`SliverPersistentHeader` 是打破平庸视觉的杀手锏。

1.  **Delegate 是核心**：通过 `shrinkOffset` 掌控一切动效的变化数值。
2.  **Pinned 属性**：让你的标题在用户最需要它指引位置时，永远“锁定”在视线内。
3.  **开发准则**：在鸿蒙端利用好渐变过渡与触感回传，是区分初级开发者与高级架构师的关键细节。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

