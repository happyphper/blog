![封面图](images/104-cover.png)

# Flutter for OpenHarmony 实战之殿堂：第一百零四篇 鸿蒙穿戴 (Watch) 体验 — 打造极致丝滑的圆形列表与手感反馈

## 前言

在手表的极小屏幕上，用户 80% 的操作都在滑动列表。如果列表稍微有一点点“粘手”或“掉帧”，在圆形屏幕的放大效应下都会清晰可见。

作为 **Flutter for OpenHarmony** 开发者，如何让列表在华为 Watch 的 1.43 英寸屏上跑出绸缎般的质感？本篇将深入研究 **圆形物理引擎** 与 **线性振动马达** 的深度协同。

---

## 一、圆形列表的视觉魔法：扇形滚动

在圆形屏上，直上直下的列表会浪费左右两侧的空间。
- **方案：Radial Layout**。即随着向上滑动，列表项不仅仅是改变 Y 轴，还应向屏幕中心靠拢，形成类似“弧形”滚动的视觉效果。

```dart
// 💡 技巧：利用 Transform.scale 与 Transform.translate 模拟弧形
Scrollbar(
  child: ListView.builder(
    itemBuilder: (context, index) {
      return LayoutBuilder(builder: (context, constraints) {
        // 计算当前项距离屏幕中心的 Y 轴位置
        double offset = calcDistanceFromCenter(context);
        return Transform.translate(
          offset: Offset(calcHorizontalShift(offset), 0), // 越靠边缘越往里收
          child: Opacity(opacity: calcOpacity(offset), child: MyWatchItem()),
        );
      });
    },
  ),
)
```

---

## 二、实战：物理表冠的“步进感”与震动协同

鸿蒙手表配备的高规格线性马达是提升手感的利器。

### 2.1 模拟物理刻度感
当用户旋转表冠切换列表项时，我们应给予精准的触觉反馈。

```typescript
// 📌 鸿蒙原生侧：触发离散型震动
import vibrator from '@ohos.vibrator';

function triggerCrownTick() {
  // ⚡️ 使用短而有力的精密震动（'haptic.watch.crown_tick'）
  vibrator.startVibration({
    type: 'preset',
    effectId: 'haptic.watch.crown_tick',
    count: 1
  });
}
```

### 2.2 列表边缘的回弹反馈
当列表滑到尽头（OverScroll）时，通过 `notification.vibrate` 触发一次强烈的震动。

---

## 三、性能优化：零 Jank 的列表渲染

### 3.1 预渲染 (CacheExtent) 的克制
在手机端我们可以预加载 5 个项，但在手表端：
- ✅ **建议**：`cacheExtent` 设置为 0 或极小。因为手表屏幕小，视口外的内容如果占用过多显存，会导致 GPU 提交指令变慢。

### 3.2 图片异步解压缓存
- ✅ **方案**：使用 `shared_preferences_ohos` 缓存图片的原始位图数据。在手表端，磁盘 I/O 是耗电大户，尽量在内存中保留最常用的 3-5 张运动图标。

<!-- IMAGE_PLACEHOLDER: 华为 Watch 4 屏幕上，Flutter 列表项随滑动呈弧形轨迹排列且带运动模糊效果的动图 -->
<!-- 类型: 动图 -->
<!-- 内容: 展示极具穿戴设备特色的 UI 动感 -->

---

## 四、OpenHarmony 平台适配要点：多分辨率兼容

不同型号的手表（Watch GT vs Watch Pro）像素密度和直径略有不同。
- ✅ **推荐做法**：不要使用绝对像素值（PX）。在鸿蒙侧，利用 `display.getDefaultDisplaySync()` 获取屏幕 DPI，并在 Flutter 侧建立一套基于 `LogicalPixel` 的**等比缩放比例尺**。

---

## 五、总结

极致的体验在于细节的“妥帖”：
1.  **视觉契合**：弧形布局是圆形屏的灵魂。
2.  **触觉反馈**：没有震动的列表滑动在手表上是“死的”。
3.  **性能极简**：用最少的显存，换取最稳定的 60FPS。

第一百零五篇，我们将为穿戴专栏收官，探讨 **鸿蒙手表的离线部署与自动化测试流程**。

---

> 📦 **圆形列表专用组件包 (ArcList)**：[open-harmony-examples/watch-arc-list](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/watch-arc-list)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
