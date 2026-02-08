# Flutter for OpenHarmony 实战之基础组件：第二十五篇 DatePicker 与 TimePicker — 日期时间选择器及本地化适配

## 前言

在处理预约挂号、设置闹钟或选择生日等业务场景时，日期和时间选择器（Pickers）是不可或缺的 UI 组件。良好的选择器不仅要操作便捷，更要符合用户所在地区的文化习惯（本地化）。

在 **Flutter for OpenHarmony** 平台上，基础的 Material `showDatePicker` 和 `showTimePicker` 能够无缝运行。通过简单的参数调优，我们可以让这些弹窗式控件在鸿蒙设备上展现出更加精致、符合中文语境的视觉表现。本文将重点介绍如何配置这些选择器，并实现完整的本地化（Localization）支持。

---

## 一、日期选择器：DatePicker

### 1.1 基础调用
在 Flutter 中，日期选择器是一个异步函数调用，会返回用户选择的 `DateTime` 对象。

```dart
Future<void> _selectDate(BuildContext context) async {
  final DateTime? picked = await showDatePicker(
    context: context,
    initialDate: DateTime.now(),
    firstDate: DateTime(2020),
    lastDate: DateTime(2030),
    helpText: '选择预约日期', // 弹窗顶部的提示文字
    cancelText: '取消',
    confirmText: '确定',
  );
  if (picked != null) {
    setState(() {
      _selectedDate = picked;
    });
  }
}
```

### 1.2 进阶定制：日期范围选择
如果需要选择一段时间（如酒店入住与退房），应使用 `showDateRangePicker`。

```dart
final DateTimeRange? pickedRange = await showDateRangePicker(
  context: context,
  firstDate: DateTime(2024),
  lastDate: DateTime(2025),
  builder: (context, child) {
    return Theme(
      data: Theme.of(context).copyWith(
        colorScheme: ColorScheme.light(primary: Colors.blue[700]!), // 选中色
      ),
      child: child!,
    );
  },
);
```

<!-- IMAGE_PLACEHOLDER: DateRangePicker 在鸿蒙设备上的全局展示效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 二、时间选择器：TimePicker

### 2.1 24小时制与12小时制
在鸿蒙系统中，用户通常更偏好 24 小时制。我们可以通过设置 `alwaysUse24HourFormat` 来强制指定。

```dart
Future<void> _selectTime(BuildContext context) async {
  final TimeOfDay? picked = await showTimePicker(
    context: context,
    initialTime: TimeOfDay.now(),
    builder: (BuildContext context, Widget? child) {
      // 强制使用 24 小时制并应用自定义样式
      return MediaQuery(
        data: MediaQuery.of(context).copyWith(alwaysUse24HourFormat: true),
        child: child!,
      );
    },
  );
  if (picked != null) {
    setState(() => _selectedTime = picked);
  }
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙风格的 24 小时制 TimePicker 运行截图 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、鸿蒙端本地化配置 (Localization)

💡 **核心痛点**：默认情况下，Flutter 的选择器显示为英文（如 "SELECT DATE"）。在鸿蒙应用中，我们需要将其设为中文环境。

### 3.1 引入依赖
在 `pubspec.yaml` 中添加本地化支持库：
```yaml
dependencies:
  flutter_localizations:
    sdk: flutter
```

### 3.2 配置入口程序
在 `MaterialApp` 中添加必要的代理。

```dart
MaterialApp(
  localizationsDelegates: const [
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
  ],
  supportedLocales: const [
    Locale('zh', 'CN'), // 中文简体
    Locale('en', 'US'), // 英文
  ],
  locale: const Locale('zh', 'CN'), // 强制设为中文
  home: MyPickerPage(),
)
```
完成此配置后，`showDatePicker` 的月份（一月、二月...）和星期（周一、周二...）将自动变为中文。

---

## 四、OpenHarmony 平台适配建议

### 4.1 窗口层级处理
在鸿蒙的分屏（Split Screen）模式下，弹窗式选择器会自动调整其在屏幕中心的位置。

✅ **推荐方案**：
对于宽度极大的鸿蒙平板，考虑使用 `showModalBottomSheet` 结合 `CupertinoDatePicker` 构建滚动式的选择器，这种样式在大屏设备上往往比居中的 Material 弹窗更易于单手操作。

### 4.2 触感反馈优化
当用户拨动时间轴或点击日期时，结合鸿蒙系统震动反馈能极大增强“确定感”。

```dart
import 'package:flutter/services.dart';

// 在 confirm 按钮回调中
void _onConfirmed() {
  HapticFeedback.vibrate(); // 提供点击确认的震感
  // ...逻辑处理
}
```

### 4.3 刘海屏与避让
虽然 `showDatePicker` 内部已处理了安全区域，但在自定义 Picker 布局时，务必使用 `SafeArea` 包裹，避免内容被鸿蒙设备的挖孔屏幕遮挡。

---

## 五、完整示例代码

以下代码演示了一个支持“中文本地化”且包含日期和时间双重选择的设置页面。

```dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

void main() {
  runApp(const MaterialApp(
    localizationsDelegates: [
      GlobalMaterialLocalizations.delegate,
      GlobalWidgetsLocalizations.delegate,
      GlobalCupertinoLocalizations.delegate,
    ],
    supportedLocales: [Locale('zh', 'CN')],
    home: PickerDemoPage(),
  ));
}

class PickerDemoPage extends StatefulWidget {
  const PickerDemoPage({super.key});

  @override
  State<PickerDemoPage> createState() => _PickerDemoPageState();
}

class _PickerDemoPageState extends State<PickerDemoPage> {
  DateTime _date = DateTime.now();
  TimeOfDay _time = const TimeOfDay(hour: 08, minute: 30);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 选择器本地化实战')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildCard(
            title: "预约日期",
            value: "${_date.year}-${_date.month}-${_date.day}",
            icon: Icons.calendar_today,
            onTap: () => _pickDate(context),
          ),
          const SizedBox(height: 16),
          _buildCard(
            title: "提醒时间",
            value: "${_time.hour} : ${_time.minute.toString().padLeft(2, '0')}",
            icon: Icons.access_time,
            onTap: () => _pickTime(context),
          ),
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 32),
            child: Text(
              "💡 小贴士：本页面已通过 GlobalMaterialLocalizations 配置为中文环境。",
              style: TextStyle(color: Colors.grey, fontSize: 13),
              textAlign: TextAlign.center,
            ),
          )
        ],
      ),
    );
  }

  Widget _buildCard({required String title, required String value, required IconData icon, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.blue.withAlpha(10),
          border: Border.all(color: Colors.blue.withAlpha(30)),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            Icon(icon, color: Colors.blue[800]),
            const SizedBox(width: 20),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(color: Colors.blueGrey, fontSize: 14)),
                const SizedBox(height: 4),
                Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ],
            ),
            const Spacer(),
            const Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
          ],
        ),
      ),
    );
  }

  Future<void> _pickDate(BuildContext context) async {
    final DateTime? d = await showDatePicker(
      context: context,
      initialDate: _date,
      firstDate: DateTime(2024),
      lastDate: DateTime(2026),
    );
    if (d != null) setState(() => _date = d);
  }

  Future<void> _pickTime(BuildContext context) async {
    final TimeOfDay? t = await showTimePicker(
      context: context,
      initialTime: _time,
    );
    if (t != null) setState(() => _time = t);
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的日常开发中，处理好日期与时间的交互是提升应用专业感的捷径。

1.  **DatePicker**：弹窗式简单直观，注意控制 `firstDate` 和 `lastDate` 的合理区间。
2.  **TimePicker**：建议在鸿蒙端优先使用 24 小时制以符合国民习惯。
3.  **本地化**：强烈建议在项目初期就配置好 `flutter_localizations`，这能让所有系统自带的对话框和提示文字自动转为中文。

通过合理的样式定制和震动反馈，这些基础组件能在鸿蒙设备上焕发出不亚于原生开发的卓越体验。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

