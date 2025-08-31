#!/bin/bash

# Git初始化和首次提交脚本
echo "🚀 开始设置Git仓库..."

# 检查是否已经是Git仓库
if [ -d ".git" ]; then
    echo "⚠️  已经是Git仓库，跳过初始化步骤"
else
    # 初始化Git仓库
    echo "📁 初始化Git仓库..."
    git init
fi

# 添加所有文件
echo "📝 添加文件到暂存区..."
git add .

# 检查是否有更改
if git diff --cached --quiet; then
    echo "ℹ️  没有新的更改需要提交"
else
    # 首次提交
    echo "💾 执行首次提交..."
    git commit -m "🎉 初始提交：随机密码生成器

✨ 功能特性：
- 支持4-50位密码长度设置
- 可选择字符类型（大写、小写、数字、符号）
- 实时密码生成
- 一键复制到剪贴板
- 历史记录管理
- 支持macOS应用打包

🔧 技术特点：
- 使用Python标准库tkinter构建GUI
- 响应式布局设计
- 支持窗口大小调整
- 完全中文化界面
- 跨平台兼容

📱 macOS支持：
- 可打包成独立应用程序
- 无需Python环境
- 原生macOS体验

📄 许可证：MIT License"

    echo "✅ 首次提交完成！"
fi

# 显示Git状态
echo ""
echo "📊 Git状态："
git status

echo ""
echo "🎯 下一步操作："
echo "1. 在GitHub上创建新仓库"
echo "2. 添加远程仓库：git remote add origin https://github.com/yourusername/password-generator.git"
echo "3. 推送代码：git push -u origin main"
echo ""
echo "💡 提示：记得在GitHub上设置仓库描述和标签！"
