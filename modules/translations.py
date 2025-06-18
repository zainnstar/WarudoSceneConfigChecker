# -*- coding: utf-8 -*-
"""
翻訳モジュール
多言語対応のための翻訳辞書とヘルパー関数を提供します。
"""

# 多言語対応用の辞書
TRANSLATIONS = {
    "ja": {
        "window_title": "Warudo シーンデータチェッカー",
        "json_group": "JSONファイル",
        "json_not_selected": "ファイルが選択されていません",
        "select_json": "JSONファイルを選択",
        "assets_group": "StreamingAssets",
        "folder_not_selected": "フォルダが選択されていません",
        "select_assets": "StreamingAssetsフォルダを選択",
        "options_group": "オプション",
        "verify_files": "ファイルの存在を検証",
        "show_debug": "デバッグ情報を表示",
        "analyze_button": "シーンデータを分析",
        "env_category": "環境 (Environment)",
        "prop_category": "アイテム (Prop)",
        "char_category": "キャラクター (Character)",
        "particle_category": "パーティクル (Particle)",
        "other_category": "その他のオブジェクト",
        "column_object": "オブジェクト",
        "column_path": "パス",
        "column_status": "状態",
        "workshop_label": "ワークショップ",
        "subfolder_label": "サブフォルダ",
        "file_verified": "ファイル確認済み",
        "file_not_found": "存在しないファイル",
        "file_loaded": "ファイルを読み込みました: {path}",
        "json_error": "JSONの解析エラー: {error}",
        "file_error": "ファイル読み込みエラー: {error}",
        "select_json_first": "まずJSONファイルを選択してください。",
        "scan_results": "--- StreamingAssetsスキャン結果 ---",
        "files_detected": "{category}: {count}個のファイルを検出",
        "file_examples": "  ファイル例:",
        "more_files": "    - その他 {count} ファイル...",
        "analysis_results": "--- 分析結果 ---",
        "env_count": "環境オブジェクト: {total}個 (ユニーク: {unique}個)",
        "prop_count": "アイテム: {total}個 (ユニーク: {unique}個)",
        "char_count": "キャラクター: {total}個 (ユニーク: {unique}個)",
        "particle_count": "パーティクル: {total}個 (ユニーク: {unique}個)",
        "other_count": "その他: {count}個",
        "subfolder_issues": "--- 潜在的な問題: サブフォルダ ---",
        "missing_files": "--- 潜在的な問題: 不足ファイル ---",
        "no_issues": "潜在的な問題は見つかりませんでした。",
        "usage_count": "使用回数: {count}",
        "subfolder_move": "{type}「{name}」はサブフォルダ（{folder}）内にあります。直接{category}フォルダに移動する必要があります。",
        "file_missing": "{type}「{name}」(パス: {path}){debug}は存在しません。",
        "menu_settings": "設定",
        "menu_language": "言語設定",
        "dialog_language": "言語の選択",
        "japanese": "日本語",
        "english": "English",
        "dialog_ok": "OK",
        "dialog_cancel": "キャンセル"
    },
    "en": {
        "window_title": "Warudo Scene Data Checker",
        "json_group": "JSON File",
        "json_not_selected": "No file selected",
        "select_json": "Select JSON File",
        "assets_group": "StreamingAssets",
        "folder_not_selected": "No folder selected",
        "select_assets": "Select StreamingAssets Folder",
        "options_group": "Options",
        "verify_files": "Verify file existence",
        "show_debug": "Show debug info",
        "analyze_button": "Analyze Scene Data",
        "env_category": "Environment",
        "prop_category": "Prop",
        "char_category": "Character",
        "particle_category": "Particle",
        "other_category": "Other Objects",
        "column_object": "Object",
        "column_path": "Path",
        "column_status": "Status",
        "workshop_label": "Workshop",
        "subfolder_label": "Subfolder",
        "file_verified": "File verified",
        "file_not_found": "File not found",
        "file_loaded": "File loaded: {path}",
        "json_error": "JSON parse error: {error}",
        "file_error": "File read error: {error}",
        "select_json_first": "Please select a JSON file first.",
        "scan_results": "--- StreamingAssets Scan Results ---",
        "files_detected": "{category}: {count} files detected",
        "file_examples": "  File examples:",
        "more_files": "    - {count} more files...",
        "analysis_results": "--- Analysis Results ---",
        "env_count": "Environment objects: {total} (Unique: {unique})",
        "prop_count": "Props: {total} (Unique: {unique})",
        "char_count": "Characters: {total} (Unique: {unique})",
        "particle_count": "Particles: {total} (Unique: {unique})",
        "other_count": "Others: {count}",
        "subfolder_issues": "--- Potential Issues: Subfolders ---",
        "missing_files": "--- Potential Issues: Missing Files ---",
        "no_issues": "No potential issues found.",
        "usage_count": "Usage count: {count}",
        "subfolder_move": "{type} '{name}' is in subfolder ({folder}). It should be moved directly to {category} folder.",
        "file_missing": "{type} '{name}' (Path: {path}){debug} is missing.",
        "menu_settings": "Settings",
        "menu_language": "Language",
        "dialog_language": "Select Language",
        "japanese": "Japanese",
        "english": "English",
        "dialog_ok": "OK",
        "dialog_cancel": "Cancel"
    }
}


def get_text(language, key, **kwargs):
    """
    指定された言語とキーの翻訳テキストを取得
    
    Args:
        language (str): 言語コード ('ja' または 'en')
        key (str): 翻訳キー
        **kwargs: フォーマット用のキーワード引数
        
    Returns:
        str: 翻訳されたテキスト
    """
    text = TRANSLATIONS[language].get(key, TRANSLATIONS["ja"][key])
    return text.format(**kwargs) if kwargs else text


def get_available_languages():
    """
    利用可能な言語の一覧を取得
    
    Returns:
        list: 利用可能な言語コードのリスト
    """
    return list(TRANSLATIONS.keys())
