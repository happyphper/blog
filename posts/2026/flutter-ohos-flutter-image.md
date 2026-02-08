# Flutter for OpenHarmony 实战：flutter_image — 增强型图片加载与缓存

## 前言

在移动应用开发中，图片加载是极其常见的场景。虽然 Flutter 原生的 `Image.network` 已经非常易用，但在网络环境不稳定的情况下（如若网、断网重连），原生的加载方式往往缺乏自动重试机制，导致用户体验不佳。

`flutter_image` 是由 Flutter 官方团队维护的一个实用库，它提供了一些增强的图片提供者（Image Provider），其中最核心的就是 `NetworkImageWithRetry`。它能够自动处理网络请求失败的情况并进行指数退避重试，非常适合 OpenHarmony 应用在复杂网络环境下的图片展示。

本文将介绍如何在 OpenHarmony 上安装和使用 `flutter_image`，并重点讲解权限配置。

## 一、核心功能

### 1.1 `NetworkImageWithRetry`
这是该库的主力功能。当图片下载失败时，它不会立即报错，而是会尝试重新下载。重试策略通常是指数级的（例如等待 1秒、2秒、4秒...），直到成功或达到最大重试次数。

### 1.2 `FadeInImage` 的完美搭档
虽然 Flutter 自带 `FadeInImage`，但结合 `NetworkImageWithRetry` 可以确保即使图片首次加载失败，用户也能在重试成功后平滑地看到图片，而不是一直对着占位图。

<!-- IMAGE_PLACEHOLDER: 流程图 -->
<!-- 内容: 描述 NetworkImageWithRetry 的内部逻辑：Request -> Fail -> Wait -> Retry -> Success -->

## 二、安装与配置

### 2.1 添加依赖

在 `pubspec.yaml` 中添加：

```yaml
dependencies:
  flutter:
    sdk: flutter
  # 请检查 pub.dev 获取最新版本
  flutter_image: ^4.1.0
```

### 2.2 OpenHarmony 权限配置（关键）

**⚠️ 注意**：这是 OpenHarmony 开发中最容易被忽略的一步。默认情况下，应用没有访问互联网的权限。如果缺少此配置，所有网络图片都将加载失败！

请确保 `entry/src/main/module.json5` 文件中包含 `ohos.permission.INTERNET`：

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

## 三、基础用法

### 3.1 使用 `NetworkImageWithRetry`

将原生的 `NetworkImage` 替换为 `NetworkImageWithRetry` 即可：

```dart
import 'package:flutter/material.dart';
import 'package:flutter_image/network.dart'; // 必须导入此文件

class ImageRetryPage extends StatelessWidget {
  const ImageRetryPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('自动重试图片加载')),
      body: Center(
        child: Image(
          image: NetworkImageWithRetry(
            'https://flutter.github.io/assets-for-api-docs/assets/widgets/owl.jpg',
            // 可选：自定义 fetch 策略，通常默认即可
          ),
          width: 300,
          height: 300,
          fit: BoxFit.cover,
        ),
      ),
    );
  }
}
```

### 3.2 结合 Avatar 使用

该库还经常用于头像显示，因为它能很好地处理加载过程中的占位。

```dart
CircleAvatar(
  radius: 50,
  backgroundImage: NetworkImageWithRetry(
    'https://example.com/user_avatar.jpg',
  ),
  onBackgroundImageError: (exception, stackTrace) {
    // 即使重试多次后依然失败，可以在这里处理
    print('图片彻底加载失败');
  },
  child: const Icon(Icons.person), // 加载失败或加载中显示的图标
)
```

## 四、OpenHarmony 平台适配与最佳实践

### 4.1 缓存策略说明

需要注意的是，`flutter_image` 主要侧重于 **加载机制（重试）**，而不是 **持久化缓存**。在 OpenHarmony 上，如果你的应用需要将大量图片缓存到本地磁盘（Disk Cache），以便下次冷启动时无需联网即可显示，建议配合 `cached_network_image` 使用，或者自行实现本地文件缓存逻辑。

OpenHarmony 的文件系统路径（通过 `path_provider` 获取）完全支持 Dart 的 `File` 操作，因此标准的文件缓存方案是通用的。

### 4.2 内存优化

OpenHarmony 设备形态多样，从低功耗设备到高性能手机。在加载高清大图时，务必指定 `cacheWidth` 或 `cacheHeight`（如果使用 `ResizeImage`），或者确保服务器返回适当分辨率的图片，避免 `ImageCache` 占用过多内存导致 OOM（内存溢出）。

```dart
Image(
  image: ResizeImage(
    NetworkImageWithRetry('https://large-image-url.jpg'),
    width: 200, // 仅解码为显示宽度的尺寸
  ),
)
```

## 五、完整示例代码

这个示例展示了一个图片网格，模拟了从网络加载多张图片的效果。

```dart
import 'package:flutter/material.dart';
import 'package:flutter_image/network.dart';

class FlutterImageDemo extends StatelessWidget {
  const FlutterImageDemo({super.key});

  // 模拟一组图片 URL
  final List<String> _imageUrls = const [
    'https://picsum.photos/200/300?random=1',
    'https://picsum.photos/200/300?random=2',
    'https://picsum.photos/200/300?random=3',
    'https://picsum.photos/200/300?random=4',
    // 一个可能不存在的 URL 来测试重试 (实际情况需关闭网络测试)
    'https://httpbin.org/image/jpeg',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Flutter Image Demo')),
      body: GridView.builder(
        padding: const EdgeInsets.all(8),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          mainAxisSpacing: 8,
          crossAxisSpacing: 8,
          childAspectRatio: 0.7,
        ),
        itemCount: _imageUrls.length,
        itemBuilder: (context, index) {
          return Card(
            clipBehavior: Clip.antiAlias,
            elevation: 4,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Expanded(
                  child: Image(
                    image: NetworkImageWithRetry(_imageUrls[index]),
                    fit: BoxFit.cover,
                    loadingBuilder: (ctx, child, progress) {
                      if (progress == null) return child;
                      return Center(
                        child: CircularProgressIndicator(
                          value: progress.expectedTotalBytes != null
                              ? progress.cumulativeBytesLoaded /
                                  progress.expectedTotalBytes!
                              : null,
                        ),
                      );
                    },
                    errorBuilder: (ctx, error, stack) {
                      return const Center(child: Icon(Icons.broken_image, size: 40, color: Colors.grey));
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text('Image ${index + 1}', textAlign: TextAlign.center),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 网格图片加载效果图 -->
<!-- 设备: 鸿蒙设备 -->
<!-- 内容: 2列网格，显示多张随机图片，展示加载状态 -->

## 六、总结

`flutter_image` 以最小的成本解决了网络抖动导致的图片加载失败问题。在 OpenHarmony 应用开发中，结合正确的权限配置（`ohos.permission.INTERNET`），它能显著提升应用的健壮性。

虽然界面上看不出太大的区别，但这种“隐形”的优化对于提升用户留存率至关重要。

---

> 📦 完整代码已上传至 AtomGit：[open-harmony-examples/flutter_image_demo](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/flutter_image_demo)
>
> 🌐 欢迎加入开源鸿蒙跨平台社区：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
