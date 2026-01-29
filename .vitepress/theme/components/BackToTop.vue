<!-- 返回顶部悬浮按钮 -->
<template>
    <div v-show="scrollData.height > 50" class="back-to-top">
        <div class="top-btn s-card" @click="smoothScrolling">
            <i class="iconfont icon-up"></i>
            <span class="top-text">返回顶部</span>
        </div>
    </div>
</template>

<script setup>
import { storeToRefs } from "pinia";
import { mainStore } from "@/store";
import { smoothScrolling } from "@/utils/helper";

const store = mainStore();
const { scrollData } = storeToRefs(store);
</script>

<style lang="scss" scoped>
.back-to-top {
    .top-btn {
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
            font-size: 1rem;
            color: var(--main-font-color);
            transition: color 0.3s;
        }

        .top-text {
            width: 0;
            opacity: 0;
            font-size: 14px;
            font-weight: bold;
            color: #fff;
            white-space: nowrap;
            transition: all 0.3s;
            margin-right: 0;
            text-align: center;
        }

        &:hover {
            max-width: 120px;
            width: 120px;
            background-color: var(--main-color);
            border-color: var(--main-color);

            .iconfont {
                color: #fff;
            }

            .top-text {
                width: 100px;
                opacity: 1;
                margin-left: 1rem;
                text-align: center;
            }
        }
    }
}
</style>
