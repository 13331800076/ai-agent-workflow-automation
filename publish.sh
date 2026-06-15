#!/bin/bash
# =============================================================================
# AI Agent Workflow — GitHub 全自动发布脚本
# =============================================================================
# 这个脚本自动完成：
#   1. 创建 GitHub 仓库（如果不存在）
#   2. 设置 Topics 标签
#   3. 替换 README 用户名
#   4. 推送代码到 main 分支
#   5. 打印后续优化清单
#
# 前置要求（二选一）：
#   A) 已安装 gh CLI 并登录：gh auth login
#   B) 设置环境变量：export GITHUB_TOKEN=你的Token
#
# 使用方式：
#   cd /Users/harryyu/ai-agent-workflow-automation
#   bash publish.sh
# =============================================================================

set -e

USERNAME="13331800076"
REPO_NAME="ai-agent-workflow-automation"
REPO_DIR="/Users/harryyu/ai-agent-workflow-automation"
REMOTE_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"
API_URL="https://api.github.com/repos/${USERNAME}/${REPO_NAME}"

echo "========================================"
echo "  🚀 GitHub 全自动发布脚本"
echo "========================================"
echo ""

cd "${REPO_DIR}"

# 检查 gh CLI 是否可用
USE_GH=false
if command -v gh &>/dev/null; then
    if gh auth status &>/dev/null; then
        USE_GH=true
        echo "✅ 检测到 gh CLI 已登录"
    else
        echo "⚠️  gh CLI 已安装但未登录"
    fi
else
    echo "⚠️  未检测到 gh CLI"
fi

# 如果没有 gh，检查 GITHUB_TOKEN
if [ "$USE_GH" = false ]; then
    if [ -z "$GITHUB_TOKEN" ]; then
        echo ""
        echo "❌ 错误：没有可用的 GitHub 认证方式"
        echo ""
        echo "请二选一："
        echo ""
        echo "  选项 A：安装 gh CLI 并登录（推荐）"
        echo "    brew install gh"
        echo "    gh auth login"
        echo ""
        echo "  选项 B：设置 Token 环境变量"
        echo "    export GITHUB_TOKEN=ghp_你的Token"
        echo "    bash publish.sh"
        echo ""
        exit 1
    else
        echo "✅ 检测到 GITHUB_TOKEN 环境变量"
    fi
fi

echo ""

# 检查仓库是否已存在
echo "🔍 检查 GitHub 仓库是否已存在..."
if [ "$USE_GH" = true ]; then
    if gh repo view "${USERNAME}/${REPO_NAME}" &>/dev/null; then
        REPO_EXISTS=true
    else
        REPO_EXISTS=false
    fi
else
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token ${GITHUB_TOKEN}" "${API_URL}")
    if [ "$HTTP_STATUS" = "200" ]; then
        REPO_EXISTS=true
    else
        REPO_EXISTS=false
    fi
fi

# 创建仓库（如果不存在）
if [ "$REPO_EXISTS" = true ]; then
    echo "✅ 仓库已存在，跳过创建"
else
    echo "📝 创建 GitHub 仓库..."
    if [ "$USE_GH" = true ]; then
        gh repo create "${REPO_NAME}" --public --description "A production-style AI agent workflow engine for automating ERP-like web operations with Playwright, tool calling, and audit trails." --source=. --remote=origin --push
        echo "✅ 仓库创建并推送完成"
        exit 0
    else
        curl -s -X POST \
            -H "Authorization: token ${GITHUB_TOKEN}" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/user/repos \
            -d "{\"name\":\"${REPO_NAME}\",\"description\":\"A production-style AI agent workflow engine for automating ERP-like web operations with Playwright, tool calling, and audit trails.\",\"private\":false,\"has_issues\":true,\"has_projects\":false,\"has_wiki\":false}" \
            > /dev/null
        echo "✅ 仓库创建成功"
    fi
fi

# 设置 Topics 标签
if [ "$REPO_EXISTS" = false ]; then
    echo "🏷️  设置 Topics 标签..."
    TOPICS='{"names":["ai-agent","playwright","fastapi","workflow-automation","llm-agent","python","automation","rpa","erp","crm"]}'
    if [ "$USE_GH" = true ]; then
        gh api "repos/${USERNAME}/${REPO_NAME}/topics" -X PUT --input - <<< "$TOPICS" &>/dev/null || true
    else
        curl -s -X PUT \
            -H "Authorization: token ${GITHUB_TOKEN}" \
            -H "Accept: application/vnd.github.mercy-preview+json" \
            "${API_URL}/topics" \
            -d "$TOPICS" \
            > /dev/null || true
    fi
    echo "✅ Topics 已设置"
fi

# 替换 README 用户名
echo "📝 检查 README..."
if grep -q "USERNAME" README.md; then
    sed -i '' "s/USERNAME/${USERNAME}/g" README.md
    git add README.md
    git commit -m "docs: update GitHub username and badges" || true
    echo "✅ README 已更新"
else
    echo "✅ README 已包含正确用户名"
fi

# 配置远程仓库
if git remote get-url origin &>/dev/null; then
    CURRENT_URL=$(git remote get-url origin)
    if [ "$CURRENT_URL" != "$REMOTE_URL" ]; then
        echo "📝 更新远程仓库 URL..."
        git remote set-url origin "${REMOTE_URL}"
    fi
else
    echo "📝 添加远程仓库..."
    git remote add origin "${REMOTE_URL}"
fi

# 推送
echo "🚀 推送到 GitHub..."
if git push -u origin main; then
    echo ""
    echo "========================================"
    echo "✅ 发布成功！"
    echo "========================================"
    echo ""
    echo "📎 仓库地址：${REMOTE_URL}"
    echo ""
    echo "📌 下一步（在网页上完成）："
    echo "   1. 打开 ${REMOTE_URL}"
    echo "   2. 点击 Settings → Pages → 选择 main 分支（可启用 GitHub Pages）"
    echo "   3. 生成 Demo GIF 放 README 首屏"
    echo "   4. 去掘金/知乎/CSDN 发文章引流"
    echo ""
    echo "⚠️  安全提醒："
    echo "   如果之前暴露过 Token，请去 https://github.com/settings/tokens 撤销！"
    echo ""
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能原因："
    echo "   1. Token 权限不足（需要 repo 权限）"
    echo "   2. 网络问题"
    echo "   3. 分支冲突"
    echo ""
    echo "请检查后重试："
    echo "   bash publish.sh"
    echo ""
    exit 1
fi
