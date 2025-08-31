#!/usr/bin/env python3
"""
macOS应用打包脚本
使用py2app将密码生成器打包成独立的.app文件
"""

import os
import shutil
import subprocess
import sys

def clean_build():
    """清理之前的构建文件"""
    print("🧹 清理之前的构建文件...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   删除目录: {dir_name}")
    
    # 清理Python缓存文件
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))
                print(f"   删除缓存: {os.path.join(root, dir_name)}")

def build_app():
    """构建macOS应用"""
    print("🔨 开始构建macOS应用...")
    
    try:
        # 运行py2app
        result = subprocess.run([
            sys.executable, 'setup.py', 'py2app', '--clean'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 应用构建成功！")
            return True
        else:
            print("❌ 构建失败:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 构建过程中出现错误: {e}")
        return False

def check_app():
    """检查生成的应用程序"""
    app_path = "dist/随机密码生成器.app"
    
    if os.path.exists(app_path):
        print(f"✅ 应用程序已生成: {app_path}")
        
        # 获取应用大小
        app_size = get_folder_size(app_path)
        print(f"📱 应用大小: {format_size(app_size)}")
        
        return True
    else:
        print("❌ 未找到生成的应用程序")
        return False

def get_folder_size(folder_path):
    """获取文件夹大小"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def main():
    """主函数"""
    print("🚀 开始打包macOS应用...")
    print("=" * 50)
    
    # 清理构建文件
    clean_build()
    print()
    
    # 构建应用
    if build_app():
        print()
        # 检查应用
        if check_app():
            print()
            print("🎉 打包完成！")
            print("📁 应用程序位置: dist/随机密码生成器.app")
            print("💡 你可以将这个.app文件拖到Applications文件夹中安装")
        else:
            print("❌ 应用检查失败")
    else:
        print("❌ 应用构建失败")

if __name__ == "__main__":
    main()
