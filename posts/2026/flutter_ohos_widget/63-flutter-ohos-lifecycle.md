# Flutter for OpenHarmony 实战之基础组件：第六十三篇 生命周期监听 — 精准掌控应用的前后台状态

## 前言

作为移动开发者，你一定遇到过这些场景：用户接了个电话，应用进入后台，这时你应该暂停视频播放或停止传感器轮询以省电；当用户重新回到应用，你需要刷新数据或检查剪贴板。

在 **Flutter for OpenHarmony** 开发中，精准识别应用及组件的“生命周期（Lifecycle）”是写出健壮、省电程序的关键。本文将带大家深入掌握如何通过 `AppLifecycleListener` 和 `WidgetsBindingObserver` 监听鸿蒙系统上应用的状态流。

---

## 一、Flutter 应用的五大生命周期状态

在鸿蒙系统底层，应用状态会映射到 Flutter 层的 `AppLifecycleState` 枚举：
1.  **resumed**：应用可见且可交互（用户在使用）。
2.  **inactive**：应用可见但不可交互（如正在下拉通知中心）。
3.  **hidden**：应用所有窗口完全隐藏（新版 Flutter 引入）。
4.  **paused**：应用进入后台（不可见、不交互）。
5.  **detached**：引擎正在解除连接（即将关闭）。

---

## 二、实战演练：监听全屏变化

### 2.1 使用 WidgetsBindingObserver
这是最经典的方式，适合在 `StatefulWidget` 中维护逻辑。

```dart
class _MyPageState extends State<MyPage> with WidgetsBindingObserver {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this); // 注册监听
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this); // 注销监听，防止内存泄漏
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused) {
      print("应用已进入鸿蒙后台，暂停视频...");
    } else if (state == AppLifecycleState.resumed) {
      print("欢迎回来，恢复数据加载...");
    }
  }
}
```

### 2.2 使用 AppLifecycleListener (Flutter 3.13+)
新版本提供了更声明式的 API，能够精细区分“即将进入”和“已进入”状态。

---

## 三、进阶：页面级可见性监听 (VisibilityDetector)

💡 **技巧补充**：有时我们不是想知道整个应用是否进入后台，而是想知道某个具名页面在 `Navigator` 栈中是否被盖住了。

对于这种情况，推荐使用 `VisibilityDetector` 插件或结合 `RouteObserver` 实现。

<!-- IMAGE_PLACEHOLDER: 鸿蒙手机在多任务切换界面展示应用处于“被覆盖/暂停”状态的示意图 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 节省鸿蒙设备的功耗
鸿蒙系统（HarmonyOS）对后台进程的管控非常严格。

✅ **推荐方案**：
当监听到 `state == AppLifecycleState.paused` 时，务必停止所有的 `Timer` 计时器、`Stream` 传感器监听以及高频动画（AnimationController）。这不仅能提升鸿蒙设备的续航，还能降低由于后台活跃度过高被系统“强杀”的风险。

### 4.2 处理大屏/折叠屏的分屏状态
由于鸿蒙支持平行视界。

💡 **调优建议**：
在分屏模式下，当用户点击了另一侧的窗口，你的应用可能会进入 `inactive` 状态。此时应用依然可见，不应暂停所有 UI 动效，但可以降低请求频率。针对折叠屏形态切换，`resumed` 状态会保持，但 `didChangeMetrics` 会触发，建议结合这两个回调同步进行 UI 重排。

### 4.3 状态恢复 (Restoration)
用户在鸿蒙多任务视图中关闭应用后再重新进入。

✅ **最佳实践**：
虽然生命周期只能告诉我们状态，但建议在 `paused` 时将当前关键业务状态（如表单填写进度）立即持久化。当应用再次回到 `resumed` 时进行状态恢复，极大地提升用户对鸿蒙应用稳定性的信心。

<!-- IMAGE_PLACEHOLDER: 鸿蒙分屏状态下，两个应用生命周期交替变化的逻辑流图 -->
<!-- 类型: 截图 -->
<!-- 设备: 模拟器 -->

---

## 五、完整示例代码

以下代码实现了一个带有“自动暂停计时器”功能的生命周期感应页面。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: LifecycleDemo()));

class LifecycleDemo extends StatefulWidget {
  const LifecycleDemo({super.key});

  @override
  State<LifecycleDemo> createState() => _LifecycleDemoState();
}

class _LifecycleDemoState extends State<LifecycleDemo> with WidgetsBindingObserver {
  String _lastState = "正在监听...";
  int _timerCount = 0;
  bool _isPaused = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _startTimer();
  }

  void _startTimer() {
    Future.doWhile(() async {
      await Future.delayed(const Duration(seconds: 1));
      if (!mounted) return false;
      if (!_isPaused) {
        setState(() => _timerCount++);
      }
      return true;
    });
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    setState(() {
      _lastState = state.toString();
    });

    // 逻辑：进入非 resumed 状态时暂停逻辑运算
    if (state != AppLifecycleState.resumed) {
      _isPaused = true;
    } else {
      _isPaused = false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 生命周期实战')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.psychology, size: 80, color: Colors.blue),
            const SizedBox(height: 20),
            Text("当前全局状态: $_lastState", style: const TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Text("活跃时长积累: $_timerCount 秒", style: const TextStyle(fontSize: 24)),
            const Padding(
              padding: EdgeInsets.all(32),
              child: Text("提示：尝试切回桌面或打开通知栏，观察状态变化及计时是否暂停。", 
                  textAlign: TextAlign.center, style: TextStyle(color: Colors.grey)),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的实际工程中，搞定“声明周期”是应用从 Demo 迈向商用且稳健的关键。

1.  **观察者模式**：通过 `WidgetsBindingObserver` 建立与宿主系统的紧密纽带。
2.  **节源开流**：在后台状态主动释放非必要资源（内存、CPU）。
3.  **鸿蒙特色**：针对分屏与平行视界下的 `inactive` 状态进行精细化适配，确保用户在多任务切换时享受连贯、省电且智能的交互体验。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

