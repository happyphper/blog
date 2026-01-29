<!-- 全局搜索 -->
<template>
    <Modal :show="store.searchShow" :mask="true" title="全局搜索" titleIcon="search" @mask-click="closeSearch"
        @modal-close="closeSearch">
        <div class="local-search">
            <div class="search-box">
                <input ref="searchInputRef" v-model="searchQuery" type="text" placeholder="想要搜点什么" autofocus
                    class="search-input" @keydown.esc="closeSearch"
                    @keydown.enter="filteredResults.length && jumpSearch(filteredResults[0].regularPath)" />
            </div>
            <Transition name="fade" mode="out-in">
                <div v-if="hasSearchValue" class="search-results">
                    <div v-if="filteredResults.length" class="search-list">
                        <div v-for="(item, index) in filteredResults" :key="index" class="search-item s-card hover"
                            @click="jumpSearch(item.regularPath)">
                            <p class="title" v-html="highlight(item.title)" />
                            <div class="meta-info">
                                <span v-if="item.categories" class="category">
                                    <i class="iconfont icon-folder" />
                                    {{ item.categories }}
                                </span>
                                <span v-if="item.date" class="date">
                                    <i class="iconfont icon-date" />
                                    {{ formatDate(item.date) }}
                                </span>
                            </div>
                            <p v-if="item.description" class="content s-card" v-html="highlight(item.description)" />
                        </div>
                    </div>
                    <div v-else class="no-result">
                        <i class="iconfont icon-search-empty" />
                        <span class="text">搜索结果为空</span>
                    </div>
                </div>
                <div v-else class="search-tip">
                    <i class="iconfont icon-search" />
                    <span class="text">输入关键词开始搜索</span>
                </div>
            </Transition>
            <div class="information">
                <span v-if="hasSearchValue" class="text"> 找到 {{ filteredResults.length }} 条结果 </span>
                <div class="power">
                    <i class="iconfont icon-technical" />
                    <span class="name">本地搜索</span>
                </div>
            </div>
        </div>
    </Modal>
</template>

<script setup>
import { mainStore } from "@/store";
import { formatDate } from "@/utils/timeTools";

const store = mainStore();
const router = useRouter();
const { theme } = useData();

const searchQuery = ref("");
const searchInputRef = ref(null);

// 监听搜索框开启状态
watch(
    () => store.searchShow,
    (val) => {
        if (val) {
            nextTick(() => {
                searchInputRef.value?.focus();
            });
        }
    }
);

// 是否具有搜索词
const hasSearchValue = computed(() => searchQuery.value.trim().length > 0);

// 搜索过滤逻辑
const filteredResults = computed(() => {
    if (!hasSearchValue.value) return [];
    const query = searchQuery.value.toLowerCase().trim();
    const results = (theme.value.postData || []).filter((post) => {
        // 基础信息匹配
        const isTitleMatch = post.title?.toLowerCase().includes(query);
        const isDescMatch = post.description?.toLowerCase().includes(query);

        // 标签匹配 (处理数组)
        const tags = Array.isArray(post.tags) ? post.tags.join(" ") : post.tags || "";
        const isTagsMatch = tags.toLowerCase().includes(query);

        // 分类匹配 (处理数组)
        const categories = Array.isArray(post.categories) ? post.categories.join(" ") : post.categories || "";
        const isCategoriesMatch = categories.toLowerCase().includes(query);

        return isTitleMatch || isDescMatch || isTagsMatch || isCategoriesMatch;
    });
    return results;
});

// 高亮关键词
const highlight = (text) => {
    if (!text) return "";
    if (!hasSearchValue.value) return text;
    const query = searchQuery.value.trim();
    const reg = new RegExp(`(${query})`, "gi");
    return text.replace(reg, '<mark>$1</mark>');
};

// 跳转搜索结果
const jumpSearch = (url) => {
    store.changeShowStatus("searchShow");
    router.go(url);
    searchQuery.value = "";
};

// 关闭搜索
const closeSearch = () => {
    store.changeShowStatus("searchShow");
    searchQuery.value = "";
};

onBeforeUnmount(() => {
    searchQuery.value = "";
});
</script>

<style lang="scss" scoped>
.local-search {
    height: 100%;
    display: flex;
    flex-direction: column;

    .search-box {
        margin-bottom: 20px;

        .search-input {
            width: 100%;
            height: 45px;
            outline: none;
            border-radius: 12px;
            font-size: 16px;
            padding: 0 1.2rem;
            color: var(--main-font-color);
            font-family: var(--main-font-family);
            border: 1px solid var(--main-card-border);
            background-color: var(--main-card-second-background);
            transition: all 0.3s;

            &:focus {
                border-color: var(--main-color);
                box-shadow: 0 8px 16px -4px var(--main-color-bg);
            }
        }
    }

    .search-results,
    .search-tip {
        min-height: 300px;
        max-height: 60vh;
        overflow-y: auto;
        padding-right: 4px;

        &::-webkit-scrollbar {
            width: 4px;
        }

        &::-webkit-scrollbar-thumb {
            background: var(--main-card-border);
            border-radius: 10px;
        }
    }

    .search-tip,
    .no-result {
        height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        opacity: 0.6;

        .iconfont {
            font-size: 48px;
            margin-bottom: 16px;
        }

        .text {
            font-size: 16px;
        }
    }

    .search-list {
        .search-item {
            padding: 1rem;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.3s;

            .title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 8px;
                color: var(--main-color);
            }

            .meta-info {
                display: flex;
                gap: 12px;
                font-size: 13px;
                margin-bottom: 8px;
                opacity: 0.7;

                .iconfont {
                    font-size: 14px;
                    margin-right: 4px;
                }
            }

            .content {
                background-color: var(--main-card-second-background);
                padding: 8px 12px;
                border-radius: 8px;
                font-size: 14px;
                line-height: 1.6;
                opacity: 0.9;
            }

            :deep(mark) {
                background-color: var(--main-color);
                color: #fff;
                padding: 0 2px;
                border-radius: 2px;
            }

            &:hover {
                transform: translateY(-2px);
                border-color: var(--main-color);
            }
        }
    }

    .information {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid var(--main-card-border);
        opacity: 0.8;
        font-size: 14px;

        .power {
            display: flex;
            align-items: center;
            gap: 4px;
            opacity: 0.6;

            .iconfont {
                font-size: 18px;
            }

            .name {
                font-weight: bold;
            }
        }
    }
}
</style>
