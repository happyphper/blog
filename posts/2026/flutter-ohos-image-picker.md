![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony：image_picker 插件鸿蒙化适配指南

> **摘要**：`image_picker` 是 Flutter 开发中最常用的多媒体插件之一，用于实现图片选择、相机拍照及视频录制功能。在 OpenHarmony 平台上，由于系统权限管理和原生接口的差异，需要使用社区适配版插件。本文将详细介绍如何在鸿蒙设备上集成并使用 `image_picker`。

## 前言

在移动端应用中，上传头像、发布朋友圈或拍摄视频是极常见的场景。`image_picker` 插件为开发者提供了跨平台的统一 API，但在 OpenHarmony Next（API 12+）环境下，官方原版插件尚未完全覆盖底层实现。

目前，通过 **OpenHarmony SIG** 社区的维护，我们已经可以使用适配后的 `image_picker` 插件来流畅调用鸿蒙系统的图库（PhotoViewPicker）和相机（CameraCenter）。

**本文你将学到**：
- 适配版 `image_picker` 的安装与依赖覆盖
- 核心功能实现：从相册选图、相机拍摄
- 鸿蒙系统权限配置（oh-package 与 module.json5）
- 异步处理与性能优化

---

## 一、OpenHarmony 环境配置

### 1.1 依赖引入

在 OpenHarmony 平台上，我们需要通过 `dependency_overrides` 机制使用适配版本：

```yaml
dependencies:
  image_picker: ^1.1.2

dependency_overrides:
  # 使用 OpenHarmony TPC 维护的兼容版本
  image_picker_ohos:
    git:
      url: "https://atomgit.com/openharmony-tpc/flutter_packages.git"
      path: "packages/image_picker/image_picker_ohos"
```

💡 **提示**：目前大部分鸿蒙适配包托管在 Gitee 的 `openharmony-sig` 组织下。

### 1.2 权限声明

在鸿蒙应用的 `entry/src/main/module.json5` 中，需要根据功能需求申请相关权限：

```json
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.CAMERA",
        "reason": "$string:camera_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
      },
      {
        "name": "ohos.permission.MICROPHONE",
        "reason": "$string:micro_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
      },
      {
        "name": "ohos.permission.WRITE_IMAGEVIDEO",
        "reason": "$string:write_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
      }
    ]
  }
}
```

---

## 二、核心功能实战

### 2.1 初始化 ImagePicker

```dart
final ImagePicker _picker = ImagePicker();
XFile? _image; // 选中的图片文件
```

### 2.2 从相册选择图片

在鸿蒙系统上，这会触发系统的 `PhotoViewPicker`：

```dart
Future<void> _pickImageFromGallery() async {
  try {
    final XFile? pickedFile = await _picker.pickImage(
      source: ImageSource.gallery,
      maxWidth: 1000, // 限制宽度减少内存占用
      imageQuality: 85, // 压缩质量
    );
    
    if (pickedFile != null) {
      setState(() {
        _image = pickedFile;
      });
    }
  } catch (e) {
    debugPrint("选择图片错误: $e");
  }
}
```

### 2.3 使用相机拍照

鸿蒙系统会唤起原子的相机拍摄界面：

```dart
Future<void> _takePhoto() async {
  final XFile? photo = await _picker.pickImage(
    source: ImageSource.camera,
  );
  
  if (photo != null) {
    setState(() {
      _image = photo;
    });
  }
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙设备唤起系统相册截图 -->
<!-- 类型: 鸿蒙设备截图 -->
<!-- 内容: 展示调用 pickImage 后，系统原生相册选择器的界面 -->

---

## 三、鸿蒙平台适配细节

### 3.1 临时路径处理

`image_picker` 返回的是一个临时文件路径。在鸿蒙上，这些文件通常存储在应用的 `cache` 目录下。如果你需要持久化存储，请结合 `path_provider` 将其移动到文档目录。

### 3.2 权限动态申请

虽然我们在 `module.json5` 中声明了权限，但在 OpenHarmony Next 中，相机等敏感权限仍需在代码中动态申请。可以结合 `permission_handler` 插件：

```dart
import 'package:permission_handler/permission_handler.dart';

Future<void> checkCameraPermission() async {
  var status = await Permission.camera.status;
  if (status.isDenied) {
    await Permission.camera.request();
  }
}
```

### 3.3 图片类型限制

在鸿蒙系统上，支持常见的 `jpg`、`png` 格式，对于部分特有的 `heif` 格式图片，建议在上传前进行格式转换或使用底层解码器。

---

## 四、完整代码示例

```dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class ImagePickerDemo extends StatefulWidget {
  const ImagePickerDemo({super.key});

  @override
  State<ImagePickerDemo> createState() => _ImagePickerDemoState();
}

class _ImagePickerDemoState extends State<ImagePickerDemo> {
  XFile? _imageFile;
  final ImagePicker _picker = ImagePicker();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 图片选择示例')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _imageFile == null
                ? const Text('尚未选择图片')
                : Image.file(File(_imageFile!.path), height: 300),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => _pickImage(ImageSource.gallery),
              child: const Text('从相册选择'),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () => _pickImage(ImageSource.camera),
              child: const Text('拍照'),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _pickImage(ImageSource source) async {
    final XFile? pickedFile = await _picker.pickImage(source: source);
    if (pickedFile != null) {
      setState(() => _imageFile = pickedFile);
    }
  }
}
```

<!-- IMAGE_PLACEHOLDER: 完整示例运行截图（展示选图后显示的效果） -->
<!-- 类型: 截图 -->
<!-- 内容: 鸿蒙实机运行效果 -->

---

## 五、总结

`image_picker` 的鸿蒙化适配极大地降低了开发者调用多媒体功能的难度。通过合理利用 `dependency_overrides` 和权限管理，我们可以无缝地为鸿蒙用户提供高质量的图库交互体验。

---


 📦 **完整代码已上传至 AtomGit**：[flutter_package_examples](https://atomgit.com/cannonjinx/flutter_package_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
