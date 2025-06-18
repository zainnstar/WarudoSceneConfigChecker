# -*- coding: utf-8 -*-
"""
設定管理モジュール
アプリケーションの設定を管理します。
"""

import json
import os


class ConfigManager:
    """設定管理クラス"""
    
    SETTINGS_FILE = "settings.json"
    
    def __init__(self):
        self._settings = {}
        self.load_settings()
    
    def load_settings(self):
        """設定ファイルから設定を読み込む"""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r", encoding="utf-8") as file:
                    self._settings = json.load(file)
            except Exception as e:
                print(f"設定ファイルの読み込みエラー: {e}")
                self._settings = {}
        else:
            self._settings = {}
    
    def save_settings(self):
        """設定を設定ファイルに保存する"""
        try:
            with open(self.SETTINGS_FILE, "w", encoding="utf-8") as file:
                json.dump(self._settings, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"設定ファイルの保存エラー: {e}")
    
    def get_language(self):
        """現在の言語設定を取得"""
        return self._settings.get("language", "ja")
    
    def set_language(self, language):
        """言語設定を更新"""
        self._settings["language"] = language
        self.save_settings()
    def get_setting(self, key, default=None):
        """指定されたキーの設定値を取得"""
        return self._settings.get(key, default)
    
    def set_setting(self, key, value):
        """指定されたキーの設定値を更新"""
        self._settings[key] = value
        self.save_settings()
    
    def get_streaming_assets_path(self):
        """StreamingAssetsパスを取得"""
        return self._settings.get("streaming_assets_path", "")
    
    def set_streaming_assets_path(self, path):
        """StreamingAssetsパスを設定"""
        self._settings["streaming_assets_path"] = path
        self.save_settings()
