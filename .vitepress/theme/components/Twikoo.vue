<script setup>
import { onMounted } from 'vue';


const props = defineProps({
    envId: {
        type: String,
        required: true
    }
});

onMounted(() => {
    import('twikoo').then((twikoo) => {
        twikoo.init({
            envId: props.envId,
            el: '#twikoo',
            lang: 'zh-CN', // 强制中文
        });
    });
});
</script>

<template>
    <div class="comment-container">
        <!-- 标题区域 -->
        <div class="comment-header">
            <i class="iconfont icon-message" />
            <span>留言板</span>
        </div>
        <div id="twikoo"></div>
    </div>
</template>

<style lang="scss" scoped>
.comment-container {
    margin-top: 2rem;
    padding: 2rem;
    background-color: var(--main-card-background);
    border: 1px solid var(--main-card-border);
    border-radius: 12px;
    box-shadow: 0 8px 16px -4px var(--main-border-shadow);
    transition: all 0.3s;
    animation: fade-in 0.5s ease;

    &:hover {
        box-shadow: 0 8px 24px -8px var(--main-border-shadow);
    }

    .comment-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        color: var(--main-font-color);
        padding-bottom: 1rem;
        border-bottom: 1px dashed var(--main-card-border);

        .iconfont {
            font-size: 1.5rem;
            color: var(--main-color);
        }
    }
}

@keyframes fade-in {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Twikoo 样式深度适配 */
:deep(.tk-meta-input) {
    background-color: var(--main-card-second-background);
    border: 1px solid var(--main-card-border);
    border-radius: 8px;

    .el-input__inner {
        background: transparent !important;
        color: var(--main-font-color) !important;
        border: none !important;
    }

    .el-input-group__append {
        background: transparent !important;
        border: none !important;
        color: var(--main-font-second-color) !important;
    }
}

:deep(.tk-content) {
    color: var(--main-font-color) !important;
    background-color: var(--main-card-second-background) !important;
    border-radius: 8px !important;
    padding: 10px 15px !important;
    margin-top: 10px;
}

:deep(.tk-submit-action-icon) {
    color: var(--main-color) !important;
}

:deep(.tk-action-link) {
    color: var(--main-font-second-color) !important;
}

:deep(.tk-avatar) {
    border: 1px solid var(--main-card-border);
    background-color: var(--main-card-background);
}

:deep(.tk-nick) {
    color: var(--main-font-color) !important;
    font-weight: bold;
}

:deep(.tk-time) {
    color: var(--main-font-second-color) !important;
}
</style>
