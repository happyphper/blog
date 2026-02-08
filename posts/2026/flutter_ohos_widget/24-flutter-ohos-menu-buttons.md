# Flutter for OpenHarmony 实战之基础组件：第二十四篇 DropdownButton 与 PopupMenuButton — 丰富的下拉与弹出菜单

## 前言

在空间有限的移动端界面中，菜单组件是实现“隐藏-展示”逻辑、提供更多操作选项的关键。无论是表单中的单项选择器（DropdownButton），还是导航栏角落的功能菜单（PopupMenuButton），它们都承担着提升交互效率重任。

在 **Flutter for OpenHarmony** 平台上，这些 Material 菜单组件能够自动适配鸿蒙的层级管理（Overlay）机制，确保弹出层始终位于正确的位置且交互丝滑。本文将带大家深入挖掘这些菜单组件的高级定制技巧，以满足鸿蒙应用对于精致 UI 的追求。

---

## 一、DropdownButton：内嵌式下拉选择

`DropdownButton` 是一个允许用户从一系列候选项中选择一个值的按钮。

### 1.1 基础用法
它需要三个要素：当前选中的值、待选列表、以及改变后的回调。

```dart
String _selectedCity = '深圳';

DropdownButton<String>(
  value: _selectedCity,
  icon: const Icon(Icons.arrow_drop_down),
  elevation: 16, // 弹出层的阴影深度
  style: const TextStyle(color: Colors.deepPurple),
  underline: Container(
    height: 2,
    color: Colors.deepPurpleAccent,
  ),
  onChanged: (String? newValue) {
    setState(() {
      _selectedCity = newValue!;
    });
  },
  items: <String>['北京', '上海', '广州', '深圳']
      .map<DropdownMenuItem<String>>((String value) {
    return DropdownMenuItem<String>(
      value: value,
      child: Text(value),
    );
  }).toList(),
)
```

### 1.2 进阶定制：搜索与列表样式
💡 **技巧**：
默认的 DropdownButton 在候选项过多时体验较差。在鸿蒙大屏设备上，建议搭配自定义的 `selectedItemBuilder` 或第三方插件来实现带搜索功能的下拉框。

---

## 二、PopupMenuButton：弹出式操作菜单

`PopupMenuButton` 通常用于提供与当前内容相关的附加操作，如“分享”、“举报”或“设置”。

### 2.1 基础实现
```dart
enum MenuAction { share, report, delete }

PopupMenuButton<MenuAction>(
  onSelected: (MenuAction result) {
    // 逻辑处理
  },
  itemBuilder: (BuildContext context) => <PopupMenuEntry<MenuAction>>[
    const PopupMenuItem<MenuAction>(
      value: MenuAction.share,
      child: ListTile(
        leading: Icon(Icons.share),
        title: Text('分享'),
      ),
    ),
    const PopupMenuItem<MenuAction>(
      value: MenuAction.report,
      child: ListTile(
        leading: Icon(Icons.report),
        title: Text('举报'),
      ),
    ),
  ],
)
```

<!-- IMAGE_PLACEHOLDER: PopupMenuButton 在鸿蒙导航栏中的弹出效果截图 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、自定义菜单布局 (Custom Menu UI)

为了让菜单更符合鸿蒙系统的视觉风格（通常带有圆角和轻微的毛玻璃感），我们可以利用 `shape` 和 `offset` 属性。

### 3.1 打造“鸿蒙感”菜单样式
```dart
PopupMenuButton<int>(
  // 设置弹出位置偏移
  offset: const Offset(0, 50),
  // 自定义弹出层的圆角形状
  shape: const RoundedRectangleBorder(
    borderRadius: BorderRadius.all(Radius.circular(12)),
  ),
  // 菜单背景颜色
  color: Colors.white.withAlpha(240), 
  itemBuilder: (context) => [
    PopupMenuItem(
      value: 1,
      child: _buildMenuItem(Icons.edit, "编辑信息"),
    ),
    const PopupMenuDivider(), // 鸿蒙风格的分隔线
    PopupMenuItem(
      value: 2,
      child: _buildMenuItem(Icons.delete, "删除记录", isDanger: true),
    ),
  ],
)

Widget _buildMenuItem(IconData icon, String text, {bool isDanger = false}) {
  return Row(
    children: [
      Icon(icon, color: isDanger ? Colors.red : Colors.blueGrey, size: 20),
      const SizedBox(width: 12),
      Text(text, style: TextStyle(color: isDanger ? Colors.red : Colors.black87)),
    ],
  );
}
```

---

## 四、OpenHarmony 平台适配

### 4.1 窗口层级与焦点管理
在鸿蒙平台上，Flutter 的菜单通过 `Overlay` 节点实现。当菜单弹出时，需要注意底层背景的点击。

✅ **最佳实践**：
- 确保菜单在窄屏设备上不会超出屏幕边缘，Flutter 内部有自动计算逻辑，但建议测试左右边界。
- 考虑到鸿蒙系统的返回手势（滑动边缘返回），菜单弹出时应支持点击背景区域自动消失。

### 4.2 触控反馈适配
菜单项被点击时，利用鸿蒙设备的震动马达提供物理确认感。

```dart
import 'package:flutter/services.dart';

onSelected: (value) {
  HapticFeedback.mediumImpact(); // 模拟点击菜单项的沉浸式反馈
  _handleAction(value);
}
```

### 4.3 多分辨率适配建议
在大屏或平板设备上，`DropdownButton` 的宽度建议设置固定上限，避免在极宽的屏幕上过度拉伸。

```dart
SizedBox(
  width: 200, // 限制在大屏下的显示宽度
  child: DropdownButton(...),
)
```

<!-- IMAGE_PLACEHOLDER: 菜单组件在鸿蒙平板横屏模式下的布局展示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 五、完整示例代码

以下代码演示了一个带有城市选择和功能菜单的综合页面。

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() => runApp(const MaterialApp(home: MenuComponentsDemo()));

class MenuComponentsDemo extends StatefulWidget {
  const MenuComponentsDemo({super.key});

  @override
  State<MenuComponentsDemo> createState() => _MenuComponentsDemoState();
}

class _MenuComponentsDemoState extends State<MenuComponentsDemo> {
  String _selectedEnv = '生产环境';
  final List<String> _envs = ['开发环境', '测试环境', '预发环境', '生产环境'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('OHOS 菜单组件实战'),
        actions: [
          // 顶部弹出菜单
          PopupMenuButton<String>(
            icon: const Icon(Icons.more_vert),
            onSelected: (v) => _showMsg("您点击了: $v"),
            itemBuilder: (context) => [
              const PopupMenuItem(value: "refresh", child: Text("刷新数据")),
              const PopupMenuItem(value: "setting", child: Text("系统设置")),
              const PopupMenuDivider(),
              const PopupMenuItem(value: "exit", child: Text("退出登录", style: TextStyle(color: Colors.red))),
            ],
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("配置项选择 (Dropdown)", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            
            // 自定义宽度的 Dropdown
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey.shade300),
                borderRadius: BorderRadius.circular(8),
              ),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<String>(
                  value: _selectedEnv,
                  isExpanded: true, // 撑满容器宽度
                  onChanged: (v) => setState(() => _selectedEnv = v!),
                  items: _envs.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
                ),
              ),
            ),
            
            const SizedBox(height: 48),
            const Text("操作菜单示例 (Popup)", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            
            // 按钮点击触发的弹出菜单
            ElevatedButton.icon(
              onPressed: () {}, // 空方法，通过下面的方式处理弹出
              icon: const Icon(Icons.flash_on),
              label: const Text("快捷操作"),
              onLongPress: () { /* 长按相关 */ },
            ),
            
            const Spacer(),
            const Center(
              child: Text(
                "💡 提示：DropdownButton 定义在 AppBar 时建议设置 background 颜色以符合鸿蒙视觉。",
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey, fontSize: 13),
              ),
            )
          ],
        ),
      ),
    );
  }

  void _showMsg(String msg) {
    HapticFeedback.lightImpact();
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 开发中，灵活运用菜单组件能极大地改善小屏幕内的交互负荷。

1.  **DropdownButton**：最适合固定选项的表单输入，配合 `DropdownButtonHideUnderline` 可以定制出更多样式的外观。
2.  **PopupMenuButton**：最适合“更多操作”的聚合，通过 `shape` 属性可以快速实现圆角优雅的鸿蒙风格菜单。
3.  **用户体验**：不管使用哪种菜单，都要确保弹出后的阴影对比度足够，且菜单项点击后能给出及时的震动或触控反馈。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

