![封面图](images/106-cover.png)

# Flutter for OpenHarmony 实战之殿堂：第一百零六篇 鸿蒙智慧屏 (TV) 适配 — 大屏焦点管控与遥控器交互

## 前言

离开了手腕上的小屏幕，我们来到了客厅的中心——**华为智慧屏 (HarmonyOS TV)**。在大屏开发中，最大的交互变更在于：用户不再用手直接触摸，而是通过离屏幕 3 米远的**遥控器**进行操作。

在 Flutter 中，如何处理这种基于方向键（D-Pad）的焦点跳转？如何在大屏上展现鸿蒙的高级视觉质感？本篇将带你攻克 **TV 端开发**的第一道防线。

---

## 一、TV 端的核心交互模型：焦点 (Focus)

在手机上，用户点哪哪响应；在 TV 上，用户通过上下左右移动“焦点”，再按 OK 键触发。
- **FocusNode**：Flutter 焦点系统的核心。
- **FocusScope**：管理一组焦点的容器，决定焦点的循环与跳转逻辑。

---

## 二、实战：打造符合鸿蒙 TV 设计规范的焦点动效

### 2.1 焦点放大与外发光效果
当一个海报图（Poster）获得焦点时，应伴随轻微的放大（Scale）与柔和的呼吸灯外发光效果。

```dart
class OhosTvCard extends StatefulWidget {
  @override
  _OhosTvCardState createState() => _OhosTvCardState();
}

class _OhosTvCardState extends State<OhosTvCard> {
  final FocusNode _node = FocusNode();
  bool _hasFocus = false;

  @override
  Widget build(BuildContext context) {
    return Focus(
      focusNode: _node,
      onFocusChange: (value) => setState(() => _hasFocus = value),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        // 💡 技巧：获得焦点时放大 1.1 倍
        transform: Matrix4.identity()..scale(_hasFocus ? 1.1 : 1.0),
        decoration: BoxDecoration(
          boxShadow: _hasFocus ? [BoxShadow(color: Colors.blue.withOpacity(0.5), blurRadius: 20)] : [],
        ),
        child: MyPoster(),
      ),
    );
  }
}
```

### 2.2 处理鸿蒙遥控器 Back 键
鸿蒙 TV 遥控器的返回键（Back）与手机的行为一致，但需要确保它不会直接退出应用。

```dart
// 📌 在外层使用 PopScope 捕获返回，回到上一级焦点区域而非退出
PopScope(
  canPop: false,
  onPopInvoked: (didPop) {
    // 逻辑：如果侧边栏打开了则关闭侧边栏，而非退出 App
  },
  child: MyTvHome(),
)
```

<!-- IMAGE_PLACEHOLDER: 该 Flutter 应用在 65 英寸华为智慧屏上运行，当前焦点停留在“最近观看”电影封面且具备呼吸灯发光动效的实拍图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示大屏 UI 的高级沉浸感 -->

---

## 三、性能优化：大屏渲染的 CPU/GPU 平衡

### 3.1 避免全局 Layout 抖动
大屏分辨率通常是 4K。如果焦点移动导致整个父容器 `setState`，代价极大。
- ✅ **方案**：使用 `RepaintBoundary` 将每一个 Card 隔离。确保焦点变化时，仅有受影响的两个 Card（失去焦点的和获得焦点的）进行重绘。

### 3.2 鸿蒙 AOT 的大屏纹理预加载
- ✅ **建议**：大屏图片通常较大。利用 `precacheImage` 在进入首页前将首屏的 10 张海报预载入显存，防止焦点快速移动时出现白块。

---

## 四、OpenHarmony 平台适配要点：多分辨率兼容

智慧屏有 1080P 和 4K 之分。
- ✅ **推荐做法**：不要在 TV 代码中使用逻辑像素（DP）进行强匹配。建议在根布局使用 `AspectRatio` 锁定 16:9，并配合 `FractionallySizedBox` 等比例容器，确保 UI 在不同尺寸的智慧屏上比例一致。

---

## 五、总结

TV 适配是“寻找焦点”的过程：
1.  **可见即可得**：所有可点区域必须能被焦点选到。
2.  **动画指引**：用柔和的 Scale 与 Shadow 告诉用户焦点在哪。
3.  **遥控先行**：代码库中必须包含通过键盘事件（D-Pad）驱动的逻辑。

第一百零七篇，我们将深入大屏的核心——**鸿蒙智慧屏的高清视频流媒体优化与 HDR 适配**。

---

> 📦 **TV 端焦点专用库 (FocusKit-TV)**：[open-harmony-examples/tv-focus-toolkit](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/tv-focus-toolkit)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
