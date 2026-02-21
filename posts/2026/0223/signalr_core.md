欢迎加入开源鸿蒙跨平台社区：[https://openharmonycrossplatform.csdn.net](https://openharmonycrossplatform.csdn.net)。

# Flutter for OpenHarmony：signalr_core — 实现高性能实时双向通信

## 前言

在现代移动应用中，实时通信已成为不可或缺的能力。无论是实时聊天、在线协作办公、甚至是股票行情的瞬时同步，都需要一套能够在服务端与客户端之间保持长连接且支持双向推送的机制。

ASP.NET Core SignalR 是一套成熟的实时通信方案，而 `signalr_core` 则是其在 Flutter 端的轻量级核心实现。在 **Flutter for OpenHarmony** 开发中，通过该库我们可以打破传统的 HTTP 轮询模式，在鸿蒙系统上构建极致流畅的实时交互体验。

## 一、实时通信的新高度

### 1.1 什么是 SignalR？
SignalR 是一个简化了在应用中添加实时 Web 功能过程的库。它允许服务器代码向连接的客户端即时推送内容。

### 1.2 为什么在鸿蒙开发中使用它？
- **自动降级机制**：SignalR 会自动选择最佳传输方式（WebSockets、Server-Sent Events 或 Long Polling），适应不同鸿蒙网络环境。
- **纯 Dart 核心**：`signalr_core` 抛弃了臃肿的依赖，针对移动端进行了深度优化，完全兼容鸿蒙内核。
- **高度抽象**：开发者只需关注业务 Hub，无需操心底层的 Socket 握手与重连。

### 1.3 通信链路模型（Mermaid）

```mermaid
graph LR
    A[鸿蒙客户端 App] <-->|SignalR 协议| B[信号分发 Hub]
    B <-->|RPC 呼叫| C[后端业务逻辑系统]
    A -- 发送消息 --> B
    B -- 推送更新 --> A
    style B fill:#8e44ad,color:white
    style A fill:#2980b9,color:white
```

## 二、核心 API 与功能讲解

### 2.1 引入依赖
在 `pubspec.yaml` 中配置：

```yaml
dependencies:
  # SignalR 核心通讯组件
  signalr_core: ^1.2.1
```

### 2.2 建立长连接
在鸿蒙应用启动或特定页面进入时初始化连接。

```dart
import 'package:signalr_core/signalr_core.dart';

Future<void> initSignalR() async {
  // 💡 配置连接参数
  final connection = HubConnectionBuilder()
    .withUrl('https://your-ohos-api.com/chatHub', HttpConnectionOptions(
      logging: (level, message) => print('SignalR 日志: $message'),
    ))
    .build();

  // 💡 监听连接关闭事件
  connection.onclose((error) => print('连接已断开，正在尝试重连...'));

  // 💡 启动连接
  await connection.start();
}
```

### 2.3 发送与接收数据
实现真正的双向互动。

```dart
// 🎨 在鸿蒙应用中监听服务器推送的消息
connection.on('ReceiveMessage', (arguments) {
  final user = arguments?[0];
  final msg = arguments?[1];
  print('来自 $user 的新消息: $msg');
});

// 🎨 向服务器 Hub 发送消息（RPC 模式）
void sendMessage() async {
  await connection.invoke('SendMessage', args: ['鸿蒙用户A', '你好！']);
}
```

## 三、鸿蒙应用实战场景

### 3.1 场景一：分布式办公实时文档
利用鸿蒙平板的大屏优势，结合 `signalr_core` 实现多人同屏实时编辑预览，每一次按键都能瞬间同步到所有协助终端。

### 3.2 场景二：后台实时监控监控系统
在工业鸿蒙平板或车载平板上，实时接收服务器推送的传感器遥测数据（Telemetry），结合仪表盘快速响应状态变更。

<!-- IMAGE_PLACEHOLDER: [SignalR 在鸿蒙设备上的实时聊天界面截图] -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->
<!-- 内容: 展示一个实时对讲界面，每条消息进入时都有顺滑的列表动画 -->

## 四、OpenHarmony 平台适配建议

### 4.1 保持后台连接
鸿蒙系统对后台长连接有较为严格的限制。
- **✅ 建议**：如果业务需要应用在切到后台后依然保持实时性，建议配合鸿蒙原生的 `ContinuousTask`（延续任务）注册。否则，断开连接后应通过鸿蒙原生的通知推送（Push Kit）来补偿即时消息。

### 4.2 网络环境自适应
- **📌 提醒**：鸿蒙设备在切换 Wi-Fi/4G/5G 时会发生网络状态偏转。务必配合 `connectivity_plus` 库，在检测到网络恢复时通过 `connection.start()` 手动重新激活 SignalR 通道。

### 4.3 性能资源消耗
- **⚠️ 警告**：长连接会显著增加系统的无线射频（Radio）唤醒频率，从而增加功耗。在非必要的实时场景下，可以通过 `connection.stop()` 及时释放资源，践行鸿蒙绿色应用的开发规范。

## 五、完整示例代码

演示一个实时数据刷新的鸿蒙仪表盘。

```dart
import 'package:flutter/material.dart';
import 'package:signalr_core/signalr_core.dart';

void main() => runApp(const MaterialApp(home: SignalRLab()));

class SignalRLab extends StatefulWidget {
  const SignalRLab({super.key});

  @override
  State<SignalRLab> createState() => _SignalRLabState();
}

class _SignalRLabState extends State<SignalRLab> {
  late HubConnection _connection;
  String _serverTime = '正在建立实时连接...';

  @override
  void initState() {
    super.initState();
    _connect();
  }

  void _connect() async {
    _connection = HubConnectionBuilder()
        .withUrl('https://api.test.ohos.com/timeHub')
        .build();

    await _connection.start();

    // ✅ 实战：监听服务器推送的时间信号
    _connection.on('UpdateTime', (args) {
      setState(() {
        _serverTime = '服务器实时时间: ${args?[0]}';
      });
    });
  }

  @override
  void dispose() {
    _connection.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('signalr_core 实时实验室')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.flash_on, size: 60, color: Colors.amber),
            const SizedBox(height: 20),
            Text(_serverTime, style: const TextStyle(fontSize: 18)),
          ],
        ),
      ),
    );
  }
}
```

## 六、总结

`signalr_core` 为 **Flutter for OpenHarmony** 应用插上了实时的翅膀。它将复杂的长连接管理、协议选择、自动重连等底层逻辑高度精炼，让开发者能像调用同步函数一样处理异步推送。

核心要点回顾：
1. **自动降级传输**：WebSocket 优先，多网络兼容。
2. **RPC 调用模型**：两端调用就像本地函数一样自然。
3. **鸿蒙适配**：重视网络状态感知，合理利用系统后台任务能力。
4. **性能管控**：避免无效长连接占用由于射频资源引发的电量消耗。

让每一个鸿蒙应用，都能拥有瞬时响应、跨屏同步的超链接能力！

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/signalr_core](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/signalr_core)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
