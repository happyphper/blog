---
title: "Flutter for OpenHarmony：品牌焕新 — App 图标定制与沉浸式启动页 (Splash) 方案"
date: 2026-02-02
tags: ["Flutter", "OpenHarmony", "图标适配", "Splash Screen"]
categories: ["Flutter for OpenHarmony 实战"]
---

# Flutter for OpenHarmony：品牌焕新 — App 图标定制与沉浸式启动页 (Splash) 方案

## 前言

开发 App 就像装修房子，代码是硬装，而图标和启动页则是门面。很多 Flutter 开发者在完成功能开发后，往往因为遗漏了 OpenHarmony 平台的资源配置，导致安装在鸿蒙手机上显示的还是那个蓝色的 Flutter 默认 Logo，这会大大降低应用的专业感。

本文将作为《Splendid Movie》系列的**品牌篇**，教你如何一键生成适配鸿蒙系统的应用图标，并实现一个无白屏、沉浸式的启动页。

<!-- IMAGE_PLACEHOLDER: 图标与启动页对比图 -->
<!-- 类型: 截图 -->
<!-- 内容: 左侧展示鸿蒙桌面上的 Splendid Movie 用于图标，右侧展示带有 Logo 的深色启动画面 -->

---

## 一、 App 图标定制：告别默认 Logo

Flutter 官方推荐使用 `flutter_launcher_icons` 插件来生成图标，好消息是，目前已有分支或工具链开始支持 OpenHarmony 资源结构的生成（或者我们可以手动对齐）。

### 1.1 准备高清素材

首先，你需要准备一张 `1024x1024` 分辨率的 PNG 原图，放置在 `assets/icon/app_icon.png`。
对于 Splendid Movie，我们的图标是一个带有霓虹光效的电影胶卷符号。

### 1.2 OpenHarmony 图标资源结构解析

Android 的图标在 `res/mipmap` 下，而 OpenHarmony 的图标资源位于 `ohos/entry/src/main/resources` 目录下。

你需要关注两个关键文件：
1.  **icon.png** (普通图标): 存放在 `base/media/icon.png`。
2.  **foreground.png & background.png** (分层图标): 如果支持鸿蒙的分层动态图标，需要分别配置。

### 1.3 手动替换指南

由于目前自动化工具对鸿蒙支持尚在完善中，手动替换是最稳妥的方案：

1.  **生成图标**：使用在线工具将你的 1024png 切割成标准尺寸（虽然鸿蒙主要是矢量或单一大图，但建议准备 192x192 备用）。
2.  **文件覆盖**：
    *   将你的图标重命名为 `icon.png`。
    *   直接覆盖 `ohos/entry/src/main/resources/base/media/icon.png`。
3.  **配置**：检查 `ohos/entry/src/main/module.json5`:

```json
{
  "module": {
    "name": "entry",
    "type": "entry",
    "description": "$string:module_desc",
    "mainElement": "EntryAbility",
    "deviceTypes": ["phone", "tablet"],
    "deliveryWithInstall": true,
    "installationFree": false,
    "pages": "$profile:main_pages",
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ets",
        "description": "$string:EntryAbility_desc",
        "icon": "$media:icon", // 👈 确保这里引用的是 icon
        "label": "$string:EntryAbility_label",
        // ...
      }
    ]
  }
}
```

---

## 二、 沉浸式启动页 (Splash Screen)

Flutter 应用启动时，引擎初始化需要几百毫秒。这期间如果这里是黑屏或白屏，体验会非常割裂。我们需要在**原生层**和**Flutter层**分别配置。

### 2.1 阶段一：原生启动屏 (ArkTS/JSON)

在鸿蒙侧，我们通过配置 `EntryAbility` 的窗口背景来实现秒开显示。

修改 `ohos/entry/src/main/resources/base/element/color.json`，添加我们 App 的深色背景：

```json
{
  "color": [
    {
      "name": "start_window_background",
      "value": "#09090F" // Splendid Movie 的深色背景
    }
  ]
}
```

这能保证用户点击图标瞬间，展现的就是我们的主题色，而不是刺眼的白色。

### 2.2 阶段二：Flutter 侧的平滑过渡

当 Flutter 引擎加载完毕，我们会进入 `main.dart`。为了实现完美的过渡，我们可以编写一个纯 Dart 的 `SplashScreen`，播放一个简短的 Logo 动画，然后跳转首页。

```dart
// lib/screens/splash_screen.dart

class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    // 2秒后跳转首页
    Timer(const Duration(seconds: 2), () {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const HomeScreen()),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset("assets/images/logo.png", width: 120),
            const SizedBox(height: 20),
            const CircularProgressIndicator(color: AppColors.primaryAccent),
          ],
        ),
      ),
    );
  }
}
```

### 2.3 最终整合

在 `main.dart` 中，将 `home` 设置为 `SplashScreen`：

```dart
class SplendidMovieApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // ...
      home: const SplashScreen(), // 👈 入口改为启动页
    );
  }
}
```

---

## 三、 总结

通过本篇的“品牌装修”，我们的 Splendid Movie 实现了：
1.  **桌面图标**：在鸿蒙桌面上显示了自定义的电影胶卷 Logo。
2.  **视觉连续性**：从点击图标（原生背景色）-> Flutter 启动页（Logo 动画）-> 首页，全流程无白屏、无跳闪。

这是应用迈向专业化的重要一步。下一篇 **【适配篇】UI 细节微调与 HarmonyOS 特有手势适配指南**，我们将深入细节，处理诸如侧滑返回冲突、系统状态栏颜色同步等极易被忽视的体验问题。

---

> 📦 **完整代码已上传至 AtomGit**：[splendid_movie](https://atomgit.com/jiang_style/splendid_movie)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
