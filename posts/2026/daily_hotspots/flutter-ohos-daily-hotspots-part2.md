![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战：每日热点 App（二）— 基于 http 的热榜服务封装与异步处理

> **摘要**：在跨平台应用开发中，网络请求是应用与世界连接的桥梁。本文将深入"每日热点"应用的逻辑层，手把手教你如何在 Flutter for OpenHarmony 中配置网络权限、封装高可用的 `http` 服务类，并优雅地处理异步数据流。

## 前言

在[《架构篇》](https://blog.csdn.net/your_link_to_part1)中，我们完成了项目的地基搭建和插件配置。地基打好后，接下来的核心任务就是**让数据流动起来**。

对于一个聚合类 App 来说，网络请求的稳定性、错误处理的健壮性直接决定了用户体验。在鸿蒙系统上，网络请求不仅涉及 Flutter 代码，还涉及原生侧的权限声明。本文将重点攻克这一环。

---

## 一、鸿蒙原生：开启网络访问门票

在鸿蒙系统（HarmonyOS）中，处于安全考虑，应用默认是不具互联网访问权限的。如果你在 Flutter 代码中写好了网络请求但发现报 `SocketException`，通常是因为忘记了在原生配置中“打招呼”。

### 1.1 配置 `module.json5`

打开项目目录下的 `ohos/entry/src/main/module.json5` 文件，在 `module` 节点下增加 `requestPermissions` 声明：

```json5
{
  "module": {
    "name": "entry",
    // ... 其他配置
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET" // 🟢 声明互联网访问权限
      }
    ]
  }
}
```

💡 **注意**：鸿蒙的权限声明需要区分大小写，且必须放在正确的位置，否则应用在真机运行时会无法联网。

---

## 二、封装 `HotBoardService`：让请求更专业

虽然直接在 UI 层调用 `http.get` 很方便，但在中大型项目中，这会导致代码难以维护。我们需要通过 **Service 层** 来隔离网络逻辑。

### 2.1 引入依赖

确保你的 `pubspec.yaml` 中已经包含了 `http` 库：

```yaml
dependencies:
  http: ^1.1.0
```

### 2.2 实现 Service 类

新建 `lib/services/hotboard_service.dart`。我们将在这里统一处理 API 地址、请求头和 JSON 转换。

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/hot_item.dart';

/// 热榜 API 服务中心
class HotBoardService {
  // 数据源来源于 UAPIS 为开源社区提供的标准接口
  static const String _baseUrl = 'https://uapis.cn/api/v1/misc/hotboard';

  /// 获取指定平台的热榜数据
  /// [type] 对应平台 ID，如 weibo, zhihu, bilibili 等
  Future<HotBoardResponse> getHotBoard(String type) async {
    try {
      final uri = Uri.parse('$_baseUrl?type=$type');

      // 模拟移动端 User-Agent，确保接口返回数据的兼容性
      final response = await http.get(
        uri,
        headers: {
          'accept': 'application/json',
          'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
        },
      ).timeout(const Duration(seconds: 10)); // 设置 10 秒超时

      if (response.statusCode == 200) {
        // 使用 utf8 刷新解码，防止中文乱码
        final body = utf8.decode(response.bodyBytes);
        final json = jsonDecode(body) as Map<String, dynamic>;
        
        // 调用上篇定义的 factory 构造函数进行转化
        return HotBoardResponse.fromJson(json);
      } else {
        throw Exception('服务器错误: ${response.statusCode}');
      }
    } catch (e) {
      // 针对异步请求中的各类异常进行捕获
      throw Exception('网络请求失败，请检查网络设置或权限。内容: $e');
    }
  }
}
```

### 2.3 技术细节深度剖析

1.  **User-Agent 模拟**：许多 API 会校验 `user-agent`。即使是鸿蒙端应用，模拟一个通用的移动端 UA 能极大提高抓取的成功率。
2.  **utf8.decode**：直接使用 `response.body` 有时会导致中文出现乱码（特别是 API 返回没有指定 charset 时）。通过 `response.bodyBytes` 手动解码是更稳妥的做法。
3.  **超时控制 (`timeout`)**：在移动端，网络环境不稳定。通过 `.timeout()` 我们可以防止应用在断网或弱网环境下长时间“转圈圈”。

---

## 三、异步状态流的流转逻辑

数据拿到后，如何传递给 UI？在复杂的 App 中，通常有 `加载中 (Loading)`、`数据展示 (Success)`、`请求失败 (Error)` 三种状态。

### 3.1 状态类定义（预习）

在 `_HotBoardPageState` 中，我们需要定义对应的状态变量：

```dart
class _HotBoardPageState extends State<HotBoardPage> {
  final HotBoardService _service = HotBoardService();
  
  // 核心状态变量
  List<HotItem> _hotItems = [];
  bool _isLoading = true;
  String? _error;

  /// 封装的加载方法
  Future<void> _loadData() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final response = await _service.getHotBoard(selectedType);
      setState(() {
        _hotItems = response.list;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }
}
```

🏆 **实战建议**：在这里我们使用了最基础的 `setState`。在第四篇《交互篇》中，我们将展示如何配合动画将这些状态转化成丝滑的界面效果。

---

## 四、鸿蒙平台适配：网络调试技巧

在鸿蒙真机或模拟器上调试网络请求时，有几个关键点需要注意：

### 4.1 HTTPS 强制校验
HarmonyOS 对安全性要求极高。如果你的数据源是 HTTP 而非 HTTPS，除了需要在 `module.json5` 中声明权限外，还需要在项目的 `network.config` 中手动允许不安全连接（Cleartext）。

✅ **推荐做法**：始终使用 HTTPS，避免因为证书校验问题导致请求被鸿蒙底层拦截。

### 4.2 网络波动处理
鸿蒙系统在后台会对高频心跳包和空闲连接进行优化。在编写代码时，我们要养成良好的习惯：**页面销毁时（`dispose`）及时取消未完成的任务。**

---

## 五、中篇总结

本篇文章我们攻克了“每日热点”应用中最核心的“管道”工程：
1.  **开通权限**：在鸿蒙 `module.json5` 中注册了上网许可。
2.  **封装请求**：实现了一个健壮、防乱码、带超时的 Service 类。
3.  **理顺逻辑**：明确了异步数据的流转路径。

现在，我们的 App 已经具备了获取全网数据的能力。但是，目前的数据还只是内存中冰冷的 JSON，如何让它们穿上漂亮的“外衣”？

在下一篇**【视觉篇】**中，我们将开启视觉盛宴，讲解如何实现高颜值的深色模式、流光溢彩的渐变效果，以及鸿蒙风格的骨架屏（Skeleton）加载动画。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-example (主分支)](https://atomgit.com/dragonbady/open-harmony-example/tree/main/examples/daily_hotspots)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
