# Flutter for OpenHarmony 实战之基础组件：第二十一篇 Checkbox, Radio 与 Switch — 基础选择控件详解

## 前言

在移动应用开发中，选择类控件（Selection Controls）是用户交互中最基础且最高频的部分。无论是设置页面的开关、注册页面的协议勾选，还是问卷调查的单多选，都离不开 `Checkbox`、`Radio` 和 `Switch` 这三剑客。

在 **Flutter for OpenHarmony** 的生态下，这些标准 Material 组件能够完美运行在鸿蒙设备上，并保持丝滑的交互体验。本文将通过实战案例，深入探讨这三种控件在鸿蒙系统中的样式定制、状态管理以及平台适配技巧。

---

## 一、选择控件的核心机制：状态管理

在开始具体组件之前，我们必须理解 Flutter 选择控件的一个核心原则：**它们是“受控组件”**。

### 1.1 什么是受控组件？
不同于原生的 HTML 表单元素，Flutter 的 `Checkbox` 或 `Switch` 自身并不维护点击后的选中状态。它们只是根据传入的 `value` 属性来展示外观，并通过 `onChanged` 回调通知开发者“用户想要改变状态”。

### 1.2 为什么状态管理很重要？
在鸿蒙应用开发中，由于设备类型多样化（手机、平板、折叠屏等），确保 UI 状态的一致性至关重要。开发者通常需要通过 `setState` 或 Provider/Riverpod 等框架来驱动这些控件的状态。

---

## 二、三剑客详解：用法与定制

### 2.1 Checkbox：多选勾选框

`Checkbox` 用于在多个独立选项中进行选择。

#### （1）基础代码实现
```dart
bool _isChecked = false;

Checkbox(
  value: _isChecked,
  onChanged: (bool? value) {
    setState(() {
      _isChecked = value ?? false;
    });
  },
)
```

#### （2）样式定制
在鸿蒙系统下，我们常需要让 Checkbox 的颜色与品牌色（如鸿蒙经典的深蓝色）对齐。
```dart
Checkbox(
  value: _isAgreed,
  activeColor: Colors.blueAccent, // 选中时的背景颜色
  checkColor: Colors.white,      // 勾选图标的颜色
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(4), // 自定义圆角，更显现代化
  ),
  onChanged: (value) => setState(() => _isAgreed = value!),
)
```

<!-- IMAGE_PLACEHOLDER: Checkbox 在鸿蒙设备上的运行效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

### 2.2 Radio：单选按钮

`Radio` 用于在互斥的选项中选择其一。

#### （1）分组逻辑
Radio 的核心在于 `groupValue`。当 `value` 等于 `groupValue` 时，该按钮被视为选中。

```dart
enum Gender { male, female, other }
Gender? _selectedGender = Gender.male;

Column(
  children: <Widget>[
    RadioListTile<Gender>(
      title: const Text('男'),
      value: Gender.male,
      groupValue: _selectedGender,
      onChanged: (Gender? value) {
        setState(() {
          _selectedGender = value;
        });
      },
    ),
    RadioListTile<Gender>(
      title: const Text('女'),
      value: Gender.female,
      groupValue: _selectedGender,
      onChanged: (Gender? value) {
        setState(() {
          _selectedGender = value;
        });
      },
    ),
  ],
)
```

💡 **技巧**：推荐使用 `RadioListTile` 替代单纯的 `Radio`，因为它自带文本标签且支持点击整行触发。

### 2.3 Switch：开关切换

`Switch` 模拟物理开关，用于开启或关闭某项设置。

#### （1）自适应样式
在 OpenHarmony 上，使用 `Switch.adaptive` 可以根据平台特性展示相应的视觉效果。

```dart
Switch.adaptive(
  value: _isNotificationEnabled,
  activeColor: Colors.green, // 开启状态颜色
  onChanged: (bool value) {
    setState(() {
      _isNotificationEnabled = value;
    });
  },
)
```

<!-- IMAGE_PLACEHOLDER: Switch 动态切换动画效果 -->
<!-- 类型: GIF -->
<!-- 设备: 鸿蒙模拟器 -->

---

## 三、常见应用场景：登录注册表单

将这三种控件整合到一个典型的鸿蒙应用设置页面中：

```dart
class SettingsPage extends StatefulWidget {
  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool _pushNotifications = true;
  int _themeMode = 0; // 0: 浅色, 1: 深色
  bool _agreeTerms = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // 开关场景
        ListTile(
          title: Text("推送通知"),
          trailing: Switch(
            value: _pushNotifications,
            onChanged: (v) => setState(() => _pushNotifications = v),
          ),
        ),
        Divider(),
        // 单选场景
        RadioListTile(
          title: Text("跟随系统"),
          value: 0,
          groupValue: _themeMode,
          onChanged: (int? v) => setState(() => _themeMode = v!),
        ),
        RadioListTile(
          title: Text("深色模式"),
          value: 1,
          groupValue: _themeMode,
          onChanged: (int? v) => setState(() => _themeMode = v!),
        ),
        Divider(),
        // 多选场景（协议勾选）
        CheckboxListTile(
          title: Text("我已阅读并同意《隐私协议》"),
          value: _agreeTerms,
          onChanged: (v) => setState(() => _agreeTerms = v!),
          controlAffinity: ListTileControlAffinity.leading,
        ),
      ],
    );
  }
}
```

---

## 四、OpenHarmony 平台适配

### 4.1 触控区域优化
鸿蒙设备拥有极佳的触控反馈，但对于 `Checkbox` 这种体积较小的控件，直接点击可能存在困难。

✅ **推荐做法**：
使用 `ListTile` 包裹控件，或通过 `MaterialTapTargetSize.padded` 扩大响应区域。

### 4.2 响应式布局考虑
在 OpenHarmony 的分屏或折叠屏状态下，单选列表可能需要从一列变为多列排列。

```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 600) {
      // 大屏/横屏：使用 Grid 布局展示单选框
      return GridView.count(crossAxisCount: 2, children: _buildOptions());
    } else {
      // 窄屏：使用标准垂直列表
      return Column(children: _buildOptions());
    }
  },
)
```

### 4.3 平台视觉的一致性
鸿蒙系统的视觉语言倾向于简洁、通透。在定制 `Switch` 颜色时，建议参考系统设置中的强调色，通常为蓝色系或具有明确情感导向的绿色（开启）与红色（警示）。

---

## 五、完整示例代码

以下代码演示了一个综合性的“用户偏好设置”界面，你可以直接运行在鸿蒙设备上查看效果。

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MaterialApp(home: SelectionControlsDemo()));
}

class SelectionControlsDemo extends StatefulWidget {
  const SelectionControlsDemo({super.key});

  @override
  State<SelectionControlsDemo> createState() => _SelectionControlsDemoState();
}

class _SelectionControlsDemoState extends State<SelectionControlsDemo> {
  // 状态变量
  bool _wifiEnabled = true;
  bool _bluetoothEnabled = false;
  String _mapType = 'standard';
  final List<String> _selectedDays = ['Mon'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter for OHOS 选择器实战'),
        backgroundColor: Colors.blue[700],
        foregroundColor: Colors.white,
      ),
      body: ListView(
        children: [
          _buildHeader("系统开关 (Switch)"),
          SwitchListTile(
            secondary: const Icon(Icons.wifi),
            title: const Text("无线局域网 (Wi-Fi)"),
            value: _wifiEnabled,
            onChanged: (v) => setState(() => _wifiEnabled = v),
          ),
          SwitchListTile(
            secondary: const Icon(Icons.bluetooth),
            title: const Text("蓝牙 (Bluetooth)"),
            value: _bluetoothEnabled,
            onChanged: (v) => setState(() => _bluetoothEnabled = v),
          ),
          
          _buildHeader("地图显示模式 (Radio)"),
          RadioListTile(
            title: const Text("标准地图"),
            value: 'standard',
            groupValue: _mapType,
            onChanged: (v) => setState(() => _mapType = v.toString()),
          ),
          RadioListTile(
            title: const Text("卫星地图"),
            value: 'satellite',
            groupValue: _mapType,
            onChanged: (v) => setState(() => _mapType = v.toString()),
          ),
          
          _buildHeader("重复周期 (Checkbox)"),
          Wrap(
            children: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].map((day) {
              return Padding(
                padding: const EdgeInsets.symmetric(horizontal: 4.0),
                child: FilterChip(
                  label: Text(day),
                  selected: _selectedDays.contains(day),
                  onSelected: (selected) {
                    setState(() {
                      if (selected) {
                        _selectedDays.add(day);
                      } else {
                        _selectedDays.remove(day);
                      }
                    });
                  },
                ),
              );
            }).toList(),
          ),
          
          const Padding(
            padding: EdgeInsets.all(20.0),
            child: Text(
              "📌 提示：在鸿蒙设备上，建议点击区域不小于 44x44vp 以保证交互质量。",
              style: TextStyle(color: Colors.grey, fontSize: 13),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildHeader(String title) {
    return Container(
      padding: const EdgeInsets.fromLTRB(16, 24, 16, 8),
      color: Colors.grey[100],
      child: Text(
        title,
        style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.blueGrey),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 完整示例在鸿蒙手机上的运行截图 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 六、总结

选择类控件虽然简单，但却是提升鸿蒙应用用户体验的关键。

1.  **Checkbox**：适用于多选，注意自定义圆角以符合现代 UI 趋势。
2.  **Radio**：适用于互斥选择，务必使用 `groupValue` 进行逻辑分组。
3.  **Switch**：适用于状态即时切换，建议在鸿蒙端使用 `adaptive` 构造器。

在 OpenHarmony 跨平台开发中，合理利用 `ListTile` 家族组件（如 `SwitchListTile`）能极大地简化布局代码，并提供符合人体工程学的点击区域。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

