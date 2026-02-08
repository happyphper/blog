![Flutter for OpenHarmony 实战：CustomScrollView 与 Slivers](./images/18-slivers.png)

# Flutter for OpenHarmony 实战之基础组件：第十八篇 布局终极者 CustomScrollView 与 Slivers

> **摘要**：如果你想打造一个像“京东/淘宝”首页那样：头部会随滑动缩小并吸顶、中间是横向滑动的广告位、底部是瀑布流列表，且整个页面共用一个顺滑的滚动条。那么普通的 `ListView` 就力不从心了。今天，我们将掌握 Flutter 滚动布局的顶峰 —— `Slivers` 体系。

## 前言

在 Flutter 中，`ListView` 实际上是一个封装好的便捷组件，但它有一个局限性：它只能包含一种滚动模式。

当页面结构变得复杂（例如：一部分是网格 Grid，一部分是列表 List，还有一个高度会变化的吸顶头部 AppBar），我们就需要使用 `CustomScrollView`。

在 `CustomScrollView` 中，所有的子组件都不再是普通的 `Widget`，而是 `Sliver`（意为“碎片/薄片”）。`Sliver` 具有特殊的本领：它们能在滚动过程中，精确地告诉父容器自己还有多少部分可见，从而实现极其复杂的联动动效。

**本文你将学到**：
- `CustomScrollView` 的基本骨架
- `SliverAppBar` 的高级用法（吸顶、伸缩背景）
- 如何在同一个页面混合 `SliverList` 与 `SliverGrid`
- 适配 OpenHarmony 的“沉浸式”头部窗口设计
- 实战：模仿主流电商 App 的“商详页”布局

---

## 一、Sliver 体系的核心组件

### 1.1 CustomScrollView：碎片的容器
它是所有 `Sliver` 的父节点。

### 1.2 SliverAppBar：会变魔术的顶栏
这是 `CustomScrollView` 最强大的排头兵。
- `floating`: 向下滑动时顶栏是否立即出现。
- `pinned`: 滚动到顶时是否吸顶。
- `expandedHeight`: 展开时的最大高度。

### 1.3 SliverList / SliverGrid
对应 `ListView` 和 `GridView` 的 Sliver 版本。

---

## 二、基础代码结构

```dart
CustomScrollView(
  slivers: [
    // 1. 吸顶顶栏
    SliverAppBar(
      pinned: true,
      expandedHeight: 200.0,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('鸿蒙精选'),
        background: Image.network('...', fit: BoxFit.cover),
      ),
    ),
    
    // 2. 网格区域
    SliverGrid(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        mainAxisSpacing: 10,
        crossAxisSpacing: 10,
      ),
      delegate: SliverChildBuilderDelegate(
        (context, index) => Container(color: Colors.orange[100 * (index % 9)]),
        childCount: 10,
      ),
    ),
    
    // 3. 列表区域
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => ListTile(title: Text('资讯条目 $index')),
        childCount: 20,
      ),
    ),
  ],
)
```

---

## 三、进阶：SliverPersistentHeader 吸顶工具

如果你想让页面中间的某个组件（比如“分类筛选栏”）在滑到顶部时也吸顶，可以使用 `SliverPersistentHeader`。

它需要一个 `SliverPersistentHeaderDelegate` 来描述吸顶时的最大和最小高度。

```dart
class MyHeaderDelegate extends SliverPersistentHeaderDelegate {
  @override
  Widget build(BuildContext context, double shrinkOffset, bool overlapsContent) {
    return Container(
      color: Colors.white,
      alignment: Alignment.center,
      child: const Text('💡 我是吸顶筛选栏'),
    );
  }

  @override
  double get maxExtent => 50.0; // 展开高度

  @override
  double get minExtent => 50.0; // 吸顶高度

  @override
  bool shouldRebuild(oldDelegate) => false;
}
```

---

## 四、OpenHarmony 平台适配：沉浸式体验

在鸿蒙系统中，我们追求“沉浸式”视觉，即应用的背景色能延伸到系统的状态栏（刘海区域）。

### 4.1 配合 SliverAppBar 实现沉浸式
当我们使用 `SliverAppBar` 时，系统会自动处理大部分状态栏的显示。但在鸿蒙上，我们需要注意：

1. **设置状态栏透明**：
   ```dart
   SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
     statusBarColor: Colors.transparent, // 设置状态栏透明
   ));
   ```

2. **活用 FlexibleSpaceBar**：
   在鸿蒙平板等大尺寸设备上，`expandedHeight` 可以设置得更有视觉冲击力。

![SliverAppBar 沉浸式吸顶效果演示](./images/18-slivers.png)
> **图 1**：利用 SliverAppBar 实现背景图片延伸至状态栏的沉浸式视觉效果，并在滚动时自动收起吸顶。

---

## 五、实战：商详页混合布局

我们来实现一个典型的“商品详情页”雏形。

```dart
class OhosProductDetail extends StatelessWidget {
  const OhosProductDetail({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          // 1. 商品图片大图 + 吸顶按钮
          SliverAppBar(
            pinned: true,
            expandedHeight: 350.0,
            backgroundColor: Colors.white,
            elevation: 0,
            leading: const Icon(Icons.arrow_back_ios, color: Colors.black),
            actions: [const Icon(Icons.share, color: Colors.black), const SizedBox(width: 16)],
            flexibleSpace: FlexibleSpaceBar(
              background: Image.network('https://images.unsplash.com/photo-1542291026-7eec264c27ff', fit: BoxFit.cover),
            ),
          ),
          
          // 2. 商品标题区 (SliverToBoxAdapter 可以把普通 Widget 转为 Sliver)
          const SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('鸿蒙智联 运动跑鞋', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  SizedBox(height: 8),
                  Text('¥ 599.00', style: TextStyle(fontSize: 20, color: Colors.orange)),
                ],
              ),
            ),
          ),
          
          // 3. 吸顶参数切换栏
          SliverPersistentHeader(
            pinned: true,
            delegate: _SliverHeaderDelegate(
              child: Container(
                color: Colors.grey[100],
                child: const TabBar(
                  tabs: [Tab(text: "介绍"), Tab(text: "规格"), Tab(text: "评论")],
                  labelColor: Colors.blue,
                ),
              ),
            ),
          ),
          
          // 4. 详情内容长列表
          SliverList(
            delegate: SliverChildBuilderDelegate(
              (context, index) => Container(
                height: 200,
                margin: const EdgeInsets.all(16),
                color: Colors.blue[50 * (index % 9 + 1)],
                child: Center(child: Text('商品详情图 $index')),
              ),
              childCount: 10,
            ),
          ),
        ],
      ),
    );
  }
}
```

---

## 六、总结

`Slivers` 是 Flutter 布局中最高级的一环，它赋予了我们“像素级”控制滚动的能力。

### 核心要点：
1. **CustomScrollView**：作为入口，承载所有 Sliver。
2. **SliverAppBar**：实现炫酷的顶栏缩放和吸顶。
3. **SliverToBoxAdapter**：这是“黏合剂”，让你可以把任何普通的 Container、Column 扔进 Sliver 列表里。
4. **适配思维**：针对鸿蒙多设备，利用 `SliverAppBar` 的伸缩特性，在手机端保持精简，在平板端展示更丰富的 Banner 视野。

### 下一篇预告
页面的功能架子搭好了，但现在看起来依然很单调。我们要如何给应用增加一点“质感”？比如像卡片一样的分块、带阴影的漂浮感、以及点击时的水波纹反馈。
**《Flutter for OpenHarmony 实战之基础组件：第十九篇 质感布局 Card 与交互水波纹》**
让我们把 UI 做得更精致！

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/18-slivers)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/18-slivers)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
