![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战：打造高颜值运动排行榜（下）— 动效交互与性能优化

> **摘要**：静态的排行榜只是数据的堆砌，动效才是交互的灵魂。本文作为运动排行榜系列的下篇，将重点讲解如何实现"数字滚动增长"动画、具有弹跳反馈的点赞交互，以及 CustomScrollView 下的下拉刷新最佳实践。通过本文，你将掌握如何让排行榜页面"活"起来，显著提升用户的操作爽感。

![运动排行榜动效演示](https://i-blog.csdnimg.cn/direct/b1fb15c41e044f3f9dcf583dc227d68b.gif)

## 前言

在上篇中，我们使用 `SliverPersistentHeader` 自定义 Delegate 打造了一个极具现代感的运动排行榜骨架。但如果步数直接显示"12,504"，用户会觉得索然无味。如果它能像里程表一样从 0 飞速滚到 12,504，成就感瞬间翻倍。

此外，当用户给好友点赞时，如果只是图标变红，未免太单调了。我们希望它能跳动一下，甚至迸发出一些小爱心。

**本文你将学到**：
- 手写 `CountUpAnimation` 数字滚动组件
- 实现 `ScaleTransition` 缩放点赞动效
- `Sliver` 体系下的下拉刷新 (`RefreshIndicator`)
- 鸿蒙上的滚动物理效果优化
- 完整的动效组件集成方案

---

## 一、数字滚动动画 (Count Up)

### 1.1 为什么需要数字滚动？

在运动类 App 中，数字的变化往往代表着用户的成就。如果数字能"滚动"起来，而不是生硬地跳变，用户的成就感会显著提升。

**设计原则**：
- **速度曲线**：先快后慢（`Curves.easeOutExpo`），模拟机械表的惯性。
- **格式化**：大数字需要千分位分隔符（12,504），提升可读性。
- **时长控制**：2 秒左右最佳，过快看不清，过慢显得拖沓。

### 1.2 实现原理

Flutter 中没有直接的 CountUp 组件，但通过 `TweenAnimationBuilder` 就能轻松实现。它的核心思路是：
1.  定义起始值（0）和结束值（实际步数）。
2.  使用 `Tween` 在两者之间插值。
3.  在 `builder` 中实时格式化数字并渲染。

### 1.3 封装 CountUpText 组件

新建 `lib/widgets/count_up_text.dart`：

```dart
import 'package:flutter/material.dart';

class CountUpText extends StatelessWidget {
  final int value;
  final TextStyle? style;
  final Duration duration;
  final Curve curve;

  const CountUpText({
    super.key,
    required this.value,
    this.style,
    this.duration = const Duration(seconds: 2), // 默认 2 秒
    this.curve = Curves.easeOutExpo,            // 先快后慢
  });

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0, end: value.toDouble()),
      duration: duration,
      curve: curve,
      builder: (context, val, child) {
        // 格式化数字：12,504
        final formatted = val.toInt().toString().replaceAllMapped(
            RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'), 
            (Match m) => '${m[1]},');
            
        return Text(formatted, style: style);
      },
    );
  }
}
```

**代码解析**：
- `TweenAnimationBuilder<double>`：自动管理动画状态，无需手动创建 `AnimationController`。
- `Tween(begin: 0, end: value.toDouble())`：定义插值范围。
- `RegExp` 正则表达式：为数字添加千分位分隔符。

### 1.4 集成到 RankListItem

在上篇的 `RankListItem` 中替换静态文本：

```dart
// 在 RankListItem 的 build 方法中，将步数部分替换为：
CountUpText(
  value: steps,
  style: const TextStyle(
    color: Color(0xFFFF6B00), 
    fontWeight: FontWeight.w900, // 极粗
    fontSize: 22,
    fontStyle: FontStyle.italic, // 斜体增加速度感
    fontFamily: 'Barlow',
  ),
),
```

**效果**：当列表项首次渲染时，步数会从 0 快速滚动到目标值，给用户带来强烈的视觉冲击。

💡 **优化技巧**：如果列表项过多，可以使用 `ListView.builder` 的 `addAutomaticKeepAlives: false` 配合 `AutomaticKeepAliveClientMixin`，确保只有可见区域的数字才会滚动，避免性能浪费。

---

## 二、Q 弹的点赞交互

### 2.1 交互设计分析

点赞是社交类功能的核心。一个优秀的点赞交互应该具备：
1.  **即时反馈**：点击瞬间图标变色。
2.  **弹性动画**：图标先放大再缩小，模拟"弹跳"效果。
3.  **状态持久化**：点赞状态需要保存（本文暂不涉及后端）。

![点赞动效演示](https://i-blog.csdnimg.cn/direct/c6bfd2000b104c03ac938a69c01057c5.gif)

### 2.2 实现原理

我们使用 `ScaleTransition` 配合 `TweenSequence` 来实现"放大-缩小"的序列动画。

**动画曲线设计**：
- **阶段 1**：从 1.0 缩放到 1.3（放大）
- **阶段 2**：从 1.3 缩放回 1.0（复原）
- **总时长**：200ms（快速反馈）

### 2.3 封装 LikeButton 组件

新建 `lib/widgets/like_button.dart`：

```dart
import 'package:flutter/material.dart';

class LikeButton extends StatefulWidget {
  final bool initialLiked;
  final int count;
  final ValueChanged<bool>? onLikeChanged; // 回调函数，用于后续集成后端

  const LikeButton({
    super.key,
    required this.initialLiked,
    required this.count,
    this.onLikeChanged,
  });

  @override
  State<LikeButton> createState() => _LikeButtonState();
}

class _LikeButtonState extends State<LikeButton> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late bool _isLiked;
  late int _count;

  @override
  void initState() {
    super.initState();
    _isLiked = widget.initialLiked;
    _count = widget.count;
    
    // 创建动画控制器
    _controller = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 200));
    
    // 缩放曲线：1.0 -> 1.3 -> 1.0 (瞬间变大再复原)
    _scaleAnimation = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 1.3), weight: 50),
      TweenSequenceItem(tween: Tween(begin: 1.3, end: 1.0), weight: 50),
    ]).animate(_controller);
  }

  void _toggleLike() {
    _controller.forward().then((_) => _controller.reset()); // 播放动画
    setState(() {
      _isLiked = !_isLiked;
      _count += _isLiked ? 1 : -1;
    });
    
    // 触发回调（用于后续集成后端）
    widget.onLikeChanged?.call(_isLiked);
  }

  @override
  void dispose() {
    _controller.dispose(); // 释放资源
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _toggleLike,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('$_count', style: const TextStyle(fontSize: 12, color: Colors.grey)),
          const SizedBox(width: 4),
          ScaleTransition(
            scale: _scaleAnimation,
            child: Icon(
              _isLiked ? Icons.favorite : Icons.favorite_border,
              size: 20, // 稍微调大一点以便手指点击
              color: _isLiked ? Colors.red : Colors.grey,
            ),
          ),
        ],
      ),
    );
  }
}
```

**代码解析**：
- `SingleTickerProviderStateMixin`：为 `AnimationController` 提供 `vsync`。
- `TweenSequence`：定义多阶段动画序列。
- `dispose()`：释放动画控制器，避免内存泄漏。

### 2.4 集成到 RankListItem

在 `RankListItem` 中替换原有的点赞部分：

```dart
// 在 RankListItem 的 build 方法中，将点赞部分替换为：
LikeButton(
  initialLiked: false,
  count: likes,
  onLikeChanged: (isLiked) {
    // TODO: 调用后端 API 更新点赞状态
    print('点赞状态变更: $isLiked');
  },
),
```

⚠️ **注意**：在实际项目中，需要将点赞状态同步到后端，并在列表刷新时恢复状态。

---

## 三、下拉刷新与 Sliver 结合

### 3.1 为什么需要下拉刷新？

运动排行榜的数据是实时变化的，用户需要能够手动刷新以获取最新排名。

![下拉刷新演示](https://i-blog.csdnimg.cn/direct/95a499d2a0544893a215710e5f6947a9.gif)

### 3.2 Sliver 体系下的刷新方案

在 `CustomScrollView` 中，普通的 `RefreshIndicator` 有时会与 `SliverAppBar` 冲突（例如下拉距离不够就触发）。

Flutter 提供了两种方案：
1.  **RefreshIndicator 包裹整个 CustomScrollView**（推荐）
2.  **CupertinoSliverRefreshControl**（iOS 风格）

我们选择方案 1，因为它在 Android/鸿蒙上的体验更好。

### 3.3 实现代码

修改 `LeaderboardPage` 的 `build` 方法：

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    body: RefreshIndicator(
      onRefresh: _handleRefresh, // 刷新回调
      edgeOffset: 120, // 调整刷新指示器的位置，以免被 AppBar 挡住
      child: CustomScrollView(
        // 鸿蒙/Android 为了拥有类似 iOS 的回弹效果，强行指定 physics
        physics: const BouncingScrollPhysics(
          parent: AlwaysScrollableScrollPhysics(), // 即使内容不足一屏也能下拉
        ),
        slivers: [
          _buildCombinedHeader(context),
          _buildRankList(),
        ],
      ),
    ),
  );
}

// 刷新逻辑
Future<void> _handleRefresh() async {
  // 模拟网络请求
  await Future.delayed(const Duration(seconds: 2));
  
  // TODO: 调用后端 API 获取最新排行榜数据
  // setState(() {
  //   users = newData;
  // });
  
  print('排行榜数据已刷新');
}
```

**代码解析**：
- `edgeOffset: 120`：由于我们的头部高度较高，需要调整刷新指示器的位置。
- `BouncingScrollPhysics`：iOS 风格的回弹效果，比 Android 默认的 Glow 更优雅。
- `AlwaysScrollableScrollPhysics`：即使内容不足一屏也能下拉刷新。

### 3.4 状态管理优化

在实际项目中，建议使用状态管理方案（如 `Provider`、`Riverpod`）来管理排行榜数据：

```dart
class LeaderboardPage extends StatefulWidget {
  const LeaderboardPage({super.key});

  @override
  State<LeaderboardPage> createState() => _LeaderboardPageState();
}

class _LeaderboardPageState extends State<LeaderboardPage> {
  List<Map<String, dynamic>> _users = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadData(); // 初始化加载数据
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    
    // TODO: 调用后端 API
    await Future.delayed(const Duration(seconds: 1));
    
    setState(() {
      _users = List.generate(20, (index) => {
        'name': 'Runner ${index + 88}',
        'steps': 20000 - index * 500,
        'likes': 10 + index,
        'avatar': 'https://i.pravatar.cc/150?img=${index + 20}',
      });
      _isLoading = false;
    });
  }

  Future<void> _handleRefresh() async {
    await _loadData();
  }

  // ... 其他代码
}
```

---

## 四、鸿蒙特有优化

### 4.1 列表的 OverScroll 效果

在 Android/鸿蒙上，列表滑动到边缘默认会有"波纹" (Glow) 效果，但在这种沉浸式头部的页面上，顶部出现的蓝色波纹会破坏美感。

我们可以替换为 `BouncingScrollPhysics`（回弹），或者去除波纹。

#### 方案 1：使用回弹效果（推荐）

```dart
CustomScrollView(
  physics: const BouncingScrollPhysics(
    parent: AlwaysScrollableScrollPhysics(),
  ),
  // ...
)
```

#### 方案 2：完全去除波纹

```dart
ScrollConfiguration(
  behavior: const ScrollBehavior().copyWith(overscroll: false),
  child: CustomScrollView(...),
)
```

💡 **设计建议**：对于运动 App，**回弹 (Bouncing)** 带来的果冻感通常更符合"活力"的设计语言，所以推荐使用方案 1。

### 4.2 性能优化建议

#### （1）列表项复用

使用 `ListView.builder` 或 `SliverList` 时，Flutter 会自动复用列表项。但如果列表项包含动画，需要注意：

```dart
// ❌ 错误做法：每次 build 都创建新的 CountUpText
Text('$steps')

// ✅ 正确做法：使用 const 或缓存
const CountUpText(value: 12504)
```

#### （2）图片缓存

头像图片应该使用缓存，避免重复加载：

```dart
CachedNetworkImage(
  imageUrl: avatarUrl,
  placeholder: (context, url) => const CircularProgressIndicator(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
)
```

#### （3）避免过度重建

使用 `const` 构造函数和 `Key` 来优化性能：

```dart
RankListItem(
  key: ValueKey(user['id']), // 使用唯一 ID 作为 Key
  rank: rank,
  // ...
)
```

### 4.3 折叠屏适配

鸿蒙设备中有折叠屏，需要监听屏幕尺寸变化：

```dart
@override
Widget build(BuildContext context) {
  final screenWidth = MediaQuery.of(context).size.width;
  
  return Scaffold(
    body: CustomScrollView(
      slivers: [
        _buildCombinedHeader(context),
        SliverPadding(
          padding: EdgeInsets.symmetric(
            horizontal: screenWidth > 600 ? 40 : 20, // 大屏增加边距
          ),
          sliver: _buildRankList(),
        ),
      ],
    ),
  );
}
```

---

## 五、完整集成示例

### 5.1 完整的 LeaderboardPage

```dart
import 'dart:ui';
import 'package:flutter/material.dart';
import '../widgets/count_up_text.dart';
import '../widgets/like_button.dart';

class LeaderboardPage extends StatefulWidget {
  const LeaderboardPage({super.key});

  @override
  State<LeaderboardPage> createState() => _LeaderboardPageState();
}

class _LeaderboardPageState extends State<LeaderboardPage> {
  List<Map<String, dynamic>> _users = [];

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    await Future.delayed(const Duration(seconds: 1));
    setState(() {
      _users = List.generate(20, (index) => {
        'name': 'Runner ${index + 88}',
        'steps': 20000 - index * 500,
        'likes': 10 + index,
        'avatar': 'https://i.pravatar.cc/150?img=${index + 20}',
      });
    });
  }

  Future<void> _handleRefresh() async {
    await _loadData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: RefreshIndicator(
        onRefresh: _handleRefresh,
        edgeOffset: 120,
        child: CustomScrollView(
          physics: const BouncingScrollPhysics(
            parent: AlwaysScrollableScrollPhysics(),
          ),
          slivers: [
            _buildCombinedHeader(context),
            _buildRankList(),
          ],
        ),
      ),
    );
  }

  // ... 其他方法（参考上篇）
}
```

### 5.2 优化后的 RankListItem

```dart
class RankListItem extends StatelessWidget {
  final int rank;
  final String name;
  final int steps;
  final String avatarUrl;
  final int likes;

  const RankListItem({
    super.key,
    required this.rank,
    required this.name,
    required this.steps,
    required this.avatarUrl,
    required this.likes,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 16,
            offset: const Offset(0, 4),
          )
        ],
      ),
      child: Row(
        children: [
          // 排名图标/数字
          SizedBox(
            width: 40,
            child: rank <= 3
                ? Icon(Icons.emoji_events, color: _getRankColor(rank), size: 32)
                : Text('#$rank', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w900, fontStyle: FontStyle.italic, color: Colors.grey[400])),
          ),
          const SizedBox(width: 12),
          
          // 头像
          CircleAvatar(radius: 24, backgroundImage: NetworkImage(avatarUrl)),
          const SizedBox(width: 16),
          
          // 姓名
          Expanded(child: Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16))),
          
          // 步数（使用 CountUpText）
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              CountUpText(
                value: steps,
                style: const TextStyle(
                  color: Color(0xFFFF6B00),
                  fontWeight: FontWeight.w900,
                  fontSize: 22,
                  fontStyle: FontStyle.italic,
                  fontFamily: 'Barlow',
                ),
              ),
              LikeButton(initialLiked: false, count: likes),
            ],
          ),
        ],
      ),
    );
  }

  Color _getRankColor(int rank) {
    switch (rank) {
      case 1: return const Color(0xFFFFD700);
      case 2: return const Color(0xFFC0C0C0);
      case 3: return const Color(0xFFCD7F32);
      default: return Colors.grey.withOpacity(0.5);
    }
  }
}
```

---

## 六、全系列总结

通过上下两篇的实战，我们完成了一个高水准的运动排行榜页面。

### 主要成就

1.  **架构**：掌握了 `CustomScrollView` + `SliverPersistentHeader` 的进阶布局。
2.  **设计**：实现了视差滚动、动态卡片淡出、玻璃拟态等高级 UI 效果。
3.  **交互**：通过数字滚动和点赞反馈，显著提升了用户的操作爽感。
4.  **性能**：针对鸿蒙平台进行了滚动物理效果和列表复用优化。

### 技术要点回顾

| 技术点 | 实现方案 | 适用场景 |
|-------|---------|---------|
| 数字滚动 | `TweenAnimationBuilder` | 步数、积分、金额等数值展示 |
| 点赞动效 | `ScaleTransition` + `TweenSequence` | 社交互动、收藏、关注等 |
| 下拉刷新 | `RefreshIndicator` + `BouncingScrollPhysics` | 列表数据更新 |
| 动态头部 | `SliverPersistentHeaderDelegate` | 个人主页、商品详情等 |

### 后续学习方向

1.  **粒子效果**：使用 `CustomPainter` 实现点赞时的爱心粒子喷射。
2.  **排名变化动画**：当排名发生变化时，列表项平滑移动到新位置。
3.  **数据持久化**：使用 `shared_preferences` 或 `sqflite` 缓存排行榜数据。
4.  **实时更新**：集成 WebSocket 实现排行榜的实时推送。

这套代码可以轻松复用到"财富榜单"、"积分排名"、"游戏排行"等任何需要展示列表的场景中。

---

## 七、常见问题与解决方案

### 7.1 数字滚动卡顿怎么办？

**问题描述**：在低端设备上，`CountUpText` 可能会出现卡顿。

**解决方案**：
1.  **降低刷新率**：将 `duration` 从 2 秒调整为 1.5 秒。
2.  **使用 `RepaintBoundary`**：隔离重绘区域。

```dart
RepaintBoundary(
  child: CountUpText(value: steps),
)
```

3.  **延迟加载**：只有当列表项进入可见区域时才开始动画。

```dart
class _RankListItemState extends State<RankListItem> with AutomaticKeepAliveClientMixin {
  bool _hasAnimated = false;

  @override
  Widget build(BuildContext context) {
    super.build(context);
    
    return VisibilityDetector(
      key: Key('rank-$rank'),
      onVisibilityChanged: (info) {
        if (info.visibleFraction > 0.5 && !_hasAnimated) {
          setState(() => _hasAnimated = true);
        }
      },
      child: _hasAnimated 
          ? CountUpText(value: steps)
          : Text('$steps'), // 未进入可见区域时显示静态文本
    );
  }

  @override
  bool get wantKeepAlive => true;
}
```

### 7.2 点赞状态如何持久化？

**问题描述**：刷新页面后，点赞状态丢失。

**解决方案**：使用 `shared_preferences` 本地缓存。

```dart
import 'package:shared_preferences/shared_preferences.dart';

class LikeService {
  static const String _keyPrefix = 'like_';

  // 保存点赞状态
  static Future<void> saveLikeStatus(String userId, bool isLiked) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('$_keyPrefix$userId', isLiked);
  }

  // 读取点赞状态
  static Future<bool> getLikeStatus(String userId) async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('$_keyPrefix$userId') ?? false;
  }
}

// 在 LikeButton 中使用
void _toggleLike() async {
  _controller.forward().then((_) => _controller.reset());
  setState(() {
    _isLiked = !_isLiked;
    _count += _isLiked ? 1 : -1;
  });
  
  // 保存到本地
  await LikeService.saveLikeStatus(widget.userId, _isLiked);
  
  // 同步到后端
  widget.onLikeChanged?.call(_isLiked);
}
```

### 7.3 下拉刷新时如何显示加载状态？

**问题描述**：刷新时用户不知道数据是否正在加载。

**解决方案**：在头部卡片中显示加载指示器。

```dart
class _LeaderboardPageState extends State<LeaderboardPage> {
  bool _isRefreshing = false;

  Future<void> _handleRefresh() async {
    setState(() => _isRefreshing = true);
    
    await _loadData();
    
    setState(() => _isRefreshing = false);
  }

  Widget _buildUserStatsCard(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 0, 20, 0),
      child: Stack(
        children: [
          Container(
            // ... 原有卡片代码
          ),
          
          // 加载指示器
          if (_isRefreshing)
            Positioned.fill(
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.3),
                  borderRadius: BorderRadius.circular(24),
                ),
                child: const Center(
                  child: CircularProgressIndicator(color: Colors.white),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
```

### 7.4 如何实现排名变化的高亮提示？

**问题描述**：用户希望看到自己的排名是上升还是下降。

**解决方案**：在列表项中增加排名变化箭头。

```dart
class RankListItem extends StatelessWidget {
  final int rank;
  final int? previousRank; // 上次的排名

  // ... 其他字段

  Widget _buildRankChange() {
    if (previousRank == null) return const SizedBox.shrink();
    
    final change = previousRank! - rank;
    if (change == 0) return const SizedBox.shrink();
    
    return Row(
      children: [
        Icon(
          change > 0 ? Icons.arrow_upward : Icons.arrow_downward,
          size: 14,
          color: change > 0 ? Colors.green : Colors.red,
        ),
        Text(
          '${change.abs()}',
          style: TextStyle(
            fontSize: 12,
            color: change > 0 ? Colors.green : Colors.red,
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      // ... 原有代码
      child: Row(
        children: [
          // 排名
          Column(
            children: [
              SizedBox(
                width: 40,
                child: rank <= 3
                    ? Icon(Icons.emoji_events, color: _getRankColor(rank), size: 32)
                    : Text('#$rank', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w900)),
              ),
              _buildRankChange(), // 排名变化指示器
            ],
          ),
          // ... 其他内容
        ],
      ),
    );
  }
}
```

### 7.5 如何优化大列表的内存占用？

**问题描述**：排行榜数据量大（如 1000+ 条）时，内存占用过高。

**解决方案**：使用分页加载 + 虚拟滚动。

```dart
class _LeaderboardPageState extends State<LeaderboardPage> {
  final List<Map<String, dynamic>> _users = [];
  int _currentPage = 1;
  bool _hasMore = true;
  bool _isLoadingMore = false;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    if (_isLoadingMore || !_hasMore) return;
    
    setState(() => _isLoadingMore = true);
    
    // 模拟分页请求
    await Future.delayed(const Duration(seconds: 1));
    final newData = List.generate(20, (index) => {
      'name': 'Runner ${(_currentPage - 1) * 20 + index + 88}',
      'steps': 20000 - ((_currentPage - 1) * 20 + index) * 500,
      // ...
    });
    
    setState(() {
      _users.addAll(newData);
      _currentPage++;
      _isLoadingMore = false;
      _hasMore = _currentPage <= 50; // 假设最多 50 页
    });
  }

  Widget _buildRankList() {
    return SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) {
          // 滚动到倒数第 3 项时，加载下一页
          if (index == _users.length - 3 && _hasMore) {
            _loadData();
          }
          
          if (index >= _users.length) {
            return const Center(child: CircularProgressIndicator());
          }
          
          final user = _users[index];
          return RankListItem(
            rank: index + 1,
            name: user['name'],
            steps: user['steps'],
            avatarUrl: user['avatar'],
            likes: user['likes'],
          );
        },
        childCount: _users.length + (_hasMore ? 1 : 0), // 多加 1 个用于显示加载指示器
      ),
    );
  }
}
```

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: project/sport-leaderboard-part2)](https://atomgit.com/dragonbady/open-harmony-example/tree/project/sport-leaderboard-part2)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
