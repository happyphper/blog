# Flutter for OpenHarmony 实战之基础组件：第四十八篇 Shared Preferences — 实现轻量级数据的本地持久化

## 前言

在移动应用开发中，并非所有数据都需要存储在沉重的数据库（如 SQLite）中。对于用户的登录状态、应用的主题配置、甚至是上次阅读的位置，我们更倾向于使用一种简单、快速且易于维护的“键值对（Key-Value）”存储方案。

在 **Flutter for OpenHarmony** 平台上，原生系统提供了 `Preferences` 接口。而在 Flutter 侧，我们通过经过适配的 `shared_preferences` 插件，可以跨平台地实现这些轻量级数据的持久化。本文将教大家如何在鸿蒙端配置并使用 Shared Preferences 记录应用状态。

---

## 一、为什么需要 Shared Preferences？

其核心价值在于“简单”：
- **存**：`prefs.setString('username', 'happyphper')`
- **取**：`prefs.getString('username')`

在鸿蒙系统底层，这些数据被序列化为 XML 或 JSON 文件存储在应用的私有目录下，即使手机重启或应用关闭，数据依然存在。

---

## 二、OpenHarmony 平台适配配置

由于鸿蒙系统的插件生态与原生 Android/iOS 不同，我们需要引入专门适配过的版本。

### 2.1 配置 shared_preferences
在项目的 `pubspec.yaml` 中进行如下配置，直接引用官方适配仓：

```yaml
dependencies:
  shared_preferences:
    git:
      url: "https://gitcode.com/openharmony-tpc/flutter_packages.git"
      path: "packages/shared_preferences/shared_preferences"
```

运行 `flutter pub get` 后，系统会自动完成原生能力的注入。

### 2.2 扩展知识：如何引用其他鸿蒙适配库
不仅是 `shared_preferences`，绝大多数官方维护的插件（如 `path_provider`, `url_launcher` 等）都已经由 **OpenHarmony TPC** 进行了适配。

如果您需要引用其他的官方库适配版，格式如下：

```yaml
dependencies:
  path_provider:
    git:
      url: "https://gitcode.com/openharmony-tpc/flutter_packages.git"
      path: "packages/path_provider/path_provider"
```

如果您正在开发原生插件，需要用到 **Pigeon** 通信工具，引用方式为：

```yaml
dev_dependencies:
  pigeon:
    git:
      url: "https://gitcode.com/openharmony-tpc/flutter_packages.git"
      path: "packages/pigeon"
```

通过这种统一的 `git + path` 引用方式，您可以确保插件在鸿蒙平台上能够正常调用底层能力，实现真正的“一份代码，全端运行”。

---

## 三、实战：保存用户登录信息

我们将实现一个简单的逻辑：保存用户的登录名，并在下次进入应用时自动填入。

### 3.1 实例化与保存数据
```dart
Future<void> _saveLoginInfo(String name) async {
  // 1. 获取实例
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  
  // 2. 写入数据 (异步过程)
  await prefs.setString('user_nickname', name);
  await prefs.setBool('is_logged_in', true);
  await prefs.setInt('last_login_time', DateTime.now().millisecondsSinceEpoch);
}
```

### 3.2 读取数据
```dart
Future<String?> _loadNickName() async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  // 读取不到时返回 null，可配合 ?? 提供默认值
  return prefs.getString('user_nickname') ?? '游客用户';
}
```

<!-- IMAGE_PLACEHOLDER: 应用重启后自动加载保存好的用户昵称截图（鸿蒙设备） -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 数据安全与目录结构
鸿蒙系统对文件沙箱（Sandbox）管理非常严格。

✅ **相关知识**：
`shared_preferences` 在鸿蒙端会将数据保存在应用沙箱内的 `preferences` 目录下。这意味着开发者不需要申请外部存储权限即可进行读写。但要注意，如果清除应用缓存，这些轻量级设置也会被一并擦除。

### 4.2 异步同步化技巧
`getInstance()` 是一个异步方法，如果你在每个 Widget 的 `build` 里都去 await 它，会造成明显的 UI 阻塞。

💡 **调优方案**：
推荐在 `main()` 函数中预先初始化，或者使用单例模式封装一个全局的存储管理类。

```dart
late SharedPreferences globalPrefs;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  globalPrefs = await SharedPreferences.getInstance();
  runApp(const MyApp());
}
```

### 4.3 处理高频写入
虽然 Shared Preferences 非常方便，但它不适合作为日志系统。

⚠️ **注意事项**：
每次 `set` 操作在鸿蒙端最终都会映射到文件系统的持久化。建议将数据先在内存中缓存（List/Map），只有在关键节点（如用户点击保存、退出页面）时，再调用 `setStringList` 等方法进行批量写回。

<!-- IMAGE_PLACEHOLDER: 设置中心中“保存设置”交互动效及其在鸿蒙端的持久化反馈 -->
<!-- 类型: 截图 -->
<!-- 设备: 模拟器 -->

---

## 五、完整示例代码

以下代码演示了一个包含“计数器持久化”和“主题模式保存”功能的综合示例。

```dart
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() => runApp(const MaterialApp(home: StorageDemoPage()));

class StorageDemoPage extends StatefulWidget {
  const StorageDemoPage({super.key});

  @override
  State<StorageDemoPage> createState() => _StorageDemoPageState();
}

class _StorageDemoPageState extends State<StorageDemoPage> {
  int _counter = 0;
  bool _darkMode = false;

  @override
  void initState() {
    super.initState();
    _loadInitialData();
  }

  // 从本地加载已有的值
  Future<void> _loadInitialData() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _counter = prefs.getInt('app_counter') ?? 0;
      _darkMode = prefs.getBool('is_dark_mode') ?? false;
    });
  }

  // 写入新值
  Future<void> _updateData(int val, bool isDark) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('app_counter', val);
    await prefs.setBool('is_dark_mode', isDark);
    setState(() {
      _counter = val;
      _darkMode = isDark;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _darkMode ? Colors.black87 : Colors.white,
      appBar: AppBar(title: const Text('OHOS 数据持久化实战')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainValue.center,
          children: [
            Text("您已打开本应用 $_counter 次", style: TextStyle(
              fontSize: 20, 
              color: _darkMode ? Colors.white : Colors.black
            )),
            const SizedBox(height: 30),
            SwitchListTile(
              title: Text("深色模式", style: TextStyle(color: _darkMode ? Colors.white : Colors.black)),
              value: _darkMode,
              onChanged: (v) => _updateData(_counter, v),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => _updateData(_counter + 1, _darkMode),
              child: const Text("增加计数并保存"),
            ),
            TextButton(
              onPressed: () async {
                final prefs = await SharedPreferences.getInstance();
                await prefs.clear(); // 演示清理全部数据
                _loadInitialData();
              },
              child: const Text("重置本地所有数据", style: TextStyle(color: Colors.red)),
            )
          ],
        ),
      ),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的日常开发中，`shared_preferences` 是解决数据“记忆力”问题的最快方案。

1.  **极简存储**：适合用户偏好设置、简单的状态标记。
2.  **安全性建议**：对于极其敏感的信息（如支付密码、Token），建议配合 `flutter_secure_storage` 等专门的加密库。
3.  **鸿蒙赋能**：在鸿蒙端，利用其原生的 Preferences 映射机制，能确保即便在系统进行内存清理时，你的关键配置依然稳如磐石。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

