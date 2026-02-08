---
title: "Flutter for OpenHarmony 实战：工程落地 — 签名、HAP 编译打包与真机发布全流程"
date: 2026-02-02
tags: ["Flutter", "OpenHarmony", "HAP打包", "签名配置"]
categories: ["Flutter for OpenHarmony 实战"]
---

# Flutter for OpenHarmony 实战：工程落地 — 签名、HAP 编译打包与真机发布全流程

## 前言

经过前七篇的连载，我们的 **Splendid Movie** 已经从设计稿变成了代码，又从代码变成了运行在 IDE 里的精美应用。现在，是时候把它打包出来，安装到用户的鸿蒙手机上了。

OpenHarmony 的打包发布流程与 Android APK 有较大区别，涉及**HAP (Harmony Ability Package)** 格式、特殊的签名证书以及复杂的构建指令。本文将手把手带你完成这至关重要的一步。

<!-- IMAGE_PLACEHOLDER: 打包成功示意图 -->
<!-- 类型: 截图 -->
<!-- 内容: 命令行显示 build successful，以及生成出的 entry-default-signed.hap 文件图标 -->

---

## 一、 签名配置：打通真机运行的关卡

不同于 Android 可以生成本地调试 keystore，鸿蒙的真机调试通常需要配合华为开发者联盟的证书（Profile）。

### 1.1 自动签名 (DevEco Studio)

对于个人开发者，最简单的方式是利用 DevEco Studio 的自动签名功能：

1.  用 DevEco Studio 打开项目的 `ohos` 目录。
2.  点击 **File > Project Structure > Project > Signing Configs**。
3.  勾选 **Automatically generate signature**。
4.  登录你的华为开发者账号，等待工具自动生成证书和 Profile。

### 1.2 手动签名与 Flutter 项目关联

自动签名后，签名文件会生成在 `ohos/sign` 目录下。你需要确保 `ohos/build-profile.json5` 中的配置正确指向了这些文件。

```json
"signingConfigs": [
  {
    "name": "default",
    "material": {
      "certpath": "sign/debug/entry-debug.cer",
      "p12path": "sign/debug/entry-debug.p12",
      "profilepath": "sign/debug/entry-debug.p7b"
    }
  }
]
```

---

## 二、 编译打包：生成 HAP

Flutter for OpenHarmony 提供了专门的构建命令，将 Dart 代码编译产物与鸿蒙原生工程混合打包。

### 2.1 常用构建命令

在项目根目录下（包含 `pubspec.yaml` 的目录），打开终端：

*   **构建 Debug 包**（用于调试，含 JIT，性能稍差）：
    ```bash
    flutter build hap --debug
    ```

*   **构建 Release 包**（用于发布，AOT 编译，性能最佳）：
    ```bash
    flutter build hap --release
    ```

### 2.2 产物位置

构建成功后，终端会提示产物路径。默认通常位于：
`build/ohos/entry/default/outputs/default/entry-default-signed.hap`

这个 `.hap` 文件就是最终的安装包，你可以通过 USB 传输给用手机，或者通过命令行安装。

---

## 三、 安装与实机验证

### 3.1 使用 hdc 安装

连接你的鸿蒙手机，开启“开发者模式”和“USB 调试”。

```bash
# 检查设备连接
hdc list targets

# 安装 HAP (替换为你的实际路径)
hdc install build/ohos/entry/default/outputs/default/entry-default-signed.hap
```

### 3.2 常见报错排查

*   **Error: install parse profile missing prop**: 通常是签名 Profile 与包名（Bundle Name）不匹配。请检查 `AppScope/app.json5` 中的 `bundleName` 是否与自动签名时生成的包名一致。
*   **Error: AOT编译失败**: 确保你的鸿蒙 SDK 版本与 Flutter 引擎要求的版本一致。建议更新 `flutter doctor` 检查环境。

---

## 四、 系列总结

至此，**《Flutter for OpenHarmony 实战：Splendid Movie》** 系列通过 8 篇文章，完整覆盖了从 UI 设计、复杂交互、性能优化到打包发布的各个环节。

我们一起见证了：
1.  **Neon Night** 暗黑主题的诞生。
2.  **玻璃拟态**在鸿蒙上的完美复刻。
3.  **自研弹幕引擎**的丝滑运行。
4.  最终打包成 **HAP** 跑在真机上。

Flutter 在 OpenHarmony 上的生态正在以惊人的速度完善。希望这一系列实战教程，能成为你探索鸿蒙跨平台开发的坚实路标。

**Keep coding, stay splendid!** 🚀

---

> 📦 **完整代码已上传至 AtomGit**：[splendid_movie](https://atomgit.com/jiang_style/splendid_movie)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
