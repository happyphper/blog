![封面图](images/79-cover.png)

# Flutter for OpenHarmony 实战之进阶：第七十九篇 Pigeon 自动代码生成 — 告别手写通信逻辑的“黑魔法”

## 前言

在上一篇中，我们学习了 **MethodChannel** 的基础用法。虽然它灵活，但缺点也非常明显：你需要手动编写 Dart 和 ArkTS 的映射字符串，一旦拼错，运行时才会报错；且数据结构的传递需要繁琐的序列化。

为了解决这个问题，Flutter 官方推出了 **Pigeon** 工具。它能根据 Dart 定义生成**两端一致的强类型通信接口**。本篇将带你在 **HarmonyOS NEXT** 环境下跑通 Pigeon 模型，彻底解放生产力。

---

## 一、为什么混合开发需要 Pigeon？

### 1.1 类型安全性 (Type Safety)
手写 MethodChannel 就像在写 JS：`invokeMethod('foo', [1, 'bar'])`。如果原生端期待的是 `[String, Int]`，程序就会崩溃。Pigeon 让你像在调用原生普通方法一样传递对象。

### 1.2 自动同步接口
当你的接口发生变更（如新增一个字段），只需重新运行 Pigeon 生成命令，Dart 和 ArkTS 端会同步更新，编译器会自动帮你报错，无需肉眼排查。

---

## 二、实战：使用 Pigeon 自动生成鸿蒙通信代码

### 2.1 定义通信契约 (Schema)
在项目根目录创建一个 `pigeons/messages.dart` 文件：

```dart
import 'pigeon.dart';

// 💡 技巧：定义跨端传输的数据结构
class UserProfile {
  String? name;
  int? age;
  bool? isMember;
}

// 💡 原理：定义接口协议
@HostApi()
abstract class OhosUserApi {
  void saveProfile(UserProfile profile);
  UserProfile getProfile(String userId);
}
```

### 2.2 配置生成脚本
在 `pubspec.yaml` 中添加 `pigeon` 依赖，并执行生成命令。

```bash
# ⚡️ 生成代码命令 (需适配 OpenHarmony 生成路径)
flutter pub run pigeon \
  --input pigeons/messages.dart \
  --dart_out lib/src/generated/messages.g.dart \
  --ohos_out ohos/entry/src/main/ets/generated/Messages.g.ets
```

---

## 三、鸿蒙原生端的实现

Pigeon 会在 ArkTS 侧生成一个 `OhosUserApi` 的抽象接口类。你只需要实现它：

```typescript
// 💡 实现生成的 Pigeon 接口
import { OhosUserApi, UserProfile } from './generated/Messages.g';

export class MyUserApiImpl extends OhosUserApi {
  saveProfile(profile: UserProfile): void {
    console.log(`📌 保存用户信息: ${profile.name}, 年龄: ${profile.age}`);
    // 执行原生存储逻辑...
  }

  getProfile(userId: string): UserProfile {
    let user = new UserProfile();
    user.name = "鸿蒙架构师";
    user.age = 25;
    return user;
  }
}

// 📌 在 Ability 启动时进行绑定
MyUserApiImpl.setup(flutterEngine.dartExecutor, new MyUserApiImpl());
```

---

## 四、OpenHarmony 平台适配要点

### 4.1 数据类型的映射映射
Pigeon 对基础类型（String, int, double, bool, List, Map）支持完美。
- ⚠️ **注意**：对于鸿蒙特有的 `PixelMap`（图片数据），Pigeon 默认无法直接映射，建议通过 `Uint8List` 传输原始字节。

### 4.2 零拷贝优化思考
虽然 Pigeon 简化了开发流程，但底层依然走的是二进制编码传输。对于超大规模的对象数组，频繁调用生成的 API 依然会有序列化开销。
- ✅ **方案**：尽量减少 Pigeon 接口的调用频次，单次调用可以携带更丰富的数据结构。

---

## 五、总结

**Pigeon** 的引入标志着你的 **Flutter for OpenHarmony** 开发进入了“工业化阶段”：
1.  **零错可能**：靠编译器而非记忆力。
2.  **效率倍增**：专注于业务逻辑，而非“搬运”字符串。
3.  **大厂规范**：这是大型跨平台项目（如闲鱼、微信）保持架构稳定的核心工具链。

扔掉那些手写的 `MethodChannel` 吧，Pigeon 才是混合开发的未来。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/pigeon-codegen](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/pigeon-codegen)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
