![封面图](images/81-cover.png)

# Flutter for OpenHarmony 实战之进阶：第八十一篇 Native 插件开发实战 (一) — 构建高质量的 ArkTS 插件

## 前言

虽然 **Flutter for OpenHarmony** 生态中现成的插件（Plugins）正在快速丰富，但在处理特定业务逻辑或对接鸿蒙系统独有的硬件能力时，亲自下场编写 Native 插件是每一位高级跨平台开发者的必修课。

本篇将带你从零开始，构建一个规范的跨平台插件，重点讲解如何在 ArkTS 侧封装鸿蒙原生 API，并以最高效的方式暴露给 Dart 层。

---

## 一、Flutter 插件工程结构详解

在鸿蒙工程中，一个标准的插件项目结构如下：

```text
my_plugin/
├── lib/
│   └── my_plugin.dart        # Dart 层公开接口
├── ohos/
│   ├── src/main/ets/
│   │   ├── MyPlugin.ets      # 📌 插件核心实现（ArkTS）
│   │   └── ...
│   └── oh-package.json5      # 鸿蒙三方库配置
└── pubspec.yaml              # 插件元数据
```

---

## 二、实战：构建一个“鸿蒙系统温度”插件

我们将实现一个读取鸿蒙设备当前电池温度的简单插件。

### 2.1 Dart 层：定义通信契约
```dart
class OhosBatteryTemp {
  static const MethodChannel _channel = MethodChannel('com.example/battery_temp');

  // 💡 技巧：使用 Future 保证异步非阻塞调用
  static Future<double> get currentTemperature async {
    final double temp = await _channel.invokeMethod('getTemperature');
    return temp / 10.0; // 鸿蒙原生返回的是摄氏度*10
  }
}
```

### 2.2 ArkTS 侧：对接鸿蒙电池服务
在鸿蒙系统中，我们需要调用 `@ohos.batteryInfo` 模块。

```typescript
// 💡 原理：封装鸿蒙系统 API 并通过 MethodChannel 回传
import { FlutterPlugin, FlutterPluginBinding, MethodCall, MethodResult, MethodChannel } from '@ohos/flutter_ohos';
import batteryInfo from '@ohos.batteryInfo';

export default class BatteryTempPlugin implements FlutterPlugin {
  private channel: MethodChannel | null = null;

  onAttachedToEngine(binding: FlutterPluginBinding): void {
    this.channel = new MethodChannel(binding.getBinaryMessenger(), "com.example/battery_temp");
    this.channel.setMethodCallHandler(this);
  }

  onMethodCall(call: MethodCall, result: MethodResult): void {
    if (call.method === "getTemperature") {
      // 📌 获取鸿蒙原生电池温度
      let temp = batteryInfo.batteryTemperature;
      result.success(temp);
    } else {
      result.notImplemented();
    }
  }

  onDetachedFromEngine(binding: FlutterPluginBinding): void {
    this.channel?.setMethodCallHandler(null);
  }
}
```

---

## 三、进阶：处理运行时权限申请

很多鸿蒙原生能力（如位置、相机）需要动态申请权限。在插件中，这需要结合 `Ability` 上下文。

### 3.1 获取上下文
```typescript
// 在插件中获取当前的 UIAbilityContext
let context = binding.getApplicationContext() as common.UIAbilityContext;
```

### 3.2 权限申请示例
```typescript
import abilityAccessCtrl from '@ohos.abilityAccessCtrl';

async function requestCameraPermission(context: common.UIAbilityContext) {
  let atManager = abilityAccessCtrl.createAtManager();
  let data = await atManager.requestPermissionsFromUser(context, ['ohos.permission.CAMERA']);
  // 处理申请结果并回调 result.success()
}
```

<!-- IMAGE_PLACEHOLDER: 插件在鸿蒙设备上请求位置权限时的原生弹窗截图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示插件与鸿蒙系统交互的真实感 -->

---

## 四、OpenHarmony 平台适配要点

### 4.1 异步编程模型 (Async/Await)
鸿蒙系统的原生 API 几乎全是异步的。
- ✅ **推荐做法**：在插件的 `onMethodCall` 中使用 `async/await`，并确保在任务执行完毕后，无论成功失败都要调用一次 `result.success()` 或 `result.error()`。

### 4.2 错误码规范映射
不要只传一个字符串错误。
- 💡 **技巧**：定义一套错误码映射表。例如，当鸿蒙系统返回权限拒绝时，回传特定的错误代号，方便 Dart 侧进行多语言展示。

---

## 五、如何发布并引用你的插件

在你的 Flutter 主项目 `pubspec.yaml` 中，可以通过相对路径引用此插件：

```yaml
dependencies:
  my_battery_plugin:
    path: ../plugins/my_battery_plugin
```

---

## 六、总结

编写 Native 插件是你从被动消费 API 转向主动创造能力的转折点：
1.  **接口先行**：想好 Dart 侧最舒服的调用方式。
2.  **安全调用**：严谨处理原生 API 的异常捕获。
3.  **遵循规范**：生命周期的注册与解除必须一丝不苟。

在接下来的 82 篇中，我们将更进一步，学习如何利用这个能力，深度定制鸿蒙的分享与通知系统。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/native-plugin-demo](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/native-plugin-demo)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
