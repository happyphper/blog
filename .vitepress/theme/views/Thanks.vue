<template>
    <div class="thanks">
        <Banner type="page" title="打赏名单" desc="感谢各位大佬的慷慨支持"
            image="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?q=80&w=1200" footer="你们的认可，是我持续创作的最大动力。"
            text-color="dark">
            <template v-slot:header-slot>
                <div class="menu">
                    <div class="menu-item reward" @click="store.changeShowStatus('rewardShow')">
                        <i class="iconfont icon-reward" />
                        <span class="name">赞赏博主</span>
                    </div>
                </div>
            </template>

        </Banner>
        <div class="thanks-content">
            <div v-for="(item, index) in thanksData" :key="index" class="flip-container">
                <div class="flip-inner">
                    <!-- 正面 -->
                    <div class="thanks-item front">
                        <div class="info">
                            <div class="header">
                                <span class="name">{{ item.name }}</span>
                                <span class="amount" :style="{ backgroundColor: getColorByAmount(item.amount) }">￥{{
                                    item.amount
                                    }}</span>
                            </div>
                            <div class="detail">
                                <span class="remark" v-if="item.remark" :title="item.remark">{{ item.remark }}</span>
                                <span class="date">{{ item.date }}</span>
                            </div>
                        </div>
                    </div>
                    <!-- 背面 -->
                    <div class="thanks-item back">
                        <div class="full-remark">
                            {{ item.remark || '这位大佬很低调，什么也没留下~' }}
                        </div>
                    </div>
                </div>
            </div>
            <!-- 引导卡片 -->
            <div class="thanks-item action" @click="store.changeShowStatus('rewardShow')">
                <div class="info">
                    <div class="header">
                        <span class="name">如何出现在这里？</span>
                        <span class="amount">
                            <span class="like-anim">👍</span>
                        </span>
                    </div>
                    <div class="detail">
                        <span class="remark" style="max-width: 100%">扫码赞赏后，由博主核实后为您上榜</span>
                    </div>
                </div>
            </div>
        </div>
        <!-- 留言板 -->
        <Twikoo envId="https://twikoo.longbao.wang" />
    </div>
</template>

<script setup>
import { mainStore } from "@/store";
import Twikoo from '../components/Twikoo.vue';
const { theme } = useData();
const store = mainStore();

// 致谢名单
// 获取颜色
const getColorByAmount = (amount) => {
    if (amount < 10) return "#7eb7f5"; // 浅蓝
    if (amount >= 10 && amount < 50) return "#357ef5"; // 深蓝
    if (amount >= 50 && amount < 100) return "#ffb802"; // 金色
    if (amount >= 100 && amount < 1000) return "#ff3e4d"; // 红色
    if (amount >= 1000) return "#8e44ad"; // 紫色（至尊）
    return "#357ef5";
};

// 致谢名单 (模拟数据)
const thanksData = [
    { name: "*笙", amount: 1.99, date: "2024/12/06", remark: "加油" },
];
</script>

<style lang="scss" scoped>
.thanks {
    margin-bottom: 4rem;

    .menu {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        align-items: flex-start;
        margin-bottom: auto;

        .menu-item {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 46px;
            padding: 12px 24px;
            border-radius: 12px;
            background-color: #ff3e4d;
            color: #fff;
            font-weight: bold;
            border: none;
            box-shadow: 0 4px 12px rgba(255, 62, 77, 0.3);
            transition: all 0.3s;
            cursor: pointer;

            .iconfont {
                font-size: 20px;
                margin-right: 8px;
                color: #fff;
            }

            &:hover {
                background-color: #ff525f;
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(255, 62, 77, 0.4);
            }
        }
    }

    .info-card {
        max-width: 500px;
        max-width: 500px;
        padding: 0.8rem 1.2rem;
        background-color: var(--main-card-background);
        border-radius: 12px;
        border: 1px solid var(--main-card-border);
        box-shadow: 0 4px 12px var(--main-border-shadow);
        position: relative;
        z-index: 1;
        color: var(--main-font-color);
        animation: border-flash 3s infinite ease-in-out;

        .title {
            font-size: 1rem;
            font-weight: bold;
            margin-bottom: 8px;
            color: var(--main-color);
            display: flex;
            align-items: center;
            gap: 8px;

            .like-anim {
                color: #ff3e4d;
                display: inline-block;
                animation: like-bounce 0.8s ease infinite;
            }
        }

        .desc {
            font-size: 0.85rem;
            line-height: 1.6;
            opacity: 0.8;

            strong {
                color: #ff3e4d;
            }
        }
    }

    .thanks-content {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 20px;
        margin-top: 2rem;

        .empty {
            grid-column: 1 / -1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 4rem 1rem;
            gap: 3rem;

            .empty-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                opacity: 0.6;
                gap: 16px;

                .iconfont {
                    font-size: 3rem;
                    color: #ff3e4d;
                }

                .text {
                    font-size: 1.25rem;
                    letter-spacing: 4px;
                }
            }
        }

        .thanks-item {
            padding: 1.5rem;
            border-radius: 12px;
            background-color: var(--main-card-background);
            border: 1px solid var(--main-card-border);
            box-shadow: 0 8px 16px -4px var(--main-border-shadow);
            transition: all 0.3s;

            &.skeleton {
                pointer-events: none;
                background-color: var(--main-card-second-background);

                .skeleton-name,
                .skeleton-amount,
                .skeleton-date {
                    background: linear-gradient(90deg,
                            var(--main-card-border) 25%,
                            var(--main-card-second-background) 37%,
                            var(--main-card-border) 63%);
                    background-size: 400% 100%;
                    animation: skeleton-loading 1.4s ease infinite;
                    border-radius: 4px;
                }

                .skeleton-name {
                    height: 1.2rem;
                    width: 40%;
                }

                .skeleton-amount {
                    height: 1.5rem;
                    width: 30%;
                    border-radius: 20px;
                }

                .skeleton-date {
                    height: 0.8rem;
                    width: 25%;
                }
            }
        }

        .flip-container {
            perspective: 1000px;

            &:hover .flip-inner {
                transform: rotateY(180deg);
            }

            .flip-inner {
                position: relative;
                width: 100%;
                height: 100%;
                text-align: center;
                transition: transform 0.6s;
                transform-style: preserve-3d;
            }

            .thanks-item.front {
                position: relative;
                z-index: 2;
                backface-visibility: hidden;
            }

            .thanks-item.back {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transform: rotateY(180deg);
                backface-visibility: hidden;

                display: flex;
                align-items: center;
                justify-content: center;
                background-color: var(--main-card-second-background);

                .full-remark {
                    padding: 1rem;
                    font-size: 0.95rem;
                    line-height: 1.5;
                    color: var(--main-font-color);
                    word-break: break-all;
                }
            }
        }

        .thanks-item {
            padding: 1.5rem;
            border-radius: 12px;
            background-color: var(--main-card-background);
            border: 1px solid var(--main-card-border);
            box-shadow: 0 8px 16px -4px var(--main-border-shadow);
            transition: all 0.3s;
            height: 100%;
            /* 确保高度撑满 */

            &.action {
                cursor: pointer;
                border: 1px dashed var(--main-color);
                animation: border-flash 3s infinite ease-in-out;

                &:hover {
                    border-style: solid;
                    background-color: var(--main-card-second-background);
                }

                .amount {
                    padding: 2px 8px !important;
                    background-color: transparent !important;
                    box-shadow: none !important;

                    .like-anim {
                        display: inline-block;
                        animation: like-bounce 0.8s ease infinite;
                    }
                }
            }

            &:hover {
                box-shadow: 0 8px 24px -8px var(--main-border-shadow);
            }

            .info {
                display: flex;
                flex-direction: column;
                gap: 8px;

                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;

                    .name {
                        font-size: 1.1rem;
                        font-weight: bold;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        max-width: 60%;
                    }

                    .amount {
                        padding: 2px 10px;
                        border-radius: 20px;
                        color: #fff;
                        font-size: 0.8rem;
                        font-weight: bold;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    }
                }

                .detail {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    gap: 8px;
                    margin-top: 4px;

                    .remark {
                        font-size: 0.85rem;
                        color: var(--main-font-second-color);
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        max-width: 60%;
                        cursor: help;
                    }

                    .date {
                        font-size: 0.75rem;
                        opacity: 0.5;
                        margin-left: auto;
                    }
                }
            }
        }
    }
}

@keyframes skeleton-loading {
    0% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0 50%;
    }
}

@keyframes border-flash {

    0%,
    100% {
        box-shadow: 0 4px 12px var(--main-border-shadow);
        border-color: var(--main-card-border);
    }

    50% {
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.4), 0 0 5px rgba(255, 255, 255, 0.8);
        border-color: rgba(255, 215, 0, 0.8);
    }
}

@keyframes like-bounce {

    0%,
    100% {
        transform: scale(1) rotate(0deg);
    }

    50% {
        transform: scale(1.3) rotate(-15deg);
    }
}
</style>
