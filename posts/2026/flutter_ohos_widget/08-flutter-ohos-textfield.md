![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第八篇 TextField 输入框与表单

> **摘要**：用户输入是 App 交互的重要环节。本文作为基础组件系列的终章，将深入解析 Flutter 中的 TextField 和 TextFormField，涵盖内容获取、表单校验、键盘遮挡优化以及如何封装一套鸿蒙风格的通用输入组件。

## 前言

从登录注册到搜索商品，输入框无处不在。

相比于展示类组件，`TextField` 明显复杂得多。你需要管理光标、处理软键盘弹起、实时监听内容变化、校验格式合法性...

**本文你将学到**：
- 控制器 (Controller) 的生命周期管理
- 实现“点击眼睛显示/隐藏密码”
- Form 表单的一键校验技巧
- 解决“键盘遮挡输入框”的经典方案
- 实战：封装现代化的登录输入组件

![Flutter 输入框与表单校验概念图 (中文版)](./images/flutter_ohos_textfield_form_concept_cn.png)

---

## 一、TextField 基础用法

### 1.1 最简单的输入框

```dart
TextField(
  decoration: InputDecoration(
    labelText: '用户名',
    hintText: '请输入手机号/邮箱',
    prefixIcon: Icon(Icons.person),
    border: OutlineInputBorder(), // 边框样式
  ),
  onChanged: (text) {
    print('当前输入: $text');
  },
)
```

### 1.2 获取与控制输入 (TextEditingController)

想要获取输入框的内容，或者设置默认值，必须使用 `TextEditingController`。

```dart
class LoginDemo extends StatefulWidget {
  const LoginDemo({super.key});

  @override
  State<LoginDemo> createState() => _LoginDemoState();
}

class _LoginDemoState extends State<LoginDemo> {
  // 1. 创建控制器
  final TextEditingController _usernameController = TextEditingController();

  @override
  void initState() {
    super.initState();
    // 2. 设置默认值 (可选)
    _usernameController.text = "admin";
  }

  @override
  void dispose() {
    // 3. ⭐️ 务必销毁，防止内存泄漏
    _usernameController.dispose();
    super.dispose();
  }

  void _login() {
    // 4. 获取内容
    final username = _usernameController.text;
    print('登录用户名: $username');
  }

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: _usernameController, // 绑定
    );
  }
}
```

### 1.3 密码框与显示/隐藏

通过 `obscureText` 属性控制是否隐藏内容（变为星号或圆点）。

```dart
bool _isObscure = true;

TextField(
  obscureText: _isObscure, // 控制密码显示
  decoration: InputDecoration(
    labelText: '密码',
    // 后缀图标：眼睛按钮
    suffixIcon: IconButton(
      icon: Icon(_isObscure ? Icons.visibility : Icons.visibility_off),
      onPressed: () {
        setState(() {
          _isObscure = !_isObscure;
        });
      },
    ),
  ),
)
```

---

## 二、Form 表单与校验

如果一个页面有多个输入框（如注册页），一个个去判断太麻烦了。Flutter 提供了 `Form` 和 `TextFormField` 来批量管理。

### 2.1 核心组件

- **Form**: 容器，通过 `GlobalKey` 管理状态。
- **TextFormField**: 也就是 `TextField` 的加强版，增加了 `validator` 和 `onSaved` 回调。

### 2.2 实战：带校验的注册表单

```dart
class RegisterForm extends StatefulWidget {
  const RegisterForm({super.key});

  @override
  State<RegisterForm> createState() => _RegisterFormState();
}

class _RegisterFormState extends State<RegisterForm> {
  // 1. 创建 GlobalKey
  final _formKey = GlobalKey<FormState>();
  
  String _email = '';
  String _password = '';

  void _submit() {
    // 2. 调用 validate() 触发所有子项校验
    if (_formKey.currentState!.validate()) {
      // 3. 校验通过，保存数据
      _formKey.currentState!.save();
      print('注册信息: $_email, $_password');
      // TODO: 发起注册请求
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey, // 绑定 Key
      child: Column(
        children: [
          TextFormField(
            decoration: const InputDecoration(labelText: '邮箱'),
            // 校验逻辑
            validator: (value) {
              if (value == null || value.isEmpty) {
                return '邮箱不能为空';
              }
              if (!value.contains('@')) {
                return '请输入有效的邮箱地址';
              }
              return null; // 返回 null 表示通过
            },
            onSaved: (val) => _email = val!,
          ),
          
          const SizedBox(height: 16),
          
          TextFormField(
            decoration: const InputDecoration(labelText: '密码'),
            validator: (value) {
              if (value == null || value.length < 6) {
                return '密码长度不能少于6位';
              }
              return null;
            },
            onSaved: (val) => _password = val!,
            obscureText: true,
          ),
          
          const SizedBox(height: 32),
          
          ElevatedButton(
            onPressed: _submit,
            child: const Text('立即注册'),
          ),
        ],
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 表单校验错误提示效果 -->
<!-- 类型: 示例图 -->
<!-- 内容: 输入框下方出现红色的"邮箱不能为空"提示文字 -->

---

## 三、常见问题解决方案

### 3.1 键盘遮挡输入框

当在底部输入时，软键盘弹起会盖住输入框。

**方案 A**: `Scaffold(resizeToAvoidBottomInset: true)` (默认开启)。这会让 Body 自动变矮。
**方案 B**: 将页面包裹在 `SingleChildScrollView` 或 `ListView` 中。当键盘弹起，页面可滚动。

```dart
Scaffold(
  body: SingleChildScrollView( // 💡 推荐这样做
    padding: EdgeInsets.all(16),
    child: Column(
      children: [
        // 很多内容...
        TextField(), // 在底部的输入框
      ],
    ),
  ),
)
```

### 3.2 点击空白处收起键盘

这在 iOS 和鸿蒙上是符合用户直觉的体验。

```dart
GestureDetector(
  behavior: HitTestBehavior.translucent, // 确保点击空白也能触发
  onTap: () {
    // 收起键盘的神奇代码
    FocusScope.of(context).unfocus();
  },
  child: RegisterForm(),
)
```

---

## 四、鸿蒙实战：封装通用输入组件

为了让 APP 风格统一，我们封装一个样式的 `InputWidget`。

```dart
class ModernTextField extends StatelessWidget {
  final TextEditingController? controller;
  final String hint;
  final IconData? icon;
  final bool isPassword;

  const ModernTextField({
    super.key,
    this.controller,
    required this.hint,
    this.icon,
    this.isPassword = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        // 增加投影，提升立体感
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            offset: const Offset(0, 4),
            blurRadius: 10,
          ),
        ],
      ),
      child: TextField(
        controller: controller,
        obscureText: isPassword,
        decoration: InputDecoration(
          hintText: hint,
          prefixIcon: icon != null ? Icon(icon, color: Colors.blue) : null,
          border: InputBorder.none, // 去掉默认下划线
          contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        ),
      ),
    );
  }
}
```

---

## 五、阶段总结

至此，**《Flutter for OpenHarmony 实战之基础组件》** 系列的前 8 篇基础中的基础已经讲解完毕！但这仅仅是开始。

我们已经掌握了：
1.  **Container**: 布局的基石。
2.  **Row/Column**: 线性排列的艺术。
3.  **Stack**: 这就是层叠（Z轴）。
4.  **Text**: 信息的传递者。
5.  **Image**: 颜值即正义。
6.  **ListView**: 动态的长河。
7.  **Button**: 交互的起点。
8.  **TextField**: 数据的入口。

掌握了这 8 大组件，你已经能画出大部分 UI 界面了。但要构建一个**完整的、有灵魂的 App**，我们还需要搭建页面的骨架（Scaffold）、与用户进行对话（Dialog）、以及更复杂的导航结构（Tabs）。

### 下一篇预告

接下来的第九篇，我们将进入**“中级组件篇”**，解决页面的结构问题：

**《Flutter for OpenHarmony 实战之基础组件：第九篇 Scaffold 与 AppBar 页面骨架》** 

我们将学习如何像搭积木一样，快速构建出具备导航栏、侧边栏和悬浮按钮的标准 Material 页面。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/8-textfield-form)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/8-textfield-form)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
