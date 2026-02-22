欢迎加入开源鸿蒙跨平台社区：[https://openharmonycrossplatform.csdn.net](https://openharmonycrossplatform.csdn.net)。

# Flutter for OpenHarmony：country — 为鸿蒙应用提供完善的国家/地区数据支持

![country](images/country.png)


## 前言

随着鸿蒙（OpenHarmony）系统在全球范围内的快速扩张，构建具备国际化能力的应用已成为开发者的必修课。无论是在注册流程中选择手机号冠字码（+86, +1, 等）、在个人中心修改地区，还是在物流应用中选择邮寄目的地，都需要一套权威、完整且易于查询的国家/地区数据库。

在 **Flutter for OpenHarmony** 开发中，我们不需要手动维护庞大的 JSON 字典。`country` 库提供了一套极其严谨的、遵循 ISO 标准的国家数据模型。今天，我们将探索如何让鸿蒙应用秒变“地理通”。

## 一、为什么集成 country 库？

### 1.1 数据权威性
该库遵循 ISO 3166-1 国际标准（包括 Alpha-2, Alpha-3 代码），确保在处理多国贸易或金融应用时，地区代码的严谨性符合全球合规。

### 1.2 核心优势
- **多语言支持**：内置了多种语言的国家名称翻译，非常适合鸿蒙应用的 `i18n` 场景。
- **丰富的元数据**：除了名字，还涵盖了货币、旗帜 Emoji、呼叫前缀、时区等 20 多项属性。
- **纯 Dart 高性能查询**：数据经过优化处理，在鸿蒙低端设备上进行全量搜索也能保持丝滑反应。

### 1.3 数据查询流转模型（Mermaid）

```mermaid
graph LR
    A[用户在鸿蒙 UI 搜索] --> B[输入过滤: "China"]
    B --> C{country 检索引擎}
    C --> D[匹配 ISO Alpha-2: CN]
    C --> E[匹配呼叫前缀: +86]
    C --> F[匹配中文译名: 中国]
    D --> G[统一 Country 对象]
    E --> G
    F --> G
    G --> H[UI 展示: 旗帜 + 名称]
    style C fill:#34495e,color:white
    style G fill:#2ecc71,color:white
```

## 二、核心 API 与功能讲解

### 2.1 引入依赖
在 `pubspec.yaml` 中配置：

```yaml
dependencies:
  # 完整的国家数据资源库
  country: ^0.1.0 
```

### 2.2 基础查询操作
根据代码或名称快速获取国家详情。

```dart
import 'package:country/country.dart';

void getCountryInfo() {
  // 💡 根据 ISO 代码获取
  final china = Countries.cn;
  
  print('全称: ${china.name}');
  print('货币: ${china.currencyCode}');
  print('呼叫前缀: ${china.phoneCode}');
  
  // 🎨 列出全球所有支持的国家数量
  print('全球国家总数: ${Countries.values.length}');
}
```

### 2.3 动态过滤与搜索
实现鸿蒙应用中常见的搜索列表。

```dart
void searchCountries(String query) {
  // 🎨 根据用户输入过滤
  final results = Countries.values.where((c) => 
    c.name.toLowerCase().contains(query.toLowerCase()) || 
    c.phoneCode.contains(query)
  ).toList();
  
  print('搜索到 ${results.length} 个结果');
}
```

## 三、鸿蒙应用实战场景

### 3.1 场景一：全球支付的货币自动切换
在鸿蒙手机的跨境电商应用中。用户选择收货地为“日本”，应用通过 `country` 库自动识别出其对应币种为 `JPY`。随后配合汇率插件，在商品详情页实现价格的实时转换展示，极具质感。

### 3.2 场景二：带旗帜的手机号注册组件
在鸿蒙应用的第一屏注册页，点击国家前缀图标，弹出一个美观的底部分类。利用 `country` 内置的 `flag` 属性，直接在 Flutter 的 `Text` 组件中渲染出对应的国旗 Emoji。

<!-- IMAGE_PLACEHOLDER: [带有旗帜与手机号前缀的国家选择器截图] -->
<!-- 类型: 截图 -->
<!-- 内容: 展示一个整齐的列表，左侧是动态生成的国旗 Emoji，中间是国家名，右侧是 +86 类冠字码 -->

## 四、OpenHarmony 平台适配建议

### 4.1 字体库支持。
- **📌 提醒**：虽然 `country` 库提供了国旗 Emoji。但在某些鸿蒙定制系统或老旧版本中，字体库可能不完整导致国旗显示为字母（如 CN 显示为 🇨 和 🇳）。建议在鸿蒙应用的主题配置中显式引入支持丰富 Emoji 的字体。

### 4.2 适配鸿蒙系统语言设置
- **✅ 建议**：`country` 库支持多语言。在鸿蒙应用内，建议读取 `window.uiContext` 中的当前语言环境，并将其映射到 `country` 的展示逻辑中，确保“中文环境显示中国，英文环境显示 China”。

### 4.3 编译体积建议。
- **⚠️ 警告**：国家数据量较大。虽然经过压缩，但在极端内存敏感的鸿蒙手表元服务上，如果不打算支持全球业务，可以考虑在打包阶段利用 Tree Shaking 排除掉非必要的数据索引。

## 五、完整示例：国家指纹看读器

演示一个可在鸿蒙端运行的“全球地理实验室”。

```dart
import 'package:flutter/material.dart';
import 'package:country/country.dart';

void main() => runApp(const MaterialApp(home: CountryLab()));

class CountryLab extends StatelessWidget {
  const CountryLab({super.key});

  @override
  Widget build(BuildContext context) {
    // ✅ 实战：获取指定国家的所有元数据
    final br = Countries.br; // 巴西

    return Scaffold(
      appBar: AppBar(title: const Text('country 鸿蒙地理实验室')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(br.flag, style: const TextStyle(fontSize: 80)), // 自动显示旗帜
            const SizedBox(height: 20),
            Text('国家: ${br.name}', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Text('货币单位: ${br.currencyCode}', style: const TextStyle(color: Colors.blue)),
            Text('呼叫代码: +${br.phoneCode}', style: const TextStyle(color: Colors.grey)),
            const SizedBox(height: 30),
            const Text('全量数据已载入，支持全球 200+ 地区', style: TextStyle(fontSize: 12)),
          ],
        ),
      ),
    );
  }
}
```

## 六、总结

在鸿蒙系统通向全球的征途中，对地理信息的精准掌握是开发者打开国际大门的敲门砖。`country` 库以其标准化的数据、高效的查询性能，成为了 **Flutter for OpenHarmony** 开发者手中的世界地图。

核心要点回顾：
1. **标准驱动**：完全对齐 ISO 3166-1 国际数据标准。
2. **场景丰富**：覆盖从货币、冠字码到 Emoji 旗帜的全栈信息。
3. **鸿蒙适配**：注意与系统语言环境的同步和 Emoji 字体兼容性。
4. **提升专业度**：告别硬编码的国家字典，拥抱自动化的数据仓库。

让您的鸿蒙应用，具备洞察全球每一寸疆土的数据视角！

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/country](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/country)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
