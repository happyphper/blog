---
title: Flutter for OpenHarmony 实战：Supabase — 跨平台后端服务首选
description: 深度解析如何在 Flutter for OpenHarmony 项目中集成 Supabase，实现认证、数据库同步及实时订阅，包含 3 个核心用法及一个完整全栈待办应用实战。
tags:
  - Flutter
  - OpenHarmony
  - Supabase
  - 后端服务
  - 实时数据库
---

# Flutter for OpenHarmony 实战：Supabase — 跨平台后端服务首选

![封面](../images/flutter-ohos-supabase-3d.png)

## 前言

在构筑 **Flutter for OpenHarmony** 应用时，开发者往往面临后端选型的难题。是自建服务器处理复杂的权限与存储，还是寻找一个现成的云服务？**Supabase** 作为开源版的 Firebase，凭借其基于 PostgreSQL 的强大能力、实时数据推送以及自带的 Auth 认证系统，成为了鸿蒙跨平台应用的首选后端方案。

在鸿蒙系统上，Supabase 通过纯 Dart 的客户端库能完美运行，无需担心平台底层的兼容性问题。本文将带你从零开始，在鸿蒙设备上打通 Supabase 的全流程。

---

## 一、为什么集成 Supabase？

### 1.1 开源与透明 🔗
Supabase 完全开源，这意味着你可以随时将其私有化部署在自己的鸿蒙服务器或私有云中，数据掌控度极高。

### 1.2 PostgreSQL 的硬实力
不同于 NoSQL，Supabase 底层是标准的 PostgreSQL。这让鸿蒙开发者可以利用外键约束、视图（Views）和触发器（Triggers）来处理复杂的业务逻辑，而不仅仅是简单的键值对。

<!-- IMAGE_PLACEHOLDER: [Supabase 架构与鸿蒙应用通信逻辑图] -->
<!-- 类型: 示意图 -->
<!-- 内容: 展示鸿蒙应用通过 Supabase SDK 直接访问存储、认证和实时库的路径 -->

---

## 二、配置环境 📦

在项目中引入 Supabase 核心包。

```yaml
dependencies:
  supabase_flutter: ^2.6.0
```

在 `main.dart` 中进行初始化：

```dart
import 'package:supabase_flutter/supabase_flutter.dart';

Future<void> main() async {
  await Supabase.initialize(
    url: 'https://your-project.supabase.co',
    anonKey: 'your-public-anon-key',
  );
  runApp(const MyApp());
}
```

💡 **注意**：在正式发布鸿蒙应用前，请确保在 Supabase 后端配置正确的 Webhook 地址及 CORS 策略。

---

## 三、核心功能：3 个场景化进阶用法

### 3.1 极简身份认证 (Authentication)
利用 Supabase 自带的认证系统，一行代码实现鸿蒙应用登录。
```dart
Future<void> signIn(String email, String password) async {
  final response = await Supabase.instance.client.auth.signInWithPassword(
    email: email,
    password: password,
  );
  if (response.user != null) {
    print('✅ 鸿蒙用户登录成功：${response.user!.id}');
  }
}
```

### 3.2 响应式实时订阅 (Real-time)
当云端数据发生变动时，鸿蒙侧 UI 会通过 Stream 自动刷新，非常适合即时通讯场景。
```dart
final _stream = Supabase.instance.client
    .from('messages')
    .stream(primaryKey: ['id'])
    .order('created_at');

// 在 Widget 中配合 StreamBuilder 使用
```

### 3.3 远程文件存储 (Storage)
将用户在鸿蒙设备上拍摄的照片直接上传至 Supabase 存储桶。
```dart
Future<void> uploadAvatar(File imageFile) async {
  final path = 'public/avatars/${DateTime.now().toIso8601String()}.png';
  await Supabase.instance.client.storage
      .from('user_assets')
      .upload(path, imageFile);
  print('✅ 资源已同步至云端');
}
```

---

## 四、OpenHarmony 平台适配建议

### 4.1 网络访问权限申请 🏗️
⚠️ **注意**：鸿蒙应用访问外部 Supabase 域名需要显式声明权限。
- **✅ 建议做法**：在 `module.json5` 的 `requestPermissions` 列表中加入 `ohos.permission.INTERNET`。

### 4.2 处理 OAuth 回调
- **💡 技巧**：在使用 Google 或 GitHub 第三方登录时，鸿蒙端的 `deep link` 协议配置至关重要。确保在后台设置的 `Redirect URL` 能正确拉起你的鸿蒙应用 Scheme。

<!-- IMAGE_PLACEHOLDER: [鸿蒙真机运行 Supabase 实时列表截图] -->
<!-- 类型: 截图 -->
<!-- 内容: 展示在华为手机上，当直接在 Supabase 后台修改数据时，手机端 UI 瞬时变动的效果 -->

---

## 五、完整实战示例：鸿蒙云端协作待办应用

我们将构建一个全栈实战案例：一个支持云端同步与认证的 Todo 应用。无论在哪个鸿蒙设备上登录相同的账号，数据都会保持同步。

```dart
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class OhosTodoPage extends StatefulWidget {
  const OhosTodoPage({super.key});

  @override
  State<OhosTodoPage> createState() => _OhosTodoPageState();
}

class _OhosTodoPageState extends State<OhosTodoPage> {
  final _client = Supabase.instance.client;
  final _todoController = TextEditingController();

  // 1. 💡 实战：新增待办到 PostgreSQL
  Future<void> _addTodo() async {
    final text = _todoController.text;
    if (text.isEmpty) return;

    await _client.from('todos').insert({
      'content': text,
      'is_complete': false,
      'user_id': _client.auth.currentUser!.id,
    });
    _todoController.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('由 Supabase 驱动的鸿蒙协作')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: _todoController,
              decoration: InputDecoration(
                hintText: '输入新的鸿蒙任务...',
                suffixIcon: IconButton(icon: const Icon(Icons.add), onPressed: _addTodo),
              ),
            ),
          ),
          // 2. 核心：实时流列表
          Expanded(
            child: StreamBuilder<List<Map<String, dynamic>>>(
              stream: _client.from('todos').stream(primaryKey: ['id']),
              builder: (context, snapshot) {
                if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
                final todos = snapshot.data!;
                return ListView.builder(
                  itemCount: todos.length,
                  itemBuilder: (context, index) {
                    final item = todos[index];
                    return CheckboxListTile(
                      title: Text(item['content']),
                      value: item['is_complete'],
                      onChanged: (val) async {
                        // 3. 💡 实战：原地更新云端状态
                        await _client.from('todos').update({'is_complete': val}).eq('id', item['id']);
                      },
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

---

## 六、总结

在 **Flutter for OpenHarmony** 开发中，`Supabase` 提供了一套免运维、高性能的后端底座。它将原本繁琐的服务器开发工作简化成了简单的 SDK 调用，让前端开发者也能轻松构建具备认证与实时特性的复杂全栈应用。

如果你正在构思一个需要云端大脑的鸿蒙 App，Supabase 绝对值得作为你的第一选择。

---

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
