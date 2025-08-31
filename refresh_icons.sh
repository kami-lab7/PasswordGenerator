#!/bin/bash

echo "🔄 刷新macOS图标缓存..."

# 刷新Finder图标缓存
echo "   刷新Finder图标缓存..."
sudo rm -rf /Library/Caches/com.apple.iconservices.store
sudo rm -rf /System/Library/Caches/com.apple.iconservices.store
sudo rm -rf ~/Library/Caches/com.apple.iconservices.store

# 刷新Dock
echo "   刷新Dock..."
killall Dock

# 刷新Finder
echo "   刷新Finder..."
killall Finder

echo "✅ 图标缓存已刷新！"
echo "💡 现在应用图标应该能正常显示了"
echo "�� 如果图标还是没有显示，请重启电脑"
