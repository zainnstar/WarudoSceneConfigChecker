# -*- coding: utf-8 -*-
"""
Warudo Scene Config Checker
メインアプリケーションファイル

Created by InamineKosuke at Circle GoodLuck
Version 2.0.0 - Refactored for better maintainability
"""

from modules.config import ConfigManager
from modules.asset_manager import AssetManager
from modules.analyzer import SceneAnalyzer
from modules.ui import MainUI


def main():
    """メインアプリケーション関数"""
    # 設定管理の初期化
    config_manager = ConfigManager()
      # アセット管理の初期化
    asset_manager = AssetManager()
    
    # 分析エンジンの初期化
    analyzer = SceneAnalyzer(asset_manager)
    
    # メインUIの初期化と実行
    app = MainUI(config_manager, asset_manager, analyzer)
    app.mainloop()


if __name__ == "__main__":
    main()
