# Flutter for OpenHarmony 实战之基础组件：第五十五篇 SliverGrid — 打造高性能的吸顶网格内容页

## 前言

在内容密集型应用中，网格布局（Grid Layout）是最高效的信息展示形态之一，通过横跨多列的卡片，用户可以快速扫描大量图片、商品或短视频封面。当我们希望这些网格能与其它层（如吸顶标题、Banner）共存于同一个滚动视图中时，普通的 `GridView` 就显得无能为力了。

在 **Flutter for OpenHarmony** 开发中，`SliverGrid` 作为 Sliver 家族的精锐成员，能让你在 `CustomScrollView` 中构建极致流畅且支持复杂滚动的网格流。本文将实战详解如何定制网格比例、列数及适配鸿蒙端的多样化屏幕。

---

## 一、SliverGrid 的核心三要素

要运行一个 `SliverGrid`，你需要指定两个核心代理：
1.  **SliverChildDelegate**：负责提供子组件（数据源）。
2.  **SliverGridDelegate**：负责确定布局算法（每行几个？间距多少？）。

### 1.1 基础实现代码
```dart
SliverGrid(
  delegate: SliverChildBuilderDelegate(
    (context, index) => Card(child: Center(child: Text("Item $index"))),
    childCount: 20,
  ),
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 2, // 核心：每行显示两列
    mainAxisSpacing: 10,
    crossAxisSpacing: 10,
    childAspectRatio: 0.8, // 宽高比
  ),
)
```

---

## 二、实战：灵活多变的网格布局

### 2.1 固定列数与自适应宽度
- **SliverGridDelegateWithFixedCrossAxisCount**：强制指定列数（如固定 3 列）。
- **SliverGridDelegateWithMaxCrossAxisExtent**：强制指定子组件的最大宽度（如不超过 200px，系统会自动计算能排成几列）。

💡 **场景选型**：在鸿蒙平板适配中，后者（`MaxCrossAxisExtent`）通常是更好的选择，因为它能自动从手机端的 2 列平滑过渡到平板端的 5 列。

```dart
gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
  maxCrossAxisExtent: 200.0,
  mainAxisSpacing: 8.0,
  crossAxisSpacing: 8.0,
  childAspectRatio: 1.0,
)
```

<!-- IMAGE_PLACEHOLDER: SliverGrid 在鸿蒙手机与平板之间自动调整列数的对比演示 -->
<!-- 类型: 截图 -->
<!-- 设备: 多端设备 -->

---

## 三、高级：实现“瀑布流”质感的网格

普通的 `SliverGrid` 所有格子必须等高（由 `childAspectRatio` 决定）。如果你需要像小红书那样的瀑布流（错落有致的高度）：

✅ **推荐方案**：
虽然 Sliver 家族没有内置动态高度的网格，但我们可以结合第三方库（如 `flutter_staggered_grid_view`）中的 `SliverStairedGrid` 或通过 `SliverList` 的复合技巧实现更复杂的排版。

---

## 四、OpenHarmony 平台适配建议

### 4.1 高效内存管理 (Sliver 的优势)
在展示具有高清封面图的网格时，内存压力巨大。

✅ **相关知识**：
`SliverGrid` 继承了 Sliver 家族的“懒加载”基因。在鸿蒙端，它仅会为当前可见区域（以及少量缓存区）的格子分配内存。当格子滑出屏幕时，其对应的内存会迅速被复用。这种高度集成的资源回收机制，是鸿蒙应用在长列表中依然保持极致流畅的关键。

### 4.2 适配折叠屏与分屏窗口
鸿蒙设备在分屏时，屏幕宽度会随拖拽条实时改变。

💡 **调优建议**：
在 `SliverGridDelegate` 中，不要写死 `crossAxisCount`。
推荐方案：使用 `MediaQuery` 测量宽度并动态返回列数。

```dart
int _calculateColumns(BuildContext context) {
  double width = MediaQuery.of(context).size.width;
  if (width > 800) return 4;
  if (width > 500) return 3;
  return 2;
}
```

### 4.3 触控动效细节
给网格卡片增加点击反馈效果，符合鸿蒙应用的设计直觉。

✅ **最佳实践**：
使用 `InkWell` 包裹 Item，并配合 `clipBehavior: Clip.antiAlias` 确保水波纹效果在圆角卡片内部不溢出。此外，鸿蒙系统对于网格选中的触感反馈（selectionClick）支持非常细腻，建议在 `onTap` 中集成。

<!-- IMAGE_PLACEHOLDER: 鸿蒙深色模式下，带微阴影和缩放动效的 SliverGrid 卡片列表展示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 五、完整示例代码

以下代码演示了一个集成“吸顶标题 + 自适应列数网格”的完整滚动页面实战。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: GridScrollPage()));

class GridScrollPage extends StatelessWidget {
  const GridScrollPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          // 1. 顶部折叠标题
          const SliverAppBar(
            pinned: true,
            expandedHeight: 180,
            flexibleSpace: FlexibleSpaceBar(title: Text("鸿蒙推荐商品")),
          ),
          
          // 2. 一个吸顶的小标题
          SliverToBoxAdapter(
            child: Container(
              padding: const EdgeInsets.all(16),
              color: Colors.blue[50],
              child: const Text("热门精选", style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ),
          
          // 3. 核心网格布局
          SliverPadding(
            padding: const EdgeInsets.all(10),
            sliver: SliverGrid(
              delegate: SliverChildBuilderDelegate(
                (context, index) => _buildGridItem(index),
                childCount: 40,
              ),
              // 使用自适应最大宽度的代理，适配手机和平板
              gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                maxCrossAxisExtent: 180,
                mainAxisSpacing: 10,
                crossAxisSpacing: 10,
                childAspectRatio: 0.75,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildGridItem(int index) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(child: Container(color: Colors.blue[100], child: const Icon(Icons.image, size: 50, color: Colors.white))),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text("鸿蒙智能单品 #$index", maxLines: 1, overflow: TextOverflow.ellipsis),
          ),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 8, bottom: 8),
            child: Text("¥ 199.0", style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的高性能商城或咨询类应用中，`SliverGrid` 是无可替代的核心布局。

1.  **懒加载机制**：是大规模数据展示的性能保障。
2.  **弹性布局**：通过 `MaxCrossAxisExtent` 实现真正的跨端（手机/平板）自动列数匹配。
3.  **开发准则**：在鸿蒙端利用好吸顶联动、圆角裁剪和精细反馈，能让你的网格列表展现出顶级应用的品质。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

