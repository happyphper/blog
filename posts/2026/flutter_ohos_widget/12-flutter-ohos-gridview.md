![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第十二篇 GridView 网格布局详解

> **摘要**：在 App 开发中，除了线性的列表，网格布局是展示图片、商品和功能的最佳方式。本文将全方位解析 Flutter 的 GridView 组件，从基础的固定列数网格，到高性能的动态懒加载，最后教你如何利用 LayoutBuilder 在 OpenHarmony 平板与折叠屏上实现自适应响应式网格。

## 前言

如果说 `ListView` 是一维的线性长河，那么 `GridView` 就是二维的矩阵世界。

无论是手机相册的缩略图、电商 App 的商品瀑布流，还是功能菜单的九宫格，都离不开 **网格布局**。

**本文你将学到**：
- `GridView.count` 与 `GridView.extent` 的区别
- 使用 `GridView.builder` 处理海量数据
- 自定义 `SliverGridDelegate` 实现复杂的异形网格
- **鸿蒙适配**：手机 vs 平板的响应式网格布局策略

---

## 一、GridView 基础构建

Flutter 提供了两个最常用的构造函数来快速创建网格。

### 1.1 固定列数：GridView.count

适用于你明确知道一行要放几个 Item 的场景（例如：不管是大屏还是小屏，我都只想要 3 列）。

```dart
GridView.count(
  crossAxisCount: 3, // 💡 核心：每行 3 个
  mainAxisSpacing: 10, // 行间距
  crossAxisSpacing: 10, // 列间距
  childAspectRatio: 1.0, // 子项宽高比 (1.0 = 正方形)
  padding: const EdgeInsets.all(10),
  children: List.generate(9, (index) {
    return Container(
      color: Colors.blue[100 * (index % 9 + 1)],
      child: Center(child: Text('Item $index')),
    );
  }),
)
```

### 1.2 固定宽度：GridView.extent

适用于你希望 Item 宽度固定，列数随屏幕宽度自动增加的场景（例如：每个 Item 必须是 150px 宽，屏幕越宽，一行放得越多）。

```dart
GridView.extent(
  maxCrossAxisExtent: 150, // 💡 核心：每个子项最大宽度 150
  mainAxisSpacing: 10,
  crossAxisSpacing: 10,
  children: [/* ... */],
)
```

---

## 二、高性能网格：GridView.builder

当你的数据量很大（比如 1000 张网络图片）时，直接用 `children: []` 列表会一次性创建所有 Widget，导致内存爆炸和卡顿。

这时必须使用 **懒加载** 的 `builder` 模式。

```dart
GridView.builder(
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 2, // 2 列
    childAspectRatio: 0.75, // 用于商品展示的长方形
  ),
  itemCount: 1000, // 数据总量
  itemBuilder: (context, index) {
    // 只有当这个 Item 滚动到屏幕可见区域时，才会执行此回调
    return Card(
      child: Column(
        children: [
          Expanded(child: Image.network('https://picsum.photos/200?random=$index')),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text('商品名称 $index'),
          ),
        ],
      ),
    );
  },
)
```

![Flutter GridView 懒加载机制原理图 (中文版)](./images/flutter_gridview_lazy_loading_concept_cn.png)

---

## 三、OpenHarmony 鸿蒙适配专题

### 3.1 响应式列数设计

OpenHarmony 生态中包含大量折叠屏和平板设备。如果我们在平板上还强制使用 `crossAxisCount: 2`，那么每个格子会被拉得非常宽，非常丑陋。

我们需要根据屏幕宽度动态决定列数。

✅ **最佳实践**：结合 `LayoutBuilder`。

```dart
class ResponsiveGrid extends StatelessWidget {
  const ResponsiveGrid({super.key});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        // 获取当前父容器的宽度
        double width = constraints.maxWidth;
        
        // 💡 策略：
        // < 600px (手机): 2 列
        // 600px - 1200px (折叠屏/平板): 4 列
        // > 1200px (桌面): 6 列
        int columns = 2;
        if (width >= 1200) {
          columns = 6;
        } else if (width >= 600) {
          columns = 4;
        }

        return GridView.builder(
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: columns, // 动态列数
            crossAxisSpacing: 10,
            mainAxisSpacing: 10,
          ),
          itemCount: 20,
          itemBuilder: (ctx, index) => _buildCard(index),
        );
      },
    );
  }
}
```

### 3.2 瀑布流布局 (Masonry)

`GridView` 目前只支持规则的网格（同一行的 Item 高度必须一致）。如果你想实现类似 Pinterest 或小红书那样的“瀑布流”（即 Item 高度参差不齐），官方组件做不到。

你需要引入社区神器：`flutter_staggered_grid_view`。

**pubspec.yaml**:
```yaml
dependencies:
  flutter_staggered_grid_view: ^0.7.0
```

代码示例：
```dart
MasonryGridView.count(
  crossAxisCount: 2,
  mainAxisSpacing: 4,
  crossAxisSpacing: 4,
  itemBuilder: (context, index) {
    return Container(
      // 高度随机，模拟不同比例的图片
      height: (index % 5 + 1) * 50.0, 
      color: Colors.teal[100 * (index % 9)],
      child: Center(child: Text('$index')),
    );
  },
)
```

---

## 四、实战：仿微信朋友圈九宫格

这是一个非常经典的面试题：
- 1 张图：显示大图
- 4 张图：显示 2x2 网格
- 9 张图：显示 3x3 网格

我们需要封装一个智能的 `NineGridWidget`。

```dart
class NineGridWidget extends StatelessWidget {
  final List<String> images; // 图片 URL 列表

  const NineGridWidget({super.key, required this.images});

  @override
  Widget build(BuildContext context) {
    int count = images.length;
    
    // 1. 单张图片处理
    if (count == 1) {
      return SizedBox(
        width: 200, 
        height: 200,
        child: Image.network(images[0], fit: BoxFit.cover),
      );
    }

    // 2. 计算列数 (4张图特殊处理为 2列，其他均为 3列)
    int crossAxisCount = (count == 4) ? 2 : 3;

    return GridView.builder(
      shrinkWrap: true, // 💡 关键：让 GridView 自适应内容高度
      physics: const NeverScrollableScrollPhysics(), // 禁止自身滚动，随父级滚动
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: crossAxisCount,
        mainAxisSpacing: 4,
        crossAxisSpacing: 4,
      ),
      itemCount: count,
      itemBuilder: (context, index) {
        return Image.network(images[index], fit: BoxFit.cover);
      },
    );
  }
}
```

---

## 五、总结

GridView 是展示集合数据的利器。

### 核心要点
1.  **选型**：数据少用 `GridView.count`，数据多用 `GridView.builder`。
2.  **交互**：在列表中嵌套 `GridView` 时，务必设置 `shrinkWrap: true` 和 `physics: NeverScrollableScrollPhysics`。
3.  **适配**：在鸿蒙大屏开发中，**不要写死列数**，请拥抱 `LayoutBuilder` 实现响应式设计。

### 下一篇预告
网格和列表虽然强大，但有时候我们需要更自由的布局，比如把文字放在图片上面，或者在一个角落挂一个“VIP”角标。
**《Flutter for OpenHarmony 实战之基础组件：第十三篇 Stack 与 Positioned 绝对定位》**
我们将学习如何脱离文档流，自由地从 Z 轴堆叠组件。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/12-gridview)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/12-gridview)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
