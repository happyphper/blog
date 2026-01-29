#!/bin/bash

# ================= 配置区域 =================
# 1. 设置您的 GitHub 仓库信息
USER="happyphper"        # 您的 GitHub 用户名
REPO="blog"              # 您的仓库名称
FILE="dist.zip"          # 构建产物的文件名 (与 workflow 中一致)

# 2. 设置网站根目录 (请修改为您实际的网站目录)
WEB_PATH="/www/wwwroot/www.longbao.wang"

# 3. 临时下载目录
TEMP_DIR="/www/server/temp_download"
# ===========================================

echo "====== 开始自动部署 ======"
date "+%Y-%m-%d %H:%M:%S"

# 创建临时目录
mkdir -p $TEMP_DIR
cd $TEMP_DIR

# 1. 获取最新 Release 版本号
# 使用 GitHub API 获取 latest release tag
echo "正在获取最新版本信息..."
LATEST_TAG=$(curl -s "https://api.github.com/repos/$USER/$REPO/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$LATEST_TAG" ]; then
    echo "❌ 获取版本号失败，请检查网络或仓库权限"
    exit 1
fi

echo "发现最新版本: $LATEST_TAG"

# 2. 构造下载链接
# 格式: https://github.com/用户名/仓库名/releases/download/Tag/文件名
DOWNLOAD_URL="https://github.com/$USER/$REPO/releases/download/$LATEST_TAG/$FILE"

# 如果国内下载慢，可以使用加速节点 (可选)
# DOWNLOAD_URL="https://ghproxy.com/$DOWNLOAD_URL"

echo "下载地址: $DOWNLOAD_URL"

# 3. 下载文件
echo "正在下载构建产物..."
wget -O $FILE $DOWNLOAD_URL

if [ ! -f "$FILE" ]; then
    echo "❌ 下载失败"
    exit 1
fi

echo "✅ 下载成功"

# 4. 解压并部署
echo "正在部署到网站目录: $WEB_PATH"

# 确保目标目录存在
if [ ! -d "$WEB_PATH" ]; then
    mkdir -p "$WEB_PATH"
fi

# 解压覆盖 (使用 -o 覆盖，-d 指定目录)
unzip -o $FILE -d $WEB_PATH

# 5. 清理临时文件
rm -f $FILE
echo "✅ 部署完成！"
echo "========================="
