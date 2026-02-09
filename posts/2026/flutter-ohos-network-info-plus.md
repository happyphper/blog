---
title: "Flutter for OpenHarmony 实战：network_info_plus 网络扫描与隐私合规深度适配"
date: 2026-02-08
tags: ["Flutter", "OpenHarmony", "network_info_plus", "IP地址", "安全合规"]
categories: ["Flutter for OpenHarmony 实战"]
---
# Flutter for OpenHarmony 实战：network_info_plus 网络扫描与隐私合规深度适配

![封面图](images/cover_flutter_ohos_network_info_plus.png)

## 前言

做 IoT（物联网）配网、局域网文件互传（类似华为分享）、或简单的 WiFi 测速 App 时，我们需要获取当前连接的 **WiFi SSID (名称)**、**BSSID (Mac 地址)** 以及本机的 **IP 地址**。

但在 **HarmonyOS NEXT** 这个极其看重隐私合规的系统中，SSID 已经不再是一个简单的字符串，它被视为用户的**物理轨迹隐私**。如果应用在未授权情况下频繁扫描网络，将面临应用商店下架的风险。`network_info_plus` 插件为我们封装了跨平台的调用逻辑，但在鸿蒙上落地，你还需要处理一些特有的权限“潜规则”。

---

## 一、 深度视角：WiFi 信息为何与位置挂钩？

### 1.1 “WiFi 列表 == 地理位置”
鸿蒙系统（以及 Android 12+）遵循一套安全原则：由于全球绝大部分 WiFi AP 的地理位置已被云端数据库索引，通过获取 BSSID (Mac 地址)，应用可以推算出误差在 50 米内的位置。
因此，在鸿蒙上获取网络详情，本质上是对 **` ohos.permission.LOCATION`** 的挑战。

### 1.2 鸿蒙 API 12+ 的隐私变更
- **SSID 屏蔽**：若未开启系统 GPS 开关且未授予精确位置权限，API 将返回 `<unknown ssid>`。
- **IP 格式**：鸿蒙底层同时支持 IPv4 和 IPv6，插件会自动选择当前活跃的本地 IP。

<!-- IMAGE_PLACEHOLDER: 鸿蒙 WiFi 获取授权决策流图 -->
<!-- 类型: 流程图 -->
<!-- 内容: 展示权限状态、GPS 开关状态对 SSID 返回值的影响 -->

---

## 二、 工程实战：合规的“全家桶”申请策略

在鸿蒙上，你不能只申请一个权限。为了保证 API 返回真实数据，你需要以下三位一体的组合：

### 2.1 权限组合配置 (module.json5)
```json5
"requestPermissions": [
  { "name": "ohos.permission.GET_WIFI_INFO" },       // 基础网络层信息
  { "name": "ohos.permission.LOCATION" },             // 💡 必需！获取 SSID/BSSID 的钥匙
  { "name": "ohos.permission.APPROXIMATELY_LOCATION" } // 伴随精确位置一起申请
]
```

### 2.2 优雅的权限检查代码
```dart
Future<void> initNetworkScan() async {
  // 1. 先检查 Wi-Fi 管理权限
  if (await Permission.location.request().isGranted) {
    // 2. 只有位置权限也被授予，SSID 才不会返回 <unknown>
    final info = NetworkInfo();
    final ssid = await info.getWifiName();
    print('当前连接的 WiFi: $ssid');
  } else {
    // 🔔 告知用户：不授权位置权限，我们就没法帮你完成配网哦
  }
}
```

---

## 三、 高级应用场景：智能投屏子网校验

在构建局域网投屏功能时，第一步是判断手机与电视是否在同一个网段。

### 3.1 同子网判断逻辑
```dart
Future<bool> isSameSubnet(String deviceIp) async {
  final info = NetworkInfo();
  final myIp = await info.getWifiIP(); // e.g., 192.168.3.15
  if (myIp == null) return false;

  final myPrefix = myIp.substring(0, myIp.lastIndexOf('.'));
  final devicePrefix = deviceIp.substring(0, deviceIp.lastIndexOf('.'));
  
  return myPrefix == devicePrefix; // 判断 C 段是否一致
}
```

### 3.2 监听网络状态变更
配合 `connectivity_plus` 使用，每当用户切换 WiFi，自动刷新 `NetworkInfo`：
```dart
Connectivity().onConnectivityChanged.listen((result) {
  if (result == ConnectivityResult.wifi) {
    refreshWifiDetails();
  }
});
```

---

## 四、 鸿蒙环境下的避坑指南 (FAQ)

### 4.1 为什么一直返回 `<unknown ssid>`？
**自查清单**：
1. **是否在真机运行？** 鸿蒙模拟器由于共享宿主网络，往往无法返回真实的 WiFi 链路信息。
2. **系统 GPS 开关开了吗？** 即使给了应用权限，如果下拉控制中心的“位置信息”总开关是关的，SSID 依然被屏蔽。
3. **API 20 的特殊性**：针对 API 20 以后的 SDK，建议显式设置请求频率，避免被系统判定为“恶意扫描”。

### 4.2 IPv6 地址解析
**挑战**：`getWifiIP` 有时会返回一段长长的十六进制地址。
**方案**：在业务逻辑中，对返回结果进行正则校验，优先过滤出符合 `^([0-9]{1,3}\.){3}[0-9]{1,3}$` 格式的 IPv4 地址。

---

## 五、 完整示例代码

以下代码演示了如何在鸿蒙应用中获取并展示当前连接的 WiFi 详细信息：

```dart
import 'package:flutter/material.dart';
import 'package:network_info_plus/network_info_plus.dart';

class NetworkInfoDemo extends StatefulWidget {
  const NetworkInfoDemo({super.key});

  @override
  State<NetworkInfoDemo> createState() => _NetworkInfoDemoState();
}

class _NetworkInfoDemoState extends State<NetworkInfoDemo> {
  final NetworkInfo _networkInfo = NetworkInfo();
  String _wifiName = "正在获取...";
  String _wifiIP = "正在获取...";

  @override
  void initState() {
    super.initState();
    _loadNetworkInfo();
  }

  Future<void> _loadNetworkInfo() async {
    final wifiName = await _networkInfo.getWifiName();
    final wifiIP = await _networkInfo.getWifiIP();

    setState(() {
      _wifiName = wifiName ?? "未连接或权限不足";
      _wifiIP = wifiIP ?? "未知";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('鸿蒙网络信息实战')),
      body: Center(
        child: Card(
          margin: const EdgeInsets.all(20),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.wifi, size: 60, color: Colors.blue),
                const SizedBox(height: 20),
                Text('当前 WiFi: $_wifiName', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 10),
                Text('本地 IP 地址: $_wifiIP'),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: _loadNetworkInfo,
                  child: const Text('刷新网络状态'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙手机显示当前 WiFi 名称及其内网 IP 地址的截图 -->
<!-- 内容: 展示 Card 布局中清晰的网络详情，体现信息获取的准确性 -->

## 六、 总结

`network_info_plus` 虽然只是一个小小的插件，但它牵动着鸿蒙最核心的隐私机制。对于 IoT 和工具类应用开发者，处理好 **“权限引导 -> 隐私合规 -> 数据解析”** 这一闭环，是打造极致用户体验的基石。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/network_info_plus](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/flutter-ohos-network-info-plus)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
