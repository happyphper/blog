![Flutter for OpenHarmony 实战：Card 与 交互水波纹](./images/19-card-inkwell.png)

# Flutter for OpenHarmony 实战之基础组件：第十九篇 质感布局 Card 与交互水波纹

> **摘要**：一个好的 UI 不仅仅是摆放整齐，还需要层次感和交互反馈。`Card`（卡片）是实现视觉分层、将信息打包的利器；而水波纹（InkWell）则是赋予静态 UI 灵活生命力的关键。本文将结合 Flutter 最新的 Material 3 设计规范，教你如何在 OpenHarmony 上打造极具“质感”的界面。

## 前言

在 OpenHarmony 的系统设计语言（HarmonyOS Design）中，“容器卡片化”是一个非常重要的核心概念。你会发现无论是控制中心、服务卡片还是桌面组件，大量使用了圆角矩形和细腻的投影。

在 Flutter 中，虽然基础的 `Container` 配合 `BoxDecoration` 也能做出卡片效果，但原生的 `Card` 组件自带了 Material Design 的精髓：它自动处理了阴影层叠（Elevation）和标准的圆角，让开发者能更快速地构建具有立体感的界面。

**本文你将学到**：
- `Card` 组件的核心属性：Elevation, Shape, Margin
- Material 2 vs Material 3：卡片样式的演进
- `InkWell` 与 `Ink`：如何给卡片添加完美的水波纹点击反馈
- 实战：打造符合鸿蒙审美的高级设置项卡片流

---

## 一、Card 组件：信息的容器

### 1.1 基础用法

```dart
Card(
  elevation: 4,               // 💡 阴影高度，数值越大阴影越柔和
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(16), // 💡 重点：适配鸿蒙推荐的大圆角
  ),
  child: const Padding(
    padding: EdgeInsets.all(16.0),
    child: Column(
      children: [
        Text('卡片标题', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        Text('这是一段卡片的描述文字，通常用于封装独立的信息块。'),
      ],
    ),
  ),
)
```

### 1.2 提升“质感”的关键属性
- **elevation**: 控制阴影物理高度。在 Material 3 中建议使用较小的数值（如 1 或 2），甚至是 0（通过背景色区分）。
- **color**: 背景颜色，默认是主题色仓库。
- **clipBehavior**: 裁剪行为。如果你的卡片图溢出了边缘，记得设置 `Clip.antiAlias` 以强制应用圆角裁剪。

---

## 二、Material 3：更现代的视觉

Flutter 现在默认推荐使用 **Material 3 (M3)**，它在卡片设计上有了显著变化：
- **填充型卡片 (Filled Card)**：没有阴影，只有浅色背景。
- **轮廓型卡片 (Outlined Card)**：没有阴影，只有细细的边框。
- **高度卡片 (Elevated Card)**：传统的阴影卡片。

```dart
// 在 MaterialApp 中开启
theme: ThemeData(useMaterial3: true),
```

在鸿蒙适配中，**填充型卡片 (Filled)** 往往看起来更干净，更像鸿蒙系统设置的风格。

---

## 三、交互反馈：水波纹 (InkWell)

如果你只是把 Card 包裹在 `GestureDetector` 里，点击时是没有任何视觉反馈的。

为了让卡片点击起来“更有弹性”，我们需要用 `InkWell`。

### 3.1 正确的嵌套方式
⚠️ **注意**：为了让水波纹在卡片内显示，且不遮挡背景，最规范的写法是：

```dart
Card(
  clipBehavior: Clip.antiAlias, // 💡 必须：切断溢出的水波纹
  child: InkWell(
    onTap: () => print('点击了卡片'),
    child: Padding(
      padding: EdgeInsets.all(16),
      child: Text('我有点击反馈！'),
    ),
  ),
)
```

![InkWell 水波纹交互效果演示](./images/19-card-inkwell.png)
> **图 1**：在 Card 内部嵌套 InkWell，可实现符合 Material Design 规范的点击水波纹反馈。

---

## 四、OpenHarmony 平台适配实战

### 4.1 场景：系统设置风格的卡片流
鸿蒙的设置页面由若干个圆角大卡片组成，每个卡片内部包含多行设置项。

### 4.2 实战代码实现

```dart
class OhosSettingsPage extends StatelessWidget {
  const OhosSettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF1F3F5), // 💡 适配鸿蒙背景灰色
      appBar: AppBar(title: const Text('系统设置'), centerTitle: true),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildOhosCard([
            _buildSettingItem(Icons.wifi, '无线网络', '已连接'),
            _buildDivider(),
            _buildSettingItem(Icons.bluetooth, '蓝牙', '正在运行'),
          ]),
          const SizedBox(height: 16),
          _buildOhosCard([
            _buildSettingItem(Icons.notifications, '通知与打扰', ''),
            _buildDivider(),
            _buildSettingItem(Icons.display_settings, '显示与亮度', ''),
          ]),
        ],
      ),
    );
  }

  // 模拟鸿蒙风格的圆角大卡片
  Widget _buildOhosCard(List<Widget> children) {
    return Card(
      elevation: 0, // 💡 鸿蒙风格倾向于无阴影背景色区分
      color: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
      child: Column(children: children),
    );
  }

  Widget _buildSettingItem(IconData icon, String title, String trailing) {
    return InkWell(
      onTap: () {},
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        child: Row(
          children: [
            Icon(icon, color: Colors.blueAccent, size: 24),
            const SizedBox(width: 16),
            Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.normal)),
            const Spacer(),
            Text(trailing, style: const TextStyle(color: Colors.grey)),
            const Icon(Icons.chevron_right, color: Colors.grey),
          ],
        ),
      ),
    );
  }

  Widget _buildDivider() {
    return Padding(
      padding: const EdgeInsets.only(left: 56), // 💡 避开图标的分割线
      child: Divider(height: 1, color: Colors.grey[200]),
    );
  }
}
```

---

## 五、总结

卡片不仅仅是一个容器，它体现了 UI 中的“分组”思想。

### 核心要点：
1. **视觉分层**：通过 `Card` 的阴影或背景色，将内容从页面中剥离出来。
2. **大圆角美学**：为了适配鸿蒙，建议使用 `borderRadius: BorderRadius.circular(20)` 以上，看起来更具现代感。
3. **点击语义**：`InkWell` 不仅提供了水波纹，还提供了无障碍访问支持，让应用“好用且好看”。
4. **适配策略**：在小屏手机上使用单列卡片；在鸿蒙平板上，利用 `GridView` 展示多列卡片。

### 下一篇预告
我们的 UI 现在既有结构又有质感。但如果这些组件能在移动、变色时更“丝滑”一点呢？我们没必要学习复杂的 AnimationController，只需要把常用的组件换一个前缀。
**《Flutter for OpenHarmony 实战之基础组件：第二十篇 零门槛动画 AnimatedContainer 与隐式动画》**
开启 UI 动效的大门！

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/19-card-inkwell)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/19-card-inkwell)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
