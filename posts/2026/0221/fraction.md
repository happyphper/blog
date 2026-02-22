---
title: "Flutter for OpenHarmony：fraction"
date: 2026-02-21
tags: [Flutter, OpenHarmony, 数学, 精度]
categories: [鸿蒙适配]
---

![fraction](images/fraction.png)

欢迎加入开源鸿蒙跨平台社区：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

# Flutter for OpenHarmony：Flutter 三方库 fraction 解决浮点数精度丢失的利器

## 前言

在使用 Flutter 编写财务核算或高精度测绘类业务时，由于所有系统双精度浮点的底层缺陷属性，常常会面临 `0.1 + 0.2` 不等于 `0.3` 这类臭名昭著的经典痛点问题。

`fraction` 库通过变换思维模式解决此类困境。它并未再造底层双极浮点编译器，而是回归朴素的数学模型——直接运用**真分数（分子 / 分母 Numerator & Denominator）**格式去表达及维护数理的计算。该库在推演运算时完全隔离了除不开的小数偏差带来的损耗，保证了从输入到运算输出的彻底绝对一致。

## 一、原理解析 / 概念介绍

### 1.1 基础概念

这个组件将原始业务中的数值剥离并裹装进一个强类型 `Fraction` 对象中进行接管。在进行四则运算时，它通过执行底层的极大值交叉同分，并在加减后利用嵌入的最大公约数 (GCD) 算法自动推崇和归整为化简的真分数格式。

```mermaid
graph TD
    A[传入待除的小数指令 例如 `1.5`] --> B[提取并包装成对应的分子分母容器 Fraction(3,2)]
    B --> C{与其它分数进行无损加减乘除复合计算}
    C --> D[实施纯粹整形交叉通分提取合成数据]
    D --> E[使用最大公约数GCD自动化简]
    E --> F[取得规避了完全精度缺失毛病的分数结果]
    F -->|末端落盘展示| G[最终在UI显示或反解为 String]
    style B fill:#9b59b6,color:white
```

### 1.2 进阶概念

- **带分数无缝包装支持 (MixedFraction)**：对于教育辅导和特定数学业务诸如 “3 又 1/2” 等包含带常数级的表达式，组件也提供了独特的类型处理和自适应四则转化能力。
- **扩展原生原型 API 融合接口**：在引入包体之后，常规 Dart 数据类型便默认外挂了特有功能入口。只需简单操作形如 `1.5.toFraction()` 即可立刻剥离系统浮点进入无损安全计算域平台。

## 二、核心 API / 组件详解

### 2.1 创建及实施分数四则混合运算

库内部对于分数的运算进行了强重载支持，写法上与使用原始浮点毫无二致。

```dart
// 记得去 yaml 文件先获取您的包 
import 'package:fraction/fraction.dart';
// 创建两个绝对基础的表示:
final fracA = Fraction(1, 4); // 即代表 1/4
final fracB = Fraction.fromString("0.2"); // 可以从字符串转化即 1/5
// 运用加减乘除，和普通业务没有代码形态鸿沟
final result = fracA * fracB;
print("运算毫无精度损毁后的结果直接是: $result"); 
// ✅ 推荐：直接使用它的核心将返回 "1/20"
```

### 2.2 直接挂在原型扩展并挖掘分数结构特征

业务层不仅可以使用，还能进一步分析这些解构后分数的结构合法性等详细要素：

```dart
// 直接激活 Extension 用法！
double mathItem = 1.34;
Fraction f = mathItem.toFraction();
// 解析判断当前这个分数的性质：是否可以完美换算？是否假分数等。
if (f.isProper) {
    print('当前确实是个合规真分数');
}
print('提取分子数据: ${f.numerator}，伴随分母 ${f.denominator}');
```

## 三、场景示例

### 3.1 场景一：商业级精密账单除算与分配闭环

例如需在三个订单里打穿并均摊一张退回的 10 元代金券。如果过早转为 `3.33333` 末尾结算时势必会导致存在坏账风险。

```dart
import 'package:fraction/fraction.dart';
class PaymentDistributor {
  /// 对复杂的鸿蒙对账单分摊金额，并能保证末尾相加依然整十！
  void calculateDiscountDist() {
    // 假设退款金额分配给三个人
    final discount = Fraction(10, 1);
    final shares = Fraction(1, 3);
    
    // 这样能完美的保持 10/3，无脑保证金额完整闭环！
    final perPerson = discount * shares; 
    
    print('每个人名下的退款份额比例实际为 $perPerson 毫不残损');
    // 当所有一切算完最后进入收银系统，统一释放成为最终处理浮点显示
    print('最终输出：¥${perPerson.toDouble().toStringAsFixed(2)}');
  }
}
```

<!-- IMAGE_PLACEHOLDER: [包含对账单据无死角完美呈现分配额展示效果比对截图] -->
<!-- 类型: 截图 -->
<!-- 内容: 展现通过分担并且毫无残渣闭环对上的数据统计UI终端 -->

### 3.2 场景二：开发面向下一代的智教算术答疑工具

开发算数辅助应用时，无需编写极其高昂费力的数学补位推导代码，直接交给内部引擎自动合并规整：

```dart
void constructMathQuiz() {
  // 定义两极带分数， 比如出题 “ 2 又 1/4 减去 1 又 1/2 等于多少？ ”
  MixedFraction q1 = MixedFraction(whole: 2, numerator: 1, denominator: 4);
  MixedFraction q2 = MixedFraction(whole: 1, numerator: 1, denominator: 2);
  
  // 引擎会完美减法并找好对应的余数归为真。
  MixedFraction answer = q1 - q2;
  print("🔥 提问：2又1/4 减去 1又1/2 是什么？");
  print("智能纠正及回答: $answer"); // 自转变成了单纯的分数形式的 3/4
}
```

## 四、OpenHarmony 平台适配挑战策略

### 4.1 UI 中文字符与分数的排版错位

在将渲染结果递交到原生系统或大屏绘制阶段，文本无法自动地将 "1/2" 改为具有数学纵向特征结构的占位排列。
🎨 **UI封装建议**：建议单独读取出 `.numerator` 与 `.denominator`，通过自定义编写包含中间带有细线 `Divider` 和垂直堆叠的特殊分数 `Widget` 来实现最佳可视反馈展现。

### 4.2 对于大型无穷数列演算极耗性能

组件为保持不转换为浮点带来的损失，分子及分母在连加除时会呈现爆炸式的数额扩张。
⚠️ 此时内部的大长整数计算往往会耗费指数级别运力。严禁在主流程 UI 线程针对极其高精无共同质数的多维分步展开超级迭代换算，这极易使得平台造成系统性的假死宕机或失帧卡顿。遇到庞杂长算式时应当配合 Isolate 离线求解再将展示交还给框架终端。

## 五、综合演示比对：防浮点穿透基盘屏障

我们把常规算法和 Fraction 安全包裹机制整合，让您体验不同路径运算得出不同维度的防抛错差别对比：

```dart
import 'package:flutter/material.dart';
import 'package:fraction/fraction.dart';
void main() => runApp(const FractionSafeguardApp());
class FractionSafeguardApp extends StatelessWidget {
  const FractionSafeguardApp({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '高精对账体系演示',
      theme: ThemeData(primarySwatch: Colors.deepPurple),
      home: const SecureCalcScreen(),
    );
  }
}
class SecureCalcScreen extends StatefulWidget {
  const SecureCalcScreen({Key? key}) : super(key: key);
  @override
  _SecureCalcScreenState createState() => _SecureCalcScreenState();
}
class _SecureCalcScreenState extends State<SecureCalcScreen> {
  String classicResult = "";
  String fractionResult = "";
  void _triggerCrashComparision() {
    // 经典的 Double 浮点崩盘例子
    double d1 = 0.1;
    double d2 = 0.2;
    
    // 使用库安全包裹执行转化
    final f1 = Fraction.fromString("0.1");
    final f2 = Fraction.fromString("0.2");
    setState(() {
      classicResult = (d1 + d2).toString(); // 不预期！
      fractionResult = (f1 + f2).toDouble().toString(); // 安全。
    });
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('鸿蒙数字安全演算基盘')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('请比对经典 "0.1 + 0.2" 计算漏洞：', 
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 30),
            Text('❌ 危险双精度结果: $classicResult', 
                 style: const TextStyle(color: Colors.redAccent, fontSize: 16)),
            const SizedBox(height: 10),
            Text('✅ Fraction 推演解回结果: $fractionResult', 
                 style: const TextStyle(color: Colors.green, fontSize: 16)),
            const SizedBox(height: 40),
            ElevatedButton(
              onPressed: _triggerCrashComparision,
              child: const Text('验证对比差异'),
            )
          ],
        ),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: [包含错误红绿演示并且正确归回真知运算数据的输出终端呈现反馈] -->
<!-- 类型: 截图 -->
<!-- 内容: 提供对于经典运算错误反馈直观视觉冲突比较参考。 -->

## 六、总结

针对要求零偏差的商业级运算需求与科学技术平台设计而言，双精度浮点永远具有阿喀琉斯之踵。在使用 Flutter 构建全场景跨端体系核心结算模块中，引入极其严谨轻巧的 `fraction` 包能从算法根源清除隐藏在框架深处造成巨型商业资损错乱。它绝对是一支不容抹煞极其牢固数字安全算子卫兵！

📦 代码配置参考及更深沉集成详见：[AtomGit 示例专栏](https://atomgit.com)
