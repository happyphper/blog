---
name: blogger
description: Flutter for OpenHarmony 技术博客写作 Agent Skill - 生成符合 CSDN 质量标准的高质量技术文章
---

# Flutter for OpenHarmony 博客写作 Agent Skill

本技能用于帮助撰写高质量的 **Flutter for OpenHarmony** 技术博客文章，确保符合社区规范和 CSDN 质量评分标准。

---

## 一、核心目标

生成符合以下标准的技术博客文章：

| 指标 | 要求 |
|-----|------|
| **CSDN 质量分** | ≥ 80 分 |
| **内容重复率** | ≤ 30% |
| **代码质量** | 可在鸿蒙设备运行，无重大逻辑错误 |
| **运行截图** | 必须包含鸿蒙设备运行截图 |

---

## 二、文章质量标准（必须遵守）

### 2.1 标题规范

标题必须明确体现所使用的鸿蒙跨平台框架：

**推荐格式**：
```
Flutter for OpenHarmony 实战：[文章主题]
Flutter for OpenHarmony：[组件名称] — [功能描述]
Flutter 三方库 [库名] 的鸿蒙化适配指南
```

**示例**：
- `Flutter for OpenHarmony 实战：TextField 与 TextFormField — 用户输入处理`
- `Flutter for OpenHarmony：Stack 与 Positioned — 层叠布局`
- `Flutter 三方库 dio 的鸿蒙化适配指南`

### 2.2 内容基础要求

| 要求项 | 说明 |
|-------|------|
| **内容导向** | 具备引导性，能指导读者实践；信息真实、准确，避免歧义 |
| **原创性** | 必须原创，禁止抄袭；不得主要由 AI 生成；重复率 ≤ 30% |
| **主题限制** | ❌ **环境安装与配置类主题不计入合格成果** |
| **技术范围** | 围绕 Flutter for OpenHarmony 展开 |

### 2.3 代码与截图要求

- **代码质量**：良好可读性，经过验证，在鸿蒙设备上可运行
- **运行截图**：**必须提供**代码在鸿蒙设备上成功运行的截图

### 2.4 品牌与链接规范

| 项目 | 规范 |
|-----|------|
| **代码托管平台** | 必须使用 **AtomGit**，链接：`https://atomgit.com` |
| **禁止品牌** | ❌ **禁止出现 "GitCode" 名称及相关链接** |
| **社区引导** | 文章末尾必须添加社区链接 |

### 2.5 代码仓库配置

**官方示例仓库**：
```
https://atomgit.com/dragonbady/open-harmony-examples
```

**仓库结构与文章对应关系**：

每篇博客文章的代码示例存放在仓库的 `examples/` 目录下，**目录名称与文章文件名一致**：

```
open-harmony-examples/
├── examples/
│   ├── container/              # 对应文章：container.md
│   │   ├── lib/
│   │   └── pubspec.yaml
│   ├── text-field/             # 对应文章：text-field.md
│   │   ├── lib/
│   │   └── pubspec.yaml
│   ├── stack-positioned/       # 对应文章：stack-positioned.md
│   │   ├── lib/
│   │   └── pubspec.yaml
│   └── ...
└── README.md
```

**文章中的仓库引用模板**：
```markdown
> 📦 完整代码已上传至 AtomGit：[open-harmony-examples/{article-name}](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/{article-name})
```

**示例**（Container 文章）：
```markdown
> 📦 完整代码已上传至 AtomGit：[open-harmony-examples/container](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/container)
```

**社区引导模板**（必须添加到结尾）：
```markdown
📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: {branch-name})](https://atomgit.com/dragonbady/open-harmony-example/tree/{branch-name})

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
```

---

## 三、CSDN 博客质量分评估体系 (V5.0)

### 3.1 加分项

| 评估维度 | 权重 | 优化策略 |
|---------|------|---------|
| **内容长度** | 高 | 文章正文 ≥ 2000 字 |
| **目录结构** | 高 | 使用多级标题（h1/h2/h3/h4），≥ 5 个子标题 |
| **代码块** | 中高 | ≥ 3 个代码块，每个 ≥ 5 行，指定语言类型 |
| **图片数量** | 中 | ≥ 3 张图片（含运行截图） |
| **链接引用** | 中 | 包含有效外部链接（参考文献、相关阅读） |

### 3.2 减分项

| 问题类型 | 影响 |
|---------|------|
| 内容过短（< 500 字） | 显著降分 |
| 无标题结构 | 降分 |
| 非 IT 技术文章 | 降分 |
| 文章结构简单 | 降分 |

### 3.3 强惩罚项

| 违规类型 | 惩罚系数 |
|---------|----------|
| 死链接 | 0.1 ~ 0.2 |
| 虚假/恶意链接 | 0.1 |
| 代码混乱/不可读 | 0.2 ~ 0.3 |
| 大量重复内容 | 0.1 ~ 0.3 |

---

## 四、标准文章结构模板

```markdown
# Flutter for OpenHarmony 实战：[主题] — [核心功能描述]

## 前言
[简要介绍文章背景、解决的问题、读者收益]

## 一、[概念介绍/原理解析]
### 1.1 [基础概念]
### 1.2 [进阶概念]

<!-- IMAGE_PLACEHOLDER: 概念架构图/原理示意图 -->

## 二、[核心 API/组件详解]
### 2.1 [基础用法]
### 2.2 [高级定制]
#### （1）[细分功能 1]
#### （2）[细分功能 2]
#### （3）[细分功能 3]

<!-- IMAGE_PLACEHOLDER: 运行效果截图（鸿蒙设备） -->

## 三、[常见应用场景]
### 3.1 [场景 1]
### 3.2 [场景 2]
### 3.3 [场景 3]

<!-- IMAGE_PLACEHOLDER: 场景效果 GIF/截图 -->

## 四、OpenHarmony 平台适配
### 4.1 [平台特性/差异分析]
### 4.2 [适配策略]
#### （1）[方案 1]
#### （2）[方案 2]
### 4.3 [最佳实践建议]

## 五、完整示例代码

[提供完整可运行的示例代码]

<!-- IMAGE_PLACEHOLDER: 完整示例运行截图（鸿蒙设备） -->

## 六、总结

[要点回顾、最佳实践、后续学习方向]

---

> 📦 完整代码已上传至 AtomGit：[项目链接](https://atomgit.com/your-repo)
>
> 欢迎加入开源鸿蒙跨平台社区：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
```

---

## 五、内容写作规范

### 5.1 代码块规范

每个代码块应：
- 指定语言类型（`dart`、`yaml`、`json` 等）
- 包含**中文注释**（重要！便于读者理解）
- 代码行数 ≥ 5 行
- 使用可在鸿蒙设备运行的真实示例

**示例**：

```dart
TextField(
  decoration: InputDecoration(
    labelText: '用户名',        // 浮动标签
    hintText: '请输入您的用户名', // 占位提示
    prefixIcon: Icon(Icons.person), // 左侧图标
    suffixIcon: IconButton(
      icon: Icon(Icons.clear),
      onPressed: () => _controller.clear(),
    ),
    border: OutlineInputBorder(), // 边框样式
  ),
)
```

### 5.2 知识点标注（Emoji 增强）

| 图标 | 用途 | 示例 |
|-----|------|------|
| 💡 | 设计原则/技巧 | `💡 技巧：使用 FocusNode 精细控制焦点` |
| ⚠️ | 注意事项/警告 | `⚠️ 注意：同时设置 left 和 right 会拉伸子项宽度` |
| ✅ | 正确做法 | `✅ 推荐：使用相对单位替代硬编码像素值` |
| ❌ | 错误做法 | `❌ 反例：Positioned(top: 100, left: 50, ...)` |
| 📌 | 重要提醒 | `📌 前提：确保已配置 OpenHarmony SDK` |
| 🎨 | UI/动画建议 | `🎨 动画增强：结合 AnimatedPositioned 实现平滑过渡` |
| 📦 | 代码仓库 | `📦 源码：https://atomgit.com/your-repo` |

### 5.3 链接格式规范

**所有链接必须使用可点击的 Markdown 格式**，禁止使用纯文本 URL。

❌ **错误示例**（纯文本链接）：
```markdown
官方下载：https://developer.huawei.com/consumer/cn/deveco-studio/
```

✅ **正确示例**（可点击链接）：
```markdown
官方下载：[DevEco Studio 下载页面](https://developer.huawei.com/consumer/cn/deveco-studio/)
```

**常用链接模板**：

| 用途 | 格式 |
|-----|------|
| 官方文档 | `[Flutter 官方文档](https://flutter.cn/docs)` |
| 下载页面 | `[DevEco Studio 下载](https://developer.huawei.com/consumer/cn/deveco-studio/)` |
| 代码仓库 | `[示例代码](https://atomgit.com/dragonbady/open-harmony-examples)` |
| 社区链接 | `[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)` |
| 参考文章 | `[相关阅读：Container 详解](链接地址)` |

### 5.4 图片/截图规范

**必须包含的截图**：
1. **鸿蒙设备运行截图**（必需）- 验证代码可运行
2. 概念/架构图（推荐）
3. 效果对比图（推荐）

**图片占位符格式**：

```markdown
<!-- IMAGE_PLACEHOLDER: [图片描述] -->
<!-- 类型: 截图/GIF/示意图 -->
<!-- 设备: 鸿蒙设备/模拟器 -->
<!-- 内容: [具体内容描述，便于后续截取或生成] -->
```

**推荐的图片插入位置**：

| 位置 | 类型 | 说明 |
|-----|------|------|
| 前言后 | 概念图 | 帮助读者快速理解主题 |
| 代码块后 | **运行截图** | 展示在鸿蒙设备上的运行效果（必需） |
| 场景说明 | 效果GIF | 展示交互效果 |
| 总结前 | 完整效果 | 最终运行截图 |

---

## 六、OpenHarmony 平台特性内容

每篇文章应包含的平台适配内容：

### 6.1 多分辨率适配

```markdown
#### OpenHarmony 多分辨率适配

OpenHarmony 设备分辨率跨度大（720×1280 ~ 3840×2160），需注意：

- 小屏设备：避免元素重叠、文字截断
- 大屏设备：避免间距过大、布局稀疏
- 折叠屏/分屏：处理尺寸动态变化

✅ 推荐做法：
- 使用 `MediaQuery` 获取屏幕尺寸
- 使用 `LayoutBuilder` 响应式布局
- 结合 `SafeArea` 处理刘海屏
```

### 6.2 平台差异说明

如有平台特有行为，需明确说明：
- 触控反馈差异
- 键盘/输入法行为
- 手势识别差异
- 性能优化建议

---

## 七、质量检查清单

发布前请逐项检查：

| # | 检查项 | 要求 | ☐ |
|---|-------|------|---|
| 1 | 标题格式 | 包含 "Flutter for OpenHarmony" | ☐ |
| 2 | 文章长度 | ≥ 2000 字 | ☐ |
| 3 | 标题层级 | 使用 h1/h2/h3/h4 | ☐ |
| 4 | 子标题数量 | ≥ 5 个 | ☐ |
| 5 | 代码块数量 | ≥ 3 个，每个 ≥ 5 行 | ☐ |
| 6 | 代码注释 | 中文注释 | ☐ |
| 7 | **鸿蒙运行截图** | **必须包含** | ☐ |
| 8 | 品牌规范 | 使用 AtomGit，无 GitCode | ☐ |
| 9 | 社区引导 | 结尾包含社区链接 | ☐ |
| 10 | 内容原创 | 重复率 ≤ 30% | ☐ |
| 11 | 主题合规 | 非环境配置类 | ☐ |
| 12 | **CSDN 质量分** | **≥ 80 分** | ☐ |

**质量分自查工具**：https://www.csdn.net/qc

---

## 八、禁止事项

| ❌ 禁止项 | 说明 |
|----------|------|
| 环境配置类主题 | 不计入合格成果 |
| GitCode 品牌/链接 | 必须使用 AtomGit |
| 全 AI 生成内容 | 需人工润色，重复率 ≤ 30% |
| 无运行截图 | 必须有鸿蒙设备截图 |
| 不可运行的代码 | 代码必须经过验证 |

---

## 九、辅助资源

本 Skill 提供以下辅助资源：

| 目录 | 内容 |
|-----|------|
| `examples/` | 参考文章示例 |
| `resources/` | 文章模板、检查清单 |
| `scripts/` | 辅助脚本（字数统计、格式检查等） |

### 9.1 使用示例

**用户请求**：
```
帮我写一篇关于 Flutter Container 组件的博客
```

**Agent 执行流程**：
1. 按标准模板生成文章结构
2. 填充 Container 组件技术内容
3. 添加 ≥3 个代码示例（含中文注释）
4. 标注 ≥3 个图片位置（含运行截图位置）
5. 包含 OpenHarmony 适配建议
6. 添加 AtomGit 链接和社区引导
7. 输出质量检查清单

---

## 十、参考资源

### 博客示例
- [TextField 与 TextFormField — 用户输入处理](https://blog.csdn.net/2501_93030156/article/details/157441189)
- [Stack 与 Positioned — 层叠布局](https://blog.csdn.net/2501_93030156/article/details/157468411)

### 质量评分规则
- [CSDN 博客质量分计算 V5.0](https://blog.csdn.net/u010280923/article/details/131449478)

### 社区资源
- 开源鸿蒙跨平台社区：https://openharmonycrossplatform.csdn.net
- 代码托管平台：https://atomgit.com

---

## 十一、真实示例分析

本 Skill 的 `examples/` 目录包含多个真实博客案例，用于学习写作模式：

### 11.1 示例文章列表

| 文件 | 主题 | 框架 |
|-----|------|------|
| `container_example.md` | Container 容器组件 | Flutter |
| `react_native_example.md` | 用户中心组件 | React Native |
| `registration_form_example.md` | 用户注册表单 | React Native |

### 11.2 真实案例共同模式

通过分析真实发布的博客文章，总结以下写作模式：

**文章结构模式**：
```
1. 前言/背景介绍
2. 环境/依赖说明
3. 核心代码实现（完整可运行）
4. 打包流程（npm run harmony）
5. 运行效果截图/GIF
6. 社区引导链接
```

**代码呈现特点**：
- 提供**完整可运行**的代码，而非片段
- 代码量充足（通常 100+ 行）
- 包含组件封装和样式定义
- TypeScript 类型注解完整

**截图要求**：
- 静态效果截图（PNG）
- 交互效果 GIF 动画
- 打包过程截图
- DevEco-Studio 工程截图

**结尾固定格式**：
```markdown
## 欢迎大家加入[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)，一起共建开源鸿蒙跨平台生态。
```

### 11.3 React Native for OpenHarmony 适配

真实案例中的 React Native 打包流程：

```bash
# 1. 打包 React Native 代码为 bundle
npm run harmony

# 2. 将打包后的文件拷贝到 DevEco-Studio 工程目录

# 3. 在 DevEco-Studio 中运行到鸿蒙设备
```

---

> ⚠️ **重要提醒**：
> 1. 本 Skill 生成的是初稿，发布前必须：
>    - 替换图片占位符为**实际鸿蒙设备截图**
>    - 验证代码在鸿蒙设备上可运行
>    - 使用 [CSDN 质量分工具](https://www.csdn.net/qc) 自查
> 2. 文章不得主要由 AI 生成，需进行人工润色和个性化修改
