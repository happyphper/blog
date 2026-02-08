# Flutter for OpenHarmony 实战之基础组件：第三十九篇 Dismissible — 极致流畅的侧滑删除体验

## 前言

在移动应用中，侧滑删除（Swipe-to-Dismiss）是一种非常直觉且高效的交互方式。无论是清理不再需要的通知消息，还是删除购物清单中的商品，用户只需轻轻一拨即可完成操作。这种符合物理直觉的交互能让应用显得更加轻盈和专业。

在 **Flutter for OpenHarmony** 平台上，`Dismissible` 组件不仅提供了极高的性能表现，还能自动适配鸿蒙系统的平滑曲线动画。本文将教大家如何从零构建一个功能完备的侧滑系统，并加入二次确认与背景定制。

---

## 一、Dismissible 的基本逻辑

`Dismissible` 组件需要一个唯一的 `key` 来标识其包裹的子组件，并在滑动消失后从数据源中移除该项。

### 1.1 基础实现代码
```dart
Dismissible(
  key: Key(item.id), // 核心：唯一标识
  onDismissed: (direction) {
    // 逻辑：从列表数据源中真正删除
    setState(() {
      items.removeAt(index);
    });
    // 提示用户
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('项已删除')));
  },
  child: ListTile(title: Text(item.title)),
)
```

### 1.2 滑动方向控制
我们可以限制只能向左滑动，或者左右滑动触发不同的逻辑。
- `direction: DismissDirection.endToStart` (限制左滑)
- `direction: DismissDirection.horizontal` (默认左右皆可)

---

## 二、进阶：背景美化与确认提示

一个合格的侧滑删除，必须在滑开后展示明确的操作背景（如红色的垃圾桶图标）。

### 2.1 自定义滑动背景
```dart
Dismissible(
  key: Key(_items[index]),
  // 滑动时露出的背景
  background: Container(
    color: Colors.red,
    alignment: Alignment.centerLeft,
    padding: const EdgeInsets.horizontal(20),
    child: const Icon(Icons.delete, color: Colors.white),
  ),
  // 第二个背景（通常是向左滑时露出）
  secondaryBackground: Container(
    color: Colors.blue,
    alignment: Alignment.centerRight,
    padding: const EdgeInsets.horizontal(20),
    child: const Icon(Icons.archive, color: Colors.white),
  ),
  child: _buildListItem(index),
)
```

### 2.2 二次确认逻辑 (confirmDismiss)
为了防止误删，我们可以要求用户在项目彻底消失前点击确认。

```dart
confirmDismiss: (direction) async {
  return await showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: const Text("确认删除?"),
      content: const Text("此操作无法撤销。"),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context, false), child: const Text("取消")),
        TextButton(onPressed: () => Navigator.pop(context, true), child: const Text("删除")),
      ],
    ),
  );
}
```

<!-- IMAGE_PLACEHOLDER: 具有红色背景和垃圾桶图标的 Dismissible 在鸿蒙设备上的删除动效 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、OpenHarmony 平台适配建议

### 3.1 列表性能调优
在长列表中（如 1000+ 条消息），侧滑动画的掉帧是非常影响体验的。

✅ **推荐方案**：
由于鸿蒙设备往往采用高刷屏幕（90Hz/120Hz），建议在 `ListItem` 中使用简单的 Widget 结构。
如果删除涉及复杂的后台网络同步，可以先执行 UI 删除（乐观更新），通过 `SnackBar` 提供“撤回”选项，这样用户不需要等待网络请求完成就能获得流畅反馈。

### 3.2 触感反馈 (Vibration)
当组件滑过临界点（即将变为删除状态）时，调用一次鸿蒙系统的触感反馈。

```dart
import 'package:flutter/services.dart';

// 在 onUpdate 回调中根据 reachThreshold 判断
onUpdate: (details) {
  if (details.reached && !_vibrated) {
    HapticFeedback.mediumImpact(); // 触发“咔嗒”一声的物理感反馈
    _vibrated = true;
  }
}
```

### 3.3 避让系统导航手势
鸿蒙手机默认使用边缘右滑返回。如果你的 `Dismissible` 被放在最靠近屏幕边缘的位置，可能会与系统返回手势冲突。

💡 **避坑指南**：
适当调整 `Dismissible` 的 `dragStartBehavior` 为 `DragStartBehavior.down`，或者在 ListView 侧边留出足够的 `padding`。

<!-- IMAGE_PLACEHOLDER: Dismissible 滑动效果在大屏/分屏模式下的交互展示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 四、完整示例代码

以下提供一个完整的“任务清单”删改示例。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: DismissibleDemo()));

class DismissibleDemo extends StatefulWidget {
  const DismissibleDemo({super.key});

  @override
  State<DismissibleDemo> createState() => _DismissibleDemoState();
}

class _DismissibleDemoState extends State<DismissibleDemo> {
  final List<String> _items = List.generate(10, (idx) => "待办任务 ${idx + 1}");

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 侧滑删除实战')),
      body: ListView.separated(
        itemCount: _items.length,
        separatorBuilder: (_, __) => const Divider(height: 1),
        itemBuilder: (context, index) {
          final item = _items[index];
          return Dismissible(
            key: Key(item),
            // 背景样式设计
            background: _buildBox(Colors.green, Icons.check, Alignment.centerLeft),
            secondaryBackground: _buildBox(Colors.red, Icons.delete, Alignment.centerRight),
            
            // 确认逻辑
            confirmDismiss: (dir) async {
              if (dir == DismissDirection.startToEnd) {
                _showMsg("任务已标记为完成");
                return false; // 不删除，仅触发逻辑
              }
              return true; // 允许删除
            },
            
            onDismissed: (dir) {
              setState(() => _items.removeAt(index));
              _showMsg("任务已从清单中移除");
            },
            
            child: ListTile(
              contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              title: Text(item, style: const TextStyle(fontSize: 18)),
              subtitle: const Text("左滑删除，右滑标记完成"),
            ),
          );
        },
      ),
    );
  }

  Widget _buildBox(Color color, IconData icon, Alignment align) {
    return Container(
      color: color,
      alignment: align,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: Icon(icon, color: Colors.white, size: 28),
    );
  }

  void _showMsg(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
  }
}
```

---

## 五、总结

在 Flutter for OpenHarmony 开发中，灵活运用 `Dismissible` 能极大地简化列表项的管理交互。

1.  **Key 的重要性**：永远不要在 Dismissible 中漏掉唯一的 Key，否则在数据变动时会出现异常。
2.  **视觉提示**：不仅要能滑动，更要通过 `background` 告知用户滑动后的结果。
3.  **适配鸿蒙**：在大屏或高刷屏上，通过触感反馈和优化列表性能，能让这一滑动动作变得更加具有“实体感”。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

