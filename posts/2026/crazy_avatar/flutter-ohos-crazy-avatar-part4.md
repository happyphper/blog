[video(video-o6HRFdgw-1769876012975)(type-csdn)(url-https://live.csdn.net/v/embed/512772)(image-https://i-blog.csdnimg.cn/img_convert/4d53d170ddaad274706bd97641c85ec1.jpeg)(title-Jan-31-2026 23-32-23)]

# Flutter for OpenHarmony 实战：疯狂头像 App（四）— 通义万相 AIGC 联调与相册持久化实战

> **摘要**：行百里者半九十。本文作为“疯狂头像”（Crazy Avatar）实战系列的终章，我们将完成从 AI 异步生成到图片系统级保存的全链路闭环。本文将重点攻克鸿蒙（HarmonyOS）侧的 `module.json5` 权限合规、媒体库写入逻辑及网络请求健壮性处理，助你打造商业级 AIGC 应用。

## 前言

在之前的[《动效篇》](https://blog.csdn.net/cannonjinx/article/details/157590679)中，我们为应用注入了生动的灵魂。但一个真正的 AI 工具，如果不能产生“作品”并持久化到物理存储，它就只是一个精致的“空中楼阁”。

在鸿蒙（HarmonyOS Next）生态中，文件的存储安全与权限管理有着极其严格的标准。本篇我们将打通阿里云通义万相的 API 联调，并深度解析如何调用鸿蒙底层能力，将创意艺术品永久存入用户相册。

---

## 零、开发环境与前置准备

为了确保代码能够准确运行，请参考以下实战环境配置：

| 环境项 | 版本/要求 | 备注 |
|---|---|---|
| **Flutter SDK** | 3.7.12-ohos | HarmonyOS 适配版 |
| **DevEco Studio** | 4.1 Release | 对应 HarmonyOS Next API 11+ |
| **API 服务** | 阿里云 DashScope | 需开启通义万相模型权限 |
| **核心依赖** | `http`, `saver_gallery` | 详见第一篇架构篇配置 |

---

## 一、AI 服务联调：接入阿里云通义万相

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/14507ca06e994af7afec2a29e2f53fd4.png)

通义万相提供了基于 `Messages` 的多模态生成接口。在鸿蒙上，我们主要处理异步的 `POST` 请求。

### 1.1 封装 AI 绘图服务

为了提升请求的健壮性，我们引入了超时处理逻辑。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6b0bcd9bb390464da521e4e6bd5a52c7.png)

```dart
Future<String> generateImage({
  required String prompt,
  required String apiKey,
  String model = "qwen-image-max",
}) async {
  final headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer $apiKey',
  };

  final body = jsonEncode({
    "model": model,
    "input": {
      "messages": [{"role": "user", "content": [{"text": prompt}]}]
    },
    "parameters": {"size": "1024*1024", "n": 1}
  });

  try {
    // 🟢 增加 30 秒超时处理，适配 AI 生成的长周期特性
    final response = await http.post(
      Uri.parse(_baseUrl), 
      headers: headers, 
      body: body
    ).timeout(const Duration(seconds: 30));
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['output']['choices'][0]['message']['content'][0]['image'];
    } else {
      throw "生成失败：Code ${response.statusCode}";
    }
  } on TimeoutException {
    throw "请求超时，AI 绘画可能需要更多时间，请检查网络";
  } catch (e) {
    throw "服务异常：$e";
  }
}
```

🏆 **实战建议**：由于通义万相是异步生成链路，虽然 API 提供了直接响应，但在高并发时可能会返回中间状态。建议在 UI 层增加对错误代码的语义化解析（如非法 Prompt 拦截）。

---

## 二、攻克鸿蒙持久化：权限合规与相册写入

在 HarmonyOS Next 中，保存图片到相册涉及“分布式能力”与“文件夹沙盒”双重规则。

### 2.1 关键：鸿蒙侧权限配置

在 `ohos/entry/src/main/module.json5` 中，必须声明媒体读写权限（针对使用三方持久化库的项目）：

```json5
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.WRITE_IMAGEVIDEO", // 🟢 允许写入相册
        "reason": "$string:reason_save_image",
        "usedScene": { "abilities": ["EntryAbility"], "when": "always" }
      }
    ]
  }
}
```

### 2.2 实现相册写入逻辑

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f69c1650485548c5b9ad1fa83ea02c8f.png)

我们采用“下载字节流 -> 调用原生通道 -> 写入媒体库”的路径。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ceccfdfea79344bd92f2a62e4f98a468.gif)

```dart
Future<void> _saveToGallery() async {
  try {
    // 1. 🟢 下载图片字节流
    final response = await http.get(Uri.parse(_imageUrl!));
    if (response.statusCode != 200) throw "图片下载失败";
    
    final Uint8List bytes = response.bodyBytes;

    // 2. 🟢 调用鸿蒙原生适配接口
    final result = await SaverGallery.saveImage(
      bytes,
      quality: 100,
      fileName: "avatar_${DateTime.now().millisecondsSinceEpoch}.png",
      androidRelativePath: "Pictures/CrazyAvatar", // 插件已适配鸿蒙媒体目录映射
    );

    if (result.isSuccess) {
      _showSuccess("创意作品已存入系统相册");
    } else {
      _showError("保存失败：${result.errorMessage}");
    }
  } catch (e) {
    _showError("操作失败：$e");
  }
}
```

---

## 三、全系列技术栈总览：从入门到进阶

经过四篇连载，我们构建的“疯狂头像” App 已涵盖 Flutter for OpenHarmony 开发的 80% 核心场景。

| 模块 | 核心方案 | 鸿蒙适配点 |
|---|---|---|
| **工程初始化** | Git 跨平台插件注入 | 引用 OpenHarmony-TPC 适配库 |
| **视觉呈现** | Glassmorphism + Stack | 背景层叠与 OLED 黑色优化 |
| **动效系统** | flutter_animate | Vsync 信号同步与 120Hz 适配 |
| **配置持久化** | shared_preferences | 映射至 ohos.Preferences 存储 |
| **AI 集成** | 阿里云 DashScope SDK (http) | 异步网络请求与超时健壮性 |
| **存储访问** | saver_gallery + module.json5 | 攻克媒体库写入权限与沙盒限制 |

---

## 四、系列心法总结

"疯狂头像"实战系列到此正式收官。作为开发者，我们不仅是在“搬运代码”，更是在**探路新生态**。

在鸿蒙 Next 时代，Flutter 已经证明了其作为“第一梯队”跨平台框架的稳定性与审美表现力。掌握这一套实战路径，你将能够：
1. **拥抱新基建**：在手机、平板乃至折叠屏上提供一致的 AI 体验。
2. **打磨精品感**：通过玻璃拟态和复合动效，让鸿蒙原生应用具有商业级的高级感。

---

 📦 **全项目源码开源地址**：[cannonjinx/crazy_avatar](https://gitcode.com/cannonjinx/crazy_avatar)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---
*感谢收看本系列！如果您在鸿蒙适配过程中遇到任何技术诡疾，欢迎在评论区留下 ErrorLog，我会第一时间为你诊断排障。下一套实战系列，你想看什么？欢迎留言！*
