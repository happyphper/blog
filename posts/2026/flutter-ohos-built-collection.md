---
title: "Flutter for OpenHarmony 实战：built_collection 全链路不可变集合模型"
date: 2026-02-09
tags: ["Flutter", "OpenHarmony", "built_collection", "数据模型", "不可变集合"]
categories: ["Flutter for OpenHarmony 实战"]
---

# Flutter for OpenHarmony 实战：built_collection 全链路不可变集合模型

![封面图](images/cover_flutter_ohos_built_collection.png)

## 前言

在之前的文章中我们讨论了如何使用 `built_value` 来创建不可变的类对象。然而，在真实的业务场景下，我们更多地是在处理列表（List）、集合（Set）和映射（Map）。普通的 Dart 集合是可变的，这意味着当你在多个服务或页面间传递一个 List 时，任何一个地方的修改都可能引发难以排查的 Bug。

**`built_collection`** 专门为解决这类问题而生。它将“不可变性（Immutability）”延伸到了集合层面，为 **HarmonyOS NEXT** 上的健壮软件架构提供了最后一块拼图。

---

---

## 一、 为什么在鸿蒙大型项目中使用不可变集合？

### 1.1 彻底消灭“侧漏异常（Side Effects）”
在常规 Dart 开发中，如果你将一个 `List` 从 UI 层传递给某个 Service 处理，Service 内部的一个 `sort()` 或 `remove()` 可能会直接修改 UI 层引用的内存对象，导致状态错乱。`built_collection` 提供的集合对象一旦创建即不可修改，任何变更操作都会明确地产生一个新指针，从而在根源上切断了非法修改的可能性。

### 1.2 物理级支持“深度值相等”
普通的 `List` 比较是 `a == b`（比较的是内存地址）。而 `BuiltList` 实现的是全成员递归比对。这在 **HarmonyOS NEXT** 的高频刷新 UI 中极具价值：如果两个新闻列表里的所有 NewsItem 内容一致，即便它们是不同的实例，Beamer 或 Bloc 也可以直接判定无须重绘，性能飞跃显著。

### 1.3 鸿蒙 Isolates 并发安全
鸿蒙系统支持强大的异步并发能力。不可变集合是多 Isolate 通信的最佳载体。由于它们是“只读快照”，多线程间共享时完全不需要繁琐的加锁保护。

---

## 二、 技术内幕：BuiltCollection 是如何做到高性能的？

### 2.1 基于 Builder 模式的伪变异
`built_collection` 利用了“影子对象（Shadow Object）”模式。当你调用 `rebuild` 时，它会临时创建一个可变的 `Builder`。在这个封闭的瞬时环境里进行集合操作，完成后立刻“冻结”并输出新的不可变实例。

### 2.2 深度哈希（Deep Hashing）算法
为了让 `BuiltSet` 或 `BuiltMap` 的查找速度不被深度相等拖慢，它在内部预计算并缓存了当前集合的哈希值。只要内容没变，所有哈希操作都是 O(1) 级别的。

---

## 三、 集成指南

### 2.1 添加依赖
```yaml
dependencies:
  built_collection: ^5.1.1
```

---

---

## 四、 实战：构建鸿蒙应用的安全列表模型

### 4.1 基础实现：从普通集合转换到 BuiltList

```dart
import 'package:built_collection/built_collection.dart';

// 💡 技巧：利用 [].toBuiltList() 快捷转换
final normalList = [1, 2, 3];
final BuiltList<int> builtInts = normalList.toBuiltList();

// 💡 亮点：任何修改都必须通过 rebuild
final updatedList = builtInts.rebuild((b) => b
  ..add(4)
  ..remove(1)
  ..sort());
```

### 4.2 深度嵌套集合的处理
在复杂的鸿蒙应用状态树中，我们可能需要修改 Map 里的 List。`rebuild` 支持嵌套操作：

```dart
final scores = BuiltMap<String, BuiltList<int>>({
  'OpenHarmony': BuiltList([98, 99]),
});

final newScores = scores.rebuild((b) => b
  ..updateValue('OpenHarmony', (list) => list.rebuild((l) => l.add(100)))
);
```

---

## 四、 鸿蒙平台的适配建议

### 4.1 内存优化
不可变集合频繁生成新对象，虽然在鸿蒙系统强大的垃圾回收（GC）面前不是问题，但在极高频更新的场景（如每秒变动上百次的进度条列表）下，建议批量合并修改任务，尽可能减少 `rebuild` 的调用次数。

### 4.2 适配原生 ArkTS 桥接
当你的 Flutter 插件需要向鸿蒙系统原生端推送大量数据列表时，封装为 `BuiltList` 可以确保在 Dart 层数据被污染前，已经以稳定的状态序列化到了原生侧。

---

## 五、 完整示例代码

以下演示了一个“鸿蒙消息流”模拟，展示了不可变集合如何保证数据流转的洁净：

```dart
import 'package:flutter/material.dart';
import 'package:built_collection/built_collection.dart';

class BuiltCollectionDemo extends StatefulWidget {
  const BuiltCollectionDemo({super.key});

  @override
  State<BuiltCollectionDemo> createState() => _BuiltCollectionDemoState();
}

class _BuiltCollectionDemoState extends State<BuiltCollectionDemo> {
  // 💡 初始不可变列表
  BuiltList<String> _logs = BuiltList<String>(['系统已启动', '正在加载鸿蒙资源...']);

  void _addLog() {
    setState(() {
      // 💡 通过 rebuild 生成新列表，保证旧引用不受干扰
      _logs = _logs.rebuild((b) => b.add('发现新任务 @ ${DateTime.now().second}s'));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('鸿蒙不可变集合实验室')),
      body: ListView.builder(
        itemCount: _logs.length,
        itemBuilder: (context, index) => ListTile(
          title: Text(_logs[index]),
          leading: const Icon(Icons.history_edu),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _addLog,
        child: const Icon(Icons.add_comment),
      ),
    );
  }
}
```

<!-- IMAGE_PLACEHOLDER: 鸿蒙手机显示的列表项增加后，通过调试器观察发现旧列表对象引用地址保持不变而新对象地址不同的内存快照截图 -->
<!-- 内容: 展示不可变集合在复杂状态流转中保护数据不被非法覆盖的架构价值 -->

## 七、 总结

`built_collection` 是对 Dart 集合功能的强有力补充。在 **HarmonyOS NEXT** 这个追求“端云一致、全场景协作”的体系中，不可变数据是构建复杂、高频率交互系统的核心法则。通过强迫自己使用不可变集合，你不仅是在写代码，更是在构建一个可预测、可信赖的优质软件工程。

---

> 📦 **完整代码已上传至 AtomGit**：[open-harmony-examples/flutter-ohos-built-collection](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/flutter-ohos-built-collection)
> 
> 🔗 **相关阅读推荐**：
> - [Effective Dart：集合设计的最佳实践](https://dart.dev/guides/language/effective-dart/design#collection)
> - [Immutability in Flutter：如何优化大型项目的渲染开销](https://flutter.dev/docs/perf/rendering/best-practices)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
