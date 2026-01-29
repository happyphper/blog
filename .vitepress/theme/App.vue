<template>
  <!-- 背景图片 -->
  <Background />
  <!-- 加载提示 -->
  <!-- <Loading /> -->
  <!-- 导航栏 -->
  <Nav />
  <!-- 主内容 -->
  <main :class="['mian-layout', { loading: loadingStatus, 'is-post': isPostPage }]">
    <!-- 404 -->
    <NotFound v-if="page.isNotFound" />
    <!-- 首页 -->
    <Home v-if="frontmatter.layout === 'home'" showHeader />
    <!-- 页面 -->
    <template v-else>
      <!-- 文章页面 -->
      <Post v-if="isPostPage" />
      <!-- 致谢页面 -->
      <Thanks v-else-if="frontmatter.layout === 'thanks'" />
      <!-- 普通页面 -->
      <Page v-else-if="!page.isNotFound" />
    </template>
  </main>
  <!-- 页脚 -->
  <FooterLink v-show="!loadingStatus" :showBar="isPostPage && !page.isNotFound" />
  <Footer v-show="!loadingStatus" />
  <!-- 悬浮菜单 -->
  <Teleport to="body">
    <!-- 右侧悬浮菜单 -->
    <div class="right-menu-floating">
      <!-- 返回顶部 -->
      <BackToTop />
      <!-- 随机文章 -->
      <RandomPost />
      <!-- 全局设置 -->
      <Settings />
    </div>
    <!-- 赞赏弹窗 -->
    <Reward />
  </Teleport>
  <!-- 全局消息 -->
  <Message />
</template>

<script setup>
import { storeToRefs } from "pinia";
import { mainStore } from "@/store";
import { calculateScroll, specialDayGray } from "@/utils/helper";

const route = useRoute();
const store = mainStore();
const { frontmatter, page, theme } = useData();
const { loadingStatus, footerIsShow, themeValue, themeType, backgroundType, fontFamily, fontSize } =
  storeToRefs(store);

// 判断是否为文章页面
const isPostPage = computed(() => {
  const routePath = decodeURIComponent(route.path);
  return routePath.includes("/posts/");
});

// 复制时触发
const copyTip = () => {
  const copiedText = window.getSelection().toString();
  // 检查文本内容是否不为空
  if (copiedText.trim().length > 0 && typeof $message !== "undefined") {
    $message.success("复制成功，在转载时请标注本文地址");
  }
};

// 更改正确主题类别
const changeSiteThemeType = () => {
  // 主题 class
  const themeClasses = {
    dark: "dark",
    light: "light",
  };
  // 必要数据
  const htmlElement = document.documentElement;
  console.log("当前模式：", themeType.value);
  // 清除所有 class
  Object.values(themeClasses).forEach((themeClass) => {
    htmlElement.classList.remove(themeClass);
  });
  // 添加新的 class
  if (themeClasses[themeType.value]) {
    htmlElement.classList.add(themeClasses[themeType.value]);
    themeValue.value = themeClasses[themeType.value];
  }
  if (backgroundType.value === "image") {
    htmlElement.classList.add("image");
  } else {
    htmlElement.classList.remove("image");
  }
};

// 切换系统字体样式
const changeSiteFont = () => {
  try {
    const htmlElement = document.documentElement;
    htmlElement.classList.remove("lxgw", "hmos");
    htmlElement.classList.add(fontFamily.value);
    htmlElement.style.fontSize = fontSize.value + "px";
  } catch (error) {
    console.error("切换系统字体样式失败", error);
  }
};

// 监听设置变化
watch(
  () => [themeType.value, backgroundType.value],
  () => changeSiteThemeType(),
);
watch(
  () => fontFamily.value,
  () => changeSiteFont(),
);

onMounted(() => {
  console.log(frontmatter.value, page.value, theme.value);
  // 脏数据修复：如果背景地址包含已失效的域名，强制重置
  if (store.backgroundUrl.includes("eees.cc")) {
    store.backgroundUrl = "https://api.paugram.com/wallpaper/";
  }
  // 全站置灰
  specialDayGray();
  // 更改主题类别
  changeSiteThemeType();
  // 切换系统字体样式
  changeSiteFont();
  // 滚动监听
  window.addEventListener("scroll", calculateScroll);
  // 复制监听
  window.addEventListener("copy", copyTip);
  // 监听系统颜色
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", changeSiteThemeType);
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", calculateScroll);
});
</script>

<style lang="scss" scoped>
.mian-layout {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  // 手动实现加载动画
  animation: show 0.5s forwards;
  animation-duration: 0.5s;
  display: block;

  &.loading {
    display: none;
  }

  @media (max-width: 768px) {
    padding: 1rem 1.5rem;

    &.is-post {
      padding: 0;
    }
  }
}

.right-menu-floating {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1002;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  transition:
    opacity 0.3s,
    transform 0.3s;

  &.hidden {
    opacity: 0;
    transform: translateY(100px);
  }
}
</style>
