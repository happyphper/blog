![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战：开发环境搭建与基础入门指南

> **摘要**：本文详细介绍 Flutter for OpenHarmony 的开发环境搭建流程，涵盖 DevEco Studio 安装、Flutter SDK 配置、项目创建与运行，并通过 Hello World 示例帮助开发者快速入门鸿蒙跨平台开发。

## 前言

Flutter 是 Google 推出的一款免费、开源的跨平台 UI 框架，其核心目标是帮助开发者通过一套代码库，高效构建在移动设备（iOS/Android）、桌面端（Windows/macOS/Linux）、Web 端乃至嵌入式设备上都能呈现原生级体验的高性能应用。

随着 **Flutter for OpenHarmony** 的推出，开发者现在可以使用 Flutter 为鸿蒙设备开发应用，实现真正的"一次开发，多端运行"。

**本文你将学到**：
- DevEco Studio 开发环境的安装与配置
- Flutter for OpenHarmony SDK 的获取与设置
- 创建并运行第一个 Flutter 鸿蒙应用
- Dart 语言基础语法入门
- Flutter Widget 核心概念理解

---

## 一、开发环境概述

### 1.1 技术栈介绍

Flutter for OpenHarmony 的开发涉及以下核心技术：

| 技术 | 说明 |
|-----|------|
| **Dart** | Flutter 的编程语言，支持 AOT 和 JIT 编译 |
| **Flutter Framework** | UI 框架，提供丰富的 Widget 组件库 |
| **OpenHarmony** | 华为开源的分布式操作系统 |
| **DevEco Studio** | 鸿蒙应用开发 IDE |

### 1.2 环境要求

在开始之前，请确保你的开发机器满足以下要求：

| 项目 | 最低要求 | 推荐配置 |
|-----|---------|---------|
| **操作系统** | Windows 10 64-bit / macOS 10.15+ | Windows 11 / macOS 13+ |
| **内存** | 8 GB RAM | 16 GB RAM |
| **磁盘空间** | 20 GB 可用空间 | 50 GB SSD |
| **处理器** | Intel i5 或同等 | Intel i7 / Apple M1+ |

![Flutter for OpenHarmony 开发环境架构图](./images/flutter_ohos_architecture.png)

💡 **提示**：建议使用 SSD 硬盘，可显著提升编译速度和开发体验。

---

## 二、DevEco Studio 安装与配置

### 2.1 下载 DevEco Studio

DevEco Studio 是华为官方提供的鸿蒙应用开发 IDE，基于 IntelliJ IDEA 开发。

**下载地址**：
- 官方下载：[DevEco Studio 下载页面](https://developer.huawei.com/consumer/cn/download/deveco-studio)

```bash
# macOS 用户也可以使用 Homebrew 安装（如果支持）
# brew install --cask deveco-studio

# 或直接下载 DMG 安装包
# 下载完成后双击安装即可
```

### 2.2 配置 OpenHarmony SDK

安装完成后，需要配置 OpenHarmony SDK：

1. 打开 DevEco Studio
2. 进入 **File → Settings → OpenHarmony SDK**
3. 点击 **Download** 下载所需的 SDK 版本

```yaml
# SDK 配置路径示例
# Windows
SDK_PATH: C:\Users\{username}\AppData\Local\OpenHarmony\Sdk

# macOS
SDK_PATH: /Users/{username}/Library/OpenHarmony/Sdk

# 环境变量配置
OHOS_SDK_HOME: {SDK_PATH}
PATH: $PATH:$OHOS_SDK_HOME/toolchains
```

### 2.3 验证安装

打开终端，执行以下命令验证安装：

```bash
# 检查 hdc 工具是否可用（类似 Android 的 adb）
hdc version

# 预期输出
# OpenHarmony HDC version: x.x.x
```

<!-- IMAGE_PLACEHOLDER: DevEco Studio 安装完成截图 -->
<!-- 类型: 软件截图 -->
<!-- 内容: 展示 DevEco Studio 主界面和 SDK 配置页面 -->

⚠️ **注意**：首次启动 DevEco Studio 时，会自动下载必要的组件，请确保网络畅通。

---

## 三、Flutter for OpenHarmony SDK 配置

### 3.1 获取 Flutter SDK

Flutter for OpenHarmony 需要使用特定的 Flutter SDK 版本：

```bash
# 克隆 Flutter for OpenHarmony 仓库
git clone https://atomgit.com/aspect-aspect/aspect.git flutter_ohos

# 进入目录
cd flutter_ohos

# 切换到稳定分支
git checkout stable

# 配置环境变量
export FLUTTER_HOME=$(pwd)
export PATH=$PATH:$FLUTTER_HOME/bin
```

### 3.2 配置 Flutter 环境

将以下配置添加到你的 shell 配置文件中：

```bash
# ~/.bashrc 或 ~/.zshrc

# Flutter for OpenHarmony 环境变量
export FLUTTER_HOME=/path/to/flutter_ohos
export PATH=$PATH:$FLUTTER_HOME/bin

# Dart SDK（Flutter 自带）
export PATH=$PATH:$FLUTTER_HOME/bin/cache/dart-sdk/bin

# OpenHarmony SDK
export OHOS_SDK_HOME=/path/to/OpenHarmony/Sdk
export PATH=$PATH:$OHOS_SDK_HOME/toolchains

# 国内镜像加速（可选）
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
```

应用配置：

```bash
# 重新加载配置
source ~/.zshrc  # 或 source ~/.bashrc

# 验证 Flutter 安装
flutter doctor

# 预期输出应包含 OpenHarmony 支持
# [✓] Flutter (Channel stable, x.x.x)
# [✓] OpenHarmony toolchain
```

### 3.3 运行 Flutter Doctor

`flutter doctor` 是诊断开发环境的重要工具：

```bash
flutter doctor -v

# 输出示例
# [✓] Flutter (Channel stable, 3.x.x, on macOS 13.x)
# [✓] OpenHarmony toolchain - develop for OpenHarmony devices
#     • OHOS_SDK_HOME = /Users/xxx/Library/OpenHarmony/Sdk
#     • DevEco Studio (version 4.x)
# [✓] Connected device (1 available)
#     • OHOS Device (mobile) • xxx • ohos-arm64 • OpenHarmony x.x
```

<!-- IMAGE_PLACEHOLDER: flutter doctor 输出截图 -->
<!-- 类型: 终端截图 -->
<!-- 内容: 展示 flutter doctor 命令的成功输出，显示 OpenHarmony 支持 -->

---

## 四、创建第一个 Flutter 鸿蒙项目

### 4.1 创建项目

使用 `flutter create` 命令创建新项目：

```bash
# 创建支持 OpenHarmony 的 Flutter 项目
flutter create --platforms ohos my_first_app

# 进入项目目录
cd my_first_app

# 查看项目结构
tree -L 2
```

项目结构如下：

```
my_first_app/
├── lib/                    # Dart 源代码目录
│   └── main.dart          # 应用入口文件
├── ohos/                   # OpenHarmony 平台特定代码
│   ├── entry/             # 应用入口模块
│   └── oh-package.json5   # 鸿蒙包配置
├── pubspec.yaml           # Flutter 项目配置文件
└── README.md
```

### 4.2 编写 Hello World

打开 `lib/main.dart`，替换为以下代码：

```dart
import 'package:flutter/material.dart';

/// 应用入口函数
void main() {
  // 运行 Flutter 应用
  runApp(const MyApp());
}

/// 根 Widget - 应用程序的顶层组件
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter for OpenHarmony',  // 应用标题
      debugShowCheckedModeBanner: false, // 隐藏调试标签
      theme: ThemeData(
        // 主题配置
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true, // 使用 Material 3 设计
      ),
      home: const HomePage(), // 首页
    );
  }
}

/// 首页 Widget
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 应用栏
      appBar: AppBar(
        title: const Text('我的第一个鸿蒙应用'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      // 页面主体
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // 欢迎图标
            const Icon(
              Icons.flutter_dash,
              size: 100,
              color: Colors.blue,
            ),
            const SizedBox(height: 24),
            // 欢迎文本
            Text(
              'Hello, OpenHarmony!',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 8),
            Text(
              '欢迎来到 Flutter 鸿蒙开发世界',
              style: Theme.of(context).textTheme.bodyLarge,
            ),
          ],
        ),
      ),
      // 悬浮按钮
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // 显示提示
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Flutter + OpenHarmony = ❤️')),
          );
        },
        child: const Icon(Icons.favorite),
      ),
    );
  }
}
```

### 4.3 运行到鸿蒙设备

确保鸿蒙设备已连接并开启开发者模式，然后运行：

```bash
# 查看已连接的设备
flutter devices

# 运行到鸿蒙设备
flutter run -d ohos

# 或使用热重载模式开发
flutter run -d ohos --hot
```

<!-- IMAGE_PLACEHOLDER: Hello World 运行效果截图 -->
<!-- 类型: 鸿蒙设备截图（必需） -->
<!-- 设备: OpenHarmony 手机/模拟器 -->
<!-- 内容: 展示 Hello OpenHarmony 应用在鸿蒙设备上的运行效果 -->

✅ **恭喜**：如果你看到了应用界面，说明环境配置成功！

---

## 五、Dart 语言基础入门

### 5.1 变量与类型

Dart 是强类型语言，但支持类型推断：

```dart
// 变量声明
var name = '张三';           // 类型推断为 String
String title = 'Flutter';   // 显式类型声明
final age = 25;             // 运行时常量，只能赋值一次
const pi = 3.14159;         // 编译时常量

// 基础类型
int count = 42;             // 整数
double price = 99.9;        // 浮点数
bool isActive = true;       // 布尔值
String message = '你好';     // 字符串

// 空安全（Null Safety）
String? nullableStr;        // 可空类型，可以为 null
String nonNullStr = 'Hi';   // 非空类型，不能为 null

// 集合类型
List<int> numbers = [1, 2, 3];         // 列表
Set<String> tags = {'flutter', 'dart'}; // 集合（无重复）
Map<String, int> scores = {'math': 90}; // 映射
```

### 5.2 函数与类

```dart
// 普通函数
int add(int a, int b) {
  return a + b;
}

// 箭头函数（单表达式）
int multiply(int a, int b) => a * b;

// 可选参数
void greet(String name, {String? title, int age = 18}) {
  print('Hello, ${title ?? ''} $name, age: $age');
}

// 类定义
class Person {
  // 属性
  final String name;
  int age;
  
  // 构造函数
  Person(this.name, this.age);
  
  // 命名构造函数
  Person.guest() : name = 'Guest', age = 0;
  
  // 方法
  void introduce() {
    print('我是 $name，今年 $age 岁');
  }
  
  // Getter
  bool get isAdult => age >= 18;
}

// 使用类
void main() {
  var person = Person('小明', 20);
  person.introduce();  // 输出: 我是 小明，今年 20 岁
  print(person.isAdult);  // 输出: true
}
```

### 5.3 异步编程

Dart 使用 `async/await` 处理异步操作：

```dart
// 异步函数：使用 async 关键字
Future<String> fetchUserData() async {
  // 模拟网络请求延迟
  await Future.delayed(const Duration(seconds: 2));
  return '{"name": "张三", "age": 25}';
}

// 调用异步函数
void loadData() async {
  print('开始加载...');
  
  try {
    // await 等待异步结果
    String data = await fetchUserData();
    print('加载成功: $data');
  } catch (e) {
    print('加载失败: $e');
  }
}

// Stream（数据流）处理
Stream<int> countStream(int max) async* {
  for (int i = 1; i <= max; i++) {
    await Future.delayed(const Duration(seconds: 1));
    yield i;  // 逐个产出数据
  }
}
```

### 5.4 控制流与运算符

Dart 提供了丰富的控制流语句和运算符，帮助你编写逻辑清晰的代码：

```dart
// 条件语句
void checkAge(int age) {
  if (age < 18) {
    print('未成年');
  } else if (age < 60) {
    print('成年人');
  } else {
    print('老年人');
  }
}

// switch 语句（Dart 3.0 支持模式匹配）
String getGrade(int score) {
  return switch (score) {
    >= 90 => '优秀',
    >= 80 => '良好',
    >= 60 => '及格',
    _ => '不及格',
  };
}

// 循环语句
void loopExamples() {
  // for 循环
  for (int i = 0; i < 5; i++) {
    print('索引: $i');
  }
  
  // for-in 遍历
  var fruits = ['苹果', '香蕉', '橙子'];
  for (var fruit in fruits) {
    print('水果: $fruit');
  }
  
  // while 循环
  int count = 0;
  while (count < 3) {
    print('计数: $count');
    count++;
  }
  
  // forEach 高阶函数
  fruits.forEach((fruit) => print('喜欢: $fruit'));
}

// 空安全运算符
void nullSafetyExamples() {
  String? name;  // 可空变量
  
  // ?? 空合并运算符：如果为 null，使用默认值
  String displayName = name ?? '匿名用户';
  
  // ?. 可空调用：如果为 null，不执行调用
  int? length = name?.length;
  
  // ! 非空断言：告诉编译器变量一定不为 null（谨慎使用）
  // String forcedName = name!;  // 如果为 null 会抛出异常
  
  // ??= 空值赋值：仅当变量为 null 时赋值
  name ??= '默认名称';
}

// 级联运算符（..）
class Builder {
  String? title;
  String? content;
  int? priority;
  
  void build() {
    print('构建: $title - $content (优先级: $priority)');
  }
}

void cascadeExample() {
  // 使用级联运算符链式调用
  Builder()
    ..title = '任务标题'
    ..content = '任务内容'
    ..priority = 1
    ..build();
}
```

### 5.5 集合操作

Dart 提供了强大的集合操作方法，类似于其他现代编程语言的函数式编程特性：

```dart
void collectionOperations() {
  var numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  
  // map - 转换每个元素
  var doubled = numbers.map((n) => n * 2).toList();
  print('翻倍: $doubled');  // [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
  
  // where - 过滤元素
  var evens = numbers.where((n) => n % 2 == 0).toList();
  print('偶数: $evens');  // [2, 4, 6, 8, 10]
  
  // reduce - 归约为单一值
  var sum = numbers.reduce((a, b) => a + b);
  print('总和: $sum');  // 55
  
  // fold - 带初始值的归约
  var product = numbers.fold(1, (a, b) => a * b);
  print('乘积: $product');
  
  // any / every - 逻辑判断
  bool hasEven = numbers.any((n) => n % 2 == 0);
  bool allPositive = numbers.every((n) => n > 0);
  print('包含偶数: $hasEven, 全为正数: $allPositive');
  
  // take / skip - 截取元素
  var first3 = numbers.take(3).toList();
  var after3 = numbers.skip(3).toList();
  print('前3个: $first3, 跳过3个: $after3');
  
  // 展开运算符（Spread Operator）
  var list1 = [1, 2, 3];
  var list2 = [4, 5, 6];
  var combined = [...list1, ...list2];
  print('合并: $combined');  // [1, 2, 3, 4, 5, 6]
  
  // 集合 if 和集合 for
  bool showExtra = true;
  var menu = [
    '首页',
    '搜索',
    if (showExtra) '设置',  // 条件添加
    for (var i in [1, 2, 3]) '项目$i',  // 循环添加
  ];
  print('菜单: $menu');
}

---

## 六、Flutter Widget 核心概念

### 6.1 Widget 是什么

在 Flutter 中，**一切皆 Widget**。Widget 是构建 UI 的基本单元：

```dart
// Widget 的两种类型
// 1. StatelessWidget - 无状态组件（不可变）
class MyLabel extends StatelessWidget {
  final String text;
  
  const MyLabel({super.key, required this.text});
  
  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: const TextStyle(fontSize: 16),
    );
  }
}

// 2. StatefulWidget - 有状态组件（可变）
class Counter extends StatefulWidget {
  const Counter({super.key});
  
  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;  // 可变状态
  
  void _increment() {
    setState(() {  // 调用 setState 触发重建
      _count++;
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('计数: $_count'),
        ElevatedButton(
          onPressed: _increment,
          child: const Text('增加'),
        ),
      ],
    );
  }
}
```

### 6.2 常用布局 Widget

```dart
// Column - 垂直布局
Column(
  mainAxisAlignment: MainAxisAlignment.center,  // 主轴居中
  crossAxisAlignment: CrossAxisAlignment.start, // 交叉轴靠左
  children: [
    Text('第一行'),
    Text('第二行'),
    Text('第三行'),
  ],
)

// Row - 水平布局
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly, // 均匀分布
  children: [
    Icon(Icons.home),
    Icon(Icons.search),
    Icon(Icons.person),
  ],
)

// Container - 容器（装饰、尺寸、边距）
Container(
  width: 200,
  height: 100,
  margin: const EdgeInsets.all(16),      // 外边距
  padding: const EdgeInsets.all(12),     // 内边距
  decoration: BoxDecoration(
    color: Colors.blue,                   // 背景色
    borderRadius: BorderRadius.circular(8), // 圆角
    boxShadow: [                          // 阴影
      BoxShadow(
        color: Colors.black26,
        blurRadius: 4,
        offset: Offset(0, 2),
      ),
    ],
  ),
  child: Text('Hello'),
)
```

### 6.3 OpenHarmony 适配注意事项

在 OpenHarmony 平台开发时，需要注意以下几点：

```dart
// 1. 使用 SafeArea 处理刘海屏
SafeArea(
  child: Scaffold(
    body: YourContent(),
  ),
)

// 2. 响应式布局适配不同分辨率
LayoutBuilder(
  builder: (context, constraints) {
    // 根据屏幕宽度调整布局
    if (constraints.maxWidth > 600) {
      return WideLayout();  // 平板/大屏布局
    } else {
      return NarrowLayout(); // 手机布局
    }
  },
)

// 3. 使用 MediaQuery 获取屏幕信息
final screenWidth = MediaQuery.of(context).size.width;
final screenHeight = MediaQuery.of(context).size.height;
final safeAreaTop = MediaQuery.of(context).padding.top;
```

### 6.4 输入与交互组件

Flutter 提供了丰富的输入和交互组件，用于构建用户界面：

```dart
// TextField - 文本输入框
class LoginForm extends StatefulWidget {
  const LoginForm({super.key});
  
  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  // 文本控制器：用于获取和设置输入内容
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;  // 密码可见性
  
  @override
  void dispose() {
    // 释放控制器资源
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
  
  void _handleLogin() {
    final username = _usernameController.text;
    final password = _passwordController.text;
    
    if (username.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('请填写用户名和密码')),
      );
      return;
    }
    
    // 执行登录逻辑
    print('登录: $username');
  }
  
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // 用户名输入框
          TextField(
            controller: _usernameController,
            decoration: const InputDecoration(
              labelText: '用户名',
              hintText: '请输入用户名',
              prefixIcon: Icon(Icons.person),
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          
          // 密码输入框
          TextField(
            controller: _passwordController,
            obscureText: _obscurePassword,  // 密码模式
            decoration: InputDecoration(
              labelText: '密码',
              hintText: '请输入密码',
              prefixIcon: const Icon(Icons.lock),
              border: const OutlineInputBorder(),
              // 密码可见性切换按钮
              suffixIcon: IconButton(
                icon: Icon(
                  _obscurePassword ? Icons.visibility_off : Icons.visibility,
                ),
                onPressed: () {
                  setState(() {
                    _obscurePassword = !_obscurePassword;
                  });
                },
              ),
            ),
          ),
          const SizedBox(height: 24),
          
          // 登录按钮
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _handleLogin,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('登录', style: TextStyle(fontSize: 16)),
            ),
          ),
        ],
      ),
    );
  }
}
```

### 6.5 列表与滚动组件

处理长列表和滚动内容是移动应用开发的常见需求：

```dart
// ListView.builder - 高效渲染长列表
class TodoList extends StatelessWidget {
  // 模拟数据
  final List<Map<String, dynamic>> todos = [
    {'title': '学习 Flutter', 'done': true},
    {'title': '完成项目需求', 'done': false},
    {'title': '代码审查', 'done': false},
    {'title': '编写单元测试', 'done': true},
    {'title': '部署到鸿蒙设备', 'done': false},
  ];
  
  TodoList({super.key});
  
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: todos.length,
      itemBuilder: (context, index) {
        final todo = todos[index];
        return Card(
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: ListTile(
            leading: Checkbox(
              value: todo['done'],
              onChanged: (value) {
                // 处理勾选状态变化
              },
            ),
            title: Text(
              todo['title'],
              style: TextStyle(
                decoration: todo['done'] 
                    ? TextDecoration.lineThrough 
                    : TextDecoration.none,
              ),
            ),
            trailing: IconButton(
              icon: const Icon(Icons.delete_outline),
              onPressed: () {
                // 删除待办事项
              },
            ),
          ),
        );
      },
    );
  }
}

// GridView - 网格布局
GridView.builder(
  padding: const EdgeInsets.all(16),
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 2,        // 每行 2 个
    crossAxisSpacing: 16,     // 水平间距
    mainAxisSpacing: 16,      // 垂直间距
    childAspectRatio: 1.0,    // 宽高比
  ),
  itemCount: 10,
  itemBuilder: (context, index) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.primaries[index % Colors.primaries.length],
        borderRadius: BorderRadius.circular(12),
      ),
      child: Center(
        child: Text(
          '项目 ${index + 1}',
          style: const TextStyle(color: Colors.white, fontSize: 18),
        ),
      ),
    );
  },
)
```

### 6.6 导航与路由

Flutter 使用 Navigator 管理页面导航：

```dart
// 基础导航
class NavigationExample extends StatelessWidget {
  const NavigationExample({super.key});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('首页')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            // 跳转到详情页
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => const DetailPage(id: 123),
              ),
            );
          },
          child: const Text('查看详情'),
        ),
      ),
    );
  }
}

class DetailPage extends StatelessWidget {
  final int id;
  
  const DetailPage({super.key, required this.id});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('详情 #$id'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),  // 返回上一页
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('详情页面 ID: $id', style: const TextStyle(fontSize: 24)),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // 返回并传递数据
                Navigator.pop(context, '来自详情页的数据');
              },
              child: const Text('返回并传递数据'),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## 七、项目打包与发布

### 7.1 调试构建

开发阶段使用调试构建：

```bash
# 调试运行（支持热重载）
flutter run -d ohos --debug

# 查看日志
flutter logs
```

### 7.2 发布构建

准备发布时，使用 release 构建：

```bash
# 构建 release 版本
flutter build ohos --release

# 构建产物位于
# build/ohos/outputs/default/entry-default-signed.hap
```

### 7.3 安装到设备

```bash
# 使用 hdc 安装 HAP 包
hdc install build/ohos/outputs/default/entry-default-signed.hap

# 启动应用
hdc shell aa start -a MainAbility -b com.example.my_first_app
```

<!-- IMAGE_PLACEHOLDER: 打包成功后的 HAP 文件截图 -->
<!-- 类型: 文件管理器截图 -->
<!-- 内容: 展示构建产物目录结构和 HAP 文件 -->

---

## 八、常见问题与解决方案

### 8.1 环境问题

| 问题 | 解决方案 |
|-----|---------|
| `flutter doctor` 找不到 OpenHarmony | 检查 `OHOS_SDK_HOME` 环境变量配置 |
| 设备未识别 | 确保开启开发者模式，检查 USB 连接 |
| 编译失败 | 执行 `flutter clean` 后重试 |
| 依赖下载慢 | 配置国内镜像源 |

### 8.2 开发调试技巧

```bash
# 清理构建缓存
flutter clean

# 重新获取依赖
flutter pub get

# 升级 Flutter SDK
flutter upgrade

# 查看详细错误信息
flutter run -d ohos --verbose
```

---

## 九、总结

本文介绍了 Flutter for OpenHarmony 开发环境的完整搭建流程：

- **DevEco Studio**：安装并配置 OpenHarmony SDK
- **Flutter SDK**：获取并配置 Flutter for OpenHarmony 版本
- **项目创建**：使用 `flutter create` 创建鸿蒙项目
- **运行调试**：使用 `flutter run -d ohos` 运行到设备
- **Dart 基础**：变量、函数、类、异步编程
- **Widget 概念**：StatelessWidget vs StatefulWidget

### 延伸学习

- 官方 Dart 语言文档：[Dart 语言指南](https://dart.cn/language)
- Flutter 官方文档：[Flutter 中文文档](https://flutter.cn/docs)
- OpenHarmony 开发者文档：[华为开发者联盟](https://developer.huawei.com)

### 下一步学习建议

1. 深入学习 Flutter 组件库（Container、Row、Column、Stack）
2. 掌握状态管理方案（Provider、Riverpod）
3. 学习三方库的鸿蒙化适配
4. 实战开发一个完整的小应用

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example](https://atomgit.com/dragonbady/open-harmony-example)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

