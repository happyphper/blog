# Flutter for OpenHarmony 实战之基础组件：第三十一篇 Chip 系列组件 — 灵活的标签化交互

## 前言

在现代移动应用的设计语言中，标签（Chip）是一种极其紧凑且高效的信息承载方式。它能将复杂的选择、过滤或状态展示浓缩为一个小巧的胶囊形元素。从搜索历史的关键字到商品分类的筛选，再到社交应用中的兴趣标签，Chip 几乎无处不在。

在 **Flutter for OpenHarmony** 平台上，Chip 系列组件不仅支持 Material 3 的精美视觉效果，还能完美适配鸿蒙系统的触控反馈。本文将详解 `Chip` 家族的四位核心成员，助你在鸿蒙应用中构建灵活的标签化交互系统。

---

## 一、Chip 家族四剑客详解

Flutter 提供了四种针对不同场景优化的标签组件：

### 1.1 ActionChip：操作型标签
类似于一个小型的按钮，点击后触发特定的动作。

```dart
ActionChip(
  avatar: const Icon(Icons.share, size: 16),
  label: const Text('分享'),
  onPressed: () {
    // 触发分享逻辑
  },
)
```

### 1.2 ChoiceChip：单选型标签
用于从一组选项中选择其一。

```dart
ChoiceChip(
  label: const Text('标准模式'),
  selected: _selectedIndex == 0,
  onSelected: (bool selected) {
    setState(() => _selectedIndex = selected ? 0 : -1);
  },
)
```

### 1.3 FilterChip：多选过滤型标签
带有复选勾号，常用于搜索筛选。

```dart
FilterChip(
  label: const Text('新品'),
  selected: _isNewArrival,
  onSelected: (bool selected) {
    setState(() => _isNewArrival = selected);
  },
)
```

### 1.4 InputChip：输入型标签
常用于联系人选择，支持删除、点击等复杂操作。

```dart
InputChip(
  avatar: const CircleAvatar(child: Text('OH')),
  label: const Text('OpenHarmony'),
  onDeleted: () {
    // 处理删除逻辑
  },
)
```

<!-- IMAGE_PLACEHOLDER: Chip 全家族组件在鸿蒙设备上的样式合集 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 二、样式定制：打造鸿蒙风格的标签

在鸿蒙系统（HarmonyOS）的设计中，UI 趋向于轻量化和通透感。我们可以通过 `ChipTheme` 或直接在组件上进行定制。

### 2.1 胶囊样式与色彩管理
```dart
FilterChip(
  label: Text("实战教程", style: TextStyle(color: _selected ? Colors.white : Colors.blueGrey)),
  selected: _selected,
  selectedColor: Colors.blue[700], // 选中时的鸿蒙蓝
  backgroundColor: Colors.blue[50], // 未选中的浅蓝色调
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(20), // 胶囊形状
    side: BorderSide(color: _selected ? Colors.transparent : Colors.blue.withAlpha(30)),
  ),
  onSelected: (v) => setState(() => _selected = v),
)
```

### 2.2 响应式布局：结合 Wrap
标签的数量通常是不确定的，直接使用 `Row` 会导致布局溢出。在鸿蒙设备上，我们几乎总是将 Chip 放在 `Wrap` 组件中。

```dart
Wrap(
  spacing: 8.0, // 左右间距
  runSpacing: 4.0, // 上下间距
  children: _tags.map((tag) => Chip(label: Text(tag))).toList(),
)
```

<!-- IMAGE_PLACEHOLDER: 利用 Wrap 自动换行排列的标签云效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、常见应用场景：商品搜索与筛选

这是 Chip 最具代表性的应用场景。

```dart
Widget _buildFilterSection() {
  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text("热门品类", style: TextStyle(fontWeight: FontWeight.bold)),
      SizedBox(height: 12),
      Wrap(
        children: [
          ChoiceChip(label: Text("手机"), selected: true, onSelected: (v) {}),
          SizedBox(width: 8),
          ChoiceChip(label: Text("平板"), selected: false, onSelected: (v) {}),
          SizedBox(width: 8),
          ChoiceChip(label: Text("穿戴设备"), selected: false, onSelected: (v) {}),
        ],
      )
    ],
  );
}
```

---

## 四、OpenHarmony 平台适配建议

### 4.1 触控精准度优化
鸿蒙设备的手势操作非常精准，但 Chip 颗粒较小。

✅ **推荐方案**：
通过 `visualDensity` 属性增加 Chip 的内边距，提升在窄屏鸿蒙设备上的点击成功率。

```dart
ChipThemeData(
  visualDensity: VisualDensity.comfortable, // 让标签在鸿蒙端看起来更饱满
  // ...
)
```

### 4.2 触感反馈 (Vibrate)
当用户点击 `FilterChip` 勾选或删除 `InputChip` 时，触发一次简短的触控反馈。

```dart
import 'package:flutter/services.dart';

onSelected: (v) {
  HapticFeedback.lightImpact(); // 给用户一个清脆的“点击感”
}
```

### 4.3 深色模式适配
鸿蒙系统用户对深色模式使用率极高。

✅ **最佳实践**：
在定制 `FilterChip` 颜色时，避免使用硬编码的 `Colors.white` 作为背景。

```dart
backgroundColor: Theme.of(context).colorScheme.surfaceVariant,
```

<!-- IMAGE_PLACEHOLDER: 深色模式下 Chip 的视觉表现 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 五、完整示例代码

以下代码实现了一个带过滤、多选功能的“搜索历史与品类筛选”页面。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: ChipDemoPage()));

class ChipDemoPage extends StatefulWidget {
  const ChipDemoPage({super.key});

  @override
  State<ChipDemoPage> createState() => _ChipDemoPageState();
}

class _ChipDemoPageState extends State<ChipDemoPage> {
  final List<String> _filters = ['鸿蒙教程', 'Flutter', 'ArkTS', '面试宝典', '源码解析'];
  final Set<String> _selectedFilters = {'Flutter'};
  String _category = '全部';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 标签组件实战')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildTitle("搜索历史 (InputChip)"),
            Wrap(
              spacing: 10,
              children: ['OpenHarmony', 'DevEco Studio'].map((e) => InputChip(
                label: Text(e),
                onDeleted: () {},
                deleteIconColor: Colors.grey,
              )).toList(),
            ),
            
            const SizedBox(height: 40),
            _buildTitle("内容多选 (FilterChip)"),
            Wrap(
              spacing: 10,
              children: _filters.map((f) => FilterChip(
                label: Text(f),
                selected: _selectedFilters.contains(f),
                onSelected: (v) {
                  setState(() {
                    v ? _selectedFilters.add(f) : _selectedFilters.remove(f);
                  });
                },
              )).toList(),
            ),
            
            const SizedBox(height: 40),
            _buildTitle("分类单选 (ChoiceChip)"),
            Wrap(
              spacing: 12,
              children: ['全部', '文章', '视频', '问答'].map((c) => ChoiceChip(
                label: Text(c),
                selected: _category == c,
                onSelected: (v) {
                  if (v) setState(() => _category = c);
                },
              )).toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTitle(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Text(text, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 开发中，Chip 是处理“多维选择”和“碎片化信息”的顶级工具。

1.  **场景化选择**：单选选 `Choice`，过滤选 `Filter`，动态删除选 `Input`。
2.  **布局搭档**：Chip 永远要放在 `Wrap` 里，否则在鸿蒙窄屏设备上极易崩溃。
3.  **视觉统一**：利用主题色体系和 `HapticFeedback` 让标签在鸿蒙端展现出丝滑的交互质感。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

