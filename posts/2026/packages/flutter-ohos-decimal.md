---
title: Flutter for OpenHarmony 实战：Decimal — 拒绝精度丢失的金融级计算
description: 深度解析如何在 Flutter for OpenHarmony 中通过 Decimal 库处理高精度货币计算，包含 3 个核心用法及一个工业级商城购物车计价引擎实战。
tags:
  - Flutter
  - OpenHarmony
  - Decimal
  - 高精度计算
  - 金融开发
---

# Flutter for OpenHarmony 实战：Decimal — 拒绝精度丢失的金融级计算

![封面](../images/cover_decimal.png)

## 前言

在开发 **Flutter for OpenHarmony** 的电商、金融或计费类应用时，开发者最担心的就是“钱算错了”。

由于计算机底层使用二进制浮点数（Floating-point）存储 `double`，像 `0.1 + 0.2` 这种极其简单的运算，在控制台输出的结果可能是 `0.30000000000000004`。这种微小的精度丢失在涉及复杂折扣、多笔汇率转换时，会累积成巨大的逻辑漏洞。**Decimal** 库通过模拟人类的十进制逻辑，确保了每一分钱的计算都精准无误。本文将教你如何为鸿蒙应用装上一颗“严谨”的计算大脑。

---

## 一、为什么金融场景严禁使用 double？

### 1.1 浮点数陷阱 ⚠️
在 Dart 中，`double` 遵循 IEEE 754 标准。二进制无法精确表示某些十进制小数，这会导致在进行金额比较（如 `if(sum == 0.3)`）时产生意想不到的 `false`。

### 1.2 Decimal 的优势
不同于普通的 `num`，`Decimal` 内部使用了 `BigInt` 来保存数值的每一位，从而消除了舍入误差。它支持无限精度的加减乘除，且具备极佳的语义化能力。

<!-- IMAGE_PLACEHOLDER: [Double 运算误差 vs Decimal 精确计算对比图] -->
<!-- 类型: 示例对比 -->
<!-- 内容: 展示 0.1+0.2 在两种类型下的输出结果及其对金额结算的影响 -->

---

## 二、配置环境 📦

在项目中引入依赖：

```yaml
dependencies:
  decimal: ^3.2.4
```

💡 **注意**：由于 `decimal` 是纯 Dart 实现，它避开了与鸿蒙原生 Native 数值类型的底层转换开销，性能非常均衡。

---

## 三、核心功能：3 个高精度计算场景

### 3.1 零误差算术运算 (Arithmetic)
实现基础的金额加减乘除，确保结果完全符合人类预期。
```dart
import 'package:decimal/decimal.dart';

void calculateTotal() {
  // 💡 技巧：强制建议使用字符串动态解析，而非直接传 double
  final d1 = Decimal.parse('0.1');
  final d2 = Decimal.parse('0.2');
  
  final sum = d1 + d2; 
  print('✅ 鸿蒙商城计价：$sum'); // 准确输出 0.3
}
```

### 3.2 严谨的金额比较 (Comparison)
避免浮点数造成的“肉眼不可见”差异导致判断失效。
```dart
void checkBalance(String balance, String cost) {
  final dBalance = Decimal.parse(balance);
  final dCost = Decimal.parse(cost);
  
  if (dBalance >= dCost) {
    print('💰 余额充足，可以购买鸿蒙周边');
  }
}
```

### 3.3 科学计数法转换与舍入 (Rounding)
针对汇率等长小数位场景，实现特定的舍入策略。
```dart
void roundResult() {
  final value = Decimal.parse('1.23456');
  // 💡 技巧：保留两位小数并向下取整
  final result = value.floor(scale: 2);
  print('折合汇率: $result'); // 1.23
}
```

---

## 四、OpenHarmony 平台适配与最佳实践

### 4.1 数据持久化的类型选择 🏗️
⚠️ **注意**：鸿蒙本地数据库（如 SQLite 或 Preferences）并不直接支持 `Decimal` 类型。
- **✅ 建议做法**：在存入鸿蒙沙箱时，务必通过 `toString()` 转换为字符串保存。读取时再重新调用 `Decimal.parse()`。严禁将其先转为 `double` 再保存，否则会在磁盘读写时引入新的精度噪声。

### 4.2 UI 展示的性能优化
- **💡 技巧**：`Decimal` 的运算成本略高于原生 `double`。在鸿蒙设备的高刷新率 UI（如每秒刷新 120 次的复杂动画）中，如果涉及上千次数值计算，建议将计算逻辑放在 Isolate 中，计算完后将格式化好的字符串传回主线程展示。

<!-- IMAGE_PLACEHOLDER: [鸿蒙真机购物车结算界面截图] -->
<!-- 类型: 截图 -->
<!-- 内容: 展示在多项商品、多重折扣叠加下，每一步计算的中间过程及最终精准的总额 -->

---

## 五、完整实战示例：构建鸿蒙商城“万无一失”计价引擎

我们将构建一个支持多笔折扣、优惠券叠加以及动态计算总价的实战类。该引擎能确保在处理上万次累加后，利润与总额依然保持绝对一致。

```dart
import 'package:decimal/decimal.dart';
import 'package:decimal/intl.dart';

/// 鸿蒙级金融结算大师
class OhosCartEngine {
  /// 计算最终实付金额
  /// [prices] 单价列表
  /// [discountRate] 折扣率（如 '0.85' 表示 8.5 折）
  /// [coupon] 满减优惠券金额
  static String computeFinalPrice(List<String> prices, String discountRate, String coupon) {
    print('--- 🚀 正在启动鸿蒙级高精度审计 ---');
    
    // 1. 实现累加
    final totalRaw = prices
        .map(Decimal.parse)
        .fold(Decimal.zero, (prev, curr) => prev + curr);
    
    // 2. 💡 实战：应用折扣
    final discounted = (totalRaw * Decimal.parse(discountRate)).toDecimal(scaleOnInfinitePrecision: 4);

    // 3. 💡 实战：扣除优惠券
    final finalResult = discounted - Decimal.parse(coupon);

    // 4. 返回人性化格式，确保不小于 0
    final saferResult = finalResult < Decimal.zero ? Decimal.zero : finalResult;
    
    return saferResult.toStringAsFixed(2);
  }
}

void main() {
  final items = ['19.99', '59.00', '124.55', '0.01'];
  final result = OhosCartEngine.computeFinalPrice(items, '0.88', '10.00');
  
  print('结算清单结果：¥$result');
}
```

---

## 六、总结

在构建 **Flutter for OpenHarmony** 商业项目时，对细节的敬畏就是对用户的负责。`Decimal` 库通过在 Dart 层模拟分毫毕现的十进制逻辑，填补了底层计算性能与业务准确性之间的鸿沟。

掌握了 `Decimal`，你的鸿蒙应用将不再有“一分钱”的烦恼。

---

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
