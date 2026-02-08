![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第四篇 Text 文本组件全解

> **摘要**：文本是 App 中最基本的信息载体。本文深入解析 Flutter 中的 Text 组件，从基础样式到 RichText 富文本，再到自定义字体的加载。特别是针对 OpenHarmony 平台，我们将探讨字体渲染的适配以及如何实现高性能的富文本交互。

## 前言

在 Flutter for OpenHarmony 开发中，`Text` 组件看似简单，实则暗藏玄机。

你是否遇到过：
- 文字太长导致黄黑条溢出？
- 想给文字中间加个“点击链接”？
- UI 设计稿里的特殊艺术字体怎么还原？
- 中英文混排时的对齐问题？

**本文你将学到**：
- TextStyle 的全能样式控制
- 处理文本溢出 (Ellipsis) 的多种姿势
- RichText 富文本与 TextSpan 的嵌套艺术
- 实战：实现“用户协议”点击跳转与“展开全文”功能
- 鸿蒙应用中的自定义字体配置

---

## 一、Text 基础用法

### 1.1 核心样式 (TextStyle)

`TextStyle` 控制着文字的颜色、大小、粗细、行高等视觉属性。

```dart
Text(
  'Flutter for OpenHarmony',
  style: TextStyle(
    color: Colors.blue,             // 颜色
    fontSize: 24,                   // 字号 (逻辑像素)
    fontWeight: FontWeight.bold,    // 粗细 (w100 - w900)
    fontStyle: FontStyle.italic,    // 斜体
    letterSpacing: 1.5,             // 字间距
    wordSpacing: 4.0,               // 单词间距
    height: 1.5,                    // 行高倍率 (fontSize * height)
    decoration: TextDecoration.underline, // 下划线
    decorationStyle: TextDecorationStyle.dashed, // 虚线
  ),
)
```

### 1.2 对齐与溢出处理

当文字内容超过容器宽度时，我们需要决定它是换行、截断还是缩放。

```dart
Container(
  width: 200,
  color: Colors.grey[200],
  child: const Text(
    '这是一段非常非常长的测试文本，它肯定会超过容器的宽度，我们需要截断它。',
    textAlign: TextAlign.justify,   // 两端对齐
    maxLines: 2,                    // 最多显示 2 行
    overflow: TextOverflow.ellipsis,// 超出显示省略号 (...)
    softWrap: true,                 // 允许自动换行
  ),
)
```

**TextOverflow 选项**：
- `clip`: 直接切断（默认，可能把字切一半）。
- `fade`: 渐变消失。
- `ellipsis`: 显示省略号 (...)。
- `visible`: 强制渲染出界（通常不推荐）。

---

## 二、RichText 富文本

如果一行文字中需要不同的样式（例如：**加粗**的标题和普通的正文，或者红色的价格），就不能只用一个 `Text` 组件了。

### 2.1 Text.rich 构造函数

Flutter 推荐使用 `Text.rich` 或 `RichText` 组件，它们通过 `TextSpan` 树来构建内容。

```dart
const Text.rich(
  TextSpan(
    text: '总计: ',
    style: TextStyle(color: Colors.black, fontSize: 16),
    children: [
      TextSpan(
        text: '¥',
        style: TextStyle(color: Colors.red, fontSize: 14),
      ),
      TextSpan(
        text: '199',
        style: TextStyle(
          color: Colors.red,
          fontSize: 24, 
          fontWeight: FontWeight.bold,
        ),
      ),
      TextSpan(
        text: '.00',
        style: TextStyle(color: Colors.red, fontSize: 14),
      ),
    ],
  ),
)
```

<!-- IMAGE_PLACEHOLDER: 价格富文本展示 -->
<!-- 类型: 示例截图 -->
<!-- 内容: 展示"总计: ¥199.00"，其中数字特别大且为红色 -->

---

## 三、实战案例 1：可点击的用户协议

登录页面常见的需求：
"登录即代表同意《用户协议》和《隐私政策》"

这里的协议名称需要高亮并可点击。

```dart
import 'package:flutter/gestures.dart'; // 必须导入

class PrivacyAgreement extends StatelessWidget {
  const PrivacyAgreement({super.key});

  @override
  Widget build(BuildContext context) {
    return Text.rich(
      TextSpan(
        text: '登录即代表同意',
        style: const TextStyle(color: Colors.grey),
        children: [
          TextSpan(
            text: '《用户协议》',
            style: const TextStyle(color: Colors.blue),
            // 添加点击事件
            recognizer: TapGestureRecognizer()
              ..onTap = () {
                print('点击了用户协议');
                // TODO: 跳转到协议详情页
              },
          ),
          const TextSpan(
            text: '和',
            style: TextStyle(color: Colors.grey),
          ),
          TextSpan(
            text: '《隐私政策》',
            style: const TextStyle(color: Colors.blue),
            recognizer: TapGestureRecognizer()
              ..onTap = () {
                print('点击了隐私政策');
              },
          ),
        ],
      ),
    );
  }
}
```

⚠️ **注意**：使用 `TapGestureRecognizer` 后，记得它是需要手动销毁的吗？在 `StatelessWidget` 中这样写通常没问题，但在 `StatefulWidget` 中如果是在 `build` 外创建，需要在 `dispose` 中处理。

---

## 四、实战案例 2：展开/收起全文

实现一个带状态的文本组件，控制长文本的显示行数。

```dart
class ExpandableText extends StatefulWidget {
  final String text;
  final int maxLines;

  const ExpandableText({
    super.key, 
    required this.text, 
    this.maxLines = 3,
  });

  @override
  State<ExpandableText> createState() => _ExpandableTextState();
}

class _ExpandableTextState extends State<ExpandableText> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          widget.text,
          // 根据状态决定是否限制行数
          maxLines: _isExpanded ? null : widget.maxLines,
          overflow: _isExpanded ? TextOverflow.visible : TextOverflow.ellipsis,
          style: const TextStyle(fontSize: 16, height: 1.5),
        ),
        GestureDetector(
          onTap: () {
            setState(() {
              _isExpanded = !_isExpanded;
            });
          },
          child: Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Text(
              _isExpanded ? '收起' : '展开全文',
              style: const TextStyle(
                color: Colors.blue,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      ],
    );
  }
}
```

---

## 五、鸿蒙应用中的字体适配

### 5.1 使用自定义字体

想要应用更有个性，通常会引入 `.ttf` 或 `.otf` 字体文件。

1.  **添加文件**：将字体文件放入项目的 `assets/fonts/` 目录（需手动创建）。
2.  **配置 pubspec.yaml**：

```yaml
flutter:
  fonts:
    - family: HarmonyOS_Sans
      fonts:
        - asset: assets/fonts/HarmonyOS_Sans_Bold.ttf
          weight: 700
        - asset: assets/fonts/HarmonyOS_Sans_Regular.ttf
          weight: 400
```

3.  **在代码中使用**：

```dart
Text(
  '鸿蒙字体演示',
  style: TextStyle(
    fontFamily: 'HarmonyOS_Sans', // 对应 yaml 中的 family
    fontSize: 20,
  ),
)
```

### 5.2 全局字体配置

为了避免在每个 Text 中都写 `fontFamily`，我们可以在 `MaterialApp` 的主题中全局配置。

```dart
MaterialApp(
  theme: ThemeData(
    fontFamily: 'HarmonyOS_Sans', // 全局生效
    textTheme: const TextTheme(
      displayLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
      bodyMedium: TextStyle(fontSize: 16),
    ),
  ),
  home: const MyHomePage(),
);
```

### 5.3 鸿蒙系统字体特性

OpenHarmony 系统自带了 **HarmonyOS Sans** 字体，它针对多终端阅读进行了优化。

> **提示**：目前 Flutter for OpenHarmony 会尝试调用系统的默认字体回退机制。如果遇到中文显示为“豆腐块”（乱码），通常是因为未正确加载中文字体，建议在发布 App 时内置一套开源中文字体（如 Noto Sans SC）以保证 100% 的兼容性。

---

## 六、特殊效果：阴影与描边

有时候为了艺术效果，我们需要给文字加阴影或描边。

```dart
Text(
  'ART TEXT',
  style: TextStyle(
    fontSize: 40,
    fontWeight: FontWeight.w900,
    color: Colors.white,
    // 描边效果：通过 shadow 模拟，或者使用 Stack 堆叠
    shadows: [
      Shadow(
        blurRadius: 10.0,
        color: Colors.blue.withOpacity(0.5),
        offset: const Offset(5.0, 5.0),
      ),
      // 描边模拟
      const Shadow(
        offset: Offset(-1.5, -1.5),
        color: Colors.black,
      ),
      const Shadow(
        offset: Offset(1.5, -1.5),
        color: Colors.black,
      ),
      const Shadow(
        offset: Offset(1.5, 1.5),
        color: Colors.black,
      ),
      const Shadow(
        offset: Offset(-1.5, 1.5),
        color: Colors.black,
      ),
    ],
  ),
)
```

---

## 七、总结

Text 组件虽然基础，但它是用户获取信息最直接的窗口。

### 核心知识点

1.  **截断**：长文本务必考虑 `maxLines` 和 `overflow`。
2.  **富文本**：`TextSpan` 是实现混排和点击事件的神器。
3.  **字体**：全局配置 `fontFamily` 可以统一 App 风格。
4.  **交互**：利用 `GestureDetector` 或 `TapGestureRecognizer` 让文字“活”起来。

### 下一篇预告

有了文字、有了布局，我们的 App 还需要更丰富的内容形式。
**《Flutter for OpenHarmony 实战之基础组件：第五篇 Image 图片组件与资源管理》**
下一篇我们将深入探讨图片的加载（本地/网络）、缓存机制、占位图处理以及如何在 OpenHarmony 中适配不同分辨率的图片资源。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/4-text)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/4-text)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
