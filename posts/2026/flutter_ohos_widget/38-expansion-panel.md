# Flutter for OpenHarmony 实战之基础组件：第三十八篇 ExpansionPanel 与 ExpansionTile — 列表交互中的折叠艺术

## 前言

在信息爆炸的移动端界面中，由于屏幕空间的局限性，我们常常需要对次要或详细的信息进行“隐藏处理”。折叠面板（Expansion Panels）就是解决这一矛盾的绝佳方案。它允许用户根据需要随时展开查看详情，或折叠起来以获取更宏观的内容预览。

在 **Flutter for OpenHarmony** 开发中，我们拥有两种处理折叠逻辑的组件：高度集成且方便快捷的 `ExpansionTile`，以及支持更复杂列表状态管理的 `ExpansionPanelList`。本文将通过实战案例，带大家掌握折叠交互的精髓。

---

## 一、ExpansionTile：最简单的单项折叠

`ExpansionTile` 类似于 `ListTile`，但它自带了展开按钮和二级内容区域。

### 1.1 基础实现
```dart
ExpansionTile(
  title: const Text('系统更新详情'),
  subtitle: const Text('点击查看新版本特性'),
  leading: const Icon(Icons.system_update_alt),
  children: const <Widget>[
    ListTile(title: Text('1. 优化内核性能')),
    ListTile(title: Text('2. 修复已知安全漏洞')),
    ListTile(title: Text('3. 提升设备续航')),
  ],
)
```

### 1.2 样式定制：颜色与图标
你可以根据折叠状态动态改变组件的外观。

```dart
ExpansionTile(
  title: const Text('展开后的诱惑'),
  collapsedBackgroundColor: Colors.grey[100], // 折叠时的背景额
  backgroundColor: Colors.blue[50],          // 展开时的背景色
  iconColor: Colors.blue,                   // 展开时右侧箭头的颜色
  collapsedIconColor: Colors.grey,          // 折叠时箭头的颜色
  children: [...],
)
```

<!-- IMAGE_PLACEHOLDER: ExpansionTile 在鸿蒙应用设置页面中的实际展示效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 二、ExpansionPanelList：手风琴效果的最佳选型

当你需要在一组面板中实现“一次只能展开一个”的逻辑（即手风琴效果）时，应使用 `ExpansionPanelList`。

### 2.1 核心驱动机制
不同于 `ExpansionTile` 内部自管理状态，`ExpansionPanelList` 需要通过 `isExpanded` 属性受控管理。

```dart
ExpansionPanelList(
  // 用户点击回调
  expansionCallback: (int index, bool isExpanded) {
    setState(() {
      // 遍历列表，将对应项的状态取反
      _data[index].isExpanded = !isExpanded;
    });
  },
  children: _data.map<ExpansionPanel>((Item item) {
    return ExpansionPanel(
      headerBuilder: (context, isExpanded) => ListTile(title: Text(item.headerValue)),
      body: ListTile(title: Text(item.expandedValue)),
      isExpanded: item.isExpanded,
    );
  }).toList(),
)
```

### 2.2 实现手风琴效果
💡 **技巧**：要在同一时间仅保持一个面板展开，修改 `expansionCallback`：
```dart
expansionCallback: (index, isExpanded) {
  setState(() {
    for (var i = 0; i < _data.length; i++) {
       _data[i].isExpanded = (i == index && !isExpanded);
    }
  });
}
```

<!-- IMAGE_PLACEHOLDER: 手风琴折叠效果在宽屏鸿蒙设备上的交互动图 -->
<!-- 类型: GIF -->
<!-- 设备: 鸿蒙模拟器 -->

---

## 三、进阶：自定义展开动画与装饰

在鸿蒙系统上，为了让界面更具高级感，我们可以在折叠容器周围添加阴影和圆角。

```dart
Card(
  elevation: 2,
  margin: const EdgeInsets.symmetric(vertical: 8),
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
  clipBehavior: Clip.antiAlias, // 确保展开内容也遵循圆角
  child: ExpansionTile(
    title: const Text('安全中心'),
    children: [
       Padding(
         padding: const EdgeInsets.all(16.0),
         child: Text("由于鸿蒙系统的底层隔离，应用权限已得到强化保护。"),
       )
    ],
  ),
)
```

---

## 四、OpenHarmony 平台适配建议

### 4.1 滚动容器中的性能优化
折叠面板展开时，会导致整个页面的高度发生变化。

✅ **推荐方案**：
在长列表中使用折叠面板时，建议配合 `ScrollPhysics` 避免滑动冲突。
如果面板内部有非常沉重的组件（如地图或视频播放器），建议仅在 `isExpanded` 为真时进行计算加载。

### 4.2 适配大尺寸字体
由于折叠面板标题区域密集，鸿蒙系统的字体缩放可能导致布局错位。

💡 **调优建议**：
在 `headerBuilder` 中使用 `Flexible` 或 `Expanded` 配合文本溢出处理（TextOverflow.ellipsis），防止展开箭头图标被挤出屏幕外。

### 4.3 触控反馈增强
展开/折叠动作发生时，调用鸿蒙系统的微弱震动，让虚拟按钮更具物理质感。

```dart
import 'package:flutter/services.dart';

onExpansionChanged: (bool expanded) {
  HapticFeedback.lightImpact(); // 轻微反馈
  // ...
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙手机处于半折叠模式下，多级折叠页面的适配表现 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙折叠屏手机 -->

---

## 五、完整示例代码

以下代码演示了一个带有“常见问题解答（FAQ）”样式的综合折叠页面示例。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: ExpansionDemo()));

class FAQItem {
  String question;
  String answer;
  bool isExpanded;
  FAQItem({required this.question, required this.answer, this.isExpanded = false});
}

class ExpansionDemo extends StatefulWidget {
  const ExpansionDemo({super.key});

  @override
  State<ExpansionDemo> createState() => _ExpansionDemoState();
}

class _ExpansionDemoState extends State<ExpansionDemo> {
  final List<FAQItem> _faqList = [
    FAQItem(question: "Flutter for OHOS 支持哪些设备？", answer: "目前已支持基于 HarmonyOS NEXT 的各种手机、平板及车载大屏。"),
    FAQItem(question: "如何提升应用在鸿蒙端的性能？", answer: "建议使用 Profiler 分析卡顿，优先处理布局抖动和资源过大的图片。"),
    FAQItem(question: "是否可以使用华为推送服务？", answer: "可以通过集成 HMS Core 的 Flutter 插件实现原生推送通知能力。"),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 折叠组件实战')),
      body: SingleChildScrollView(
        child: Column(
          children: [
            const Padding(
              padding: EdgeInsets.all(16.0),
              child: Text("常见问题 (ExpansionPanelList)", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ),
            
            // 核心折叠列表
            ExpansionPanelList(
              elevation: 1,
              expandedHeaderPadding: EdgeInsets.zero,
              expansionCallback: (index, isExpanded) {
                setState(() => _faqList[index].isExpanded = !isExpanded);
              },
              children: _faqList.map<ExpansionPanel>((item) {
                return ExpansionPanel(
                  headerBuilder: (context, _) => ListTile(title: Text(item.question, style: const TextStyle(fontWeight: FontWeight.w500))),
                  body: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
                    width: double.infinity,
                    color: Colors.grey[50],
                    child: Text(item.answer, style: const TextStyle(color: Colors.black87, height: 1.5)),
                  ),
                  isExpanded: item.isExpanded,
                );
              }).toList(),
            ),
            
            const SizedBox(height: 40),
            
            // 独立的 Tile 示例
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16),
              child: ExpansionTile(
                title: Text("高级功能设置"),
                leading: Icon(Icons.security, color: Colors.blue),
                childrenPadding: EdgeInsets.only(left: 48),
                children: [
                  ListTile(title: Text("开启隐私保护")),
                  ListTile(title: Text("清除缓存数据")),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 开发中，折叠面板是平衡“信息密度”与“视觉简洁”的终极法宝。

1.  **ExpansionTile**：极致便捷，适合菜单导航和简单的列表详情。
2.  **ExpansionPanelList**：高度可控，适合复杂业务逻辑及手风琴效果。
3.  **用户体验**：针对鸿蒙端，推荐结合 Card 组件进行圆角化装饰，并赋予精准的 HapticFeedback 以增加交互感。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

