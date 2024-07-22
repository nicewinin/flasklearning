# config.py
import os

# 获取环境变量或使用默认值
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///vs_sqlite.db')
