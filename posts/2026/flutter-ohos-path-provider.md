![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony：path_provider 插件指南

> **摘要**：在移动应用开发中，管理文件系统路径（如应用私有目录、缓存目录、外部存储）是常见需求。`path_provider` 作为 Flutter 官方插件，为获取这些路径提供了便捷的平台无关 API。本文将介绍如何在 Flutter for OpenHarmony 项目中集成适配版的 `path_provider`。

## 前言

由于每个操作系统的文件系统沙盒机制不同，硬编码文件路径（如 `/data/user/0/...`）会导致应用在不同平台上崩溃或无法读取数据。OpenHarmony (鸿蒙) 系统同样具有严密的沙盒设计。

`path_provider` 的作用就是抹平平台差异，让开发者通过统一的 Dart 接口获取当前系统下合法的存储位置。

**本文你将学到**：
- 鸿蒙适配版 `path_provider` 的集成方式
- 常用 API 对应鸿蒙系统的具体路径
- 文件读写实战演示
- 鸿蒙 Next 沙盒权限与路径规则说明

---

## 一、OpenHarmony 集成配置

### 1.1 依赖覆盖

在 OpenHarmony 平台上，官方 `path_provider` 需要配合鸿蒙专用的实现包使用。在 `pubspec.yaml` 中添加以下配置：

```yaml
dependencies:
  path_provider: ^2.1.3

dependency_overrides:
  # 使用 OpenHarmony TPC 维护的兼容版本
  path_provider_ohos:
    git:
      url: "https://atomgit.com/openharmony-tpc/flutter_packages.git"
      path: "packages/path_provider/path_provider_ohos"
```

### 1.2 执行依赖获取

```bash
flutter pub get
```

---

## 二、核心 API 详解

### 2.1 临时目录（Temporary Directory）

用于存放临时文件，系统可能会在设备空间不足时自动清理。

- **API**: `getTemporaryDirectory()`
- **鸿蒙路径**: 对应 `cache` 目录。
- **场景**: 网络图片缓存、导出的临时 PDF。

### 2.2 应用程序文档目录（Application Documents Directory）

用于存放应用生成的、不能由系统清理的文件。

- **API**: `getApplicationDocumentsDirectory()`
- **鸿蒙路径**: 对应应用沙盒内的 `files` 目录。
- **场景**: 用户配置、SQLite 数据库文件、持久化数据。

### 2.3 应用支持目录（Application Support Directory）

用于存放应用支持运行的文件，通常对用户不可见。

- **API**: `getApplicationSupportDirectory()`
- **场景**: 应用状态同步文件、离线地图包。

### 2.4 外部存储目录（External Storage）

获取外部 SD 卡或公共存储空间的路径（*注意：OpenHarmony Next 加强了隐私管理，通常推荐使用沙盒内部路径*）。

---

## 三、文件读写实战

以下是一个在鸿蒙应用中保存文本数据的完整示例：

```dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';

class PathProviderDemo extends StatefulWidget {
  const PathProviderDemo({super.key});

  @override
  State<PathProviderDemo> createState() => _PathProviderDemoState();
}

class _PathProviderDemoState extends State<PathProviderDemo> {
  String _content = "尚未读取数据";

  // 写入文件
  Future<void> _saveData() async {
    final directory = await getApplicationDocumentsDirectory();
    final file = File('${directory.path}/hello_ohos.txt');
    
    debugPrint("文件存储路径: ${file.path}");
    await file.writeAsString("来自鸿蒙的持久化数据 - ${DateTime.now()}");
    
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('保存成功！')),
    );
  }

  // 读取文件
  Future<void> _readData() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final file = File('${directory.path}/hello_ohos.txt');
      
      if (await file.exists()) {
        final text = await file.readAsString();
        setState(() => _content = text);
      } else {
        setState(() => _content = "文件不存在");
      }
    } catch (e) {
      setState(() => _content = "读取失败: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 文件系统测试')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('文件内容：', style: const TextStyle(fontWeight: FontWeight.bold)),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text(_content),
            ),
            ElevatedButton(onPressed: _saveData, child: const Text('写入文件')),
            const SizedBox(height: 10),
            ElevatedButton(onPressed: _readData, child: const Text('读取文件')),
          ],
        ),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙设备运行结果及 Log 输出 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示文件保存成功并在控制台输出沙盒路径的部分 -->

---

## 四、鸿蒙平台适配细节

### 4.1 路径前缀（Context Context）

鸿蒙系统的沙盒路径通常以 `/data/storage/el2/base/haps/entry/...` 开头。`path_provider_ohos` 插件底层通过 `ohos.app.Context` 接口动态获取这些映射路径，确保应用在不同用户或多 Ability 环境下逻辑正确。

### 4.2 文件权限（Permissions）

在鸿蒙沙盒目录（如 `getApplicationDocumentsDirectory` 返回的路径）内读写文件**不需要**申请额外权限。但如果涉及到访问用户的公共相册（MediaLibrary），则需要额外申请。

📌 **建议**：优先将业务数据存储在应用私有沙盒内，以避免繁琐的权限申请。

---

## 五、总结

`path_provider` 是 Flutter for OpenHarmony 开发必备的底层工具。通过它，我们可以安全、合规地管理应用数据，充分利用鸿蒙系统的文件隔离机制。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/path-provider](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/path-provider)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
