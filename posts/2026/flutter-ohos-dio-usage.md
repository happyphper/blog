# Flutter for OpenHarmony 实战：网络请求神器 Dio 的基础使用与热榜 API 接入指南

## 前言

在现代移动应用开发中，网络请求是核心功能之一。无论是获取用户信息、展示图片，还是实时更新数据，都离不开一个稳定且高效的 HTTP 客户端。在 Flutter 开发中，`dio` 凭借其强大的功能（如拦截器、全局配置、FormData 支持等）成为了事实上的行业标准。

随着 **OpenHarmony (鸿蒙)** 生态的崛起，如何在该平台上优雅地进行网络请求成为了开发者必须掌握的技能。本文将带你手把手实战，在鸿蒙平台上使用 Dio 接入一个真实的网络热榜接口，涵盖从权限配置到数据解析的全流程。


![Flutter for OpenHarmony Dio 实战](./images/22-dio-cover.png)

---

## 一、为什么在鸿蒙开发中首选 Dio？

在 Flutter for OpenHarmony 的开发环境中，虽然 Dart 原生提供了 `HttpClient`，但我们在实际项目中通常会选择 `dio`，原因如下：

### 1.1 强大的拦截器机制
Dio 支持在请求发送前、响应返回后以及报错时进行拦截处理。这对于鸿蒙应用中常见的全局 Token 注入、统一日志记录和错误上报非常有用。

### 1.2 高度可配置性
通过 `BaseOptions`，我们可以轻松设置 `baseUrl`、超时时间、请求头等公共参数。

### 1.3 跨平台兼容性
Dio 在鸿蒙平台上的表现非常稳定。由于鸿蒙环境下的 Flutter 引擎底层对网络协议栈的支持相对完善，Dio 几乎可以无缝迁移。

![Dio 架构与鸿蒙网络协议栈示意图](./images/22-dio-architecture.png)

---

## 二、环境准备：鸿蒙网络权限与依赖配置

在鸿蒙设备上进行网络请求，第一步不是写代码，而是“申请通行证”。

### 2.1 添加 Dio 依赖

在你的 Flutter 项目根目录下的 `pubspec.yaml` 文件中添加最新版 Dio：

```yaml
dependencies:
  flutter:
    sdk: flutter
  # 💡 技巧：对于大型项目，建议锁定版本以确保鸿蒙端稳定性
  dio: ^5.7.0
```

### 2.2 配置鸿蒙网络权限

鸿蒙系统对安全性有严格要求。你需要在 `ohos/entry/src/main/module.json5` 文件中声明 `ohos.permission.INTERNET` 权限，否则所有网络请求都会被系统拦截。

```json
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET",
        "reason": "$string:reason_internet",
        "usedScene": {
          "abilities": ["EntryAbility"],
          "when": "always"
        }
      }
    ]
  }
}
```

📌 **提醒**：修改权限文件后，建议重新编译工程以确保配置生效。

---

## 三、网络请求实战：接入“查询热榜”接口

我们将接入一个真实的聚合 API（`uapis.cn`），获取各大平台的热搜内容。

### 3.1 接口分析（参考图片）

- **接口地址**：`https://uapis.cn/api/v1/misc/hotboard`
- **请求方法**：`GET`
- **必填参数**：`type`（平台类型，如 `bilibili`、`weibo` 等）
- **响应结构**：包含 `update_time` 和一个 `list` 数组。

### 3.2 封装 Dio 工具类

为了避免在每个页面重复创建 Dio 对象，我们使用单例模式进行封装。

```dart
import 'package:dio/dio.dart';

class HttpManager {
  static final HttpManager _instance = HttpManager._internal();
  late Dio _dio;

  factory HttpManager() => _instance;

  HttpManager._internal() {
    // 💡 技巧：根据鸿蒙设备的网络状况优化超时时间
    BaseOptions options = BaseOptions(
      baseUrl: "https://uapis.cn",
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 5),
      headers: {
        "Content-Type": "application/json",
      },
    );
    _dio = Dio(options);
    
    // 添加日志拦截器，方便在 DevEco Studio 终端调试
    _dio.interceptors.add(LogInterceptor(responseBody: true));
  }

  Future<Response> get(String path, {Map<String, dynamic>? params}) async {
    return await _dio.get(path, queryParameters: params);
  }
}
```

### 3.3 数据模型（Model）定义

手动解析 JSON 容易出错，建议定义 Model 类。

```dart
class HotItem {
  final int index;
  final String title;

  HotItem({required this.index, required this.title});

  factory HotItem.fromJson(Map<String, dynamic> json) {
    return HotItem(
      index: json['index'] ?? 0,
      title: json['title'] ?? '',
    );
  }
}
```

---

## 四、UI 呈现：在鸿蒙页面展示热榜列表

我们使用 `FutureBuilder` 来处理网络请求的异步状态。

<!-- IMAGE_PLACEHOLDER: 鸿蒙手机端热榜接口调试效果 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示调用 bilibili 热榜接口后的 JSON 响应原文 -->

### 4.1 编写展示页面

```dart
class HotBoardPage extends StatefulWidget {
  const HotBoardPage({super.key});

  @override
  State<HotBoardPage> createState() => _HotBoardPageState();
}

class _HotBoardPageState extends State<HotBoardPage> {
  late Future<List<HotItem>> _hotListFuture;

  @override
  void initState() {
    super.initState();
    _hotListFuture = _fetchHotStore();
  }

  // 核心请求逻辑
  Future<List<HotItem>> _fetchHotStore() async {
    try {
      final response = await HttpManager().get(
        "/api/v1/misc/hotboard",
        params: {"type": "bilibili"}, // 也可以换成 weibo 或 zhihu
      );
      
      if (response.statusCode == 200) {
        List list = response.data['list'];
        return list.map((item) => HotItem.fromJson(item)).toList();
      } else {
        throw Exception("接口异常");
      }
    } catch (e) {
      // ⚠️ 注意：鸿蒙环境下需正确处理无网状态
      rethrow;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('哔哩哔哩热榜 - 鸿蒙实战'),
        backgroundColor: Colors.pinkAccent.shade100,
      ),
      body: FutureBuilder<List<HotItem>>(
        future: _hotListFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("数据加载失败: ${snapshot.error}"));
          } else {
            final items = snapshot.data!;
            return ListView.separated(
              itemCount: items.length,
              separatorBuilder: (_, __) => const Divider(),
              itemBuilder: (context, index) {
                return ListTile(
                  leading: CircleAvatar(
                    backgroundColor: Colors.pink,
                    child: Text("${items[index].index}", style: const TextStyle(color: Colors.white)),
                  ),
                  title: Text(items[index].title),
                );
              },
            );
          }
        },
      ),
    );
  }
}
```

---

## 五、鸿蒙平台适配进阶建议

### 5.1 处理 HTTPS 安全验证
鸿蒙对未经过认证的 HTTPS 证书校验非常严格。如果在开发环境下遇到证书问题，可以通过 Dio 的 `onHttpClientCreate` 进行临时处理（仅限测试）：

```dart
(_dio.httpClientAdapter as IOHttpClientAdapter).onHttpClientCreate = (client) {
  client.badCertificateCallback = (cert, host, port) => true;
  return client;
};
```

### 5.2 响应式列表适配
由于鸿蒙设备包含从 6 英寸手机到 12.6 英寸平板的不同形态，建议在展示热榜列表时使用 `LayoutBuilder`。

✅ **推荐做法**：
- 小屏设备：单列显示。
- 大屏设备/折叠屏展开态：双列或宫格显示。

<!-- IMAGE_PLACEHOLDER: 热榜页面在鸿蒙折叠屏上的运行效果 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示左侧展示列表，右侧展示详情的适配效果 -->

---

## 六、完整示例代码

请确保你已经安装了 `dio` 包。

```dart
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(useMaterial3: true),
      home: const HotBoardPage(),
    );
  }
}

// 模型定义与请求逻辑同上一章节...
```

---

## 七、总结

通过本文的实战，我们掌握了如何在 **Flutter for OpenHarmony** 项目中从零开始接入 Dio 开发网络功能。关键点在于：**声明权限、单例封装、优雅解析以及平台适配**。

Dio 的强大远不止于此，在进阶开发中，你还可以结合 `PrettyDioLogger` 进行美观的日志打印，或者使用 `CancelToken` 处理页面的无用网络请求。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/dio_hotboard](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/dio_hotboard)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
