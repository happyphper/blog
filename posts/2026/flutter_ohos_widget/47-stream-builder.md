# Flutter for OpenHarmony 实战之基础组件：第四十七篇 StreamBuilder — 掌握流式数据的即时渲染

## 前言

如果说 `Future` 代表了一份等待送达的单次快递，那么 `Stream`（流）就是一套实时输送的水管系统。在处理诸如股票行情实时更新、聊天室消息推送、甚至是传感器数据采集等高频、持续变化的数据时，`Stream` 是 Flutter 中数据处理的核心武器。

在 **Flutter for OpenHarmony** 开发中，`StreamBuilder` 允许我们监听这些持续不断的数据流，并根据每一条新波动的脉冲实时刷新 UI。本文将深入讲解 `StreamBuilder` 的使用模式，并演示一个基于“秒表计时器”的流式数据实战。

---

## 一、Stream vs Future：核心逻辑差异

- **Future**：只能接收一次结果（要么成功，要么失败）。就像请求一个网页。
- **Stream**：可以持续不断地接收结果。就像看一场实时直播。

`StreamBuilder` 会在监听到流中有新数据（Event）抛出时，立即触发其 `builder` 函数进行局部刷新。

---

## 二、实战演练：流式计数器系统的构建

我们将构建一个每秒更新一次的倒计时/计时系统，模拟鸿蒙端后台持续任务的数据反馈。

### 2.1 创建数据流 (Stream)
```dart
Stream<int> counterStream() async* {
  int count = 0;
  while (true) {
    await Future.delayed(const Duration(seconds: 1));
    yield ++count; // 持续吐出新数据
  }
}
```

### 2.2 使用 StreamBuilder 渲染
```dart
StreamBuilder<int>(
  stream: counterStream(),
  builder: (BuildContext context, AsyncSnapshot<int> snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
       return const Text("正在连接流...");
    }
    
    if (snapshot.hasError) {
       return Text("流出错: ${snapshot.error}");
    }
    
    // 核心：每当流中有 yield 产生，这里的数据就会由快照 snapshot.data 提供
    return Text(
      "累计在线时长: ${snapshot.data} 秒",
      style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
    );
  },
)
```

<!-- IMAGE_PLACEHOLDER: StreamBuilder 实现的实时秒表在鸿蒙设备上的运行动图 -->
<!-- 类型: GIF -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、进阶：管理 WebSocket 或持久监听

对于真实的业务场景（如聊天），我们通常会维护一个 `StreamController`。

```dart
final StreamController<String> _chatController = StreamController<String>();

// 发送消息
void _sendMessage(String msg) {
  _chatController.sink.add(msg);
}

// 别忘了销毁流控制器，防止内存泄漏
@override
void dispose() {
  _chatController.close();
  super.dispose();
}
```

---

## 四、OpenHarmony 平台适配建议

### 4.1 传感器流数据与刷新率
鸿蒙设备搭载了丰富的传感器（加速度、陀螺仪）。

✅ **推荐方案**：
通过 `StreamBuilder` 监听传感器数据流。由于传感器推送速率极高，建议在数据进入 `Stream` 前使用 `buffer` 或 `throttleTime` 进行节流处理。这样既能保持 UI 的实时性，又能避免鸿蒙系统因频繁重建 UI 导致的过度功耗。

### 4.2 路由切换时的流管控
当流所在的页面在鸿蒙系统中被置于后台或在 Tab 切换中不可见。

💡 **调优建议**：
如果 `Stream` 正在进行高宽带操作（如通过 Socket 接收视频二进制流），建议利用 `onVisibilityChanged` 或是路由监听。当页面不可见时，暂停流监听（Pause），可见时再继续（Resume）。

### 4.3 连接状态语义化
鸿蒙系统对网络状态变更（Active 到 Done）反馈非常敏感。

✅ **最佳实践**：
要在 `builder` 中精确区分 `ConnectionState.active`（流处于活跃发送状态）和 `ConnectionState.done`（流已关闭）。对于已经关闭的流，在鸿蒙端的 UI 上应给予明确的“连接已断开”提示。

<!-- IMAGE_PLACEHOLDER: 鸿蒙应用在监控传感器数据波动时的 Stream 曲线预览 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 五、完整示例代码

以下代码演示了一个带有“动态添加消息”功能的即时通讯流模型示例。

```dart
import 'package:flutter/material.dart';
import 'dart:async'; // 核心：使用 Stream 必须引入

void main() => runApp(const MaterialApp(home: LiveDataPage()));

class LiveDataPage extends StatefulWidget {
  const LiveDataPage({super.key});

  @override
  State<LiveDataPage> createState() => _LiveDataPageState();
}

class _LiveDataPageState extends State<LiveDataPage> {
  // 1. 定义一个控制 String 类型数据的流控制器
  final StreamController<List<String>> _msgController = StreamController<List<String>>();
  final List<String> _history = [];

  void _addNewMessage() {
    String newMsg = "来自鸿蒙系统的消息 #${_history.length + 1}";
    _history.insert(0, newMsg); // 模拟新消息排在前面
    _msgController.sink.add(_history); // 将新列表灌入流中
  }

  @override
  void dispose() {
    _msgController.close(); // 2. 页面销毁前必须关闭流，避免鸿蒙内存泄漏
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 即时通讯流实战')),
      floatingActionButton: FloatingActionButton(
        onPressed: _addNewMessage,
        child: const Icon(Icons.send),
      ),
      body: StreamBuilder<List<String>>(
        stream: _msgController.stream, // 3. 关联流控制器的流对象
        initialData: const [], // 初始占位数据
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting && snapshot.data!.isEmpty) {
            return const Center(child: Text("等待第一条消息推送..."));
          }

          final msgs = snapshot.data!;
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: msgs.length,
            itemBuilder: (context, index) => Card(
              color: Colors.blue[50],
              margin: const EdgeInsets.only(bottom: 12),
              child: ListTile(
                leading: const Icon(Icons.chat_bubble_outline, color: Colors.blue),
                title: Text(msgs[index]),
                trailing: Text(DateTime.now().toString().split(' ').last.substring(0, 5)),
              ),
            ),
          );
        },
      ),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的动态交互体系中，`StreamBuilder` 是处理“变动性数据”的重型武器。

1.  **即时响应**：流中一有气泡产生，UI 立即精准跟随。
2.  **生命周期**：一定要管控好 `StreamController` 的开启与闭合，防止鸿蒙设备资源白白耗费。
3.  **多态处理**：通过 `snapshot` 处理好等待、正常、错误以及完成的所有语义状态。

掌握了 `StreamBuilder`，你就能在鸿蒙生态中构建出极具动态呼吸感的高性能实时应用。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

