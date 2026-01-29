<template>
  <div class="about">
    <h1 class="title">关于本站</h1>
    <div class="about-content" style="grid-template-columns: 3fr 2fr">
      <!-- 介绍 -->
      <div class="about-item hello">
        <span class="text1">你好，很高兴认识你👋</span>
        <span class="text2 title2">我是 王码码</span>
        <span class="text3">是一名 全栈开发工程师、自由职业者</span>
      </div>
      <!-- 追求 -->
      <div class="about-item pursuit">
        <span class="tip">追求</span>
        <span class="title2">终身学习</span>
        <span class="title2">从后端到全栈</span>
        <span class="title2">通往财富自由之路</span>
      </div>
    </div>
    <div class="about-content" style="grid-template-columns: 2fr 3fr">
      <!-- 技能 -->
      <div class="about-item skills">
        <span class="tip">技能</span>
        <span class="title2">开启创造力</span>
        <div class="skills-list">
          <a v-for="(item, index) in skillsData" :key="index" :style="{ '--color': item.color }" :href="item.link"
            class="skills-item" target="_blank">
            <div class="skills-logo">
              <i :class="`iconfont icon-${item.icon}`"></i>
            </div>
            <span class="skills-name">{{ item.name }}</span>
          </a>
        </div>
      </div>
      <!-- 生涯 -->
      <div class="about-item career image"
        style="background-image: url(https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=800); --color: #00000080">
        <div class="image-content">
          <span class="tip">生涯</span>
          <span class="title2">
            <i>无限进步</i>
          </span>
          <div class="list">
            <span class="list-item" style="--color: #357ef5">中国人民大学 · 计算机科学与技术</span>
            <span class="list-item" style="--color: #eb372a">自由职业 · 全栈开发工程师</span>
          </div>
        </div>
      </div>
    </div>
    <div class="about-content" style="grid-template-columns: 3fr 2fr">
      <!-- 性格 -->
      <div class="about-item character" style="--color: #4298b4">
        <span class="tip">性格</span>
        <span class="title2">架构师</span>
        <span class="title2" style="color: var(--color)">INTJ-A / INTJ-T</span>
        <span class="more">
          在
          <a href="https://www.16personalities.com/ch/" target="_blank">16personalities</a>
          了解更多关于
          <a href="https://www.16personalities.com/ch/intj-%E4%BA%BA%E6%A0%BC" target="_blank">
            架构师
          </a>
        </span>
        <img src="https://images.unsplash.com/photo-1610484826967-09c5720778c7?q=80&w=400" alt="character"
          class="male" />
      </div>
      <!-- 座右铭 -->
      <div class="about-item motto">
        <span class="tip">座右铭</span>
        <span class="title1">脚踏实地</span>
        <span class="title2">诚实守信</span>
      </div>
    </div>
    <div class="about-content" style="grid-template-columns: 2fr 3fr">
      <!-- 数据 -->
      <div class="about-item static image" style="
          background-image: url(https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=800);
        ">
        <div class="image-content">
          <span class="tip">数据</span>
          <span class="title2">运行状态</span>
          <div class="static-data">
            <div class="static-item">
              <span class="static-name">文章总数</span>
              <span class="static-num">{{ theme.postData.length }}</span>
            </div>
            <div class="static-item">
              <span class="static-name">运行天数</span>
              <span class="static-num">{{ runtimeDays }}</span>
            </div>
          </div>
          <div class="image-desc opacity">
            <span class="left">
              始终保持对技术的热爱
            </span>
          </div>
        </div>
      </div>
      <!-- 信息 -->
      <div class="about-item child">
        <div class="about-item map image"
          style="background-image: url(https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?q=80&w=1000)">
          <span class="position">我现在住在 <strong>中国，北京市</strong></span>
        </div>
        <div class="about-item info">
          <div class="info-item">
            <span class="info-name">生于</span>
            <span class="info-num" style="--color: #43a6c6">1992</span>
          </div>
          <div class="info-item">
            <span class="info-name">现在职业</span>
            <span class="info-num" style="--color: #dfac46">自由职业者</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getStatistics } from "@/api";

const { theme } = useData();

// 技能数据
const skillsData = [
  {
    name: "PHP",
    color: "#777bb4",
    icon: "php",
    link: "https://www.php.net/",
  },
  {
    name: "Go",
    color: "#00add8",
    icon: "go",
    link: "https://go.dev/",
  },
  {
    name: "Python",
    color: "#3776AB",
    icon: "python",
    link: "https://www.python.org/",
  },
  {
    name: "JavaScript",
    color: "#f1e05abd",
    icon: "javascript",
    link: "https://developer.mozilla.org/zh-CN/docs/Web/JavaScript",
  },
  {
    name: "TypeScript",
    color: "#3178c6",
    icon: "typescript",
    link: "https://www.typescriptlang.org/",
  },
  {
    name: "Vue",
    color: "#41b883",
    icon: "vue",
    link: "https://cn.vuejs.org/",
  },
  {
    name: "Solidity",
    color: "#363636",
    icon: "solidity",
    link: "https://soliditylang.org/",
  },
  {
    name: "Web3",
    color: "#f16822",
    icon: "web3",
    link: "https://web3js.org/",
  },
  {
    name: "Smart Contracts",
    color: "#2496f2",
    icon: "contract",
    link: "https://ethereum.org/zh/developers/docs/smart-contracts/",
  },
  {
    name: "量化交易",
    color: "#eb372a",
    icon: "chart",
    link: "https://en.wikipedia.org/wiki/Quantitative_analysis_(finance)",
  },
  {
    name: "Docker",
    color: "#2496f2",
    icon: "docker",
    link: "https://www.docker.com/",
  },
  {
    name: "Git",
    color: "#F05032",
    icon: "git",
    link: "https://git-scm.com/",
  },
];

// 运行天数
const runtimeDays = computed(() => {
  const diff = new Date().getTime() - new Date(theme.value.since).getTime();
  return Math.floor(diff / (24 * 3600 * 1000));
});

onMounted(() => {
  // 百度统计脚本已通过 inject 注入
});
</script>

<style lang="scss" scoped>
.about {
  .title {
    font-size: 2.4rem;
    text-align: center;
    border: none;
  }

  .about-content {
    display: grid;
    grid-template-columns: auto auto;
    gap: 20px;
    margin-bottom: 20px;

    .about-item {
      position: relative;
      display: flex;
      flex-direction: column;
      width: 100%;
      padding: 1.2rem 2rem;
      border-radius: 12px;
      background-color: var(--main-card-background);
      border: 1px solid var(--main-card-border);
      box-shadow: 0 8px 12px -4px var(--main-border-shadow);
      overflow: hidden;

      .tip {
        font-size: 14px;
        opacity: 0.8;
        margin-bottom: 12px;
      }

      .title1 {
        font-size: 36px;
        font-weight: bold;
        opacity: 0.6;
      }

      .title2 {
        font-size: 36px;
        font-weight: bold;
        margin-right: 4rem;
      }

      .text {
        font-size: 18px;
        margin: 0.6rem 0;
      }

      &.child {
        background-color: transparent;
        border: none;
        box-shadow: none;
        padding: 0;
        gap: 20px;

        .about-item {
          height: 100%;
        }
      }

      &.hello {
        justify-content: center;
        padding: 2rem;
        color: #fff;
        background-image: linear-gradient(120deg, #5b27ff 0%, #00d4ff 100%);
        background-size: 200% 200%;
        animation: gradientFlow 6s ease infinite;

        .title2 {
          line-height: 2;
        }
      }

      &.motto {
        justify-content: center;
        color: #fff;
        background-image: linear-gradient(120deg, #1e3c72 0%, #2a5298 50%, #2c3e50 100%);
        background-size: 200% 200%;
        animation: gradientFlow 6s ease infinite;

        .title1 {
          opacity: 0.8;
          font-size: 28px;
        }

        .title2 {
          line-height: 1.5;
        }
      }

      &.pursuit {
        .title2 {
          line-height: 1.2;

          &:last-child {
            display: inline-block;
            background-size: 100% 100%;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-repeat: no-repeat;
            background-image: linear-gradient(45deg, #fa7671 50%, #f45f7f);
          }
        }
      }

      &.character {
        min-height: 220px;
        cursor: pointer;

        .more {
          margin-top: auto;
          font-size: 14px;
          color: var(--main-color-gray);

          a {
            color: var(--main-color-gray);

            &:hover {
              color: var(--color);
            }
          }
        }

        .male {
          position: absolute;
          top: 30px;
          right: 10px;
          height: 100%;
          width: auto;
          transition: transform 0.5s;
          transform-origin: top center;

          @media (max-width: 768px) {
            height: 80%;
          }
        }

        &:hover {
          .male {
            transform: scale(1.2);
          }
        }
      }

      &.skills {
        .skills-list {
          margin-top: 12px;
          display: flex;
          flex-direction: row;
          flex-wrap: wrap;

          .skills-item {
            display: flex;
            align-items: center;
            margin-right: 10px;
            margin-top: 10px;
            padding: 8px 12px 8px 8px;
            border-radius: 40px;
            background-color: var(--main-site-background);
            border: 1px solid var(--main-card-border);
            box-shadow: 0 8px 12px -4px var(--main-border-shadow);
            transition: background-color 0.3s;
            cursor: pointer;

            .skills-logo {
              display: flex;
              align-items: center;
              justify-content: center;
              width: 32px;
              height: 32px;
              margin-right: 8px;
              border-radius: 50%;
              background-color: var(--color);

              .iconfont {
                color: #fff;
              }
            }

            .skills-name {
              font-weight: bold;
              transition: color 0.3s;
            }

            &:hover {
              background-color: var(--main-card-background);
            }
          }
        }
      }

      &.career {
        .title2 {
          letter-spacing: 0.2rem;
          font-size: 40px;
        }

        .list {
          margin-top: 12px;
          display: flex;
          flex-direction: column;

          .list-item {
            display: flex;
            flex-direction: row;
            align-items: center;
            margin-bottom: 12px;
            color: #fff;
            z-index: 2;

            &::before {
              content: "";
              display: block;
              width: 16px;
              height: 16px;
              background-color: var(--color);
              border-radius: 50%;
              margin-right: 8px;
            }
          }
        }

        .career-img {
          position: absolute;
          bottom: -10px;
          left: 0;
          width: 100%;

          @media (max-width: 768px) {
            position: static;
          }
        }
      }

      &.game {
        min-height: 300px;

        @media (max-width: 768px) {
          min-height: 240px;
        }
      }

      &.like {
        min-height: 400px;

        @media (max-width: 768px) {
          min-height: 300px;
        }
      }

      &.image {
        background-position: center;
        background-size: cover;
        background-repeat: no-repeat;

        .image-content {
          flex-grow: 1;
          display: flex;
          flex-direction: column;
          z-index: 2;
          color: #fff;

          .image-desc {
            width: 100%;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            margin-top: auto;

            &.opacity {
              font-size: 14px;
              color: #eee;
              opacity: 0.8;

              a {
                color: #eee;

                &:hover {
                  color: var(--main-color);
                }
              }
            }
          }
        }

        &::after {
          content: "";
          position: absolute;
          width: 100%;
          height: 100%;
          top: 0;
          left: 0;
          background-color: var(--color);
          backdrop-filter: blur(1px);
          -webkit-backdrop-filter: blur(2px);
          z-index: 0;
        }

        &.map::after,
        &.static::after {
          backdrop-filter: none;
          -webkit-backdrop-filter: none;
        }
      }

      &.static {
        .static-data {
          display: grid;
          gap: 12px;
          grid-template-columns: 1fr 1fr;
          margin: 20px 0;

          .static-item {
            display: flex;
            flex-direction: column;

            .static-name {
              font-size: 15px;
              opacity: 0.8;
            }

            .static-num {
              font-size: 34px;
              font-weight: bold;
            }
          }
        }
      }

      &.map {
        min-height: 170px;
        background-size: 100%;
        transition: background 1.5s ease-in-out;
        cursor: pointer;

        @media (max-width: 768px) {
          background-size: cover;
          pointer-events: none;
        }

        .position {
          display: block;
          position: absolute;
          left: 0;
          bottom: 0;
          width: 100%;
          padding: 20px 30px;
          color: #fff;
          background-color: #636352;
          font-size: 20px;
          transition: bottom 1s;
        }

        &:hover {
          background-size: 120%;
          background-position-x: 0;
          background-position-y: 36%;

          .position {
            bottom: -80px;
          }
        }
      }

      &.info {
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;

        .info-item {
          display: flex;
          flex-direction: column;
          margin-right: 32px;

          .info-name {
            font-size: 14px;
            margin-bottom: 8px;
            color: var(--main-font-second-color);
          }

          .info-num {
            font-size: 34px;
            font-weight: bold;
            color: var(--color);
          }
        }
      }
    }

    &:last-child {
      margin-bottom: 0;
    }

    @media (max-width: 768px) {
      display: flex;
      flex-direction: column;
    }
  }
}
</style>
