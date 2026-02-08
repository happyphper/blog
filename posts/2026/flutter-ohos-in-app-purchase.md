# Flutter for OpenHarmony 实战：in_app_purchase — 应用内支付（IAP）指南

## 前言

商业化变现是移动应用生态中不可或缺的一环。对于 Flutter 应用而言，`in_app_purchase` 是官方提供的通用支付插件，用于接入 Apple App Store 和 Google Play。

在 OpenHarmony 生态中，应用内支付通常对接的是华为支付服务（IAP Kit）。虽然 OpenHarmony 的支付生态正在快速演进，但在 Flutter 侧，我们依然希望能保持 API 的统一性。

本文将介绍如何使用 Flutter 的 `in_app_purchase` 包结构，并结合 OpenHarmony 平台的特性（如华为 IAP 适配），实现商品查询和购买流程。

> ⚠️ **主要提示**：目前 OpenHarmony 的 `in_app_purchase` 官方适配可能尚处于早期或社区维护阶段。实际接入时，可能需要依赖特定的社区包（如 `flutter_in_app_purchase_ohos` 或类似名称），或者通过 `url_launcher` 跳转支付宝/微信 H5 支付作为临时替代方案。本文将侧重于**标准接口的使用**，这些逻辑在适配完成后是通用的。

## 一、核心概念

`in_app_purchase` 的设计非常统一，主要包含以下几个步骤：

1.  **连接商店 (Availability)**: 检查当前设备是否支持支付。
2.  **查询商品 (Product Details)**: 从商店获取商品信息（价格、描述）。
3.  **发起购买 (Purchase)**: 用户点击购买，调起系统支付界面。
4.  **监听状态 (Purchase Stream)**: 处理成功、失败或取消的回调。
5.  **完成交易 (Complete)**: 尤其是消耗型商品，必须确认交易以避免重复发货。

<!-- IMAGE_PLACEHOLDER: IAP 支付流程图 -->
<!-- 内容: Client -> Query Products -> Store -> Show UI -> Buy -> Validate -> Complete -->

## 二、安装与配置

### 2.1 添加依赖

在 `pubspec.yaml` 中添加。**注意**：针对 OpenHarmony，请务必在社区寻找是否有特定的 endorsed implementation。

```yaml
dependencies:
  flutter:
    sdk: flutter
  in_app_purchase: ^3.1.0
  # 假设存在社区适配包 (示例)
  # in_app_purchase_ohos:
  #   git: https://atomgit.com/openharmony-sig/flutter_in_app_purchase_ohos.git
```

### 2.2 OpenHarmony 权限配置

涉及支付通常需要在 `entry/src/main/module.json5` 配置网络权限，以及可能的支付相关权限（视 IAP SDK 要求而定）。

```json5
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET"
      }
    ]
  }
}
```

此外，你还需要在华为 AppGallery Connect 后台配置商品信息（商品 ID、价格等），这与在 App Store Connect 或 Google Play Console 上的操作类似。

## 三、代码实现

### 3.1 初始化与监听

支付的结果是通过 Stream 异步返回的，因此要在应用的生命周期早期开始监听。

```dart
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:in_app_purchase/in_app_purchase.dart';

class IAPPage extends StatefulWidget {
  const IAPPage({super.key});

  @override
  State<IAPPage> createState() => _IAPPageState();
}

class _IAPPageState extends State<IAPPage> {
  final InAppPurchase _iap = InAppPurchase.instance;
  late StreamSubscription<List<PurchaseDetails>> _subscription;
  
  List<ProductDetails> _products = [];
  bool _isAvailable = false;

  @override
  void initState() {
    super.initState();
    // 1. 监听购买更新
    final purchaseUpdated = _iap.purchaseStream;
    _subscription = purchaseUpdated.listen((purchaseDetailsList) {
      _listenToPurchaseUpdated(purchaseDetailsList);
    }, onDone: () {
      _subscription.cancel();
    }, onError: (error) {
      // 处理错误
    });
    
    // 2. 初始化链接
    _initStore();
  }

  Future<void> _initStore() async {
    final bool isAvailable = await _iap.isAvailable();
    setState(() {
      _isAvailable = isAvailable;
    });

    if (isAvailable) {
      // 3. 查询商品 (替换为你自己在后台配置的 Product ID)
      const Set<String> _kIds = {'coin_100', 'vip_monthly'};
      final ProductDetailsResponse response = await _iap.queryProductDetails(_kIds);
      
      if (response.notFoundIDs.isNotEmpty) {
        print('未找到商品: ${response.notFoundIDs}');
      }
      
      setState(() {
        _products = response.productDetails;
      });
    }
  }

  @override
  void dispose() {
    _subscription.cancel();
    super.dispose();
  }
  
  // ... build method ...
}
```

### 3.2 发起购买

当用户点击按钮时调用：

```dart
void _buyProduct(ProductDetails product) {
  final PurchaseParam purchaseParam = PurchaseParam(productDetails: product);
  
  if (_iap.isAvailable()) {
    // 区分消耗型(Consumable)和非消耗型(NonConsumable)
    // 假设是充值金币（消耗型）
    _iap.buyConsumable(purchaseParam: purchaseParam);
    // 如果是永久去广告（非消耗型）
    // _iap.buyNonConsumable(purchaseParam: purchaseParam);
  }
}
```

### 3.3 处理回调

这是最关键的一步，必须正确处理每一种状态。

```dart
void _listenToPurchaseUpdated(List<PurchaseDetails> purchaseDetailsList) {
  for (final PurchaseDetails purchaseDetails in purchaseDetailsList) {
    if (purchaseDetails.status == PurchaseStatus.pending) {
      // 显示加载圈
    } else {
      if (purchaseDetails.status == PurchaseStatus.error) {
        // 提示错误
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('支付失败: ${purchaseDetails.error?.message}')),
        );
      } else if (purchaseDetails.status == PurchaseStatus.purchased ||
                 purchaseDetails.status == PurchaseStatus.restored) {
        // 验证收据 (Server-side Verification)
        // 验证通过后发放商品
        _deliverProduct(purchaseDetails);
      }
      
      // ⚠️ 无论成功与否，必须 complete 订单，否则后续无法再买
      if (purchaseDetails.pendingCompletePurchase) {
        _iap.completePurchase(purchaseDetails);
      }
    }
  }
}
```

## 四、OpenHarmony 平台适配注意事项

### 4.1 华为 IAP 沙盒测试

在 OpenHarmony 上开发支付功能，通常需要在华为 AppGallery Connect 中设置沙盒测试账号。确保你的测试设备登录了该测试账号，否则 `queryProductDetails` 可能会返回空列表。

### 4.2 错误码处理

OpenHarmony（华为 IAP）有特定的错误码体系（如 `60050` 表示用户取消）。在 `PurchaseDetails.error` 中可能包含这些原生信息的映射，调试时请重点关注日志输出。

### 4.3 备选方案

如果当前的 `in_app_purchase` 适配层尚不支持某些高级特性（如订阅升级/降级），可以考虑使用 **MethodChannel** 直接调用鸿蒙原生的 IAP Kit 接口来实现，或者暂时通过 H5 支付过渡。

## 五、完整示例代码

一个简单的商品列表与购买演示：

```dart
import 'package:flutter/material.dart';
import 'package:in_app_purchase/in_app_purchase.dart';

// 此示例假设在此之前已完成了 Stream 监听的设置
class IAPDemoList extends StatelessWidget {
  final List<ProductDetails> products;
  final Function(ProductDetails) onBuy;

  const IAPDemoList({
    super.key, 
    required this.products, 
    required this.onBuy
  });

  @override
  Widget build(BuildContext context) {
    if (products.isEmpty) {
      return const Center(child: Text('暂无可购买商品或正在加载...'));
    }

    return ListView.builder(
      itemCount: products.length,
      itemBuilder: (context, index) {
        final product = products[index];
        return Card(
          margin: const EdgeInsets.all(8),
          child: ListTile(
            title: Text(product.title), // 例如 "100 金币"
            subtitle: Text(product.description), // 例如 "用于购买道具"
            trailing: ElevatedButton(
              onPressed: () => onBuy(product),
              child: Text(product.price), // 例如 "￥6.00"
            ),
          ),
        );
      },
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 购买页运行截图 -->
<!-- 设备: 鸿蒙设备 -->
<!-- 内容: 显示商品列表，点击购买按钮弹起系统支付窗口 -->

## 六、总结

在 OpenHarmony 上实现应用内支付，核心流程与 iOS/Android 并无二致。`in_app_purchase` 插件为我们提供了一致的抽象。

随着 OpenHarmony 生态的完善，支付链路的打通是必然的。建议开发者密切关注 OpenHarmony SIG 社区的动态，以及华为开发者联盟关于 IAP Kit 的最新文档。

---

> 📦 完整代码已上传至 AtomGit：[open-harmony-examples/iap_demo](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/iap_demo)
>
> 🌐 欢迎加入开源鸿蒙跨平台社区：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
