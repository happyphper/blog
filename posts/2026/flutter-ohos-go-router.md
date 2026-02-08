![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战：go_router 声明式路由完全指南

> **摘要**：在 Flutter 应用开发中，路由管理是核心环节。`go_router` 作为官方推荐的声明式路由库，以其 URL 驱动、支持深层链接（Deep Linking）及高度灵活的嵌套导航受到开发者青睐。本文将详细介绍如何在 Flutter for OpenHarmony 项目中集成并高效使用 `go_router`。

## 前言

随着 Flutter for OpenHarmony 的成熟，开发者在构建复杂的鸿蒙应用时，对路由管理的需求也日益增加。传统的 `Navigator` 1.0 虽然简单，但在处理复杂的嵌套导航、深层链接以及 URL 同步时显得力不从心。

`go_router` 建立在 Flutter 的 `Router` API（Navigator 2.0）之上，通过简洁的声明式语法，极大地简化了路由配置和页面跳转逻辑。

**本文你将学到**：
- `go_router` 的核心概念与配置
- 参数传递与重定向逻辑
- 嵌套路由与 ShellRoute 的高级用法
- OpenHarmony 平台上的导航适配建议

---

## 一、go_router 基础概念

### 1.1 为什么选择 go_router

相比于传统的命名路由，`go_router` 具有以下优势：
- **声明式路由**：路径结构一目了然。
- **URL 驱动**：完美支持浏览器地址同步及移动端深层链接。
- **嵌套导航**：通过 `ShellRoute` 轻松实现底部导航栏等嵌套布局。
- **重定向机制**：方便处理登录鉴权等逻辑。

### 1.2 环境集成

在项目的 `pubspec.yaml` 中添加依赖。在 OpenHarmony 平台上，推荐使用经过 TPC 社区适配的兼容版本：

```yaml
dependencies:
  go_router:
    git:
      url: "https://atomgit.com/openharmony-tpc/flutter_packages.git"
      path: "packages/go_router"
```

💡 **提示**：`go_router` 是纯 Dart 包，不依赖原生代码，因此在 OpenHarmony 平台上具有完美的兼容性。

---

## 二、核心用法详解

### 2.1 简单路由配置

在应用入口处配置 `GoRouter` 实例：

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

final _router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'details',
          builder: (context, state) => const DetailsScreen(),
        ),
      ],
    ),
  ],
);

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: _router,
      title: 'Flutter OHOS Router',
    );
  }
}
```

### 2.2 页面跳转与参数传递

`go_router` 支持路径参数和查询参数：

```dart
// 跳转
context.go('/details/123?name=flutter');

// 定义路由获取参数
GoRoute(
  path: 'details/:id',
  builder: (context, state) {
    final id = state.pathParameters['id']; // 获取路径参数
    final name = state.uri.queryParameters['name']; // 获取查询参数
    return DetailsScreen(id: id, name: name);
  },
)
```

⚠️ **注意**：`context.go()` 会替换当前路由栈，而 `context.push()` 会在栈顶压入新页面。

### 2.3 ShellRoute 嵌套导航

对于带有底部导航栏（BottomNavigationBar）的应用，`ShellRoute` 是最佳方案：

```dart
final _router = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) {
        return Scaffold(
          body: child, // 这里的 child 就是子路由对应的页面
          bottomNavigationBar: BottomNavigationBar(
            items: const [
              BottomNavigationBarItem(icon: Icon(Icons.home), label: '首页'),
              BottomNavigationBarItem(icon: Icon(Icons.person), label: '我的'),
            ],
            onTap: (index) {
              if (index == 0) context.go('/');
              else context.go('/profile');
            },
          ),
        );
      },
      routes: [
        GoRoute(path: '/', builder: (context, state) => const HomeScreen()),
        GoRoute(path: '/profile', builder: (context, state) => const ProfileScreen()),
      ],
    ),
  ],
);
```

<!-- IMAGE_PLACEHOLDER: ShellRoute 嵌套导航运行效果 -->
<!-- 类型: 鸿蒙设备截图 -->
<!-- 内容: 展示带有状态保持的底部导航栏效果 -->

---

## 三、OpenHarmony 平台适配建议

### 3.1 物理返回键处理

在 OpenHarmony 设备上，物理返回键（或侧滑返回手势）默认由 Flutter 引擎接管。由于 `go_router` 深度集成了 Flutter 的 `Router` API，回退逻辑通常会自动生效。

如果你需要拦截返回键，建议使用 `PopScope`：

```dart
PopScope(
  canPop: false,
  onPopInvoked: (didPop) async {
    if (didPop) return;
    // 自定义返回逻辑
    final shouldPop = await _showExitDialog(context);
    if (shouldPop) {
      context.pop();
    }
  },
  child: const HomeScreen(),
)
```

### 3.2 响应式布局自适应

OpenHarmony 设备涵盖了手机、平板和折叠屏。结合 `go_router` 的响应式设计至关重要：

```dart
final isTablet = MediaQuery.of(context).size.width > 600;

// 在 Tablet 上可能希望使用左右分栏，而在手机上使用单页导航
```

💡 **进阶技巧**：可以利用 `redirect` 属性在跳转前根据屏幕尺寸重定向到不同的布局路由。

---

## 四、完整示例代码

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

void main() => runApp(const RouterApp());

final GoRouter _router = GoRouter(
  routes: <RouteBase>[
    GoRoute(
      path: '/',
      builder: (BuildContext context, GoRouterState state) {
        return const HomeScreen();
      },
      routes: <RouteBase>[
        GoRoute(
          path: 'details/:msg',
          builder: (BuildContext context, GoRouterState state) {
            return DetailsScreen(msg: state.pathParameters['msg'] ?? '');
          },
        ),
      ],
    ),
  ],
);

class RouterApp extends StatelessWidget {
  const RouterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: _router,
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.blue),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 路由首页')),
      body: Center(
        child: ElevatedButton(
          onPressed: () => context.go('/details/来自鸿蒙的问候'),
          child: const Text('跳转到详情页'),
        ),
      ),
    );
  }
}

class DetailsScreen extends StatelessWidget {
  final String msg;
  const DetailsScreen({super.key, required this.msg});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('详情页')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('参数内容: $msg'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => context.pop(),
              child: const Text('返回'),
            ),
          ],
        ),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 完整示例运行截图（鸿蒙设备） -->
<!-- 类型: 截图 -->
<!-- 内容: 展示首页跳转至详情页并携带参数的流程 -->

## 五、总结

`go_router` 在 Flutter for OpenHarmony 中提供了强大且稳定的路由管理能力。通过路径驱动的模式，不仅提升了代码的可维护性，也为未来支持多端、深层链接打下了坚实基础。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/flutter-ohos-go-router](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/flutter-ohos-go-router)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
