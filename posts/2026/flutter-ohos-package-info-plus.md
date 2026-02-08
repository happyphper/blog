---
title: "Flutter 实战：利用 package_info_plus 精准获取鸿蒙应用版本与原生元数据"
date: 2026-02-07
tags: ["Flutter", "OpenHarmony", "package_info_plus", "元数据", "版本管理"]
categories: ["Flutter for OpenHarmony 实战"]
---

# Flutter 实战：利用 package_info_plus 精准获取鸿蒙应用版本与原生元数据

![封面图](images/cover_flutter_ohos_package_info_plus.png)

## 前言

在 App 开发中，诸如“检查更新”、“展示应用版本号”或“在关于页面显示内部 Build 号”是极其常见的需求。这些信息被统称为“应用元数据”。

在 **OpenHarmony** 平台上，这些元数据被定义在项目的 `module.json5` 和 `AppScope/app.json5` 中。传统的硬编码（Hardcoding）方案不仅低效且容易出错。今天我们来看一看如何通过 `package_info_plus` 这个业界最流行的插件，实现对鸿蒙应用信息的自动化提取。

---

## 一、 package_info_plus 的核心价值

### 1.1 自动化同步
你只需在鸿蒙原生配置文件中修改一次版本号，Dart 代码层通过 `package_info_plus` 即可实时同步获取。

### 1.2 跨平台抽象
它为 `bundleName` (在 Android 上是 packageName, 在鸿蒙上是 bundleName)、`version` (版本名) 和 `buildNumber` (构建号) 提供了统一的 API，极大地降低了多端分发的复杂度。

<!-- IMAGE_PLACEHOLDER: 鸿蒙手机“关于”页面展示出从 package_info_plus 获取的版本信息截图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示版本号 v1.0.1+100 等数据 -->

---

## 二、 集成指南

### 2.1 添加依赖
```yaml
dependencies:
  package_info_plus: ^5.0.1 # 请确保使用支持鸿蒙平台的官方/社区适配版本
```

### 2.2 鸿蒙原生侧确认
`package_info_plus` 会读取鸿蒙工程中的以下字段：
- **App Name**: 对应 `AppScope/app.json5` 中的 `label`。
- **Package Name**: 对应 `AppScope/app.json5` 中的 `bundleName`。
- **Version**: 对应 `AppScope/app.json5` 中的 `versionName`。
- **Build Number**: 对应 `AppScope/app.json5` 中的 `versionCode`。

---

## 三、 实战代码解析

### 3.1 异步初始化
由于读取系统信息属于异步操作，我们需要在应用启动之初或特定页面初始化时获取。

```dart
import 'package:package_info_plus/package_info_plus.dart';

void _initPackageInfo() async {
  PackageInfo packageInfo = await PackageInfo.fromPlatform();

  String appName = packageInfo.appName;
  String packageName = packageInfo.packageName;
  String version = packageInfo.version;
  String buildNumber = packageInfo.buildNumber;

  print('应用名称: $appName');
  print('鸿蒙 BundleID: $packageName');
  print('版本号: $version');
  print('构建号: $buildNumber');
}
```

### 3.2 UI 展示组件
推荐结合 `FutureBuilder` 使用，避免 UI 阻塞。

```dart
Widget buildVersionTile() {
  return FutureBuilder<PackageInfo>(
    future: PackageInfo.fromPlatform(),
    builder: (context, snapshot) {
      if (snapshot.hasData) {
        return ListTile(
          title: const Text('当前版本'),
          subtitle: Text('${snapshot.data!.version}+${snapshot.data!.buildNumber}'),
          trailing: const Icon(Icons.info_outline),
        );
      } else {
        return const SizedBox.shrink();
      }
    },
  );
}
```

---

## 四、 鸿蒙环境下的进阶场景

### 4.1 自动检查更新逻辑
通过 `package_info_plus` 获取 `versionCode` (buildNumber)，与远程服务器返回的最新的 `min_version_code` 进行对比，实现强制更新或弹窗提醒。

### 4.2 适配鸿蒙多版本 SDK
在鸿蒙系统中，API 版本迭代迅速。
- ✅ **建议**：在鸿蒙端如果遇到版本号读取为 `null`，请检查 `module.json5` 的权限声明及 `hvigor` 构建版本是否对齐。

---

## 五、 完整 Demo 示例

```dart
import 'package:flutter/material.dart';
import 'package:package_info_plus/package_info_plus.dart';

class AboutPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('关于 Splendid Movie')),
      body: Center(
        child: FutureBuilder<PackageInfo>(
          future: PackageInfo.fromPlatform(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const CircularProgressIndicator();
            }
            final info = snapshot.data!;
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const FlutterLogo(size: 80),
                const SizedBox(height: 16),
                Text(info.appName, style: Theme.of(context).textTheme.headlineMedium),
                Text('BundleID: ${info.packageName}'),
                const Divider(),
                Text('Version: ${info.version}'),
                Text('Code: ${info.buildNumber}'),
              ],
            );
          },
        ),
      ),
    );
  }
}
```

---

## 六、 总结

`package_info_plus` 插件让鸿蒙 Flutter 开发者能够：
1.  **统一元数据获取路径**，代码多端通用。
2.  **为应用升级、日志统计等核心业务提供精准的版本依据**。
3.  **完全兼容鸿蒙的安全访问规范**，无侵入性。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/package_info_plus](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/flutter-ohos-package-info-plus)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
