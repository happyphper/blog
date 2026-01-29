<!-- 随机文章悬浮按钮 -->
<template>
    <div class="random-post">
        <div class="shuffle-btn s-card" @click="router.go(shufflePost(theme.postData))">
            <i class="iconfont icon-shuffle"></i>
            <span class="shuffle-text">随机文章</span>
        </div>
    </div>
</template>

<script setup>
import { shufflePost } from "@/utils/helper";

const router = useRouter();
const { theme } = useData();
</script>

<style lang="scss" scoped>
.random-post {
    .shuffle-btn {
        position: relative;
        display: flex;
        flex-direction: row-reverse;
        align-items: center;
        width: 42px;
        height: 42px;
        min-width: 42px;
        max-width: 42px;
        padding: 0 !important;
        margin-top: 10px;
        border-radius: 40px;
        background-color: var(--main-card-background);
        border: 1px solid var(--main-card-border);
        box-shadow: 0 4px 12px -2px var(--main-dark-shadow);
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;

        .iconfont {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            font-size: 20px;
            color: var(--main-font-color);
            transition: color 0.3s;
        }

        .shuffle-text {
            width: 0;
            opacity: 0;
            font-size: 14px;
            font-weight: bold;
            color: #fff;
            white-space: nowrap;
            transition: all 0.3s;
            margin-right: 0;
        }

        &:hover {
            max-width: 120px;
            width: 120px;
            background-color: var(--main-color);
            border-color: var(--main-color);

            .iconfont {
                color: #fff;
            }

            .shuffle-text {
                width: 70px;
                opacity: 1;
                margin-left: 1rem;
            }
        }
    }
}
</style>
