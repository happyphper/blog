import { defineStore } from "pinia";

export const mainStore = defineStore("main", {
  state: () => {
    return {
      // 主题类别
      themeType: "light",
      themeValue: "light",
      // banner
      bannerType: "half",
      // 加载状态
      loadingStatus: true,
      // 滚动高度
      scrollData: {
        // 滚动高度
        height: 0,
        // 滚动百分比
        percentage: 0,
        // 滚动方向
        direction: "down",
      },
      // 页脚可见性
      footerIsShow: false,
      // 中控台显示
      controlShow: false,
      // 搜索框显示
      searchShow: false,
      // 个性化配置显示
      showSeetings: false,
      // 播放器数据
      playState: false,
      playerShow: true,
      playerVolume: 0.7,
      playerData: {
        name: "未知曲目",
        artist: "未知艺术家",
      },
      // 移动端菜单显示
      mobileMenuShow: false,
      // 使用自定义右键菜单
      useRightMenu: true,
      // 背景模糊
      backgroundBlur: false,
      // 全站字体
      fontFamily: "hmos",
      // 全站字体大小
      fontSize: 16,
      // 信息显示位置
      infoPosition: "fixed",
      // 上次滚动位置
      lastScrollY: 0,
      // 站点背景
      backgroundType: "patterns",
      backgroundUrl: "https://api.paugram.com/wallpaper/",
      // 赞赏显示
      rewardShow: false,
    };
  },
  getters: {},
  actions: {
    // 切换应用状态
    changeShowStatus(value, blur = true) {
      this[value] = !this[value];
      // 全局模糊
      const globalApp = document.getElementById("app");
      this[value] && this.backgroundBlur && blur
        ? globalApp.classList.add("blur")
        : globalApp.classList.remove("blur");
    },
    // 更改字体大小
    changeFontSize(isAdd = false) {
      if (isAdd) {
        if (this.fontSize < 20) {
          this.fontSize++;
        }
      } else {
        if (this.fontSize > 14) {
          this.fontSize--;
        }
      }
      const htmlElement = document.documentElement;
      htmlElement.style.fontSize = this.fontSize + "px";
    },
    // 切换明暗模式
    changeThemeType() {
      this.themeType === "light"
        ? (this.themeType = "dark")
        : (this.themeType = "light");
      // 弹窗提示

    },
  },
  // 数据持久化
  persist: [
    {
      key: "siteData",
      paths: [
        "themeType",
        "bannerType",
        "useRightMenu",
        "playerShow",
        "playerVolume",
        "backgroundBlur",
        "backgroundType",
        "fontFamily",
        "fontSize",
        "infoPosition",
        "backgroundUrl",
      ],
    },
  ],
});
