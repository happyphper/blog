# Flutter for OpenHarmony 实战之基础组件：第六十篇 Stepper — 实现清晰的步骤引导式流程

## 前言

在处理诸如注册流程、实名认证、甚至是物流追踪等具有明确先后顺序的任务时，如果将所有表单项堆砌在一个页面，会给用户带来巨大的认知压力。分步式引导（Step-by-Step）是解决这一问题的经典方案，它能让复杂的长流程拆解为一个个可消化的微动作。

在 **Flutter for OpenHarmony** 平台上，内置的 `Stepper` 组件提供了完整的垂直与水平步骤管理体系。配合鸿蒙系统的流式设计，我们可以快速构建出逻辑清晰、体验连贯的引导系统。本文将带大家通过实战跑通 `Stepper` 的核心用法及适配策略。

---

## 一、Stepper 的核心结构

`Stepper` 主要由一组 `Step`（步骤）组成，每个步骤包含：
- **title**：步骤标题。
- **content**：该步骤展示的子组件（表单等）。
- **isActive**：当前是否处于该步骤。
- **state**：步骤状态（Indexed, Editing, Complete, Error）。

### 1.1 基础实现代码
```dart
Stepper(
  currentStep: _index, // 当前激活的步骤索引
  onStepTapped: (index) => setState(() => _index = index), // 点击跳转
  onStepCancel: () => _onCancel(),                         // 点击取消
  onStepContinue: () => _onContinue(),                     // 点击继续
  steps: <Step>[
    Step(title: const Text('下单'), content: Text('配置您的鸿蒙智能设备参数...'), isActive: _index >= 0),
    Step(title: const Text('支付'), content: Text('请选择支付方式...'), isActive: _index >= 1),
    Step(title: const Text('收获'), content: Text('填写您的收货地址...'), isActive: _index >= 2),
  ],
)
```

---

## 二、进阶：垂直与水平模式的动态切换

在鸿蒙手机上，垂直（Vertical）模式是首选，因为它符合长页面的浏览习惯；但在平板或横屏模式下，水平（Horizontal）模式能更好地利用屏幕空间。

### 2.1 响应式模式切换
```dart
Stepper(
  type: screenWidth > 600 ? StepperType.horizontal : StepperType.vertical,
  //...
)
```

<!-- IMAGE_PLACEHOLDER: Stepper 在鸿蒙设备上垂直与水平两种模式的对比演示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、实战：带校验功能的表单分步提交

💡 **业务技巧**：在用户点击“继续”之前，先进行当前步骤内容的表单校验。

```dart
void _onContinue() {
  if (_index < _stepsCount - 1) {
    // 执行当前步骤的校验逻辑
    if (currentFormValid) {
      setState(() => _index += 1);
    } else {
      // 标记当前步骤为 Error 状态
    }
  } else {
    // 提交最终结果
  }
}
```

<!-- IMAGE_PLACEHOLDER: 具有 Complete 状态勾号和 Editing 状态标记的 Stepper 运行详情 -->
<!-- 类型: 截图 -->
<!-- 设备: 模拟器 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 适配鸿蒙系统长屏幕
最近的鸿蒙手机（如 Mate 系列）屏幕比例较长。

✅ **推荐方案**：
在垂直模式下，如果 `Step` 内容过多，会导致页面产生内滚动。由于 `Stepper` 本身已经处理了滚动逻辑，请确保不要将其包裹在高度无限的组件内。在鸿蒙端，建议给 `Stepper` 提供一个带有底边距的 `Padding`，防止最后一项步骤的控制按钮被系统底部的“手势导航条”遮挡。

### 4.2 触感交互补偿
当用户点击“下一步”并成功切换步骤时。

💡 **调优方案**：
在 `onStepContinue` 中触发 `HapticFeedback.lightImpact()`。特别是在所有步骤完成进入 `StepState.complete` 时，触发一次 `HapticFeedback.mediumImpact()`，能给用户带来仪式感。

### 4.3 状态的可视化反馈
鸿蒙 UI 强调高对比度和清晰的状态指示。

✅ **最佳实践**：
充分利用 `StepState`。
- 如果某一步骤校验失败，务必设为 `StepState.error`，此时图标会变为红色的感叹号。
- 已完成的步骤设为 `StepState.complete`，图标会变为绿色的对勾。
在多端显示的鸿蒙平板上，这种明确的状态指示能极大降低用户的操作困惑。

<!-- IMAGE_PLACEHOLDER: 鸿蒙平板折叠屏下的分步注册页面适配效果展示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 五、完整示例代码

以下代码演示了一个包含“基本信息”、“安全设置”、“完成确认”三个环节的综合步骤引导示例。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: StepperDemo()));

class StepperDemo extends StatefulWidget {
  const StepperDemo({super.key});

  @override
  State<StepperDemo> createState() => _StepperDemoState();
}

class _StepperDemoState extends State<StepperDemo> {
  int _currentIdx = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 分步流程引导')),
      body: Stepper(
        currentStep: _currentIdx,
        onStepTapped: (v) => setState(() => _currentIdx = v),
        onStepContinue: () {
          if (_currentIdx < 2) setState(() => _currentIdx += 1);
        },
        onStepCancel: () {
          if (_currentIdx > 0) setState(() => _currentIdx -= 1);
        },
        steps: [
          Step(
            title: const Text("账号信息"),
            content: TextFormField(decoration: const InputDecoration(hintText: "请输入鸿蒙 ID")),
            isActive: _currentIdx >= 0,
            state: _currentIdx > 0 ? StepState.complete : StepState.editing,
          ),
          Step(
            title: const Text("隐私权限"),
            content: const Text("请确认同意获取系统位置与通知权限，以便为您提供精准服务。"),
            isActive: _currentIdx >= 1,
            state: _currentIdx > 1 ? StepState.complete : StepState.editing,
          ),
          Step(
            title: const Text("开启体验"),
            content: const Text("恭喜，您已完成全部配置！"),
            isActive: _currentIdx >= 2,
            state: _currentIdx == 2 ? StepState.editing : StepState.indexed,
          ),
        ],
      ),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的业务系统开发中，`Stepper` 是提升用户耐心与操作准确率的核心组件。

1.  **分步治之**：将庞大的表单压力分散到各个微小的步骤中。
2.  **状态驱动**：利用 `StepState` 提供实时的正确/错误反馈。
3.  **鸿蒙适配**：在长屏设备上注意按钮位置避让，在大屏设备上灵活切换水平布局，并配合触控震感打造顶级交互手感。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

