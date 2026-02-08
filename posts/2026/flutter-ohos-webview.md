# Flutter for OpenHarmony 实战：webview_flutter — 混合开发核心

## 前言

在现代 App 开发中，混合开发（Hybrid Development）是一种非常流行的模式。通过将部分业务逻辑或展示页面使用 Web 技术（HTML/CSS/JS）实现，可以极大地提高开发效率和动态更新能力。每个成熟的 App 几乎都离不开 WebView。

在 Flutter 生态中，`webview_flutter` 是官方维护的首选插件。好消息是，该插件已经适配了 OpenHarmony 平台，基于系统原生的 ArkWeb 内核封装，性能优异且功能完备。

本文将带领大家在 OpenHarmony 项目中集成 `webview_flutter`，实现网页加载、JS 交互以及简单的导航控制。

## 一、核心组件与架构

`webview_flutter` 采用了“Platform View”的机制，将原生的 OpenHarmony WebView 组件嵌入到 Flutter 的 Widget 树中。

### 1.1 `WebViewController`
这是控制 WebView 的核心类。从 4.0 版本开始，API 发生了重大重构，不再通过 Widget 参数初始化，而是通过创建一个 `WebViewController` 实例来配置和管理 WebView。

### 1.2 `WebViewWidget`
这是一个纯展示用的 Widget，它接受一个 `WebViewController` 实例，负责在界面上渲染 WebView。

<!-- IMAGE_PLACEHOLDER: 架构图 -->
<!-- 内容: 展示 WebViewController 如何控制底层的 ArkWeb 实例 -->

## 二、安装与配置

### 2.1 添加依赖

在 `pubspec.yaml` 中添加：

```yaml
dependencies:
  flutter:
    sdk: flutter
  # 请务必检查 pub.dev 或 OpenHarmony 社区以获取适配 OHOS 的最新版本
  webview_flutter: ^4.7.0
```

> 💡 **提示**：如果官方版本尚未合并 OHOS 支持，请指向 OpenHarmony SIG 的仓库或使用 `webview_flutter_ohos`。

### 2.2 OpenHarmony 权限配置（必做）

WebView 加载网页属于网络操作，**必须**申请网络权限。打开 `entry/src/main/module.json5`：

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

此外，OpenHarmony 默认禁止明文流量（HTTP）。如果需要加载 HTTP 链接，需在 `module.json5` 中配置 `requestPermissions` 同级的 `metadata` 或查阅最新的网络安全配置指南（通常建议全站 HTTPS）。

## 三、基础用法：加载网页

### 3.1 初始化控制器

```dart
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class WebViewPage extends StatefulWidget {
  const WebViewPage({super.key});

  @override
  State<WebViewPage> createState() => _WebViewPageState();
}

class _WebViewPageState extends State<WebViewPage> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    // 1. 创建控制器
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted) // 允许执行 JS
      ..setBackgroundColor(const Color(0x00000000)) // 设置背景透明
      ..setNavigationDelegate(
        NavigationDelegate(
          onProgress: (int progress) {
            debugPrint('加载进度: $progress%');
          },
          onPageStarted: (String url) {
            debugPrint('开始加载: $url');
          },
          onPageFinished: (String url) {
            debugPrint('加载完成: $url');
          },
          onWebResourceError: (WebResourceError error) {
            debugPrint('加载错误: ${error.description}');
          },
        ),
      )
      ..loadRequest(Uri.parse('https://openharmony.cn')); // 加载目标 URL
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OpenHarmony 官网')),
      body: WebViewWidget(controller: _controller), // 2. 显示 WebView
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 网页加载效果截图 -->
<!-- 设备: 鸿蒙设备 -->
<!-- 内容: 在应用内显示 openharmony.cn 网页 -->

## 四、进阶用法：JS 交互

WebView 的强大之处在于原生代码与网页脚本的交互。

### 4.1 Flutter 调用 JS

使用 `runJavaScript` 或 `runJavaScriptReturningResult`：

```dart
// 修改网页标题
_controller.runJavaScript("document.title = 'Hello from Flutter!'");

//以此获取网页标题
var title = await _controller.runJavaScriptReturningResult("document.title");
print("当前标题: $title");
```

### 4.2 JS 调用 Flutter (JavaScriptChannels)

这是 H5 唤起原生功能的常用方式。例如，H5 点击按钮触发 Flutter 的 `SnackBar`。

1.  **配置 Channel**：

```dart
_controller.addJavaScriptChannel(
  'Toaster', // Channel 名称，JS 端通过 window.Toaster 访问
  onMessageReceived: (JavaScriptMessage message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('H5 传来的消息: ${message.message}')),
    );
  },
);
```

2.  **HTML端代码**：

```html
<button onclick="Toaster.postMessage('我是来自 H5 的问候');">点击我</button>
```

## 五、OpenHarmony 平台适配细节

### 5.1 软键盘遮挡问题

在混合开发中，输入框被键盘遮挡是常见痛点。OpenHarmony 版本的 `webview_flutter` 通常已处理了 Resize 逻辑。建议在 `Scaffold` 中设置 `resizeToAvoidBottomInset: true`（默认即为 true）。

### 5.2 视频全屏播放

如果网页包含 `<video>` 标签，全屏播放可能需要额外的配置。请关注相关 Issue 或确保正确处理了 `NavigationDelegate` 中的请求。

### 5.3 性能调优

*   **复用机制**：WebView 是重资源组件，尽量避免频繁创建和销毁。
*   **缓存**：合理利用 `clearCache` 和 `clearLocalStorage` 管理存储空间。

## 六、完整示例代码

本示例演示了一个带有加载进度条和 JS 交互功能的简易浏览器。

```dart
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class FullFeatureWebView extends StatefulWidget {
  const FullFeatureWebView({super.key});

  @override
  State<FullFeatureWebView> createState() => _FullFeatureWebViewState();
}

class _FullFeatureWebViewState extends State<FullFeatureWebView> {
  late final WebViewController _controller;
  double _progress = 0.0;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onProgress: (int progress) {
            setState(() {
              _progress = progress / 100;
            });
          },
          onPageStarted: (String url) {},
          onPageFinished: (String url) {},
          onWebResourceError: (WebResourceError error) {},
          onNavigationRequest: (NavigationRequest request) {
            if (request.url.startsWith('https://www.youtube.com/')) {
              debugPrint('拦截了跳转: ${request.url}');
              return NavigationDecision.prevent; // 拦截特定 URL
            }
            return NavigationDecision.navigate;
          },
        ),
      )
      ..addJavaScriptChannel(
        'OnHarmony',
        onMessageReceived: (message) {
          showDialog(
            context: context,
            builder: (ctx) => AlertDialog(
              title: const Text('JavaScript 消息'),
              content: Text(message.message),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(ctx),
                  child: const Text('关闭'),
                )
              ],
            ),
          );
        },
      )
      ..loadRequest(Uri.parse('https://flutter.dev'));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('OHOS WebView'),
        actions: [
          IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () async {
              if (await _controller.canGoBack()) {
                await _controller.goBack();
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => _controller.reload(),
          ),
        ],
      ),
      body: Column(
        children: [
          if (_progress < 1.0)
            LinearProgressIndicator(value: _progress, color: Colors.blue),
          Expanded(child: WebViewWidget(controller: _controller)),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.code),
        onPressed: () {
          _controller.runJavaScript(
              "OnHarmony.postMessage('当前的 URL 是: ' + window.location.href)");
        },
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 完整示例运行截图 -->
<!-- 内容: 顶部有进度条、AppBar有后退刷新按钮、内容区显示 Flutter 官网 -->

## 七、总结

`webview_flutter` 在 OpenHarmony 上的表现已经相当成熟，足以支撑大部分混合开发场景。通过掌握 `WebViewController` 的配置和 `JavaScriptChannel` 的使用，开发者可以轻松构建功能丰富的 Web 容器应用。

---

> 📦 完整代码已上传至 AtomGit：[open-harmony-examples/webview_demo](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/webview_demo)
>
> 🌐 欢迎加入开源鸿蒙跨平台社区：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
