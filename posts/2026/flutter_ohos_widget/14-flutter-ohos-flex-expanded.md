![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第十四篇 Expanded, Flexible 与 Spacer 弹性布局

> **摘要**：在 UI 开发中，固定尺寸的组件往往无法通过不同屏幕的考验。为了让界面能像弹簧一样伸缩自如，我们需要掌握 Flutter 的弹性布局三剑客：Expanded（强制撑满）、Flexible（松散自适应）和 Spacer（留白占位）。本文将通过大量对比案例，彻底根治 RenderFlex overflowed 这一常见顽疾。

## 前言

如果你是 Flutter 新手，你一定遇到过那个令人抓狂的黑黄条纹警告：
`Bottom overflowed by 20 pixels`.

这通常意味着你的组件尺寸超出了屏幕边界。在 Row 或 Column 中，子组件默认是“能占多大就占多大”或者“固定多大就多大”。

如果我们需要实现：
- 左边图片固定宽，右边文字**自动填满剩余空间**？
- 上中下三块区域，按照 **1:2:1** 的比例分配高度？

这时，弹性布局（Flex Layout）就是唯一的救星。

**本文你将学到**：
- `Expanded` vs `Flexible` 的核心区别
- `flex` 系数的数学原理 (2:1 比例怎么写)
- `Spacer`：最优雅的留白方式
- **鸿蒙适配**：利用 Flex 实现平板上的左右分栏布局

---

## 一、三剑客详解

这三个组件都**必须**用在 `Row`、`Column` 或 `Flex` 的直系子级中，否则会报错。

### 1.1 Expanded：霸道总裁 (强制撑满)

`Expanded` 会强迫子组件**占满所有剩余空间**。无论子组件自己想要多宽，都会被忽略，直接拉伸。

```dart
Row(
  children: [
    Container(width: 50, color: Colors.blue), // 固定宽
    Expanded(
      child: Container(color: Colors.green), // 💡 霸占剩下的所有宽度
    ),
    Container(width: 50, color: Colors.blue), // 固定宽
  ],
)
```

### 1.2 Flexible：佛系青年 (自适应)

`Flexible` 也会让子组件占满剩余空间，但它有一个 `fit` 属性：
- `FlexFit.loose` (默认)：如果子组件本身很小（比如只有 10px），那就**只占 10px**，剩下的空间空着。
- `FlexFit.tight`：等同于 Expanded，强迫撑满。

**场景对比**：
当你想让一段长文字自动换行而不溢出屏幕时，用 `Expanded` 或 `Flexible` 均可（通常用 Expanded）。

### 1.3 Spacer：透明空气 (占位)

`Spacer` 本质上就是一个空的 `Expanded`。它专门用来在组件之间制造弹性的空白。

```dart
Row(
  children: [
    Text('标题'),
    Spacer(), // 💡 自动把标题顶到左边，按钮顶到右边
    ElevatedButton(onPressed: (){}, child: Text('更多')),
  ],
)
```

![Flutter Flex 弹性布局原理图 (中文版)](./images/flutter_flex_layout_concept_cn.png)

---

## 二、Flex 系数：比例的艺术

如果有多个弹性组件，如何分配空间？通过 `flex` 属性（整数）。默认是 1。

**案例：黄金比例分割**

```dart
Column(
  children: [
    Expanded(
      flex: 1, // 占 1/3
      child: Container(color: Colors.red),
    ),
    Expanded(
      flex: 2, // 占 2/3
      child: Container(color: Colors.blue),
    ),
  ],
)
```

原理：系统会把所有 flex 值相加 (1+2=3)，然后按份数分配。

---

## 三、OpenHarmony 鸿蒙适配专题

### 3.1 左右分栏布局 (Master-Detail UI)

在鸿蒙平板或折叠屏上，常见的布局是：左侧导航栏（固定宽度），右侧内容区（自适应撑满）。

这种经典的布局结构，正是 `Row` + `Expanded` 的最佳舞台。

```dart
class TabletLayout extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          // 1. 左侧侧边栏：固定宽度 250
          Container(
            width: 250,
            color: Colors.grey[200],
            child: ListView(children: [/* 菜单项 */]),
          ),
          
          // 2. 右侧内容区：自适应撑满
          Expanded(
            child: Container(
              color: Colors.white,
              child: Center(child: Text('详细内容区域')),
            ),
          ),
        ],
      ),
    );
  }
}
```

---

## 四、实战：仿“微信朋友圈”条目布局

朋友圈的一条动态包含：头像、昵称、内容、图片、时间、点赞按钮。这是一个非常复杂的嵌套布局。

**难点**：时间在左，点赞按钮在右，且中间距离不固定。

```dart
Row(
  crossAxisAlignment: CrossAxisAlignment.start, // 顶部对齐
  children: [
    // 1. 头像 (固定)
    Container(
      width: 44, height: 44,
      decoration: BoxDecoration(color: Colors.grey, borderRadius: BorderRadius.circular(4)),
    ),
    SizedBox(width: 10),
    
    // 2.右侧内容区域 (自适应撑满)
    Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('微信昵称', style: TextStyle(color: Colors.blue, fontWeight: FontWeight.bold)),
          SizedBox(height: 4),
          Text('今天天气真不错，Flutter 布局真好用！', style: TextStyle(fontSize: 15)),
          SizedBox(height: 10),
          
          // 底部栏：时间 + Spacer + 点赞
          Row(
            children: [
              Text('1小时前', style: TextStyle(fontSize: 12, color: Colors.grey)),
              Spacer(), // 💡 自动挤开中间空间
              Icon(Icons.more_horiz, color: Colors.blueGrey),
            ],
          ),
        ],
      ),
    ),
  ],
)
```

---

## 五、总结

弹性布局是解决屏幕适配问题的银弹。

### 核心要点
1.  **原则**：在 `Row`/`Column` 里，只要子组件宽度/高度不确定，就包一层 `Expanded`。
2.  **比例**：用 `flex` 属性轻松实现 1:1, 1:2 等比例分割。
3.  **留白**：用 `Spacer` 代替 `MainAxisAlignment.spaceBetween`，代码更具可读性。
4.  **警告**：千万别在 `Expanded` 外部再包 `Container` 限制宽高，这会破坏弹性机制。

### 下一篇预告
终于讲完了这些基础的“方块”组件。接下来，我们将把前面学到的所有 14 篇知识融会贯通，来一场激动人心的**大练兵**！
**《Flutter for OpenHarmony 实战之基础组件：第十五篇 综合案例 —— 打造高颜值“个人中心”页》**
我们将从零开始，手写一个包含头像、波浪背景、功能列表的完整页面，为基础篇画上完美的句号。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/14-flex-expanded)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/14-flex-expanded)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
