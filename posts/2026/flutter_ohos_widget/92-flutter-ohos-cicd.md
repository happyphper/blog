![封面图](images/92-cover.png)

# Flutter for OpenHarmony 实战之进阶：第九十二篇 CI/CD 自动化构建与部署 — 高效发布 Flutter 应用至鸿蒙应用市场

## 前言

手动打包（Build Hap/Splitted Libs）并上传应用市场是低效且易出错的。在 **HarmonyOS NEXT** 的企业级开发流程中，搭建一套成熟的 **CI/CD (持续集成与持续部署)** 流水线是刚需。

如何配置 Jenkins/GitHub Actions 自动执行 Flutter 鸿蒙版的构建？如何实现测试包的自动分发？本篇将带你打造自动化的“鸿蒙发布工厂”。

---

## 一、流水线核心流程设计

一套标准的 Flutter for OpenHarmony 自动化流程包含：
1.  **代码静态扫描**：运行 `flutter analyze` 确保 Dart 代码质量。
2.  **依赖安装**：自动执行 `flutter pub get` 与鸿蒙 `ohpm install`。
3.  **产物构建**：根据不同环境（Debug/Release）生成 HAP 包。
4.  **自动化签名**：使用鸿蒙开发者证书对 HAP 进行签名。
5.  **分发与归档**：将产物同步至内部下载站或应用市场后台。

---

## 二、实战：使用命令行执行鸿蒙自动化构建

在服务器环境下，我们脱离 DevEco Studio 界面，直接使用命令行工具。

### 2.1 环境变量配置
确保服务器已安装 **Command Line Tools** (鸿蒙命令行工具链) 并配置 `HOS_SDK_HOME`。

### 2.2 自动化构建脚本脚本
```bash
#!/bin/bash
# 💡 技巧：一键自动化脚本
echo "🚀 开始构建鸿蒙 Release 包..."

# 1. 清理缓存
flutter clean

# 2. 定制化编译
# --release 指标 AOT 压缩，--obfuscate 混淆代码
flutter build hap --release --obfuscate --split-debug-info=./debug_symbols

echo "✅ 构建完成：./ohos/entry/build/default/outputs/default/entry-default-signed.hap"
```

---

## 三、GitHub Actions 云端自动化配置

通过 `.github/workflows/ohos_build.yml` 实现云端自动打包。

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'
      
      - name: Install Harmony SDK
        run: |
          # 📌 这里需要模拟鸿蒙命令行工具的拉取逻辑
          # 由于鸿蒙 SDK 需登录下载，目前通常采用私有 Runner 预装模式
      
      - name: Build Hap
        run: flutter build hap --release
```

<!-- IMAGE_PLACEHOLDER: CI/CD 流水线成功运行，自动将构建产物上传至蒲公英/内测平台的通知截图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示流程自动化的闭环体验 -->

---

## 四、OpenHarmony 平台适配要点

### 4.1 签名文件的安全性管理
鸿蒙的 `.p12` 证书和密码绝不能直接提交到代码库。
- ✅ **方案**：使用 GitHub Secrets 或 Jenkins Credentials 插件加密存储。在流水线运行时，通过环境变量注入签名配置。

### 4.2 适配低内存、低存储服务器
鸿蒙 AOT 编译过程对 CPU 和内存要求较高。
- ✅ **建议**：服务器配置建议不低于 4 核 8G。如果资源受限，可在构建命令中增加 `--no-tree-shake-icons` 等参数微调，以空间换性能。

---

## 五、最终检查清单 (DevOps Checklist)

1.  ✅ **版本号递增**：流水线是否能自动修改 `pubspec.yaml` 中的 `version` 字段？
2.  ✅ **日志归档**：构建失败时，是否能正确保存 `build.log` 方便排查？
3.  ✅ **全测全闭环**：是否包含了 Unit Test 环节？

---

## 六、总结

自动化不是为了偷懒，而是为了**确定性**：
1.  **代码即规范**：流水线是最后一道质量防线。
2.  **减少人为干预**：避免因打包人员电脑环境不同导致的“玄学 Bug”。
3.  **极速迭代**：从提交代码到测试拿到包，应缩短在 10 分钟内。

掌握了 CI/CD，你的 Flutter 团队才能在鸿蒙生态的快节奏迭代中立于不败之地。

---

> 📦 **完整配置模板已上传至 AtomGit**：[open-harmony-examples/cicd-automation](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/cicd-automation)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
