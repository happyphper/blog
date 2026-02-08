![封面图](images/103-cover.png)

# Flutter for OpenHarmony 实战之殿堂：第一百零三篇 鸿蒙穿戴 (Watch) 交互 — 音频同步与语音交互实战

## 前言

智能手表不仅是健康的守护者，更是“随身听”与“语音助手”的承载体。想象一下，用户通过手表上的 Flutter 应用，一句话就能控制智能家居，或者在跑步时通过蓝牙耳机收听来自手表的离线音乐。

本篇将聚焦 **HarmonyOS Wearable** 的多媒体与 AI 能力，教你如何在 Flutter 中实现丝滑的手表端语音与音频体验。

---

## 一、穿戴端音频输出的特殊架构

在鸿蒙手表上，音频输出遵循 **“音频独占”** 且 **“蓝牙优先”** 的原则：
- **音频输出**：通常输出至已配对的蓝牙耳机，而非手表扬声器（为了省电与隐私）。
- **AVSession 在手表的延伸**：穿戴端也支持播控中心，允许用户在表盘上直接切歌。

---

## 二、实战：构建手表端的离线音乐播放器

### 2.1 适配鸿蒙音频策略
在手表端，我们必须在播放前检测是否有蓝牙音频设备连接。

```dart
// 💡 原理：通过原生插件获取鸿蒙音频输出设备列表
static Future<bool> isBluetoothAudioConnected() async {
  final List devices = await _channel.invokeMethod('getAudioOutputDevices');
  return devices.any((d) => d['type'] == 'bluetooth_sco');
}
```

### 2.2 离线资产的高速读取
手表存储速度较慢。
- ✅ **方案**：不要将音乐存放在 Flutter Assets 中，应通过我们在 84 篇学过的分布式文件访问，从手机端同步到手表的 `files/music` 目录，利用鸿蒙原生的数据漫游。

---

## 三、语音交互：集成鸿蒙原生语音识别 (ASR)

手表上没有键盘（或者很小），**语音输入**是第一交互力。

### 3.1 调起系统级语音面板
不要在 Flutter 中自己写声波动效，直接调起鸿蒙系统原生的语音录入面板（Voice Recognition Kit）。

```typescript
// 📌 鸿蒙原生侧封装：启动语音识别小部件
import voiceRecognition from '@ohos.ai.voiceRecognition';

async function startVoiceInput() {
  let result = await voiceRecognition.showDialog(); 
  // 传回给 Flutter 自动填充搜索框
  this.channel.invokeMethod('onVoiceResult', result.text);
}
```

### 3.2 实现“语音触发指令”
当用户对着手表说“开始跑步”时，Flutter 应用应如何响应？
- ✅ **技巧**：监听鸿蒙系统的 `ohos.intent.action.VOICE_ASSISTANT`，在 Flutter 的入口处根据意图参数直接跳转到功能页。

<!-- IMAGE_PLACEHOLDER: 用户对着华为 Watch 说话，Flutter 应用实时转换文字并触发智能家居开关的场景截图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示手表端 AI 交互的高效性 -->

---

## 四、OpenHarmony 平台适配要点：音量与表冠联动

在手表播放场景下，用户习惯通过**表冠（Crown）**调节音量。
- ✅ **推荐做法**：捕获我们在 101 篇讲过的表冠旋转事件。每旋转一格，通过原生 `AudioRenderer` 增减 10% 的系统音量，并配合震动反馈。

---

## 五、总结

穿戴交互是“动口不动手”：
1.  **链路前置**：先检查音频设备，再开始播放业务。
2.  **拥抱 AI**：将语音作为第一输入手段。
3.  **系统级控制**：让 App 的状态同步到鸿蒙控制中心和蓝牙耳机。

第一百零四篇，我们将攻克穿戴设备最基础也最关键的——**鸿蒙手表端的列表极致流畅度与手感调优**。

---

> 📦 **语音播放库的手表适配版已发布**：[open-harmony-examples/watch-media-kit](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/watch-media-kit)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
