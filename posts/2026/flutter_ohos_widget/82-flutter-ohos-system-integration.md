![封面图](images/82-cover.png)

# Flutter for OpenHarmony 实战之进阶：第八十二篇 鸿蒙原生分享、通知与权限系统深度接入

## 前言

一个真正“接地气”的应用，必须深度融入目标操作系统的生态。在 **HarmonyOS NEXT** 中，其特有的“系统级分享”、高度自定义的“通知中心”以及更严苛的“动态权限”模型，是跨平台框架必须完美跨越的三座大山。

本篇将教会你如何在 **Flutter for OpenHarmony** 中，利用原生插件能力，丝滑对接这些鸿蒙核心系统服务。

---

## 一、鸿蒙原生分享 (System Share) 连通

鸿蒙系统鼓励通过 `systemShare` 模块进行跨应用的数据传递，这比传统的自定义分享弹窗更美观且符合系统设计规范。

### 1.1 ArkTS 侧对分享能力的封装
```typescript
import systemShare from '@ohos.systemShare';
import common from '@ohos.app.ability.common';

async function shareText(context: common.UIAbilityContext, content: string) {
  let shareData = new systemShare.SharedData({
    utd: 'general.plain-text',
    content: content
  });
  let controller = await systemShare.makeController(shareData);
  controller.show(context, {
    previewMode: systemShare.SharePreviewMode.DETAIL,
    selectionMode: systemShare.SelectionMode.SINGLE
  });
}
```

### 1.2 Flutter 侧调用
开发者只需通过我们在 81 篇学习的 `MethodChannel` 即可发起调用。

<!-- IMAGE_PLACEHOLDER: Flutter 应用调起鸿蒙系统原生分享面板的效果截图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示分享至 HarmonyOS 微信、微博等面板的真实效果 -->

---

## 二、消息通知 (Notification) 的精细化管理

鸿蒙的通知中心支持分类提醒（Slot）、带操作按钮的通知以及大张图通知。

### 2.1 创建通知通道 (Slot)
在鸿蒙端，重要通知必须归属至特定的 Slot，用户可以针对 Slot 单独开关权限。

```typescript
import notificationManager from '@ohos.notificationManager';

async function publishNotification() {
  let request = {
    content: {
      contentType: notificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT,
      normal: {
        title: "来自 Flutter 的技术动态",
        text: "您的第 82 篇进阶教程已更新！",
        additionalText: "点击继续学习"
      }
    },
    id: 1, // 通知 ID
    slotType: notificationManager.SlotType.SOCIAL_COMMUNICATION // 📌 社交类通知，拥有高优先级
  };
  await notificationManager.publish(request);
}
```

### 2.2 监听点击回调
当用户点击通知进入应用时，需要通过 `Ability` 的 `onNewWant` 回调捕获参数，并异步通知给 Flutter 侧跳转到特定路由。

---

## 三、鸿蒙端动态权限管理的最佳实践

鸿蒙系统的权限分为“系统授权”和“用户授权”。

### 3.1 权限申请组件化
建议在 Flutter 侧统一封装一套逻辑：
1.  **检查权限状态**：通过原生插件询问系统。
2.  **触发申请弹窗**：调用鸿蒙 `atManager`。
3.  **结果反馈**：处理用户“永久拒绝”后的引导去设置页逻辑。

```dart
// 💡 技巧：强类型权限枚举，统一管理
enum OhosPermission {
  camera,
  location,
  microphone
}

class OhosPermissionManager {
  static Future<bool> request(OhosPermission p) async {
    // ... 调用底层插件
  }
}
```

---

## 四、OpenHarmony 平台适配要点

### 4.1 通知图标自适应
鸿蒙系统对通知栏的小图标有严格的黑白对比度要求。
- ✅ **建议**：在鸿蒙工程的 `resources` 目录下，准备一张纯白色背景、透明镂空的 PNG 图片作为通知专用图标。

### 4.2 分享资产文件的绝对路径
当你分享图片文件时，鸿蒙原生期望的是文件系统中的绝对路径或 `fd` (File Descriptor)。
- ⚠️ **注意**：Flutter 的 AOT 资源（Assets）在鸿蒙端是压缩打包的，**无法通过简单的路径直接分享**。必须先通过 `path_provider` 将图片拷贝到鸿蒙应用的沙盒缓存区 (`cacheDir`)，再进行分享。

---

## 五、总结

深度接入系统服务是消除“跨平台痕迹”最有效的手段：
1.  **尊重用户**：使用系统原生分享，而非 ad-hoc 的自定义弹窗。
2.  **精准触达**：规范化管理通知 Slot，避免用户反感全量关掉通知。
3.  **合规合用**：最小化申请权限，并在申请前向用户解释原因。

在这一篇的加持下，你的应用将正式具备“鸿蒙原生灵魂”。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/system-services-integration](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/system-services-integration)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
