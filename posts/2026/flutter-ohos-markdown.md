# Flutter for OpenHarmony 实战：flutter_markdown — 高效渲染 Markdown 文本

## 前言

在现代移动应用开发中，Markdown 渲染是一个非常常见的需求。无论是用于显示应用的更新日志、用户协议，还是作为内容管理系统（CMS）的前端展示，Markdown 都以其轻量级和易读性成为了首选格式。

在 OpenHarmony 生态中，Flutter 的 `flutter_markdown` 库同样表现出色。它是一个纯 Dart 实现的 Markdown 渲染库，这意味着它不需要额外的原生代码适配即可在 OpenHarmony 设备上完美运行。

本文将详细介绍如何在 Flutter for OpenHarmony 项目中集成和使用 `flutter_markdown`，并演示如何自定义样式和处理点击事件。

## 一、核心组件解析

`flutter_markdown` 提供了两个核心组件来通过 Flutter 渲染 Markdown 内容：

### 1.1 `Markdown` 组件
这是一个包含滚动视图（ScrollView）的组件，适用于显示较长的 Markdown 文档。它会自动处理滚动，类似于 `ListView`。

### 1.2 `MarkdownBody` 组件
这是一个非滚动的组件，它会根据内容计算自身的高度。适用于将 Markdown 内容嵌入到其他滚动视图（如 `Column`, `ListView`）中的场景。

<!-- IMAGE_PLACEHOLDER: 概念架构图：Markdown 文本解析为 Flutter Widget 树的流程 -->
<!-- 类型: 示意图 -->
<!-- 内容: 展示 Markdown -> AST Nodes -> Widget Builder -> Rendering 的过程 -->

## 二、安装与基础使用

首先，我们需要在项目的 `pubspec.yaml` 中添加依赖：

```yaml
dependencies:
  flutter:
    sdk: flutter
  # 请检查 pub.dev 获取最新版本
  flutter_markdown: ^0.7.1
```

### 2.1 简单渲染

最基础的用法是直接传入 data 字符串：

```dart
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

class SimpleMarkdownPage extends StatelessWidget {
  const SimpleMarkdownPage({super.key});

  final String _markdownData = """
# 标题 H1
## 标题 H2

这是一段普通的文本，支持 **加粗** 和 *斜体*。

- 列表项 1
- 列表项 2

[点击访问 OpenHarmony 社区](https://openharmonycrossplatform.csdn.net)
""";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Markdown 基础示例')),
      body: Markdown(
        data: _markdownData,
        padding: const EdgeInsets.all(16.0),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 基础渲染效果 -->
<!-- 设备: 鸿蒙设备 -->
<!-- 内容: 展示上述代码在 OpenHarmony 手机上的渲染效果，包含标题和列表 -->

## 三、进阶定制

在实际业务中，默认的黑白样式往往无法满足设计需求。`flutter_markdown` 提供了强大的样式定制能力。

### 3.1 自定义样式表 (StyleSheet)

我们可以使用 `styleSheet` 属性来覆盖默认的文本样式。例如，修改 H1 的颜色和字体大小：

```dart
Markdown(
  data: data,
  styleSheet: MarkdownStyleSheet(
    h1: const TextStyle(
      color: Colors.blueAccent, 
      fontSize: 24, 
      fontWeight: FontWeight.bold
    ),
    p: const TextStyle(fontSize: 16, color: Colors.black87),
    blockquote: const TextStyle(color: Colors.grey),
    blockquoteDecoration: BoxDecoration(
      color: Colors.grey[100],
      border: const Border(left: BorderSide(color: Colors.blue, width: 4)),
    ),
  ),
)
```

### 3.2 处理图片与链接

`flutter_markdown` 默认支持网络图片（需配置网络权限），也支持通过 `imageBuilder` 自定义图片加载逻辑，或者通过 `onTapLink` 处理链接点击。

```dart
Markdown(
  data: "Hello [Flutter](https://flutter.dev)",
  onTapLink: (text, href, title) {
    // 在这里处理跳转，例如使用 url_launcher 或 go_router
    print('点击了链接: $href');
  },
  // 自定义图片构建器
  imageBuilder: (uri, title, alt) {
    return Image.network(
      uri.toString(),
      loadingBuilder: (ctx, child, progress) {
        if (progress == null) return child;
        return const CircularProgressIndicator();
      },
      errorBuilder: (ctx, error, stack) => const Icon(Icons.error),
    );
  },
)
```

## 四、OpenHarmony 平台适配

### 4.1 网络权限配置

如果你的 Markdown 内容中包含网络图片（如 `![](https://example.com/img.png)`），必须在 OpenHarmony 工程中声明网络权限。

打开 `entry/src/main/module.json5`，添加 `ohos.permission.INTERNET`：

```json5
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET"
      }
    ]
  }
}
```

### 4.2 性能优化建议

在 OpenHarmony 设备上渲染大量 Markdown 文本时，建议：

1.  **使用 `Markdown` 而非 `SingleChildScrollView` + `MarkdownBody`**：前者利用了懒加载机制，性能更佳。
2.  **图片缓存**：如果 Markdown 中包含大量高清图，建议结合 `cached_network_image` 在 `imageBuilder` 中进行缓存处理，避免滑动时重复下载导致的卡顿。

## 五、完整示例代码

下面是一个集成了样式定制、代码高亮（简单模拟）和链接处理的完整示例。

```dart
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

class MarkdownFullDemo extends StatelessWidget {
  const MarkdownFullDemo({super.key});

  @override
  Widget build(BuildContext context) {
    // 模拟一段富文本 Markdown 数据
    const String markdownContent = """
# Flutter for OpenHarmony

OpenHarmony 是由开放原子开源基金会（OpenAtom Foundation）孵化及运营的开源项目。

## 为什么选择 Flutter?

1. **跨平台**：一套代码，多端运行。
2. **高性能**：Skia/Impeller 渲染引擎。
3. **热重载**：极速开发体验。

## 代码示例

```dart
void main() {
  print('Hello OpenHarmony!');
}
```

> 💡 提示：确保配置了 `module.json5` 中的网络权限。

![OpenHarmony Logo](https://images.gitee.com/uploads/images/2021/1214/110542_8930c88a_9519623.png)
""";

    return Scaffold(
      appBar: AppBar(
        title: const Text('Markdown 渲染演示'),
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
      ),
      body: Markdown(
        data: markdownContent,
        selectable: true, // 允许长按复制文本
        padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 24.0),
        onTapLink: (text, href, title) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('即将跳转: $href')),
          );
        },
        styleSheet: MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
          h1: const TextStyle(color: Colors.deepPurple, fontSize: 26),
          h2: const TextStyle(color: Colors.deepPurpleAccent, fontSize: 22),
          code: const TextStyle(
            backgroundColor: Color(0xFFEEEEEE),
            fontFamily: 'monospace',
          ),
          blockquote: const TextStyle(color: Colors.grey, fontStyle: FontStyle.italic),
          blockquoteDecoration: BoxDecoration(
            color: Colors.blue.withOpacity(0.1),
            borderRadius: BorderRadius.circular(4),
            border: const Border(left: BorderSide(color: Colors.blue, width: 4)),
          ),
        ),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 完整示例运行截图 -->
<!-- 设备: 鸿蒙设备 -->
<!-- 内容: 展示包含高亮代码块、引用块和图片的完整渲染界面 -->

## 六、总结

`flutter_markdown` 是一个功能强大且易于使用的库，完美支持 OpenHarmony 平台。通过简单的配置和自定义，我们就可以在鸿蒙应用中优雅地展示富文本内容。

对于更复杂的需求（如 LaTeX 公式支持、复杂的 HTML 混排），可以考虑结合 `webview_flutter`（需确认 OHOS 适配进度）或其他 HTML 渲染库，但对于纯文档展示，`flutter_markdown` 无疑是最佳选择。

---

> 📦 完整代码已上传至 AtomGit：[open-harmony-examples/flutter_markdown_demo](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/flutter_markdown_demo)
>
> 🌐 欢迎加入开源鸿蒙跨平台社区：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
