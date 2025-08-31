from setuptools import setup

APP = ['password_generator.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,  # 可以添加自定义图标文件路径
    'plist': {
        'CFBundleName': '随机密码生成器',
        'CFBundleDisplayName': '随机密码生成器',
        'CFBundleGetInfoString': '一个功能完整的随机密码生成器',
        'CFBundleIdentifier': 'com.password.generator',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
    },
    'packages': ['tkinter'],
    'includes': ['random', 'string', 'datetime'],
    'excludes': ['matplotlib', 'numpy', 'pandas', 'scipy'],  # 排除不需要的大型库
    'optimize': 2,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
