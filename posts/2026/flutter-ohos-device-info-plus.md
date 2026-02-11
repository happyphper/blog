---
title: "Flutter for OpenHarmony 实战：device_info_plus 精准获取鸿蒙设备参数"
date: 2026-02-09
tags: ["Flutter", "OpenHarmony", "device_info_plus", "设备信息", "系统版本"]
categories: ["Flutter for OpenHarmony 实战"]
---

# Flutter for OpenHarmony 实战：device_info_plus 精准获取鸿蒙设备参数

![封面图](images/cover_flutter_ohos_device_info.png)

## 前言

在进行 **HarmonyOS NEXT** 适配时，我们经常需要回答这样一个问题：当前 App 是运行在华为 Mate 60 Pro 手机上，还是在一台鸿蒙平板电脑上？系统版本是首个全自研正式版还是开发测试版？

获取这些硬件与系统维度的“身份标识”，是实现差异化体验、数据埋点以及 Bug 追踪的基础。**`device_info_plus`** 插件通过原生插件体系，为我们打通了获取鸿蒙设备底层参数的通道。

---

---

## 一、 device_info_plus 在鸿蒙端的角色

### 1.1 精准的硬件“用户画像”
在 **HarmonyOS NEXT** 的星辰大海中，设备形态极其多样。`device_info_plus` 可以告诉你该设备是品牌旗舰（如 Mate 60 系列）还是大屏生产力工具（MatePad）。通过获取 `marketName`，开发者可以针对不同档位的硬件性能，自适应地开启或关闭复杂的着色器动效。

### 1.2 系统鉴权与合规性检查
鸿蒙系统迭代飞快。通过获取 `osFullName` 和 `sdkApiVersion`，我们可以精准判断当前运行环境是开发者预览版还是商用正式版，从而动态调整 App 的安全策略或 API 调用链路。

### 1.3 解决多端适配的“最后一公里”
尤其对于折叠屏（Foldables）设备，判断 `productModel` 有助于我们在 Flutter 侧提前预载针对性侧边导航或双栏布局，确保 UI 切换过程中的无感平滑。

---

## 二、 技术内幕：鸿蒙特有的设备信息字段映射

在鸿蒙端调用 `deviceInfo.ohosInfo` 返回的是 `OhosDeviceInfo` 对象。以下是几个极其重要且具有鸿蒙特色的字段解析：

| 字段名 | 含义 | 鸿蒙实战价值 |
| :--- | :--- | :--- |
| **`osFullName`** | 操作系统全称 | 用于展示“关于”页面，体现鸿蒙纯血身份 |
| **`displayVersion`** | 用户可见的版本号 | 辅助排查用户反馈的 Bug 归属于哪个具体补丁包 |
| **`sdkApiVersion`** | 系统 API 级别 | 判断是否支持特定的鸿蒙原生功能（如分布式软总线） |
| **`productModel`** | 内部产品代号 | 识别设备的具体物理规格（如是否支持手写笔） |

---

## 三、 集成指南

### 2.1 添加依赖
```yaml
dependencies:
  device_info_plus: ^12.3.0
```

---

---

## 四、 实战：构建鸿蒙全场景设备探测引擎

### 4.1 核心获取代码 (适配 OhosDeviceInfo)

```dart
import 'package:device_info_plus/device_info_plus.dart';

final DeviceInfoPlugin deviceInfo = DeviceInfoPlugin();

Future<void> getOhosInfo() async {
  // 💡 提示：OhosDeviceInfo 仅在鸿蒙平台可用
  if (Platform.isOHOS) {
    final ohosInfo = await deviceInfo.ohosInfo;
    
    print('市场名称: ${ohosInfo.marketName}'); // 如：HUAWEI Mate 60 Pro
    print('版本全称: ${ohosInfo.osFullName}'); 
    print('硬件特征: ${ohosInfo.hwApiVersion}');
    
    // 💡 亮点：识别当前是否为鸿蒙平板模式
    bool isTablet = ohosInfo.deviceType == 'tablet';
  }
}
```

### 4.2 场景进阶：基于型号的折叠屏布局适配
如果我们检测到是特定的折叠屏型号，可以动态调整 Flutter 的逻辑：

```dart
Future<void> adaptiveLayout() async {
  final info = await DeviceInfoPlugin().ohosInfo;
  // 💡 技巧：根据型号特定的代号判断特定的 UI 策略
  if (info.productModel.contains('ALT')) {
    loadFoldableWideLayout();
  } else {
    loadStandardPhoneLayout();
  }
}
```

---

## 四、 鸿蒙平台的适配建议

### 4.1 隐私与 ID 限制
在 **HarmonyOS NEXT** 中，出于隐私保护，像原始 IMEI 或 MAC 地址这类硬件唯一标识通常是不允许（或需要极高权限）获取的。`device_info_plus` 提供的是符合系统规范的基础信息。如果需要唯一标识，建议结合 `id` 字段并配合业务测的混淆算法。

### 4.2 处理模拟器与真机差异
在鸿蒙模拟器上运行时，部分硬件参数（如 `board` 或 `manufacturer`）可能会返回 "unknown" 或特定的模拟器标志。在编写业务代码时，务必做好空值或异常值的兜底：
```dart
final model = ohosInfo.productModel ?? '未知设备';
```

---

## 五、 完整示例代码

以下演示了一个“鸿蒙硬件配置详情页”，实时展示当前运行环境：

```dart
import 'package:flutter/material.dart';
import 'package:device_info_plus/device_info_plus.dart';

class DeviceInfoPage extends StatefulWidget {
  const DeviceInfoPage({super.key});

  @override
  State<DeviceInfoPage> createState() => _DeviceInfoPageState();
}

class _DeviceInfoPageState extends State<DeviceInfoPage> {
  Map<String, dynamic> _deviceData = {};

  @override
  void initState() {
    super.initState();
    _initDeviceInfo();
  }

  Future<void> _initDeviceInfo() async {
    final deviceInfo = DeviceInfoPlugin();
    // 💡 提示：在实际鸿蒙环境，这里会返回 ohosInfo 对象
    // 本文代码通过通用方式演示其通用属性获取
    try {
      final info = await deviceInfo.deviceInfo;
      setState(() {
        _deviceData = info.data;
      });
    } catch (e) {
      debugPrint("获取设备信息失败: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('鸿蒙设备信息探测器')),
      body: _deviceData.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              children: _deviceData.keys.map((key) {
                return ListTile(
                  title: Text(key, style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text('${_deviceData[key]}'),
                  leading: const Icon(Icons.info_outline, color: Colors.blue),
                );
              }).toList(),
            ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙手机显示的系统型号、内核版本以及 API 级别的详细列表截图 -->
<!-- 内容: 展示如何通过插件提取鸿蒙原子系统的底层元数据 -->

## 七、 总结

获取设备信息是 App “精细化运营”的第一步。通过 `device_info_plus` 对鸿蒙平台的深度支持，我们能够写出更懂用户设备的代码。在折叠屏手机、平板、智慧屏组成的鸿蒙全场景生态下，利用好这些参数，将助你打造出极致适配的跨端体验。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/flutter-ohos-device-info-plus](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/flutter-ohos-device-info-plus)
> 
> 🔗 **相关阅读推荐**：
> - [鸿蒙设备属性获取原生 API (deviceInfo) 规范](https://developer.huawei.com/consumer/cn/doc/harmonyos-references/js-apis-device-info-0000001774281358)
> - [鸿蒙应用隐私保护与标识符使用原则](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/privacy-protection-0000001774120158)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
