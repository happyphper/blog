![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战：每日热点 App（一）— 项目初始化与鸿蒙插件配置

> **摘要**：在鸿蒙原生应用开发中，如何快速搭建一个功能完备、体验流畅的跨平台应用？本文将以"每日热点"（Daily Hotspots）应用为例，开启专栏的第一篇。我们将从项目初始化开始，重点讲解如何在鸿蒙环境下配置专用的三方插件，并构建健壮的应用数据模型。

## 前言

随着 HarmonyOS 下的跨平台开发生态日益完善，Flutter 已成为许多开发者在鸿蒙上构建高性能应用的首选。为了让大家能系统地掌握实战技巧，我规划了这套《每日热点 App》系列教程，共 4 篇：
1.  **架构篇：项目初始化与鸿蒙插件配置（本文）**
2.  **逻辑篇：基于 http 的热榜服务封装与异步处理**
3.  **视觉篇：深色模式适配与高级 UI 组件封装**
4.  **交互篇：打磨交互细节与鸿蒙系统能力调用**

本文作为开篇，将带你打好地基，解决开发者在鸿蒙环境下最常遇到的"库配置"和"模型设计"问题。

---

## 一、项目背景与需求分析

"每日热点"是一款聚合类阅读应用，它可以实时抓取微博、知乎、B 站、百度、知乎等主流平台的实时榜单。

**核心功能需求**：
- **热点分类**：支持主流平台一键切换。
- **深色模式**：提供极致的沉浸式阅读体验。
- **沉浸式头部**：自动适配鸿蒙设备状态栏。
- **外部跳转**：一键跳转至原平台浏览器阅读。

![每日热点 App 全系列架构图](./images/daily_hotspots_architecture.png)


---

## 二、环境准备与项目创建

在开始之前，请确保你已经安装了支持 OpenHarmony 的 Flutter SDK（例如：OpenHarmony-SIG 提供的版本）。

### 2.1 创建鸿蒙项目

执行以下命令创建纯净的鸿蒙项目：

```bash
# 创建项目，明确只开启 ohos 平台支持
flutter create --platforms ohos daily_hotspots

# 进入目录
cd daily_hotspots
```

### 2.2 目录结构规划

为了遵循 Flutter 最佳实践并方便鸿蒙工程维护，我们按照以下结构组织代码：

```text
lib/
├── models/         # 存放数据模型 (JSON 序列化)
├── services/       # 存放网络请求与本地存储服务
├── pages/          # 存放主页面
├── theme/          # 存放全局配色方案
├── widgets/        # 存放可复用的 UI 单元
└── main.dart       # 应用入口
```

---

## 三、重难点：配置鸿蒙适配插件

在 Flutter for OpenHarmony 开发中，许多传统的 `pub.dev` 插件可能还未完全适配鸿蒙原生底层。此时，我们需要直接引用 OpenHarmony-TPC 组提供的适配版本。

### 3.1 pubspec.yaml 深度配置

我们需要核心依赖：`http`（网络请求）和 `url_launcher`（网页跳转）。注意 `url_launcher` 需要特殊的 `git` 配置。

```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6
  http: ^1.1.0

  # 🟢 重点：配置 OpenHarmony 官方适配的跳转插件
  url_launcher:
    git:
      url: "https://gitcode.com/openharmony-tpc/flutter_packages.git"
      ref: "br_url_launcher-v6.3.0_ohos"
      path: "packages/url_launcher/url_launcher"
      
  # 🟢 重点：明确引入鸿蒙原生实现包
  url_launcher_ohos:
    git:
      url: "https://gitcode.com/openharmony-tpc/flutter_packages.git"
      ref: "br_url_launcher-v6.3.0_ohos"
      path: "packages/url_launcher/url_launcher_ohos"
```

💡 **技巧**：在鸿蒙实战中，建议优先在 [OpenHarmony-TPC](https://gitcode.com/openharmony-tpc) 查找已经适配好的插件分支。

---

## 四、构建应用数据模型

好的模型设计是高性能数据渲染的前提。在建模之前，我们需要先了解数据的来源。本项项目使用的是 [UAPIS 全网热榜接口](https://uapis.cn/)，它将各大平台的复杂数据进行了标准化处理，非常适合用于跨平台实战。

- **接口地址**：`https://uapis.cn/api/v1/misc/hotboard`
- **数据格式**：支持 `type` 参数（如 weibo, zhihu 等），返回标准的 JSON 列表。

### 4.1 定义热点条目：HotItem


我们在 `lib/models/hot_item.dart` 中定义包含各种统计数据的模型。考虑到不同平台（知乎、B站）返回的图片字段名不同，我们需要在 `Extra` 中做兼容处理。

```dart
/// 热榜条目数据模型
class HotItem {
  final int index;      // 排名
  final String title;   // 标题
  final String url;     // 原文链接
  final String hotValue; // 热度数值
  final HotItemExtra? extra;

  HotItem({
    required this.index,
    required this.title,
    required this.url,
    required this.hotValue,
    this.extra,
  });

  factory HotItem.fromJson(Map<String, dynamic> json) {
    return HotItem(
      index: json['index'] ?? 0,
      title: json['title'] ?? '',
      url: json['url'] ?? '',
      hotValue: json['hot_value'] ?? '',
      extra: json['extra'] != null ? HotItemExtra.fromJson(json['extra']) : null,
    );
  }
}
```

### 4.2 定义多平台配置：Platform

为了方便在界面上显示不同的 Logo 和配色，我们在 `lib/models/platform.dart` 中采用枚举类的思想定义平台配置。

```dart
class Platform {
  final String id;
  final String name;
  final String? logoUrl; // 品牌官方 Logo
  final Color color;      // 品牌主题色
  final Color iconBgColor;

  const Platform({
    required this.id,
    required this.name,
    this.logoUrl,
    required this.color,
    required this.iconBgColor,
  });
}

// 示例：所有支持的平台
class Platforms {
  static const List<Platform> all = [
    Platform(
      id: 'weibo',
      name: '微博',
      logoUrl: 'https://img.icons8.com/color/48/weibo.png',
      color: Color(0xFFE6162D),
      iconBgColor: Color(0x1AE6162D),
    ),
    Platform(
      id: 'zhihu',
      name: '知乎',
      logoUrl: 'https://img.icons8.com/?size=48&id=DVtS4lF5-eqh&format=png&color=0066FF',
      color: Color(0xFF0066FF),
      iconBgColor: Color(0x1A0066FF),
    ),
    Platform(
      id: 'github',
      name: 'GitHub',
      logoUrl: 'https://img.icons8.com/ios-filled/50/ffffff/github.png',
      color: Color(0xFF24292F),
      iconBgColor: Color(0x1A24292F),
    ),
    // ... 其他平台
  ];
}
```

---

## 五、应用入口与鸿蒙状态栏初始化

在鸿蒙设备上，我们要实现沉浸式顶部，需要通过 `SystemChrome` 来管理状态栏颜色。

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // 1. 设置鸿蒙系统状态栏样式为透明沉浸式
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
      systemNavigationBarColor: Color(0xFF1D1B20),
      systemNavigationBarIconBrightness: Brightness.light,
    ),
  );

  runApp(const DailyHotspotsApp());
}
```

📌 **注意事项**：确保在 `MaterialApp` 中设置 `debugShowCheckedModeBanner: false`，让鸿蒙设备的演示界面更加清爽。

---

## 六、上篇小结

作为实战系列的第一篇，我们解决了以下核心问题：
1.  **项目创建**：正确初始化 Flutter for OpenHarmony 工程。
2.  **依赖攻坚**：通过 `git` 配置解决了鸿蒙环境下跳转插件的适配。
3.  **模型构建**：搭建了兼容多平台数据差异的高扩展性 Model 层。

在下一篇**【逻辑篇】**中，我们将深入网络请求服务层，讲解如何封装一个高效的 API 调用中心，并处理鸿蒙下的网络通信权限。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-example (主分支)](https://atomgit.com/dragonbady/open-harmony-example/tree/main/examples/daily_hotspots)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
