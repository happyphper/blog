欢迎加入开源鸿蒙跨平台社区：[https://openharmonycrossplatform.csdn.net](https://openharmonycrossplatform.csdn.net)

![cover](./images/get_ip_address.png)

# Flutter for OpenHarmony: Flutter 三方库 get_ip_address 快速获取鸿蒙设备的内外网 IP 身份（网络诊断利器）

## 前言

在进行 OpenHarmony 的网络应用开发时，我们经常需要获取设备的 IP 地址：
1. **多端互联**：在鸿蒙分布式组网中，需要知道本地 IP 以建立 Socket 连接。
2. **后台审计**：在用户登录时记录其外网出口 IP，增强账户安全。
3. **网络诊断**：当应用无法联网时，快速判断设备是否已分配到正确的 IP。

**`get_ip_address`** 软件包是一个极其轻量且纯净的工具。它能帮你一键获取全球唯一的公网外网 IP 或局域网内网 IP，是鸿蒙网络层底座中一个虽小但非常实用的“零件”。

---

## 二、核心 API 实战

### 2.1 获取公网外网 IP

通过访问全球各地的 IP 反查节点，自动提取设备出口 IP。

```dart
import 'package:get_ip_address/get_ip_address.dart';

void fetchPublicIp() async {
  try {
    /// 💡 调用全球 IP 探测服务
    var ipAddress = IpAddress(type: RequestType.json);
    dynamic data = await ipAddress.getIpAddress();
    
    print('鸿蒙设备公网 IP: ${data['ip']}');
    print('所在地区: ${data['country']}');
  } catch (e) {
    print('获取失败: $e');
  }
}
```

### 2.2 获取局域网内网 IP (结合 Dart IO)

```dart
import 'dart:io';

Future<String> getLocalIp() async {
  for (var interface in await NetworkInterface.list()) {
    for (var addr in interface.addresses) {
      if (addr.type == InternetAddressType.IPv4) {
        return addr.address;
      }
    }
  }
  return '127.0.0.1';
}
```

---

## 三、常见应用场景

### 3.1 鸿蒙分布式文件传输指引
在鸿蒙手机尝试向电视投屏或传输文件时，通过该库获取本地 IP 并生成一个临时的 HTTP 地址或二维码。另一台设备扫码后即可通过 IP 指向进行高速传输，无需经过云端中转。

### 3.2 鸿蒙应用防刷与安全控制
在进行关键操作（如领取红包、重置密码）时，通过 `get_ip_address` 获取实时 IP。如果发现 IP 归属地与常用地严重不符，鸿蒙应用可以自动弹出人机验证（CAPTCHA），多加一层安全栅栏。

---

## 四、OpenHarmony 平台适配

### 4.1 适配鸿蒙的权限声明
💡 **技巧**：要在鸿蒙设备上通过外网服务探测 IP，必须在 `module.json5` 中声明 `ohos.permission.INTERNET` 权限。同时，该库默认访问的可能是一些国际常用的 IP 探测节点，在开发针对国内市场的鸿蒙应用时，建议通过配置将其指向国内延迟更低的 API 节点，从而缩短网络解析过程中的等待时长。

### 4.2 处理网络切换时的 IP 刷新
在鸿蒙物理设备上，用户可能会频繁在 Wi-Fi 和 5G 之间切换。`get_ip_address` 的调用应当具有“被动触发”机制。通过监听鸿蒙系统的网络状态变更事件，当网络从 4G 切换到 Wi-Fi 后，自动重置一次 IP 探测逻辑，确保鸿蒙应用内显示的身份信息永远与当前最新的物理链路同步。

---

## 五、完整实战示例：鸿蒙工程“网联审计”工具

本示例展示如何构建一个能够同时反馈内外网信息的网络诊断器。

```dart
import 'package:get_ip_address/get_ip_address.dart';

class OhosNetInfoProvider {
  /// 💡 一键审计鸿蒙当前网络拓扑
  Future<void> auditNetwork() async {
    print('🔍 正在启动鸿蒙网络链路审计...');
    
    final ipProvider = IpAddress();
    
    try {
      final publicIp = await ipProvider.getIpAddress();
      print('--- 审计报告 ---');
      print('🌐 公网出口: ${publicIp['ip']}');
      print('📍 地理定位: ${publicIp['city']}');
    } catch (e) {
      print('外网审计探测失败');
    }
  }
}

void main() async {
  final provider = OhosNetInfoProvider();
  await provider.auditNetwork();
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙手机中心显示当前实时 IP、地理归属地以及网络供应商（ISP）信息的极简风面板截图 -->

---

## 六、总结

`get_ip_address` 软件包是 OpenHarmony 开发者打理“网络身份”的数字名片。它以极低的代码量实现了原本复杂的网络探测逻辑。在构建万物互联、强调分布式协作的鸿蒙原生应用生态中，清晰定位每一台设备的“经纬度（IP）”，是你实现全栈智能化、全链路安全管控的坚实第一步。
