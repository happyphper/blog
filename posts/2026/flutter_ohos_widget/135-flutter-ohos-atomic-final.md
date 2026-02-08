![封面图](images/135-cover.png)

# Flutter for OpenHarmony 实战之殿堂：第一百三十五篇 鸿蒙元服务 (Atomic Service) 收官 — 全量分发与服务直达

## 前言

作为“鸿蒙元服务专栏”的收官之作，我们要解决最重要的问题：**如何让用户找到你的服务？** 在 **HarmonyOS NEXT** 的全场景中，元服务不仅存在于负一屏，它还可以通过短信链接、浏览器、甚至是扫描一个物理二维码被瞬间拉起。

本篇将教你配置 **App Linking** 服务，实现各种入口到 Flutter 精准页面的“秒级触达”，并总结元服务的商业分发规范。

---

## 一、元服务的多维触达矩阵

在鸿蒙生态中，元服务有以下顶级入口：
- **扫码直达**：扫描万能码（智慧码），直接唤起特定功能的卡片。
- **App Linking**：通过 HTTPS 链接，在短信、社媒中点击直接入屏。
- **全局搜索 (Search)**：用户在桌面下滑搜索关键词，你的元服务直接以卡片形式出现在搜索结果第一位。

---

## 二、实战：配置 App Linking 实现“链接拉起卡片”

### 2.1 声明域名关联 (Asset-Links)
你需要在自己的服务器根目录放置 `assetlinks.json`，证明你拥有该域名的控制权。

```json
{
  "applinks": {
    "apps": [
      {
        "appID": "com.happyphper.blog.atomic",
        "fingerprint": ["SHA256_FINGERPRINT_HERE"]
      }
    ]
  }
}
```

### 2.2 鸿蒙侧：处理深度链接深度链接
在 `module.json5` 中配置元服务的路由规则。

```json
{
  "abilities": [
    {
      "skills": [
        {
          "actions": ["ohos.want.action.VIEW_DATA"],
          "uris": [{ "scheme": "https", "host": "happyphper.com", "path": "/article" }]
        }
      ]
    }
  ]
}
```

### 2.3 Flutter 侧：参数提取与动态路由动态路由
一旦通过链接拉起，Flutter 侧需要瞬时解析参数。

```dart
// 📌 在入口处解析跳转参数参数
void handleIncomingLink(String url) {
  final uri = Uri.parse(url);
  final articleId = uri.queryParameters['id'];
  // ⚡️ 极致体验：直接推送到具体的业务详情页详情页
  Navigator.of(context).pushNamed('/detail', arguments: articleId);
}
```

<!-- IMAGE_PLACEHOLDER: 用户在短信中点击一个普通的 URL，手机界面瞬间弹出一个半屏的 Flutter 风格元服务面板且已自动填充了所有业务信息的演示图 -->
<!-- 类型: 截图 -->
<!-- 内容: 展示 App Linking 带来的爆破式分发效果 -->

---

## 三、进阶：集成系统级“全场景分发”分发”

如何让你的元服务出现在桌面的“小艺建议”里？
- ✅ **方案**：适配我们在 133 篇讲过的意图框架。
- ✅ **结果**：当用户在搜索框输入“天气”时，如果你的应用是天气类元服务，它会以 2 * 2 动态卡片的形式直接预览，无需用户点开应用。

---

## 四、OpenHarmony 平台适配要点：上架“合规红线”

元服务审核极严，避坑要点：
1.  **功能单一性**：一个元服务必须只解决一个核心问题（如打车、查快递），严禁做成全功能的超级 App。
2.  **默认 UI 规范**：背景必须适配鸿蒙的深浅色模式，卡片边缘必须符合鸿蒙 24 像素的圆角标准。
3.  **落地页一致性**：点击卡片后的跳转页面风格，必须与卡片本身高度一致，不能有明显的“视觉断层”。

---

## 五、总结：元服务专题回顾

至此，我们完成了 131-135 篇的元服务深度通关：
1.  **形态认知**：理解了元服务零安装、碎片化的核心特质。
2.  **交互进化**：打通了万能卡片的实时刷新与双向通信。
3.  **深度赋能**：实现了小艺建议联动、负一屏直达与动态卡片配置。
4.  **分发闭环**：攻克了 App Linking、全局搜索与万能码实战。

**至此，您的鸿蒙跨平台应用已经具备了“病毒式传播”的技术底座。**

**第一百三十六篇，我们将进入【鸿蒙跨平台插件内核、鸿蒙 NAPI 开发与 C++ 后台引擎深度定制专题】。**

---

> 📦 **全场景分发示例代码包 (OhosAtomic-Distro)**：[open-harmony-examples/atomic-distribution-pro](https://atomgit.com/dragonbady/open-harmony-examples/tree/main/examples/atomic-distribution-pro)
>
> 🌐 **欢迎加入开源鸿蒙跨平台社区** [开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)
