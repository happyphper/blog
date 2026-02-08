![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第五篇 Image 图片组件与资源管理

> **摘要**：图片是提升 App 视觉体验的关键。本文详细介绍 Flutter 中 Image 组件的加载方式（网络、本地、内存），深入讲解 cached_network_image 缓存策略、SVG 矢量图的使用，以及在 OpenHarmony 多设备环境下的图片适配最佳实践。

## 前言

一个精美的 App 离不开高质量的图片。在 Flutter for OpenHarmony 中，图片的加载远不止 `Image.network` 这么简单。

我们需要考虑：
- 网络图片加载慢怎么办？（Loading 占位）
- 图片加载失败显示什么？（Error Widget）
- 如何根据不同屏幕密度加载 2x/3x 图？
- 列表快速滑动时如何优化内存？

**本文你将学到**：
- Image 组件的 4 种加载模式
- BoxFit 适配模式全图解
- 实现圆角图片的 3 种方式
- 使用 cached_network_image 实现高效缓存
- 鸿蒙资源文件 (Assets) 的配置与读取

---

## 一、Image 基础加载模式

Flutter 提供了多种构造函数来加载不同来源的图片。

### 1.1 加载网络图片

最常用的方式，支持 WebP、JPEG、PNG、GIF (含动画) 等格式。

```dart
Image.network(
  'https://example.com/flutter_ohos.png',
  width: 300,
  height: 200,
  fit: BoxFit.cover, // 填充模式
)
```

### 1.2 加载本地资源 (Assets)

加载打包在 App 安装包内的图片。

**步骤 1：配置 pubspec.yaml**
```yaml
flutter:
  assets:
    - assets/images/logo.png
    - assets/images/banner.jpg
```

**步骤 2：代码调用**
```dart
Image.asset(
  'assets/images/logo.png',
  width: 100,
)
```

### 1.3 加载文件系统图片 (File)

通常用于显示用户相册选择或相机拍摄的照片。

```dart
Image.file(File('/path/to/image.jpg'))
```

---

## 二、BoxFit 适配模式图解

`fit` 属性决定了图片如何适应容器的尺寸。这是布局中最容易迷惑的地方。

| 模式 | 描述 | 场景 |
|---|---|---|
| **BoxFit.contain** | (默认) 等比缩放，完全显示图片，可能留白 | 详情页看大图 |
| **BoxFit.cover** | 等比缩放，填满容器，超出部分被裁剪 | **最常用**，Banner、头像 |
| **BoxFit.fill** | 拉伸填满，图片会变形 | 不推荐，除非为了背景铺满 |
| **BoxFit.fitWidth** | 宽度填满，高度自适应 (可能裁剪顶/底) | 定宽列表项 |
| **BoxFit.fitHeight** | 高度填满，宽度自适应 | 横向滚动列表 |
| **BoxFit.none** | 不缩放，按原图大小居中显示 | 原始尺寸展示 |

```dart
Container(
  width: 200,
  height: 200,
  color: Colors.grey[200],
  child: Image.network(
    url,
    fit: BoxFit.cover, // 裁切填满
  ),
)
```

<!-- IMAGE_PLACEHOLDER: BoxFit 模式效果对比 -->
<!-- 类型: 示例图 -->
<!-- 内容: 展示同一张猫咪图片在不同 fit 模式下的显示效果 -->

---

## 三、进阶技巧：占位图与错误处理

直接用 `Image.network` 在网速慢时会留白，体验不好。

### 3.1 使用 FrameBuilder (原生方式)

```dart
Image.network(
  'https://example.com/large_image.jpg',
  loadingBuilder: (context, child, loadingProgress) {
    if (loadingProgress == null) return child;
    return Center(
      child: CircularProgressIndicator(
        value: loadingProgress.expectedTotalBytes != null
            ? loadingProgress.cumulativeBytesLoaded / 
              loadingProgress.expectedTotalBytes!
            : null,
      ),
    );
  },
  errorBuilder: (context, error, stackTrace) {
    return const Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(Icons.error, color: Colors.red),
        Text('加载失败'),
      ],
    );
  },
)
```

### 3.2 使用 cached_network_image (推荐)

在生产环境中，强烈建议使用 `cached_network_image` 库，它提供了内存+磁盘双重缓存，能显著节省用户流量。

**安装依赖**：
```bash
flutter pub add cached_network_image
```

**使用代码**：
```dart
CachedNetworkImage(
  imageUrl: "https://example.com/image.jpg",
  placeholder: (context, url) => const CircularProgressIndicator(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
  fit: BoxFit.cover,
  // 仅在内存中缓存 100 张
  memCacheHeight: 400, // 优化：仅缓存指定高度，减少内存占用
)
```

---

## 四、图片裁剪与圆角

### 4.1 CircleAvatar (圆形头像)

专门用于头像，自带圆形裁切。

```dart
CircleAvatar(
  radius: 40,
  backgroundImage: NetworkImage(avatarUrl),
)
```

### 4.2 ClipRRect (圆角矩形)

最通用的裁切组件。

```dart
ClipRRect(
  borderRadius: BorderRadius.circular(16),
  child: Image.network(
    imageUrl,
    width: 200,
    height: 120,
    fit: BoxFit.cover,
  ),
)
```

### 4.3 ClipOval (椭圆/圆形)

将非正方形图片裁切为圆形或椭圆。

```dart
ClipOval(
  child: Image.asset('assets/avatar.jpg'),
)
```

---

## 五、OpenHarmony 资源适配指南

### 5.1 多倍图适配 (2.0x, 3.0x)

Flutter 使用 **逻辑像素**。在不同像素密度的设备上，需要加载不同清晰度的图片。

如果你的代码是：
```dart
Image.asset('assets/images/icon.png')
```

你需要构建如下目录结构：

```
assets/
  images/
    icon.png      (1.0x 基准图，对应低分屏)
    2.0x/
      icon.png    (2.0x 高清图，对应普通手机)
    3.0x/
      icon.png    (3.0x 超清图，对应旗舰机/平板)
```

Flutter 会根据当前设备的 `devicePixelRatio` 自动加载对应的图片！

### 5.2 矢量图 SVG

为了进一步减少包体积并适配任意分辨率，推荐使用 SVG。需要引入 `flutter_svg` 库。

```dart
SvgPicture.asset(
  'assets/icons/heart.svg',
  width: 24,
  height: 24,
  colorFilter: const ColorFilter.mode(Colors.red, BlendMode.srcIn), // 动态染色
)
```

---

## 六、实战：封装通用图片组件

我们在项目中通常会封装一个统一的图片组件，统一处理缓存、圆角和占位。

```dart
class CommonImage extends StatelessWidget {
  final String imageUrl;
  final double? width;
  final double? height;
  final double radius;
  final BoxFit fit;

  const CommonImage({
    super.key,
    required this.imageUrl,
    this.width,
    this.height,
    this.radius = 0,
    this.fit = BoxFit.cover,
  });

  @override
  Widget build(BuildContext context) {
    // 1. 处理圆角
    return ClipRRect(
      borderRadius: BorderRadius.circular(radius),
      // 2. 使用缓存图片
      child: CachedNetworkImage(
        imageUrl: imageUrl,
        width: width,
        height: height,
        fit: fit,
        // 3. 统一占位图 (骨架屏效果)
        placeholder: (context, url) => Container(
          color: Colors.grey[200],
          child: const Center(
            child: Icon(Icons.image, color: Colors.grey),
          ),
        ),
        // 4. 统一错误图
        errorWidget: (context, url, error) => Container(
          color: Colors.grey[100],
          child: const Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.broken_image, color: Colors.grey),
              SizedBox(height: 4),
              Text('加载失败', style: TextStyle(fontSize: 10, color: Colors.grey)),
            ],
          ),
        ),
      ),
    );
  }
}
```

---

## 七、总结

Image 组件是 App 内容展示的核心。

### 核心要点
1.  **加载方式**：网络图用 `CachedNetworkImage`，本地图用 `Asset`。
2.  **适配模式**：牢记 `BoxFit.cover` 是万金油。
3.  **多倍图**：利用 `2.0x/3.0x` 文件夹实现自动分辨率适配。
4.  **性能**：列表中的图片务必设置 `memCacheHeight` 以减少内存占用，防止 OOM (Out Of Memory)。

### 下一篇预告
图片通常不会单独存在，而是存在于长列表中。
**《Flutter for OpenHarmony 实战之基础组件：第六篇 ListView 列表组件详解》**
我们将学习如何构建高性能的滚动列表、实现下拉刷新与上拉加载更多。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/5-image)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/5-image)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
