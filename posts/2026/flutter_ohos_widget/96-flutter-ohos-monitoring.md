![封面图](images/96-cover.png)

# Flutter for OpenHarmony 实战之进阶：第九十六篇 企业级异常监控与全链路日志体系 (OhosLog + Sentry)

## 前言

在真实的上架环境中，我们无法盯着用户的手机看。当 **Flutter for OpenHarmony** 应用在用户手中发生崩溃、卡顿或网络异常时，如何第一时间感知并精准定位到哪一行代码？

本篇将带你搭建一套工业级的“全链路监控体系”，结合鸿蒙原生日志系统与 Sentry/性能平台，让线上 Bug 无所遁形。

---

## 一、双端日志系统深度整合

在鸿蒙工程中，我们需要同时捕获两个维度的日志：
- **Flutter 层日志**：Dart 运行时的 Exception、页面生命周期。
- **鸿蒙原生层日志**：Plugin 崩溃、Native 闪退。

### 1.1 封装 OhosLogger
利用鸿蒙原生的 `hilog` 模块，将 Dart 侧的日志实时同步到 DevEco Studio 的控制台。

```dart
// 💡 技巧：通过 MethodChannel 将 Dart 日志转发至原生 hilog
class OhosLogger {
  static const _channel = MethodChannel('com.happyphper.blog/logger');

  static void info(String msg) {
    _channel.invokeMethod('logInfo', {'message': msg});
    print("[FLUTTER_INFO] $msg");
  }
}
```

### 1.2 原生侧处理
```typescript
import hilog from '@ohos.hilog';

// 📌 鸿蒙 hilog 打点
hilog.info(0x0000, 'FLUTTER_TAG', '%{public}s', params.message);
```

---

## 二、实战：接入 Sentry 异常监控

Sentry 目前已支持针对 Flutter 鸿蒙版的私有化集成方案。

### 2.1 捕获 Dart 异常
```dart
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  await SentryFlutter.init(
    (options) {
      options.dsn = 'YOUR_DSN';
      // 📌 建议：在鸿蒙端开启分片采样，减少流量损耗
      options.tracesSampleRate = 1.0;
    },
    appRunner: () => runApp(const MyApp()),
  );
}
```

### 2.2 自动捕获组件树状态
当发生崩溃时，Sentry 能够回溯崩溃瞬间的组件树（Widget Tree）快照，极大地辅助了排查。

---

## 三、性能监控 (APM) 在鸿蒙端的落地

### 3.1 监听 FPS 掉帧
利用 `WidgetsBinding` 监控每秒帧数。

```dart
void initFpsMonitor() {
  // 💡 原理：每次渲染结束后的时间戳计算
  WidgetsBinding.instance.addPersistentFrameCallback((timeStamp) {
    // 逻辑处理：如果连续 5 帧超过 16ms，向 APM 平台发送预警
  });
}
```

### 3.2 鸿蒙原生：捕获 ANR (应用无响应)
ANR 通常由原生主线程阻塞导致。
- ✅ **方案**：利用鸿蒙系统的 `FaultLogger` 机制，当系统检测到进程僵死时，自动将 `cpp` 堆栈保存并上传至监控后台。

<!-- IMAGE_PLACEHOLDER: Sentry 后台展示的鸿蒙端 Flutter 崩溃堆栈（已通过符号表还原代码行） -->
<!-- 类型: 截图 -->
<!-- 内容: 展示精准的错误定位能力 -->

---

## 四、OpenHarmony 平台适配要点

### 4.1 符号表 (Symbol Maps) 的重要性
构建 HAP 产物时会经过混淆。
- ⚠️ **重中之重**：务必在每次 CI 构建时，备份 `./build/ohos/.../app_debug_symbol`。没有它，你看到的监控堆栈就是一堆乱码。

### 4.2 日志脱敏与隐私政策
遵循鸿蒙应用上架规范。
- ✅ **安全提醒**：严禁在 `hilog` 或监控平台上载用户的手机号、身份证、实时经纬度等隐私信息。所有上云日志必须经过正则表达式脱敏处理。

---

## 五、总结

监控体系是架构师的“眼睛”：
1.  **全局捕获**：不放过任何一个异步异常。
2.  **符号还原**：混淆后的堆栈必须自动还原。
3.  **分级预警**：崩溃立项，卡顿观察。

有了这套体系，你的 Flutter 项目在鸿蒙森林里才算真正具备了生存和自我进化的能力。

---

> 📦 **监控架构代码模版已上传至 AtomGit**：[open-harmony-examples/error-monitoring-adv](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/error-monitoring-adv)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
