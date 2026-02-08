# Flutter for OpenHarmony 实战之基础组件：第三十五篇 SnackBar 与 MaterialBanner — 灵活的应用消息反馈

## 前言

在应用运行过程中，我们需要不断向用户同步当前的状态：操作是否成功？网络是否断开？是否需要立即升级？针对这些不同程度、不同优先级的反馈，Flutter 提供了 `SnackBar`（底部快报）和 `MaterialBanner`（顶部公告）两套标准方案。

在 **Flutter for OpenHarmony** 平台上，这两者不仅能完美兼顾鸿蒙系统的沉浸式 UI 规范，还能通过流式布局和手势交互，为用户提供不打断流程的轻量级反馈。本文将解析这两者的核心差异、样式定制及鸿蒙端的适配最佳实践。

---

## 一、SnackBar：底部的轻量反馈

`SnackBar` 通常显示在屏幕底部，经过短暂的显示后会自动消失。它最适合“操作成功”、“已删除”这类低优先级的状态确认。

### 1.1 基础唤起方式
从 Flutter 3.x 开始，我们使用 `ScaffoldMessenger` 来统筹管理 SnackBar 的弹出。

```dart
ScaffoldMessenger.of(context).showSnackBar(
  const SnackBar(
    content: Text('消息发送成功'),
    duration: Duration(seconds: 3),
  ),
);
```

### 1.2 进阶定制：操作按钮与形状
💡 **实战技巧**：
为了让 SnackBar 看起来更像鸿蒙系统的原生气泡，我们可以设置 `behavior` 为 `floating` 并增加圆角。

```dart
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    content: const Text('文件已归档'),
    behavior: SnackBarBehavior.floating, // 浮动样式
    width: 280, // 指定宽度（仅在 floating 时有效）
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    backgroundColor: Colors.blue[800],
    action: SnackBarAction(
      label: '撤回',
      textColor: Colors.white,
      onPressed: () {
        // 执行撤回逻辑
      },
    ),
  ),
);
```

<!-- IMAGE_PLACEHOLDER: 浮动样式的 SnackBar 在鸿蒙设备底部的展示效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 二、MaterialBanner：顶部的强力提醒

相比于 SnackBar 的“转瞬即逝”，`MaterialBanner` 显示在应用顶部（通常位于 AppBar 之下），除非用户手动关闭，否则它会一直保持显示状态。适合展示“网络连接断开”或“账户风险提示”等高优先级信息。

### 2.1 核心属性
```dart
ScaffoldMessenger.of(context).showMaterialBanner(
  MaterialBanner(
    content: const Text('您的应用版本过低，建议立即升级以体验新功能。'),
    leading: const Icon(Icons.info, color: Colors.blue),
    backgroundColor: Colors.blue[50], // 品牌背景色
    actions: [
      TextButton(
        onPressed: () => ScaffoldMessenger.of(context).hideCurrentMaterialBanner(),
        child: const Text('稍后再说'),
      ),
      TextButton(
        onPressed: () { /* 执行升级逻辑 */ },
        child: const Text('立即升级'),
      ),
    ],
  ),
);
```

<!-- IMAGE_PLACEHOLDER: MaterialBanner 在鸿蒙 AppBar 之下的视觉效果截图 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、SnackBar vs MaterialBanner：如何选型？

| 特性 | SnackBar | MaterialBanner |
|-----|----------|----------------|
| **显示位置** | 底部 | 顶部（组件树内） |
| **持续时间** | 自动消失 | 需手动关闭 |
| **优先级** | 低（信息确认） | 中高（状态持续警示） |
| **遮挡行为** | 会遮挡 FloatingActionButton | 会将下方内容整体下移 |

---

## 四、OpenHarmony 平台适配建议

### 4.1 避让底部手势条 (SafeArea)
鸿蒙系统的“手势导航条”位于屏幕正下方。如果你的 SnackBar 采用了固定的 `fixed` 模式，内容可能会被手势条遮挡。

✅ **推荐方案**：
始终建议使用 `behavior: SnackBarBehavior.floating`。由于浮动模式会自动避开底部安全区，能完美适配鸿蒙设备的挖孔和手势条。

### 4.2 结合触感反馈
消息弹出时，利用鸿蒙设备的震动能力让反馈更立体。

```dart
import 'package:flutter/services.dart';

void _notify() {
  HapticFeedback.lightImpact(); // 轻微震动提示用户有消息到达
  _showMySnackBar();
}
```

### 4.3 宽屏/平板适配建议
在 12 英寸的鸿蒙平板上，全宽的 SnackBar 会显得非常突兀。

✅ **优化建议**：
在 LayoutBuilder 中判断宽度。如果是大屏设计，建议将 SnackBar 的 `margin` 设置较大，或固定其 `width` 使其居中，避免视觉信息过于分散。

```dart
SnackBar(
  behavior: SnackBarBehavior.floating,
  margin: EdgeInsets.symmetric(
    horizontal: MediaQuery.of(context).size.width > 600 ? 100 : 20,
    vertical: 20
  ),
  //...
)
```

---

## 五、完整示例代码

以下代码演示了一个包含“各种通知类型触发器”的综合控制页面。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: NotificationDemoPage()));

class NotificationDemoPage extends StatelessWidget {
  const NotificationDemoPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 消息提示实战')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => _showTopBanner(context),
              child: const Text("触发顶部 Banner (公告)"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => _showBottomSnackBar(context),
              child: const Text("触发底部 SnackBar (反馈)"),
            ),
          ],
        ),
      ),
    );
  }

  void _showBottomSnackBar(BuildContext context) {
    final messenger = ScaffoldMessenger.of(context);
    messenger.removeCurrentSnackBar(); // 清理旧的
    
    messenger.showSnackBar(
      SnackBar(
        content: const Row(
          children: [
            Icon(Icons.check_circle, color: Colors.greenAccent, size: 20),
            SizedBox(width: 10),
            Text("文章已成功收藏！"),
          ],
        ),
        behavior: SnackBarBehavior.floating,
        duration: const Duration(seconds: 2),
        margin: const EdgeInsets.fromLTRB(16, 0, 16, 80), // 向上偏移避开底部
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
      ),
    );
  }

  void _showTopBanner(BuildContext context) {
    final messenger = ScaffoldMessenger.of(context);
    messenger.removeCurrentMaterialBanner();
    
    messenger.showMaterialBanner(
      MaterialBanner(
        elevation: 2,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        content: const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text("系统更新提示", style: TextStyle(fontWeight: FontWeight.bold)),
            Text("HarmonyOS NEXT 已发布新版本，建议立即安装。"),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => messenger.hideCurrentMaterialBanner(),
            child: const Text("忽略"),
          ),
          TextButton(
            onPressed: () {},
            child: const Text("去更新", style: TextStyle(color: Colors.blue, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 开发中，合理利用 SnackBar 和 MaterialBanner 能让你的应用展现出更强的生命力和响应力。

1.  **SnackBar**：侧重于异步操作的结果反馈，重点关注 `floating` 样式的圆角适配。
2.  **MaterialBanner**：侧重于全局性的状态告知，重点关注与 AppBar 和内容区的布局联动。
3.  **用户体验**：不管使用哪种形式，都应避免频繁弹出干扰用户，并充分利用鸿蒙终端的触感反馈提升操作质感。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

