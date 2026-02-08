![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战：疯狂头像 App（一）— 架构设计与秘钥管理系统

> **摘要**：在 AIGC 热潮下，如何快速将 AI 绘画能力带入鸿蒙生态？本文将开启“疯狂头像”（Crazy Avatar）实战专栏。我们将从工程架构设计出发，讲解如何构建一个安全的秘钥管理系统，并适配鸿蒙系统的本地存储机制。

![疯狂头像 App 技术架构图](./images/crazy_avatar_architecture.png)

## 前言

随着 HarmonyOS Next 商业化进程的推进，开发者们对高性能、高颜值的鸿蒙应用需求日益增长。Flutter 作为顶级的跨平台框架，在鸿蒙上的表现非常惊艳。

为了让大家系统性地掌握 Flutter for OpenHarmony 的高级实战技巧，我规划了《疯狂头像 App》专栏，共 4 篇：
1.  **架构篇：架构设计与秘钥管理系统（本文）**
2.  **视觉篇：层叠背景与极致玻璃拟态 (Glassmorphism)**
3.  **动效篇：复合动画与交互反馈 — 让 UI 跃动起来**
4.  **集成篇：通义万相 AIGC 联调与相册持久化实战**

本文作为开篇，将带你打好工程地基。

---

## 一、技术选型与架构蓝图

"疯狂头像"是一款基于 AI 的创意头像生成应用，用户输入一段文字，App 调用大模型生成独特的头像。

**技术栈选型**：
- **UI 框架**：Flutter (OpenHarmony 适配版)
- **动效库**：`flutter_animate` (实现高级流光动效)
- **字体**：`google_fonts` (Google Font 鸿蒙化适配)
- **存储**：`shared_preferences` (键值对持久化)
- **AI 引擎**：阿里云通义万相 (提供专业绘图 API)

### 架构设计思路

我们采用简单的 **Service - Page** 架构：
- **Logic 层**：封装 `SettingsService` 和 `AliyunService`，负责数据持久化和 API 通信。
- **UI 层**：利用 `CustomScrollView` 和 `Sliver` 体系构建高性能列表，结合 `Stack` 实现层叠背景装饰。

---

## 二、项目初始化与鸿蒙版插件配置

在鸿蒙上进行 Flutter 开发，最关键的一步是正确引用已经适配好的插件。

### 2.1 pubspec.yaml 深度解析

我们需要在 `pubspec.yaml` 中特别配置指向 OpenHarmony-TPC 组的插件：

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.6.0
  google_fonts: ^6.3.0
  flutter_animate: ^4.5.2
  
  # 🟢 重点：使用由鸿蒙社区维护的适配插件
  shared_preferences:
    git:
      url: https://gitcode.com/openharmony-tpc/flutter_packages.git
      path: packages/shared_preferences/shared_preferences

  # 🟢 重点：saver_gallery 4.0.0+ 已原生支持鸿蒙
  saver_gallery: ^4.0.0
```

提示：在鸿蒙开发初期，插件的 `git` 指向非常重要，确保你引用的是社区验证过的可用版本。

---

## 三、核心架构：SettingsService 秘钥管理

由于 AI 生成需要 API Key，让用户自行配置 Key 是比较灵活且降低成本的做法。我们需要一个单例 Service 来管理这些配置。

### 3.1 秘钥持久化实现

我们使用 `shared_preferences` 在鸿蒙侧持久化数据。新建 `lib/services/settings_service.dart`:

```dart
import 'package:shared_preferences/shared_preferences.dart';

class SettingsService {
  static const String _keyApiKey = 'aliyun_api_key';
  static const String _keyModel = 'aliyun_model_name';

  // 保存 API Key
  Future<void> saveApiKey(String apiKey) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyApiKey, apiKey);
  }

  // 获取 API Key
  Future<String?> getApiKey() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyApiKey);
  }

  // 默认模型配置
  static const String defaultModel = 'qwen-image-max';
}
```

💡 **技巧**：在鸿蒙上，`shared_preferences` 会自动映射到鸿蒙系统的 `Preferences` 存储，性能表现非常均衡。

---

## 四、UI 实战：打造 Premium 感的配置页面

即使是设置页面，我们也追求极致的视觉体验。

### 4.1 玻璃拟态 Card (Glass Card)

通过 `BackdropFilter` 实现毛玻璃效果，配合深色模式背景极其优雅。

```dart
Widget _buildGlassCard({required Widget child}) {
  return ClipRRect(
    borderRadius: BorderRadius.circular(24),
    child: BackdropFilter(
      filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
      child: Container(
        padding: const EdgeInsets.all(32),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.05),
          border: Border.all(color: Colors.white.withOpacity(0.1)),
          gradient: LinearGradient(
            colors: [Colors.white.withOpacity(0.1), Colors.white.withOpacity(0.02)],
          ),
        ),
        child: child,
      ),
    ),
  );
}
```

### 4.2 设置页面逻辑：防抖自动保存

为了提升用户体验，我们为 `TextField` 添加监听器，实现 800ms 的输入防抖自动保存，减少用户的手动“保存”操作。

```dart
void _onInputChanged() {
  if (_debounce?.isActive ?? false) _debounce!.cancel();
  _debounce = Timer(const Duration(milliseconds: 800), () {
    _saveSettings(); // 间隔 800ms 自动保存到鸿蒙 Preferences
  });
}
```

---

## 五、鸿蒙平台适配建议

1.  **权限声明**：在鸿蒙侧调用 `shared_preferences` 不需要特殊权限，但后续保存相册则需要。
2.  **字体加载**：鸿蒙系统自带字体与 `GoogleFonts` 的融合度很高，但在极端弱网环境下，建议内置核心字体的 `.ttf` 以防界面空白。
3.  **调试技巧**：使用 `DevEco Studio` 的实时日志查看持久化写入是否成功，确保 `Preferences` 文件的路径正确。

---

## 六、上篇小结

通过本篇架构篇，我们完成了以下任务：
- 建了项目地基，配置了**鸿蒙版专用的三方件**。
- 实现了核心的**秘钥管理系统**。
- 封装了具备高级感的**玻璃拟态组件**。

地基虽然打好，但现在的应用看起来还是比较单一。

在下一篇**【视觉篇】**中，我们将开启视觉盛宴：讲解如何通过 Flutter 的 `Stack` 和 `Positioned` 打造具有层次感的玫瑰色渐变背景，并深度定制符合鸿蒙调性的玻璃拟态 UI。

---

> 📦 **完整代码已上传至 AtomGit**：[cannonjinx/crazy_avatar (GitHub 镜像)](https://gitcode.com/cannonjinx/crazy_avatar)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
