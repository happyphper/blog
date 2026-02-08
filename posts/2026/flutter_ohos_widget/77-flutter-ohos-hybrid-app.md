![封面图](images/77-cover.png)

# Flutter for OpenHarmony 实战之进阶：第七十七篇 混合开发实战 — 在鸿蒙原生应用中嵌入 Flutter Module

## 前言

在实际的企业级项目开发中，很少有从零开始全量使用 Flutter 开发的情况。更多时候，我们需要在现有的 **HarmonyOS NEXT** 原生项目（使用 ArkTS 开发）中，将某个复杂的业务模块（如账单中心、活动页）交由 Flutter 负责。

这就是所谓的“混合开发（Add-to-App）”模式。本篇将手把手带你完成 Flutter Module 在鸿蒙原生工程中的集成，并解决最头疼的资源共享与跳转问题。

---

## 一、混合开发的核心架构

在混合模型中，Flutter 被视为一个“特殊的 View”或一个“能力插件”。
- **原生侧 (Host)**: 负责应用的生命周期管理、窗口能力及主要的系统权限申请。
- **Flutter 侧 (Module)**: 负责特定页面的高性能渲染，通过 `MethodChannel` 接收原生的指令。

---

## 二、实战：将 Flutter 集成至鸿蒙原生项目

### 2.1 创建 Flutter Module
首先，我们需要创建一个专门用于混合集成的 Module 工程。

```bash
# 💡 技巧：创建一个 module 类型的工程，而非独立 app
flutter create --template module my_flutter_module
```

### 2.2 鸿蒙原生工程配置
在鸿蒙工程的 `oh-package.json5` 中，引用这个新创建的 Flutter Module。

```json
{
  "dependencies": {
    "my_flutter_module": "file:../my_flutter_module/.ohos/har/my_flutter_module.har"
  }
}
```

### 2.3 原生端加载 FlutterAbility
在 ArkTS 中，通过 `FlutterAbility` 或 `FlutterComponent` 来承载 Flutter 内容。

```typescript
// 💡 原理：在鸿蒙原生 Ability 中路由到 Flutter
import { FlutterAbility } from '@ohos/flutter_ohos';

export default class HybridAbility extends FlutterAbility {
  // 📌 可以在这里指定 Flutter 的初始路由名
  getInitialRoute(): string {
    return "/billing_module";
  }
}
```

---

## 三、混合开发中的资源同步

### 3.1 资产 (Assets) 共享
混合开发最常见的问题是：原生的图片资源，Flutter 侧能不能复用？
- ✅ **方案**：在 Flutter 的 `pubspec.yaml` 中，可以通过特定的路径映射直接访问鸿蒙项目的 `resources` 目录。

### 3.2 字体库同步
为了保证视觉一致性，建议将 **HarmonyOS Sans** 作为全局字体，由鸿蒙原生下载并安装，Flutter 侧直接引用对应的 FamilyName。

---

## 四、OpenHarmony 平台适配挑战

### 4.1 多 Ability 跳转难题
鸿蒙系统采用了基于 `UIAbility` 的任务管理。从一个原生 Ability 跳转到一个包含 Flutter 的 Ability 时，可能会存在明显的窗口切换动效。
- ✅ **建议**：尽量在同一个 `EntryAbility` 中使用不同的 `Page` 来切换原生与 Flutter，利用 Flutter 提供的组件化集成方式 (`FlutterView`) 以获得更无缝的体验。

### 4.2 内存隔离与共享
混合开发模式下，Dart 虚拟机会占用额外的原生内存。
- ⚠️ **切记**：当不再需要 Flutter 模块时，务必调用 `engine.destroy()`，释放鸿蒙端的纹理与内存占用，防止应用因内存过载被系统杀死。

---

## 五、混合开发最佳实践清单

1.  ✅ **路由管理**：原生侧建立路由表，通过参数决定 Flutter 显示哪个片段。
2.  ✅ **解耦通信**：所有与原生的交互必须通过 `MethodChannel` 封装，不要在 Flutter 代码里硬编码平台逻辑。
3.  ✅ **包体积控制**：Flutter Module 生成的 HAR 包体积应严格监控，避免拖累鸿蒙主包的下载转化率。

---

## 六、总结

混合开发是 Flutter 在鸿蒙生态大规模落地的必备技能：
1.  **稳健为主**：利用原生稳住基础框架。
2.  **敏捷为王**：利用 Flutter 快速迭代业务页面。
3.  **深度桥接**：打破 ArkTS 与 Dart 的次元壁。

掌握了混合开发，你就具备了将原有庞大鸿蒙项目平滑升级到跨平台架构的能力。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/hybrid-module](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/hybrid-module)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
