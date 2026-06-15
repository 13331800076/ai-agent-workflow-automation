#!/bin/bash
# =============================================================================
# GitHub Push Helper Script
# =============================================================================
# 这个脚本帮你把本地项目推送到 GitHub 远程仓库。
# 运行前请确保：
#   1. 你已经在 GitHub 创建了一个空仓库（不要初始化 README）
#   2. 仓库名：ai-agent-workflow-automation
#   3. 仓库地址：https://github.com/13331800076/ai-agent-workflow-automation
#
# 使用方式：
#   cd /Users/harryyu/ai-agent-workflow-automation
#   bash push_to_github.sh
#
# 如果提示输入密码，请输入你的 GitHub Personal Access Token（不是登录密码）
# =============================================================================

set -e  # 遇到错误立即退出

REPO_DIR="/Users/harryyu/ai-agent-workflow-automation"
USERNAME="13331800076"
REPO_NAME="ai-agent-workflow-automation"
REMOTE_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

echo "========================================"
echo "  AI Agent Workflow Automation 推送助手"
echo "========================================"
echo ""

# 检查是否在正确目录
if [ ! -d "${REPO_DIR}" ]; then
    echo "❌ 错误：找不到项目目录 ${REPO_DIR}"
    echo "   请确认路径正确，或修改脚本中的 REPO_DIR 变量"
    exit 1
fi

cd "${REPO_DIR}"

# 检查是否有 Git 仓库
if [ ! -d ".git" ]; then
    echo "❌ 错误：当前目录不是 Git 仓库"
    exit 1
fi

# 替换 README 中的占位符
if grep -q "USERNAME" README.md; then
    echo "📝 替换 README 中的用户名占位符..."
    sed -i '' "s/USERNAME/${USERNAME}/g" README.md
    git add README.md
    git commit -m "docs: update GitHub username in README and badges" || true
    echo "✅ README 已更新"
else
    echo "✅ README 用户名已替换，跳过"
fi

echo ""

# 配置远程仓库
if git remote get-url origin &>/dev/null; then
    echo "📝 检测到已有远程仓库 origin，更新 URL..."
    git remote set-url origin "${REMOTE_URL}"
else
    echo "📝 添加远程仓库 origin..."
    git remote add origin "${REMOTE_URL}"
fi
echo "✅ 远程仓库：${REMOTE_URL}"

echo ""

# 推送
# 注意：如果这是首次推送，git 会提示你输入用户名和密码
# 用户名：你的 GitHub 用户名（13331800076）
# 密码：你的 Personal Access Token（不是 GitHub 登录密码）
echo "🚀 推送到 GitHub..."
echo ""
echo "   💡 提示：如果要求输入密码，请输入你的 GitHub Personal Access Token"
echo "      （不是 GitHub 登录密码！）"
echo ""

git push -u origin main

echo ""
echo "========================================"
echo "✅ 推送完成！"
echo "========================================"
echo ""
echo "查看仓库：${REMOTE_URL}"
echo ""
echo "⚠️  重要安全提醒："
echo "   如果你之前在任何地方（包括聊天）暴露过 GitHub Token，"
echo "   请立即前往 https://github.com/settings/tokens 撤销并重新生成。"
echo ""
echo "📌 推送到 GitHub 后的下一步："
echo "   1. 打开 ${REMOTE_URL}"
echo "   2. 点击右侧 'About' 旁边的 ⚙️ 图标，添加 Topics："
echo "      ai-agent, playwright, fastapi, workflow-automation, llm-agent, python"
echo "   3. 在网页上生成一个 30 秒 GIF 放 README 首屏（推荐 ScreenStudio 或 LICEcap）"
echo "   4. 在掘金/知乎/CSDN 发文章，标题建议："
echo "      《从零构建可测试的 AI Agent 工作流：Playwright + FastAPI 实战》"
echo ""
