#!/usr/bin/env python3
"""
macOS应用打包脚本
使用PyInstaller将密码生成器打包成独立的.app文件
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
    
    # 清理spec文件
    spec_file = "password_generator.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"   删除文件: {spec_file}")
    
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
        # 使用PyInstaller构建应用
        cmd = [
            'pyinstaller',
            '--onefile',           # 打包成单个文件
            '--windowed',          # 无控制台窗口
            '--name=随机密码生成器',  # 应用名称
            '--distpath=dist',     # 输出目录
            '--workpath=build',    # 工作目录
            '--clean',             # 清理临时文件
            'password_generator.py'
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
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

def create_app_bundle():
    """创建.app包"""
    print("📱 创建macOS应用包...")
    
    app_name = "随机密码生成器"
    app_path = f"dist/{app_name}.app"
    
    # 创建.app包结构
    os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
    os.makedirs(f"{app_path}/Contents/Resources", exist_ok=True)
    
    # 复制可执行文件
    executable_path = f"dist/{app_name}"
    if os.path.exists(executable_path):
        shutil.copy2(executable_path, f"{app_path}/Contents/MacOS/{app_name}")
        os.chmod(f"{app_path}/Contents/MacOS/{app_name}", 0o755)
        print(f"   复制可执行文件到: {app_path}/Contents/MacOS/")
    else:
        print(f"❌ 未找到可执行文件: {executable_path}")
        return False
    
    # 创建Info.plist文件
    info_plist = f"""{app_path}/Contents/Info.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>{app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.password.generator</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleDisplayName</key>
    <string>{app_name}</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
</dict>
</plist>"""
    
    with open(f"{app_path}/Contents/Info.plist", 'w', encoding='utf-8') as f:
        f.write(info_plist)
    
    print(f"   创建Info.plist文件")
    
    # 删除原始可执行文件
    os.remove(executable_path)
    print(f"   清理临时文件")
    
    return True

def check_app():
    """检查生成的应用程序"""
    app_path = "dist/随机密码生成器.app"
    
    if os.path.exists(app_path):
        print(f"✅ 应用程序已生成: {app_path}")
        
        # 获取应用大小
        app_size = get_folder_size(app_path)
        print(f"📱 应用大小: {format_size(app_size)}")
        
        # 检查应用结构
        print("📁 应用结构:")
        for root, dirs, files in os.walk(app_path):
            level = root.replace(app_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
        
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
        # 创建.app包
        if create_app_bundle():
            print()
            # 检查应用
            if check_app():
                print()
                print("🎉 打包完成！")
                print("📁 应用程序位置: dist/随机密码生成器.app")
                print("💡 你可以将这个.app文件拖到Applications文件夹中安装")
                print("💡 或者双击直接运行")
            else:
                print("❌ 应用检查失败")
        else:
            print("❌ 应用包创建失败")
    else:
        print("❌ 应用构建失败")

if __name__ == "__main__":
    main()
