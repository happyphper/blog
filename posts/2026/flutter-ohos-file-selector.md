# Flutter for OpenHarmony 实战：file_selector — 原生文件选择指南

## 前言

在移动应用开发中，让用户选择文件（如图片、文档、视频）是一个非常高频的需求。虽然 `image_picker` 可以处理图片和视频，但当我们需要选择任意类型的文件（如 PDF、JSON、ZIP）时，就需要更通用的解决方案。

`file_selector` 是 Flutter 官方提供的插件，旨在提供跨平台（iOS, Android, Web, Desktop, OpenHarmony）的统一文件选择能力。在 OpenHarmony 上，它对接了系统的 `FilePicker` 接口，能够拉起原生的文件选择器，用户体验非常流畅。

本文将介绍如何在 OpenHarmony 项目中集成 `file_selector`，实现单文件选择、多文件选择以及保存文件（另存为）的功能。

## 一、核心功能

`file_selector` 的 API 设计非常简洁，主要包含以下几个核心方法：

*   `openFile`: 选择单个文件。
*   `openFiles`: 选择多个文件。
*   `getSaveLocation`: 获取文件保存路径（即“另存为”对话框）。

<!-- IMAGE_PLACEHOLDER: 架构图 -->
<!-- 内容: Flutter App -> file_selector interface -> file_selector_ohos -> OHOS FilePicker API -->

## 二、安装与配置

### 2.1 添加依赖

在 `pubspec.yaml` 中添加：

```yaml
dependencies:
  flutter:
    sdk: flutter
  # 请务必检查 pub.dev 或 OpenHarmony SIG 仓库获取适配 OHOS 的版本
  file_selector: ^1.0.0
  # 如果官方插件尚未完全合并 OHOS 支持，建议显式引入适配包或通过 git 依赖
  # file_selector_ohos: ...
```

### 2.2 OpenHarmony 权限配置

使用系统的 Picker 接口选择文件通常是一个“用户授权”的过程（用户主动选择文件即视为授权），因此通常**不需要**像 Android 那样申请 `READ_EXTERNAL_STORAGE` 权限。OpenHarmony 的沙箱机制会自动授权应用读取用户选中的那个文件。

但是，如果你需要访问特定公共目录，可以按需检查 `module.json5` 中的权限配置，一般来说，基础的文件选择无需额外配置。

## 三、代码实现

### 3.1 选择单个文件

我们可以指定 `XTypeGroup` 来过滤文件类型，例如只允许选择文本文件或图片。

```dart
import 'package:flutter/material.dart';
import 'package:file_selector/file_selector.dart';

class FileSelectorPage extends StatelessWidget {
  const FileSelectorPage({super.key});

  Future<void> _pickSingleFile(BuildContext context) async {
    // 定义文件类型过滤器
    const XTypeGroup typeGroup = XTypeGroup(
      label: 'images',
      extensions: <String>['jpg', 'png'],
    );
    
    // 打开选择器
    final XFile? file = await openFile(
      acceptedTypeGroups: <XTypeGroup>[typeGroup],
    );

    if (file != null) {
      // 获取文件名和路径
      print('文件名: ${file.name}');
      print('路径: ${file.path}');
      
      // 读取文件内容
      final int size = await file.length();
      print('文件大小: $size 字节');
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('已选择: ${file.name}')),
      );
    } else {
      // 用户取消了选择
      print('用户取消操作');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('文件选择演示')),
      body: Center(
        child: ElevatedButton(
          onPressed: () => _pickSingleFile(context),
          child: const Text('选择一张图片'),
        ),
      ),
    );
  }
}
```

### 3.2 选择多个文件

使用 `openFiles` 方法即可，返回的是 `List<XFile>`。

```dart
Future<void> _pickMultipleFiles() async {
  final List<XFile> files = await openFiles(
    acceptedTypeGroups: <XTypeGroup>[
      const XTypeGroup(label: 'All Files'), // 允许所有类型
    ],
  );

  print('选择了 ${files.length} 个文件');
  for (var file in files) {
    print('路径: ${file.path}');
  }
}
```

### 3.3 保存文件（另存为）

在 OpenHarmony 上，这会拉起系统的“保存文件”面板，让用户选择保存的位置和文件名。

```dart
Future<void> _saveFile() async {
  const String fileName = 'my_export_data.txt';
  
  // 提示用户选择保存位置
  final FileSaveLocation? result = await getSaveLocation(
    suggestedName: fileName,
  );

  if (result != null) {
    final String path = result.path;
    print('用户选择保存至: $path');
    
    // 写入数据（这里需要使用 dart:io 或 XFile 的 API）
    // 注意：path 可能是沙箱路径或公共目录路径，确保有写入权限
    final File file = File(path);
    await file.writeAsString('Hello OpenHarmony from Flutter!');
  }
}
```

## 四、OpenHarmony 平台适配细节

### 4.1 路径与沙箱

OpenHarmony 采用严格的沙箱机制。当用户通过 Picker 选择文件后，系统通常会授予应用对该文件的临时读写权限。`file_selector` 返回的 `path` 通常是一个可以直接供 Dart `File` 对象读取的路径。

### 4.2 MIME Type 过滤

`XTypeGroup` 支持 `extensions`（扩展名）、`mimeTypes`（MIME类型）和 `macUTIs`（iOS专用）。在 OpenHarmony 上，建议优先使用 **extensions**，兼容性最好。

```dart
// 推荐做法：使用扩展名
const XTypeGroup(extensions: ['pdf', 'doc']);

// 可能存在兼容性差异：使用 MIME
// const XTypeGroup(mimeTypes: ['application/pdf']); 
```

### 4.3 UI 差异

`file_selector` 在 OpenHarmony 上调用的是系统级的 UI（FilePicker）。这意味着 UI 样式（如列表视图、网格视图、排序方式）是由系统决定的，Flutter 无法修改其外观，只能控制可选的文件类型。

## 五、完整示例代码

下面是一个综合示例，包含单选、多选和保存功能。

```dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_selector/file_selector.dart';

class FileSelectorDemo extends StatefulWidget {
  const FileSelectorDemo({super.key});

  @override
  State<FileSelectorDemo> createState() => _FileSelectorDemoState();
}

class _FileSelectorDemoState extends State<FileSelectorDemo> {
  String _statusText = '请选择操作';
  List<XFile> _selectedFiles = [];

  // 选择图片
  Future<void> _pickImage() async {
    const XTypeGroup typeGroup = XTypeGroup(
      label: 'images',
      extensions: <String>['jpg', 'png', 'gif'],
    );
    final XFile? file = await openFile(acceptedTypeGroups: [typeGroup]);
    if (file != null) {
      setState(() {
        _statusText = '已选择: ${file.name}';
        _selectedFiles = [file];
      });
    }
  }

  // 选择多个文档
  Future<void> _pickDocs() async {
    const XTypeGroup typeGroup = XTypeGroup(
      label: 'documents',
      extensions: <String>['pdf', 'txt', 'json'],
    );
    final List<XFile> files = await openFiles(acceptedTypeGroups: [typeGroup]);
    if (files.isNotEmpty) {
      setState(() {
        _statusText = '已选择 ${files.length} 个文件';
        _selectedFiles = files;
      });
    }
  }

  // 另存为
  Future<void> _saveText() async {
    final FileSaveLocation? result = await getSaveLocation(
      suggestedName: 'example.txt',
    );
    if (result != null) {
      final file = File(result.path);
      await file.writeAsString('这是通过 Flutter file_selector 保存的文件内容。');
      setState(() {
        _statusText = '文件已保存至: ${result.path}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('File Selector OHOS')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(_statusText, style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 20),
            if (_selectedFiles.isNotEmpty) ...[
              const Text('选中文件列表:', style: TextStyle(fontWeight: FontWeight.bold)),
              Expanded(
                child: ListView.builder(
                  itemCount: _selectedFiles.length,
                  itemBuilder: (ctx, index) => ListTile(
                    leading: const Icon(Icons.description),
                    title: Text(_selectedFiles[index].name),
                    subtitle: Text(_selectedFiles[index].path),
                  ),
                ),
              ),
            ] else
              const Spacer(),
            Wrap(
              spacing: 16,
              children: [
                ElevatedButton.icon(
                  onPressed: _pickImage,
                  icon: const Icon(Icons.image),
                  label: const Text('选图片'),
                ),
                ElevatedButton.icon(
                  onPressed: _pickDocs,
                  icon: const Icon(Icons.library_books),
                  label: const Text('选文档(多选)'),
                ),
                ElevatedButton.icon(
                  onPressed: _saveText,
                  icon: const Icon(Icons.save),
                  label: const Text('另存为'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 操作效果图 -->
<!-- 设备: 鸿蒙设备 -->
<!-- 内容: 1. 弹出系统文件选择器的截图 2. 应用内显示选中文件路径的列表 -->

## 六、总结

`file_selector` 为 OpenHarmony 应用提供了标准化的文件交互能力。相比于直接调用原生 Channel，使用此插件能保持代码的跨平台一致性。

在处理大文件读取时，建议配合 Dart 的 `Stream` 或 `Isolate` 来避免阻塞 UI 线程。

---

> 📦 完整代码已上传至 AtomGit：[open-harmony-examples/file_selector_demo](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/file_selector_demo)
>
> 🌐 欢迎加入开源鸿蒙跨平台社区：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
