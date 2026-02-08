# Flutter for OpenHarmony 实战之基础组件：第二十七篇 BottomSheet — 动态底部弹窗与底部栏菜单

## 前言

底部弹窗（BottomSheet）是移动端 UI 设计中非常受青睐的一种交互组件。相比于传统的居中对话框，底部弹窗更符合用户的点击习惯（离大拇指更近），且能承载从简单的功能选择到复杂的详情页预览等多种任务。

在 **Flutter for OpenHarmony** 开发中，我们可以利用 `Scaffold` 内置的 `bottomSheet` 属性实现持久化底部栏，或通过 `showModalBottomSheet` 调起模态选择器。本文将详解这两种模式的区别、定制化样式以及在鸿蒙设备上的交互优化。

---

## 一、模态底部弹窗：showModalBottomSheet

`showModalBottomSheet` 是最常用的 API，它会弹出一个半透明遮罩覆盖主页面，禁止用户与背景交互，直到弹窗关闭。

### 1.1 基础用法
```dart
void _showSimpleBottomSheet(BuildContext context) {
  showModalBottomSheet(
    context: context,
    builder: (BuildContext context) {
      return Container(
        height: 200,
        color: Colors.white,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              const Text('底部弹窗示例'),
              ElevatedButton(
                child: const Text('关闭'),
                onPressed: () => Navigator.pop(context),
              )
            ],
          ),
        ),
      );
    },
  );
}
```

### 1.2 圆角与样式定制
💡 **技巧**：
为了让 BottomSheet 看起来更具“鸿蒙感”，通常会为其添加大圆角边框。

```dart
showModalBottomSheet(
  context: context,
  shape: const RoundedRectangleBorder(
    borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
  ),
  clipBehavior: Clip.antiAliasWithSaveLayer, // 确保子元素不超出圆角
  builder: (context) => _buildSelectionList(),
)
```

<!-- IMAGE_PLACEHOLDER: 圆角 BottomSheet 在鸿蒙手机上的展示效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 二、持久化底部栏：showBottomSheet

不同于模态弹窗，持久化底部栏（Persistent BottomSheet）通常依附于 `Scaffold`，不会阻止用户与背景交互。它常用于展示正在播放的歌曲信息、文件上传进度等。

### 2.1 基础实现
```dart
Scaffold(
  appBar: AppBar(title: Text("持久化底部栏")),
  body: Center(child: Text("主内容区域")),
  // 在 Scaffold 中直接定义或通过全局 Key 触发
  bottomSheet: Container(
    height: 60,
    color: Colors.blue[50],
    child: Row(
      children: [
        Icon(Icons.music_note),
        Text("正在播放：Harmony Symphony"),
        Spacer(),
        IconButton(icon: Icon(Icons.pause), onPressed: () {}),
      ],
    ),
  ),
)
```

### 2.2 两种模式的区别自检
| 特性 | 模态 (Modal) | 持久化 (Persistent) |
|-----|-------------|-------------------|
| **调用方式** | `showModalBottomSheet(...)` | `Scaffold.bottomSheet` 属性 |
| **交互限制** | 阻塞背景点击 | 不阻塞背景点击 |
| **遮罩层** | 有灰色半透明遮罩 | 无遮罩 |
| **适用场景** | 功能选择、信息录入 | 状态监测、辅助控制 |

---

## 三、进阶：全屏弹窗与手势拖拽

在鸿蒙系统上，我们经常看到一些可以向上拖动展开至全屏，或者向下拖动关闭的弹窗。

### 3.1 开启拖拽关闭 (isScrollControlled)
如果你的弹窗包含大量内容（如评论列表），务必设置 `isScrollControlled: true`。

```dart
showModalBottomSheet(
  context: context,
  isScrollControlled: true, // 允许弹窗高度超过半屏
  builder: (context) {
    return DraggableScrollableSheet(
      initialChildSize: 0.5, // 初始高度占比
      minChildSize: 0.3,     // 最小占比
      maxChildSize: 0.9,     // 最大占比
      expand: false,
      builder: (_, controller) {
        return ListView.builder(
          controller: controller, // 核心：绑定滚动控制器
          itemCount: 50,
          itemBuilder: (c, i) => ListTile(title: Text("Item $i")),
        );
      },
    );
  },
)
```

<!-- IMAGE_PLACEHOLDER: 可滑动展开的 BottomSheet 动效动图 -->
<!-- 类型: GIF -->
<!-- 设备: 鸿蒙模拟器 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 底部安全区 (SafeArea)
鸿蒙设备底部通常有“经典三键”或“手势条”。弹窗内容如果贴着最底部，极易发生误触。

✅ **推荐做法**：
使用 `SafeArea` 处理弹窗内容。

```dart
showModalBottomSheet(
  context: context,
  builder: (context) => SafeArea(child: myContent()), // 自动避开鸿蒙底部手势条
)
```

### 4.2 触控震动反馈
在点击触发弹窗，或者将弹窗拖动到关闭临界点时，调用鸿蒙系统的微弱震动，能给用户极佳的机械确认感。

```dart
import 'package:flutter/services.dart';

void _onShow() {
  HapticFeedback.mediumImpact(); // 唤起弹窗时的体感正向反馈
}
```

### 4.3 多分辨率布局设计
在宽屏鸿蒙平板上，全宽的 BottomSheet 会显得异常窄长且视觉重心不稳。

✅ **适配建议**：
在宽屏下，推荐将 BottomSheet 的 `maxWidth` 限制在合理范围内（如 500px），并使其居中显示。

```dart
showModalBottomSheet(
  context: context,
  constraints: BoxConstraints(maxWidth: 500), // 针对平板的适配
  // ...
)
```

---

## 五、完整示例代码

以下代码演示了一个带有“拖拽手势”和“内容自适应”的分享弹窗示例。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: BottomSheetDemo()));

class BottomSheetDemo extends StatelessWidget {
  const BottomSheetDemo({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 底部弹窗实战')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => _showShareSheet(context),
              child: const Text("点击分享 (Modal)"),
            ),
            const SizedBox(height: 20),
            const Text("底部常驻栏示例见下方蓝色条", style: TextStyle(color: Colors.grey)),
          ],
        ),
      ),
      // 演示：持久化底部栏
      bottomSheet: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        height: 60,
        color: Colors.blue[600],
        child: Row(
          children: [
            const Icon(Icons.info_outline, color: Colors.white),
            const SizedBox(width: 10),
            const Text("应用更新已准备就绪", style: TextStyle(color: Colors.white)),
            const Spacer(),
            TextButton(
              onPressed: () {},
              child: const Text("立即安装", style: TextStyle(color: Colors.yellow)),
            )
          ],
        ),
      ),
    );
  }

  void _showShareSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisSize: MainAxisSize.min, // 高度自适应内容
            children: [
              Container( // 仿系统拉环
                width: 40, height: 4,
                decoration: BoxDecoration(color: Colors.grey[300], borderRadius: BorderRadius.circular(2)),
              ),
              const SizedBox(height: 24),
              const Text("分享到", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 32),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _shareItem(Icons.chat, "微信"),
                  _shareItem(Icons.camera, "朋友圈"),
                  _shareItem(Icons.link, "复制链接"),
                  _shareItem(Icons.more_horiz, "更多"),
                ],
              ),
              const SizedBox(height: 24),
            ],
          ),
        );
      },
    );
  }

  Widget _shareItem(IconData icon, String label) {
    return Column(
      children: [
        CircleAvatar(
          radius: 28,
          backgroundColor: Colors.grey[100],
          child: Icon(icon, color: Colors.black87),
        ),
        const SizedBox(height: 8),
        Text(label, style: const TextStyle(fontSize: 12)),
      ],
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 完整示例在鸿蒙设备上的静态预览与动效标注 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 六、总结

在 Flutter for OpenHarmony 开发中，底部弹窗不仅是 UI 布局的补充，更是承载核心操作的交互热点。

1.  **模态弹窗 (Modal)**：通过大圆角、阻断背景来强调当前任务。
2.  **持久弹窗 (Persistent)**：适合状态通知，不会打断用户流程。
3.  **用户体验**：务必配合 `SafeArea` 处理鸿蒙的底部手势栏，并在大屏设备上进行合理的宽度约束。

结合 `DraggableScrollableSheet`，你可以构建出极具动态美感的“抽屉式”详情页效果，让你的鸿蒙应用交互更上一层楼。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

