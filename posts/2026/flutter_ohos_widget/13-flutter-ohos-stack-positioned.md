![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第十三篇 Stack 与 Positioned 绝对定位详解

> **摘要**：在 Flutter 的布局世界里，Row 和 Column 负责二维平面的线性排列，而 Stack 则赋予了我们 Z 轴堆叠的能力。本文将深度解析 Stack 与 Positioned 的配合艺术，从简单的角标实现到全屏背景布局，并探讨其在 OpenHarmony 沉浸式 UI 设计中的关键作用。

## 前言

试想一下，如果你想在一张用户头像的右上角放一个红色的小圆点（消息红点），或者在一张海报图片的左上角贴一个“VIP”标签，用 `Row` 或 `Column` 能实现吗？

很难。因为这些需求本质上是 **由下而上** 的层叠关系，而不是 **由左及右** 或 **由上及下** 的排列关系。

**Stack** 就是为此而生的。它允许我们将组件像图层（Layer）一样叠加在一起。

**本文你将学到**：
- `Stack` 的绘制顺序与对齐策略
- `Positioned` 四个方位的定位逻辑
- `StackFit.expand` 撑满全屏的妙用
- **鸿蒙适配**：利用 Stack 实现自定义的沉浸式导航栏背景

---

## 一、Stack：Z 轴的魔法

`Stack` 的布局逻辑非常简单：**先添加的在底下，后添加的在上面**（Painter's Algorithm）。

### 1.1 基础对齐 (Alignment)

如果不使用定位组件，`Stack` 里的子组件默认会根据 `alignment` 属性堆在一起。

```dart
Stack(
  alignment: Alignment.center, // 💡 所有子组件居中堆叠
  children: [
    Container(width: 200, height: 200, color: Colors.blue), // 底层：大蓝块
    Container(width: 150, height: 150, color: Colors.green), // 中层：中绿块
    Container(width: 100, height: 100, color: Colors.red),   // 顶层：小红块
  ],
)
```

### 1.2 撑满与松散 (StackFit)

很多时候，我们希望底层的背景图能自动撑满整个父容器，而不是由图片原本的大小决定。这时就需要调整 `fit` 属性。

*   `StackFit.loose` (默认)：子组件多大就多大。
*   `StackFit.expand`：强迫所有**没有定位**的子组件撑满 Stack 的最大空间。

```dart
Stack(
  fit: StackFit.expand, // 💡 强迫子组件撑满
  children: [
    Image.asset('assets/bg.jpg', fit: BoxFit.cover), // 这张图会自动铺满全屏
    Center(child: Text('登录')), // 顶层内容
  ],
)
```

![Flutter Stack 层叠布局原理图 (中文版)](./images/flutter_stack_concept_cn.png)

---

## 二、Positioned：绝对定位

在 `Stack` 内部，我们可以用 `Positioned` 包裹子组件，来精确控制它离上下左右边缘的距离。

**核心规则**：
*   指定 `left` + `width` = 确定横向位置
*   指定 `left` + `right` = 强迫横向拉伸（常用！）
*   如果不包裹 `Positioned`，组件遵循 `Stack.alignment`。

### 2.1 案例：消息红点 (Badge)

```dart
Stack(
  clipBehavior: Clip.none, // 💡 允许子组件超出边界 (画红点时常用)
  children: [
    Icon(Icons.notifications, size: 40),
    Positioned(
      right: -2, // 往右偏出一点
      top: -2,   // 往上偏出一点
      child: Container(
        padding: EdgeInsets.all(4),
        decoration: BoxDecoration(
          color: Colors.red,
          shape: BoxShape.circle,
        ),
        child: Text('9', style: TextStyle(color: Colors.white, fontSize: 10)),
      ),
    ),
  ],
)
```

### 2.2 案例：底部固定的按钮栏

```dart
Stack(
  children: [
    // 底部内容
    ListView(...),
    
    // 悬浮在底部的按钮
    Positioned(
      left: 0,
      right: 0, // 💡 左右都设为 0，相当于 width: double.infinity
      bottom: 0,
      child: Container(
        height: 60,
        color: Colors.white,
        child: ElevatedButton(onPressed: (){}, child: Text('提交')),
      ),
    ),
  ],
)
```

---

## 三、OpenHarmony 鸿蒙适配专题

### 3.1 自定义沉浸式导航栏

在原生鸿蒙开发中，如果想要一个背景是一张图片扩展到状态栏（Status Bar）区域的效果，通常需要复杂的 Window 设置。在 Flutter 中，利用 `Stack` 可以轻松实现。

如果你的 App 设计图要求导航栏背景不是纯色，而是和 Body 背景融为一体的渐变色或图片：

```dart
class ImmersivePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true, // 💡 让 Body 延伸到 AppBar 后面
      appBar: AppBar(
        backgroundColor: Colors.transparent, // 必须透明
        elevation: 0,
        title: Text('沉浸式页面'),
      ),
      body: Stack(
        fit: StackFit.expand, // 撑满屏幕
        children: [
          // 1. 底层：全屏背景图 (覆盖状态栏)
          Image.asset(
            'assets/harmony_bg.jpg', 
            fit: BoxFit.cover,
          ),
          
          // 2. 顶层：与安全区域避让的内容
          SafeArea(
            child: Center(
              child: Text('内容显示在安全区域内'),
            ),
          ),
        ],
      ),
    );
  }
}
```

### 3.2 鸿蒙原子化服务卡片 (Service Widget)

虽然目前我们主要讲 App 开发，但鸿蒙的特色是**服务卡片**。服务卡片的布局能力有限，但 **Stack + Positioned** 依然是卡片布局的核心手段之一（例如：在卡片左下角显示天气温度，右上角显示更新时间）。

掌握好 Stack 布局，未来迁移或开发鸿蒙原生卡片时会非常顺手。

---

## 四、实战：封装一个 "VIP" 专属头像组件

这是一个非常通用的需求：头像本身是圆的，但右下角要压一个“V”字认证标，底部稍微有一点重叠。

```dart
class VipAvatar extends StatelessWidget {
  final String imageUrl;
  final bool isVip;

  const VipAvatar({
    super.key,
    required this.imageUrl,
    this.isVip = false,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 80,
      height: 80,
      child: Stack(
        children: [
          // 1. 头像本体
          Positioned.fill(
            child: CircleAvatar(
              backgroundImage: NetworkImage(imageUrl),
            ),
          ),
          
          // 2. VIP 标识 (仅 VIP 显示)
          if (isVip)
            Positioned(
              right: 0,
              bottom: 0,
              child: Container(
                padding: const EdgeInsets.all(2),
                decoration: const BoxDecoration(
                  color: Colors.white, // 白边
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.verified, 
                  color: Colors.blue, 
                  size: 20,
                ),
              ),
            ),
        ],
      ),
    );
  }
}
```

---

## 五、总结

Stack 打破了线性布局的桎梏，让我们拥有了“图层”的概念。

### 核心要点
1.  **顺序**：代码在前的在底下，代码在后的在上面。
2.  **定位**：用 `Positioned` 精确控制位置；如果不加 Positioned，默认居中或通过 alignment 控制。
3.  **约束**：想做全屏背景？请毫不犹豫地使用 `StackFit.expand`。
4.  **鸿蒙**：配合 `Scaffold.extendBodyBehindAppBar`，Stack 是实现沉浸式视觉的最佳搭档。

### 下一篇预告
到目前为止，我们组件的大小都是“固定的”或者“自适应的”。如果我想把屏幕垂直切成两半，上面占 1/3，下面占 2/3，该怎么写？
**《Flutter for OpenHarmony 实战之基础组件：第十四篇 Expanded, Flexible 与 Spacer 弹性布局》**
我们将深入 Flex 布局的核心，彻底解决 `RenderFlex overflowed` 的噩梦。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/13-stack-positioned)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/13-stack-positioned)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
