![封面图](images/88-cover.png)

# Flutter for OpenHarmony 实战之进阶：第八十八篇 音频播放与鸿蒙播控中心（AVSession）集成

## 前言

一个专业的音视频应用，不仅要在 App 内部能响，更要能在系统的**播控中心**（控制中心、锁屏界面）进行交互。在 **HarmonyOS NEXT** 中，这套机制被称为 **AVSession**。

本篇将带你使用 Flutter 结合鸿蒙原生 AVSession 能力，打造一个具备锁屏控制、蓝牙耳机切歌功能的专业播放器。

---

## 一、鸿蒙 AVSession 架构全解析

AVSession 是鸿蒙系统用于管理媒体会话的统一入口：
- **媒体生产者**：你的 Flutter 播放器。
- **媒体消费者**：控制中心、锁屏界面、智能手表。
- **交互流**：你的 App 告知系统“我在放什么”，系统告知你的 App“用户按了暂停”。

---

## 二、实战：Flutter 播放器集成系统控制

### 2.1 依赖选择
推荐使用适配了鸿蒙版的 `audioplayers` 或 `just_audio`。

### 2.2 鸿蒙原生侧：注册会话
在 ArkTS 侧，我们需要创建一个 `AVSession` 实例。

```typescript
// 💡 原理：在原生层建立播控管道
import avSession from '@ohos.multimedia.avSession';

async function createSession(meta: any) {
  let session = await avSession.createAVSession(context, "MyFlutterMusic", 'audio');
  
  // 📌 设置媒体信息（歌名、歌手、封面）
  session.setAVMetadata({
    assetId: '123',
    title: meta.title,
    artist: meta.artist
  });

  // 📌 监听系统控制指令
  session.on('play', () => {
    // 通过 MethodChannel 通知 Flutter 播放
  });
}
```

### 2.3 Flutter 侧：同步播放进度
```dart
void onPositionChanged(Duration p) {
  // ⚡️ 实时同步进度给鸿蒙系统，确保锁屏进度条丝滑
  _channel.invokeMethod('updateProgress', p.inMilliseconds);
}
```

<!-- IMAGE_PLACEHOLDER: Flutter 音乐应用运行在鸿蒙系统上，且锁屏界面显示同步封面与歌名时的效果截图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示与 HarmonyOS 系统级播控的完美融合 -->

---

## 三、进阶：处理音频焦点（Audio Focus）

当用户正在听你的音乐，突然接到了电话，或者打开了抖音，你的 App 应该怎么做？这就是音频焦点的管理。

### 3.1 监听焦点丢失
鸿蒙音频引擎会发出焦点变更信号。
- ✅ **推荐做法**：当收到 `AUDIO_INTERRUPT_TYPE_PAUSE` 时，Flutter 侧应立即使播放器进入 `pause` 状态，并保存当前进度。

---

## 四、OpenHarmony 平台适配要点

### 4.1 蓝牙耳机按键适配
鸿蒙系统已将蓝牙耳机的“单击暂停”、“双击切歌”抽象为 AVSession 的标准指令。
- ✅ **方案**：只要你正确实现了 `session.on('play/pause/next')`，无需额外编写蓝牙适配逻辑。

### 4.2 封面图的加载优化
锁屏封面往往需要高质量位图。
- ⚠️ **注意**：大图会拖慢 AVSession 的响应。建议传给系统的封面图经过 `InstantiateImageCodec` 重新采样，控制在 512x512 以内。

---

## 五、总结

音频开发不仅是发声，更是“社交”：
1.  **主动宣告**：通过 AVSession 告诉系统你的存在。
2.  **优雅回应**：处理好音频焦点切换。
3.  **多端同步**：让用户在锁屏、手表上也能掌控你的 App。

掌握了 AVSession 深度集成，你的 Flutter 播放器才真正从“简陋工具”进化为“鸿蒙一等公民”。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/audio-avsession-adv](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/audio-avsession-adv)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
