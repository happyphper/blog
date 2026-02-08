# Flutter for OpenHarmony 实战之基础组件：第二十六篇 Scaffold 中的 Drawer 与 EndDrawer — 完善的侧边栏菜单

## 前言

侧边栏抽屉菜单（Drawer）是移动应用中最为经典的设计模式之一。它能巧妙地将低频率操作（如个人资料、系统设置、切换账号等）隐藏在屏幕之外，保持主页面的简洁与专注。

在 **Flutter for OpenHarmony** 平台上，`Scaffold` 组件提供的 `Drawer` 和 `EndDrawer` 能够通过简单的左右滑动或点击图标唤起，且能自动处理系统的沉浸式导航栏遮挡问题。本文将深入讲解如何在鸿蒙应用中定制侧边栏，从基础结构到高阶手势控制。

---

## 一、Drawer 的基础结构

抽屉菜单通常依附于 `Scaffold`，通过左侧滑入（Drawer）或右侧滑入（EndDrawer）展现。

### 1.1 核心组件关系
- `Scaffold.drawer`: 定义左侧抽屉。
- `Scaffold.endDrawer`: 定义右侧抽屉。
- `DrawerHeader`: 抽屉顶部的基本展示区域。

### 1.2 基础代码实现
```dart
Scaffold(
  appBar: AppBar(title: Text("OHOS 侧边栏示例")),
  // 定义左侧抽屉
  drawer: Drawer(
    child: ListView(
      padding: EdgeInsets.zero, // 消除顶部状态栏留白
      children: [
        const DrawerHeader(
          decoration: BoxDecoration(color: Colors.blue),
          child: Text('我的应用', style: TextStyle(color: Colors.white, fontSize: 24)),
        ),
        ListTile(
          title: const Text('首页'),
          onTap: () => Navigator.pop(context), // 点击后自动关闭抽屉
        ),
      ],
    ),
  ),
  body: Center(child: Text("向右滑动开启抽屉")),
)
```

<!-- IMAGE_PLACEHOLDER: 基础 Drawer 在鸿蒙手机上的展开效果 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 二、高级定制：打造精美的用户中心

默认的 `DrawerHeader` 较为简单，在实际的鸿蒙应用中，我们常需要加入头像、背景图和统计数据。

### 2.1 使用 UserAccountsDrawerHeader
这是 Flutter 专门为用户信息展示设计的快捷头组件。

```dart
Drawer(
  child: Column(
    children: [
      UserAccountsDrawerHeader(
        currentAccountPicture: CircleAvatar(
          backgroundImage: AssetImage("assets/avatar.png"),
        ),
        accountName: Text("HarmonyOS 开发者"),
        accountEmail: Text("developer@harmony.os"),
        decoration: BoxDecoration(
          image: DecorationImage(
            image: NetworkImage("https://example.com/bg.jpg"),
            fit: BoxFit.cover,
          ),
        ),
      ),
      Expanded(
        child: ListView(
          children: [
            _buildDrawerItem(Icons.settings, "系统设置"),
            _buildDrawerItem(Icons.nightlight_round, "深色模式"),
            const Divider(),
            _buildDrawerItem(Icons.logout, "退出登录", isDanger: true),
          ],
        ),
      ),
    ],
  ),
)
```

### 2.2 EndDrawer：右侧辅助抽屉
在某些特殊的业务场景（如详情页的筛选、多维参数调节）中，右侧抽屉 `EndDrawer` 非常实用。

```dart
Scaffold(
  endDrawer: Drawer(
    width: MediaQuery.of(context).size.width * 0.8, // 控制抽屉宽度
    child: Center(child: Text("右侧筛选菜单")),
  ),
)
```

<!-- IMAGE_PLACEHOLDER: EndDrawer 在鸿蒙设备上的运行截图 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、交互进阶：手势与编程控制

### 3.1 禁用侧滑手势
如果不希望用户通过边缘滑动开启抽屉（例如在带有横向滑动的地图页面），可以将其禁用。

```dart
Scaffold(
  drawer: MyDrawer(),
  // 禁用滑动开启，只能通过按钮开启
  drawerEnableOpenDragGesture: false,
  endDrawerEnableOpenDragGesture: false,
)
```

### 3.2 编程方式开启/关闭
有时你需要通过点击页面中间的一个按钮来开启侧边栏，而非顶部导航栏图标。

```dart
Builder(
  builder: (context) => ElevatedButton(
    onPressed: () => Scaffold.of(context).openDrawer(), // 通过 Context 开启
    child: const Text("开启更多选项"),
  ),
)
```

💡 **注意**：必须使用 `Builder` 包裹来获取 `Scaffold` 之下的 `BuildContext`。

---

## 四、OpenHarmony 平台适配建议

### 4.1 沉浸式状态栏避让
鸿蒙设备通常具有极窄的边框和刘海屏/挖孔屏，抽屉顶部内容很容易被状态栏遮挡。

✅ **推荐做法**：
在 `DrawerHeader` 中不使用 `padding: EdgeInsets.zero`，或者使用 `SafeArea` 包裹抽屉内部的头部内容。

```dart
Drawer(
  child: SafeArea( // 确保头像不被鸿蒙顶部的挖孔挡住
    top: false, // 如果 ListView 处理了 padding，这里可以灵活调整
    child: ... 
  ),
)
```

### 4.2 大屏与平板适配
在大屏鸿蒙设备（如 MatePad）上，传统的覆盖式抽屉会遮挡大部分内容，用户体验欠佳。

✅ **优化建议**：
当检测到屏幕宽度大于 600px 时，考虑放弃 `Drawer`，转而使用水平排列的 `NavigationRail`（导航侧栏），或者将抽屉设为持久显示的 Permanent 模式。

```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 700) {
      return Row(child: [Sidebar(), Expanded(child: MainContent())]);
    } else {
      return Scaffold(drawer: MobileDrawer(), body: MainContent());
    }
  }
)
```

### 4.3 触控动效适配
在侧滑唤起抽屉时，鸿蒙设备会提供非常线性的物理反馈。确保你的抽屉内没有过于沉重的 Widget 渲染，否则侧滑过程会出现掉帧。

<!-- IMAGE_PLACEHOLDER: 抽屉菜单在鸿蒙平板的分屏模式下展示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 五、完整示例代码

以下提供一个包含丰富个人中心头部的左侧抽屉完整示例。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: DrawerDemo()));

class DrawerDemo extends StatelessWidget {
  const DrawerDemo({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('OHOS 侧边栏实战'),
        backgroundColor: Colors.blue[800],
        foregroundColor: Colors.white,
      ),
      // 核心配置：左侧抽屉
      drawer: _buildLeftDrawer(context),
      body: Center(
        child: Column(
          mainAxisAlignment: MainValue.center,
          children: [
            const Icon(Icons.swipe_right, size: 64, color: Colors.grey),
            const SizedBox(height: 20),
            const Text("从屏幕左侧向右滑动"),
            const SizedBox(height: 40),
            Builder(
              builder: (ctx) => ElevatedButton(
                onPressed: () => Scaffold.of(ctx).openDrawer(),
                child: const Text("点击按钮开启"),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildLeftDrawer(BuildContext context) {
    return Drawer(
      child: Column(
        children: [
          // 1. 用户信息头部
          const UserAccountsDrawerHeader(
            accountName: Text("HappyPHPer", style: TextStyle(fontWeight: FontWeight.bold)),
            accountEmail: Text("admin@happyphper.com"),
            currentAccountPicture: CircleAvatar(
              backgroundColor: Colors.white,
              child: Icon(Icons.person, size: 40, color: Colors.blue),
            ),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.blue, Colors.blueAccent],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
          ),
          
          // 2. 菜单列表
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                _buildListTile(context, Icons.home, "首页", () {}),
                _buildListTile(context, Icons.collections, "我的收藏", () {}),
                _buildListTile(context, Icons.cloud_download, "离线下载", () {}),
                const Divider(),
                _buildListTile(context, Icons.settings, "系统设置", () {}),
                _buildListTile(context, Icons.help_outline, "帮助与反馈", () {}),
              ],
            ),
          ),
          
          // 3. 底部版权信息
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Text("Version 1.0.0 (Harmony Edition)", style: TextStyle(color: Colors.grey, fontSize: 12)),
          )
        ],
      ),
    );
  }

  Widget _buildListTile(BuildContext context, IconData icon, String title, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: Colors.blueGrey),
      title: Text(title),
      onTap: () {
        Navigator.pop(context); // 必须先关闭抽屉
        onTap();
      },
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的界面开发中，侧边栏不仅是菜单容器，更是应用品牌形象的重要展示。

1.  **Drawer**：适合存放中低频的全局功能，通过 `UserAccountsDrawerHeader` 可以极速搭建用户中心。
2.  **EndDrawer**：适合局部辅助功能，如详情筛选、参数快速调节。
3.  **大屏适配**：鸿蒙生态包含大量平板与折叠屏设备，务必根据宽度动态调整抽屉的显示模式。

通过合理定制 Header 样式并处理好状态栏避让，你就能为鸿蒙用户提供一套得心应手的功能导航系统。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

