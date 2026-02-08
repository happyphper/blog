![封面图](images/105-cover.png)

# Flutter for OpenHarmony 实战之殿堂：第一百零五篇 鸿蒙穿戴 (Watch) 收官 — 离线部署与独立连网实战

## 前言

作为“鸿蒙穿戴专栏”的收官之作，我们要解决最后一个大难题：**脱离手机独立生存**。华为 Watch 4 等旗舰手表支持 eSIM 和 Wi-Fi，这意味着你的 Flutter 应用必须具备在没有蓝牙连接时，独立进行网络请求与离线数据持久化的能力。

本篇将教你如何配置手表的独立通信，并分享一套针对穿戴设备的自动化部署与测试流程。

---

## 一、手表的“独立宣言”：eSIM 与 Wi-Fi 调度

在鸿蒙系统中，穿戴设备具备独立的 **Network Manager**。

### 1.1 自动切换链路策略
应用应优先使用蓝牙（通过手机中转，省电），当蓝牙断开时自动切换至 eSIM/Wi-Fi。

```dart
// 💡 架构思路：在 Flutter 侧感知鸿蒙网络状态
void monitorWatchConnectivity() {
  connectivity.onConnectivityChanged.listen((ConnectivityResult result) {
    if (result == ConnectivityResult.wifi || result == ConnectivityResult.mobile) {
      // ⚡️ 提示用户：当前处于独立连网模式，注意电量
      showWatchToast("独立连网模式已开启");
    }
  });
}
```

### 1.2 网络请求瘦身
手表端网络带宽有限且极度耗电。
- ✅ **方案**：使用 **Protobuf** 替代 JSON 进行数据序列化。
- ✅ **技巧**：强制开启 `gzip` 压缩，并将请求超时时间（Timeout）调大至 30 秒，以应对弱网环境。

---

## 二、实战：离线地图与核心数据持久化

由于手表常在户外运动时使用，离线能力是刚需。

### 2.1 矢量瓦片离线存储
针对手表端地图，不建议实时下发。
- ✅ **做法**：在手机端通过 Flutter 预下载地图切片，通过我们在 84 篇学过的分布式文件服务，在充电时静默同步至手表的沙盒目录。

### 2.2 数据最终一致性
当手表在户外记录了运动数据：
1.  **本地落库**（手表 SQLite）。
2.  **标记同步状态**。
3.  **蓝牙恢复后**，触发后台同步 Service，自动将数据推送到服务器或手机端。

<!-- IMAGE_PLACEHOLDER: 通过 DevEco Studio 命令行将 Flutter HAP 产物一键部署到华为 Watch 真机并运行的终端截图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示穿戴端完整的开发构建闭环 -->

---

## 三、进阶：针对圆形屏的自动化 UI 测试

如何确保你的 UI 没有在某款圆形屏上被遮挡？

### 3.1 截图回归测试
利用 Flutter 的 `golden_test`，但要加载自定义的手表剪裁蒙版。

```dart
testWidgets('Watch UI Golden Test', (tester) async {
  await tester.pumpWidget(const MyApp());
  // 📌 核心：模拟手表特有的物理屏蔽区域
  await expectLater(find.byType(MyApp), matchesGoldenFile('watch_round_mask.png'));
});
```

---

## 四、OpenHarmony 平台适配要点：后台保活

鸿蒙系统对穿戴应用的后台存活限制极死。
- ✅ **推荐做法**：如果需要后台计步或定位，必须申请并启动 **Foreground Service (前台服务)**。在 Flutter 侧，通过插件在鸿蒙原生侧绑定一个 `Sticky Notification`，防止应用被系统强制回收。

---

## 五、总结：穿戴专题回顾

至此，我们完成了 101-105 篇的穿戴深度探索：
1.  **形态适配**：圆形屏幕的面积计算与交互安全区。
2.  **效能优先**：传感器、渲染与网络请求的低功耗治理。
3.  **独立生态**：eSIM 连网与离线数据兜底。

掌握了这些，你已经具备了独立开发“现象级”鸿蒙手表应用的能力。

**第一百零六篇，我们将离开手腕，目光转向客厅的中心——【鸿蒙智慧屏 (TV) 与多端投屏实战】。**

---

> 📦 **穿戴端独立连网模板代码包**：[open-harmony-examples/watch-standalone-kit](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/watch-standalone-kit)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
