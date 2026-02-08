![Flutter for OpenHarmony Banner](./images/flutter_ohos_banner.png)

# Flutter for OpenHarmony 实战之基础组件：第十篇 Dialog, SnackBar 与 BottomSheet 交互反馈

> **摘要**：一个好的 App 不仅要展示信息，更要对用户的操作给予及时的反馈。本文将深入讲解 Flutter 中三类核心反馈组件：模态对话框 (Dialog)、轻量级提示 (SnackBar) 以及底部控制面板 (BottomSheet)。我们将对比它们的使用场景，并手把手教你在 OpenHarmony 上封装一套优雅的通用弹窗管理器。

## 前言

用户点击了删除按钮，你是否应该弹窗确认？
用户保存了图片，是弹出一个大框告诉他成功，还是在底部轻轻提示一下？

在 UI 交互设计中，**反馈 (Feedback)** 的轻重缓急至关重要。Flutter 提供了丰富的组件来应对不同等级的打扰：

1.  **强反馈 (Dialog)**：打断用户，强迫做出选择（如：确认删除）。
2.  **中反馈 (BottomSheet)**：半屏操作，用户依然在一个流程中（如：选择相册/相机）。
3.  **弱反馈 (SnackBar/Toast)**：不打断用户，仅作为信息告知（如：已加入购物车）。

**本文你将学到**：
- `AlertDialog` 与 `SimpleDialog` 的标准用法
- 自定义全屏 `Dialog` (利用 `Dialog` 组件)
- `showModalBottomSheet` 的圆角与高度控制
- `SnackBar` 的行为控制（悬浮 vs 固定）
- **鸿蒙适配**：处理系统侧滑手势与 BottomSheet 的冲突

---

## 一、Dialog：强交互对话框

当需要用户必须做出决策时，使用 Dialog。

### 1.1 AlertDialog (警告框)

这是最常见的“标题 + 内容 + 按钮”结构。

```dart
void _showConfirmDialog(BuildContext context) {
  showDialog(
    context: context,
    // 点击背景是否关闭 (默认 true)
    barrierDismissible: false, 
    builder: (ctx) {
      return AlertDialog(
        title: const Text('确认删除？'),
        content: const Text('删除后无法恢复，请谨慎操作。'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx), // 关闭弹窗
            child: const Text('取消'),
          ),
          TextButton(
            onPressed: () {
              // 执行删除逻辑
              Navigator.pop(ctx);
              print('已删除');
            },
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('删除'),
          ),
        ],
      );
    },
  );
}
```

### 1.2 SimpleDialog (简单选择框)

当有多个选项供用户选择时使用。

```dart
void _showAccountSelector(BuildContext context) {
  showDialog(
    context: context,
    builder: (ctx) {
      return SimpleDialog(
        title: const Text('切换账号'),
        children: [
          SimpleDialogOption(
            onPressed: () => Navigator.pop(ctx, 'user1'),
            child: const Row(
              children: [
                CircleAvatar(child: Text('A')),
                SizedBox(width: 12),
                Text('Admin'),
              ],
            ),
          ),
          SimpleDialogOption(
            onPressed: () => Navigator.pop(ctx, 'user2'),
            child: const Row(
              children: [
                CircleAvatar(child: Text('G')),
                SizedBox(width: 12),
                Text('Guest'),
              ],
            ),
          ),
        ],
      );
    },
  ).then((value) {
    // 获取返回值
    if (value != null) print('选择了: $value');
  });
}
```

---

## 二、BottomSheet：底部面板

在移动端，底部面板是比 Dialog 更友好的交互方式，因为它离拇指更近。

### 2.1 showModalBottomSheet (模态底部弹窗)

这是标准的 Material 底部弹窗。

```dart
void _showEditPanel(BuildContext context) {
  showModalBottomSheet(
    context: context,
    // 💡 关键：设置圆角
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
    // 💡 关键：允许全屏高度的一半以上 (isScrollControlled)
    isScrollControlled: true, 
    builder: (ctx) {
      return Padding(
        // 处理键盘遮挡 (MediaQuery.viewInsets)
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(ctx).viewInsets.bottom,
        ),
        child: Container(
          height: 300,
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min, // 自适应高度
            children: [
              const Text('编辑备注', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              const TextField(decoration: InputDecoration(hintText: '请输入...')),
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => Navigator.pop(ctx),
                  child: const Text('保存'),
                ),
              ),
            ],
          ),
        ),
      );
    },
  );
}
```

![Flutter 反馈组件全家桶概念图 (中文版)](./images/flutter_feedback_components_concept_cn.png)

---

## 三、SnackBar：轻提示

`SnackBar` 通常用于告诉用户“操作成功”或“网络错误”。它会自动消失，不打断用户流程。

### 3.1 基础与进阶用法

```dart
void _showSnackBar(BuildContext context) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: const Text('已添加到收藏夹 ❤️'),
      duration: const Duration(seconds: 2), // 显示时长
      action: SnackBarAction(
        label: '撤销',
        onPressed: () {
          print('执行撤销逻辑');
        },
      ),
      // 💡 浮动样式 (默认是 Fixed 固定在底部)
      behavior: SnackBarBehavior.floating, 
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      margin: const EdgeInsets.all(16),
    ),
  );
}
```

---

## 四、OpenHarmony 鸿蒙适配专题

### 4.1 侧滑手势与 BottomSheet

在鸿蒙系统上，从屏幕**左/右边缘向内滑动**是系统级的“返回”手势。

当 `BottomSheet` 弹出时，用户可能习惯性地使用侧滑手势来关闭它。Flutter 默认已经适配了这一点：
- 点击遮罩层 -> 关闭
- 向下滑动面板 -> 关闭
- **按系统返回键 (或侧滑返回)** -> 关闭

**⚠️ 常见坑点**：
如果你在 `BottomSheet` 里放了一个横向滑动的 `PageView` 或 `ListView` (水平方向)，此时用户的横滑操作可能会和系统的侧滑返回冲突。

✅ **解决方案**：
在鸿蒙上，尽量避免在 BottomSheet 边缘放置横滑组件，或者告知用户尽量在屏幕中间区域滑动。

### 4.2 沉浸式下的 Dialog 遮罩

在开启了沉浸式状态栏 (透明状态栏) 后，`showDialog` 弹出的黑色半透明遮罩层 (Barrier) 会覆盖整个屏幕（包括状态栏）。这是符合预期的 Material 规范。

如果你希望状态栏区域**不被遮罩**（保持亮色），可以使用 `SafeArea` 包裹 Dialog 内容，但这通常无法去除背景遮罩。原生 App 通常也是覆盖全屏的，一般无需特殊处理。

---

## 五、实战：封装通用 DialogManager

为了避免在业务代码里写满 `showDialog`，我们可以封装一个 `DialogManager`。

```dart
class ToastUtils {
  // 显示加载框
  static void showLoading(BuildContext context, {String msg = "加载中..."}) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) => Dialog(
        backgroundColor: Colors.transparent, // 背景透明
        elevation: 0,
        child: Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: Colors.black87,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const CircularProgressIndicator(color: Colors.white),
              const SizedBox(height: 16),
              Text(msg, style: const TextStyle(color: Colors.white)),
            ],
          ),
        ),
      ),
    );
  }

  // 显示简易提示
  static void showToast(BuildContext context, String msg) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(msg), behavior: SnackBarBehavior.floating),
    );
  }
}
```

---

## 五、总结

交互反馈是提升 App 质感的关键细节。

### 核心要点
1.  **Dialog**: 慎用，仅用于关键决策。优先使用 `AlertDialog`。
2.  **BottomSheet**: 推荐使用。它是现代 App 处理复杂表单和菜单的首选，记得设置 `isScrollControlled: true` 并处理键盘遮挡。
3.  **SnackBar**: 最轻量。记得使用 `floating` 样式，在鸿蒙大屏上更美观。
4.  **鸿蒙适配**: 相信 Flutter 的默认行为，它能很好地响应鸿蒙的系统返回手势。

### 下一篇预告
我们已经学会了画页面（Scaffold）和弹窗（Dialog）。如果我们的 App 很复杂，需要底部的 4 个 Tab 来切换不同功能模块，该怎么做？
**《Flutter for OpenHarmony 实战之基础组件：第十一篇 BottomNavigationBar 与 TabBar 多页切换》**
我们将学习如何构建像微信一样的多 Tab 首页架构。

---

📦 **完整代码已上传至 AtomGit**：[open-harmony-example (分支: basic/10-dialog-feedback)](https://atomgit.com/dragonbady/open-harmony-example/tree/basic/10-dialog-feedback)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
