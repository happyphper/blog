<template>
    <Modal :show="rewardShow" title="赞赏博主" @modal-close="store.changeShowStatus('rewardShow')"
        @mask-click="store.changeShowStatus('rewardShow')">
        <div class="reward-content">
            <p class="tip">如果觉得本站对你有帮助，可以请博主喝杯咖啡哦~ ☕️</p>
            <div class="qr-codes">
                <div class="qr-item">
                    <img :src="theme.rewardData.wechat" alt="微信赞赏" class="qr-img" />
                    <span class="name">微信</span>
                </div>
                <div class="qr-item">
                    <img :src="theme.rewardData.alipay" alt="支付宝赞赏" class="qr-img" />
                    <span class="name">支付宝</span>
                </div>
            </div>
            <p class="footer-tip">非常感谢您的支持与厚爱！</p>
        </div>
    </Modal>
</template>

<script setup>
import { storeToRefs } from "pinia";
import { mainStore } from "@/store";

const store = mainStore();
const { thematic, theme } = useData();
const { rewardShow } = storeToRefs(store);
</script>

<style lang="scss" scoped>
.reward-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;

    .tip {
        font-size: 15px;
        opacity: 0.8;
        margin-bottom: 20px;
        text-align: center;
    }

    .qr-codes {
        display: flex;
        flex-direction: row;
        gap: 30px;
        margin-bottom: 20px;

        .qr-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;

            .qr-img {
                width: 280px;
                height: 280px;
                background-color: #fff;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid var(--main-card-border);
            }

            .name {
                font-weight: bold;
                font-size: 14px;
            }
        }

        @media (max-width: 500px) {
            flex-direction: column;
            gap: 20px;

            .qr-item .qr-img {
                width: 160px;
                height: 160px;
            }
        }
    }

    .footer-tip {
        font-size: 13px;
        opacity: 0.6;
        margin-top: 10px;
    }
}
</style>
