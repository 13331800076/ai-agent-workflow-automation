#!/bin/bash
# =============================================================================
# 🚀 AI Agent Workflow Automation — GitHub 全自动发布脚本
# =============================================================================
# 功能：自动创建 GitHub 仓库 → 设置 Topics → 推送代码 → 验证
#
# 前置条件（二选一）：
#   方案 A: 安装并登录 gh CLI 工具
#     brew install gh   # macOS
#     gh auth login
#
#   方案 B: 设置环境变量
#     export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
#
# 运行方式：
#   cd /Users/harryyu/ai-agent-workflow-automation
#   bash push_to_github.sh
# =============================================================================

set -e

# ─── 配置 ───────────────────────────────────────────────────────────────────
REPO_DIR="/Users/harryyu/ai-agent-workflow-automation"
USERNAME="13331800076"
REPO_NAME="ai-agent-workflow-automation"
REMOTE_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"
TOPICS='["ai-agent","playwright","fastapi","workflow-automation","llm-agent","python","automation","rpa"]'

# ─── 颜色输出 ─────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()  { echo -e "${BLUE}ℹ️  $1${NC}"; }
succ()  { echo -e "${GREEN}✅ $1${NC}"; }
warn()  { echo -e "${YELLOW}⚠️  $1${NC}"; }
err()   { echo -e "${RED}❌ $1${NC}"; }

# ─── 检查目录 ─────────────────────────────────────────────────────────────
if [ ! -d "${REPO_DIR}" ]; then
    err "找不到项目目录 ${REPO_DIR}"
    exit 1
fi

cd "${REPO_DIR}"

# ─── 检查 Git ─────────────────────────────────────────────────────────────
if [ ! -d ".git" ]; then
    err "当前目录不是 Git 仓库"
    exit 1
fi

# ─── 替换 README 用户名 ─────────────────────────────────────────────────────
if grep -q "USERNAME" README.md; then
    info "替换 README 中的用户名占位符..."
    sed -i '' "s/USERNAME/${USERNAME}/g" README.md
    git add README.md
    git commit -m "docs: update GitHub username and badges" || true
    succ "README 已更新"
else
    succ "README 用户名已替换，跳过"
fi

# ─── 检测认证方式 ─────────────────────────────────────────────────────────
AUTH_METHOD=""

if command -v gh &> /dev/null && gh auth status &> /dev/null; then
    AUTH_METHOD="gh-cli"
    succ "检测到 gh CLI 已登录"
elif [ -n "${GITHUB_TOKEN}" ]; then
    AUTH_METHOD="token"
    succ "检测到 GITHUB_TOKEN 环境变量"
else
    warn "未检测到 gh CLI 或 GITHUB_TOKEN"
    echo ""
    echo "请选择认证方式："
    echo ""
    echo "  方案 A（推荐）: 安装 gh CLI 并登录"
    echo "    brew install gh"
    echo "    gh auth login"
    echo ""
    echo "  方案 B: 设置 Token 环境变量"
    echo "    export GITHUB_TOKEN=你的GitHub_Personal_Access_Token"
    echo ""
    echo "  方案 C: 使用 curl 交互式（会提示输入用户名和密码）"
    echo ""
    read -p "输入 A/B/C: " choice
    case $choice in
        A|a)
            brew install gh 2>/dev/null || apt-get install gh 2>/dev/null || pip install ghapi 2>/dev/null
            gh auth login
            AUTH_METHOD="gh-cli"
            ;;
        B|b)
            read -sp "请输入你的 GitHub Personal Access Token: " token
            echo ""
            export GITHUB_TOKEN="$token"
            AUTH_METHOD="token"
            ;;
        C|c)
            AUTH_METHOD="interactive"
            ;;
        *)
            err "无效选择"
            exit 1
            ;;
    esac
fi

# ─── 创建 GitHub 仓库 ─────────────────────────────────────────────────────
info "检查 GitHub 仓库是否存在..."

REPO_EXISTS=false
if [ "$AUTH_METHOD" = "gh-cli" ]; then
    if gh repo view "${USERNAME}/${REPO_NAME}" &> /dev/null; then
        REPO_EXISTS=true
    fi
elif [ "$AUTH_METHOD" = "token" ]; then
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        "https://api.github.com/repos/${USERNAME}/${REPO_NAME}")
    if [ "$HTTP_STATUS" = "200" ]; then
        REPO_EXISTS=true
    fi
fi

if [ "$REPO_EXISTS" = true ]; then
    succ "GitHub 仓库已存在，跳过创建"
else
    info "创建 GitHub 仓库..."
    if [ "$AUTH_METHOD" = "gh-cli" ]; then
        gh repo create "${USERNAME}/${REPO_NAME}" \
            --public \
            --description "A production-style AI agent workflow engine for automating ERP-like web operations with Playwright, tool calling, and audit trails." \
            --source="${REPO_DIR}" \
            --remote=origin \
            --push
        succ "仓库已创建并推送（gh CLI 模式）"
        exit 0
    elif [ "$AUTH_METHOD" = "token" ]; then
        curl -s -X POST \
            -H "Authorization: token ${GITHUB_TOKEN}" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/user/repos \
            -d "{
                \"name\": \"${REPO_NAME}\",
                \"description\": \"A production-style AI agent workflow engine for automating ERP-like web operations with Playwright, tool calling, and audit trails.\",
                \"private\": false,
                \"has_issues\": true,
                \"has_projects\": false,
                \"has_wiki\": false
            }" > /dev/null
        succ "GitHub 仓库已创建"
    else
        err "无法自动创建仓库，请先手动创建：https://github.com/new"
        exit 1
    fi
fi

# ─── 设置 Topics 标签 ───────────────────────────────────────────────────
if [ "$AUTH_METHOD" = "token" ]; then
    info "设置 Topics 标签..."
    curl -s -X PUT \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.mercy-preview+json" \
        https://api.github.com/repos/${USERNAME}/${REPO_NAME}/topics \
        -d "{
            \"names\": ${TOPICS}
        }" > /dev/null
    succ "Topics 已设置: ai-agent, playwright, fastapi, workflow-automation, llm-agent, python, automation, rpa"
fi

# ─── 配置远程仓库 ─────────────────────────────────────────────────────────
if git remote get-url origin &> /dev/null; then
    info "更新远程仓库地址..."
    git remote set-url origin "${REMOTE_URL}"
else
    info "添加远程仓库 origin..."
    git remote add origin "${REMOTE_URL}"
fi
succ "远程仓库: ${REMOTE_URL}"

# ─── 推送代码 ─────────────────────────────────────────────────────────────
info "推送到 GitHub..."
if [ "$AUTH_METHOD" = "interactive" ]; then
    echo ""
    warn "即将执行 git push，请按提示输入："
    echo "  用户名: ${USERNAME}"
    echo "  密码: 你的 GitHub Personal Access Token（不是登录密码）"
    echo ""
fi

git push -u origin main

succ "推送完成！"

# ─── 验证 ─────────────────────────────────────────────────────────────────
info "验证仓库可访问性..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/repos/${USERNAME}/${REPO_NAME}")
if [ "$HTTP_STATUS" = "200" ]; then
    succ "仓库验证通过！"
else
    warn "仓库可能尚未公开，等待 5 秒后重试..."
    sleep 5
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/repos/${USERNAME}/${REPO_NAME}")
    if [ "$HTTP_STATUS" = "200" ]; then
        succ "仓库验证通过！"
    fi
fi

# ─── 完成 ─────────────────────────────────────────────────────────────────
echo ""
echo "========================================"
echo "🎉 发布完成！"
echo "========================================"
echo ""
echo "📦 仓库地址: ${REMOTE_URL}"
echo ""
echo "📌 下一步（手动完成）："
echo ""
echo "  1. 录制 Demo GIF"
echo "     工具推荐: ScreenStudio (Mac) 或 LICEcap"
echo "     命令: workflow-agent run \"Create a new customer...\""
echo "     保存为 demo.gif 放项目根目录，README 首屏添加:"
echo "     ![Demo](demo.gif)"
echo ""
echo "  2. 写文章引流"
echo "     掘金/知乎/CSDN: 《从零构建可测试的 AI Agent 工作流》"
echo "     文末放 GitHub 链接"
echo ""
echo "  3. 社区分享"
echo "     Reddit: r/MachineLearning, r/Python"
echo "     Hacker News: Show HN"
echo "     V2EX: 推广区"
echo ""
echo "⚠️  安全提醒："
echo "     如果你之前暴露过 Token，请立即撤销："
echo "     https://github.com/settings/tokens"
echo ""
