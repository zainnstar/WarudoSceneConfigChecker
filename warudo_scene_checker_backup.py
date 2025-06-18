# created by InamineKosuke at Circle GoodLuck

import sys
import os
import json
import re
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font

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


class LanguageDialog(tk.Toplevel):
    def __init__(self, parent=None, current_language="ja"):
        super().__init__(parent)
        self.parent = parent
        self.current_language = current_language
        self.result = None
        self.setup_ui()
        
        # モーダルダイアログにする
        self.transient(parent)
        self.grab_set()
        
    def setup_ui(self):
        self.title(self.parent.get_text("dialog_language"))
        
        # 言語選択用のラジオボタン
        self.language_var = tk.StringVar(value=self.current_language)
        
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 日本語
        ttk.Radiobutton(frame, text=self.parent.get_text("japanese"),
                        variable=self.language_var, value="ja").pack(anchor=tk.W)
        
        # 英語
        ttk.Radiobutton(frame, text=self.parent.get_text("english"),
                        variable=self.language_var, value="en").pack(anchor=tk.W)
        
        # ボタンレイアウト
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # OKボタン
        ok_button = ttk.Button(button_frame, text=self.parent.get_text("dialog_ok"), 
                               command=self.ok_clicked)
        ok_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # キャンセルボタン
        cancel_button = ttk.Button(button_frame, text=self.parent.get_text("dialog_cancel"), 
                                   command=self.cancel_clicked)
        cancel_button.pack(side=tk.RIGHT)
        
        # ダイアログをセンタリング
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def ok_clicked(self):
        self.result = self.language_var.get()
        self.destroy()
        
    def cancel_clicked(self):
        self.destroy()
    
    def get_selected_language(self):
        return self.result


class WarudoSceneChecker(tk.Tk):
    SETTINGS_FILE = "settings.json"


    def __init__(self):
        super().__init__()
        self.current_language = self.load_language_setting()  # 言語設定を復元

        # 色の定義
        self.workshop_color = "#90EE90"  # 薄緑色（ライトグリーン）
        self.missing_file_color = "#FF0000"  # 赤色（存在しないファイル）
        self.subfolder_colors = {
            "Props": "#FFC800",       # 濃い黄色
            "Environment": "#87CEFA", # 明るい青色
            "Characters": "#FFA07A",  # 明るいサーモンピンク
            "Particles": "#DDA0DD"    # 薄い紫色
        }
        
        # プロトコル接頭辞リスト
        self.protocols = {
            "Environment": "environment://",
            "Props": "prop://",
            "Characters": "character://",
            "Particles": "particle://"
        }
        
        # カテゴリ名とパスのマッピング（複数形に対応）
        self.category_paths = {
            "Environment": ["Environment", "Environments"],  # 単数形と複数形の両方に対応
            "Props": ["Props", "Prop"],
            "Characters": ["Characters", "Character"],
            "Particles": ["Particles", "Particle"]
        }
        
        # JSONパスのフォルダ名正規化マッピング
        self.json_path_mapping = {
            "data/Environment/": ["Environment", "Environments"],
            "data/Environments/": ["Environment", "Environments"],
            "data/Props/": ["Props", "Prop"],
            "data/Characters/": ["Characters", "Character"],
            "data/Particles/": ["Particles", "Particle"]
        }
        
        # StreamingAssetsのパスとアセットの存在確認用
        self.streaming_assets_path = None
        self.asset_files = {
            "Environment": [],
            "Props": [],
            "Characters": [],
            "Particles": []
        }
        
        self.debug_mode = False  # デバッグモード
        
        # ウィンドウの設定
        self.title(self.get_text("window_title"))
        self.geometry("1000x700")
        
        # メニューバーの作成
        self.create_menu_bar()
        
        # UIの構築
        self.setup_ui()
        
        # データ保存用
        self.current_file_path = None
        self.scene_data = None


    def load_language_setting(self):
        """保存された言語設定を読み込む"""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r", encoding="utf-8") as file:
                    settings = json.load(file)
                    return settings.get("language", "ja")  # デフォルトは日本語
            except:
                return "ja"
        return "ja"


    def save_language_setting(self):
        """現在の言語設定を保存する"""
        settings = {"language": self.current_language}
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)


    def create_menu_bar(self):
        """メニューバーを作成する"""
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # 設定メニュー
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(
            label=self.get_text("menu_language"), 
            command=self.show_language_dialog
        )
        self.menu_bar.add_cascade(label=self.get_text("menu_settings"), menu=settings_menu)


    def show_language_dialog(self):
        """言語設定ダイアログを表示"""
        dialog = LanguageDialog(self, self.current_language)
        self.wait_window(dialog)
        
        new_language = dialog.get_selected_language()
        if new_language and new_language != self.current_language:
            self.current_language = new_language
            self.save_language_setting()  # 設定を保存
            self.update_ui_texts()
            # メニューバーも更新
            self.menu_bar.destroy()
            self.create_menu_bar()


    def get_text(self, key, **kwargs):
        """指定されたキーの翻訳テキストを取得"""
        text = TRANSLATIONS[self.current_language].get(key, TRANSLATIONS["ja"][key])
        return text.format(**kwargs) if kwargs else text


    def update_ui_texts(self):
        """UI全体のテキストを現在の言語で更新"""
        self.title(self.get_text("window_title"))
        
        if hasattr(self, 'file_path_label'):
            if self.current_file_path:
                self.file_path_label["text"] = os.path.basename(self.current_file_path)
            else:
                self.file_path_label["text"] = self.get_text("json_not_selected")

        if hasattr(self, 'assets_path_label'):
            if self.streaming_assets_path:
                self.assets_path_label["text"] = os.path.basename(self.streaming_assets_path)
            else:
                self.assets_path_label["text"] = self.get_text("folder_not_selected")

        if hasattr(self, 'json_group'):
            self.json_group["text"] = self.get_text("json_group")

        if hasattr(self, 'assets_group'):
            self.assets_group["text"] = self.get_text("assets_group")

        if hasattr(self, 'options_group'):
            self.options_group["text"] = self.get_text("options_group")

        if hasattr(self, 'file_select_button'):
            self.file_select_button["text"] = self.get_text("select_json")

        if hasattr(self, 'assets_select_button'):
            self.assets_select_button["text"] = self.get_text("select_assets")

        if hasattr(self, 'verify_files_cb'):
            self.verify_files_cb["text"] = self.get_text("verify_files")

        if hasattr(self, 'debug_cb'):
            self.debug_cb["text"] = self.get_text("show_debug")

        if hasattr(self, 'analyze_button'):
            self.analyze_button["text"] = self.get_text("analyze_button")

        # ツリービューの列ヘッダーも更新
        if hasattr(self, 'tree_widget'):
            self.tree_widget.heading("#1", text=self.get_text("column_object"))
            self.tree_widget.heading("#2", text=self.get_text("column_path"))
            self.tree_widget.heading("#3", text=self.get_text("column_status"))


    def setup_ui(self):
        # メインフレーム
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ファイル選択エリア
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        # JSON選択グループ
        self.json_group = ttk.LabelFrame(file_frame, text=self.get_text("json_group"))
        self.json_group.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        json_inner_frame = ttk.Frame(self.json_group, padding=5)
        json_inner_frame.pack(fill=tk.X, expand=True)

        self.file_path_label = ttk.Label(json_inner_frame, text=self.get_text("json_not_selected"))
        self.file_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.file_select_button = ttk.Button(json_inner_frame, text=self.get_text("select_json"), command=self.select_file)
        self.file_select_button.pack(side=tk.RIGHT)

        # StreamingAssets選択グループ
        self.assets_group = ttk.LabelFrame(file_frame, text=self.get_text("assets_group"))
        self.assets_group.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))

        assets_inner_frame = ttk.Frame(self.assets_group, padding=5)
        assets_inner_frame.pack(fill=tk.X, expand=True)

        self.assets_path_label = ttk.Label(assets_inner_frame, text=self.get_text("folder_not_selected"))
        self.assets_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.assets_select_button = ttk.Button(
            assets_inner_frame, 
            text=self.get_text("select_assets"), 
            command=self.select_streaming_assets
        )
        self.assets_select_button.pack(side=tk.RIGHT)

        # オプショングループ
        self.options_group = ttk.LabelFrame(file_frame, text=self.get_text("options_group"))
        self.options_group.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        options_inner_frame = ttk.Frame(self.options_group, padding=5)
        options_inner_frame.pack(fill=tk.X, expand=True)

        self.verify_var = tk.BooleanVar(value=True)
        self.verify_files_cb = ttk.Checkbutton(
            options_inner_frame, 
            text=self.get_text("verify_files"),
            variable=self.verify_var
        )
        self.verify_files_cb.pack(side=tk.LEFT, padx=(0, 10))

        self.debug_var = tk.BooleanVar(value=False)
        self.debug_cb = ttk.Checkbutton(
            options_inner_frame, 
            text=self.get_text("show_debug"),
            variable=self.debug_var, 
            command=self.toggle_debug_mode
        )
        self.debug_cb.pack(side=tk.LEFT)

        # ペインウィンドウ（分割ビュー）
        paned = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # ツリービュー
        tree_frame = ttk.Frame(paned)
        paned.add(tree_frame, weight=3)

        # スクロールバー
        tree_scroll_y = ttk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview ウィジェット
        self.tree_widget = ttk.Treeview(
            tree_frame, 
            columns=("object", "path", "status"), 
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        self.tree_widget.pack(fill=tk.BOTH, expand=True)

        # スクロールバーをツリービューに接続
        tree_scroll_y.config(command=self.tree_widget.yview)
        tree_scroll_x.config(command=self.tree_widget.xview)

        # 列の設定
        self.tree_widget.heading("object", text=self.get_text("column_object"))
        self.tree_widget.heading("path", text=self.get_text("column_path"))
        self.tree_widget.heading("status", text=self.get_text("column_status"))
        
        self.tree_widget.column("object", width=300)
        self.tree_widget.column("path", width=400)
        self.tree_widget.column("status", width=100)

        # テキスト表示エリア
        text_frame = ttk.Frame(paned)
        paned.add(text_frame, weight=1)

        # テキストウィジェットとスクロールバー
        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_edit = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD)
        self.text_edit.pack(fill=tk.BOTH, expand=True)
        self.text_edit.config(state=tk.DISABLED)  # 読み取り専用
        
        text_scroll.config(command=self.text_edit.yview)
        self.text_edit.config(yscrollcommand=text_scroll.set)

        # 分析ボタン
        self.analyze_button = ttk.Button(
            main_frame, 
            text=self.get_text("analyze_button"), 
            command=self.analyze_scene_data
        )
        self.analyze_button.pack(fill=tk.X)
    
    def toggle_debug_mode(self):
        """デバッグモードの切り替え"""
        self.debug_mode = self.debug_var.get()
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="JSONファイルを選択", 
            filetypes=[("JSONファイル", "*.json")]
        )
        if file_path:
            self.current_file_path = file_path
            self.file_path_label["text"] = os.path.basename(file_path)
            
            # ファイル読み込み
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.scene_data = json.load(f)
                self._set_text_content(self.get_text("file_loaded", path=file_path))
            except json.JSONDecodeError as e:
                self._set_text_content(self.get_text("json_error", error=str(e)))
                self.scene_data = None
            except Exception as e:
                self._set_text_content(self.get_text("file_error", error=str(e)))
                self.scene_data = None
    
    def select_streaming_assets(self):
        folder_path = filedialog.askdirectory(title="StreamingAssetsフォルダを選択")
        if folder_path:
            self.streaming_assets_path = folder_path
            self.assets_path_label["text"] = os.path.basename(folder_path) or folder_path
            
            # StreamingAssets内のファイル一覧を収集
            self._scan_streaming_assets()
            
            # 見つかったファイルの情報を表示
            asset_summary = self.get_text("scan_results") + "\n"
            for category, files in self.asset_files.items():
                asset_summary += self.get_text("files_detected", category=category, count=len(files)) + "\n"
                
                # デバッグモードの場合、ファイルリストの詳細を表示
                if self.debug_mode and files:
                    asset_summary += self.get_text("file_examples") + "\n"
                    for i, asset in enumerate(files[:3]):  # 最初の3件だけ表示
                        asset_summary += f"    - {asset.get('name')} ({asset.get('rel_path')})\n"
                    if len(files) > 3:
                        asset_summary += self.get_text("more_files", count=len(files) - 3) + "\n"
                    
            self._set_text_content(asset_summary)

    def _set_text_content(self, text):
        """テキストエディタの内容を設定する"""
        self.text_edit.config(state=tk.NORMAL)
        self.text_edit.delete(1.0, tk.END)
        self.text_edit.insert(tk.END, text)
        self.text_edit.config(state=tk.DISABLED)
    def _scan_streaming_assets(self):
        """StreamingAssetsフォルダをスキャンしてファイル一覧を作成"""
        if not self.streaming_assets_path or not os.path.exists(self.streaming_assets_path):
            return
            
        # カテゴリ別のフォルダと拡張子のマッピング（複数形/単数形の両方に対応）
        category_folders = {
            "Environment": ["Environment", "Environments"],
            "Props": ["Props", "Prop"],
            "Characters": ["Characters", "Character"],
            "Particles": ["Particles", "Particle"]
        }
        
        # 各カテゴリのファイルリストをクリア
        for category in self.asset_files:
            self.asset_files[category] = []
            
        # StreamingAssetsフォルダを再帰的に探索
        for root, dirs, files in os.walk(self.streaming_assets_path):
            rel_path = os.path.relpath(root, self.streaming_assets_path).replace("\\", "/")
            
            # カテゴリにマッチするかチェック
            current_category = None
            is_subfolder = False
            subfolder_name = ""
            
            # パス階層を分析
            path_parts = rel_path.split("/")
            
            for category, folders in category_folders.items():
                for folder in folders:
                    for i, part in enumerate(path_parts):
                        if part.lower() == folder.lower():
                            current_category = category
                            
                            # サブフォルダかどうかの判定
                            if i < len(path_parts) - 1:
                                is_subfolder = True
                                subfolder_name = path_parts[i+1]
                            break
                    if current_category:
                        break
                if current_category:
                    break
            
            if current_category:
                # このフォルダ内の.warudoファイルを追加
                for file in files:
                    if file.endswith(".warudo"):
                        full_path = os.path.join(root, file).replace("\\", "/")
                        file_rel_path = os.path.relpath(full_path, self.streaming_assets_path).replace("\\", "/")
                        
                        # カテゴリフォルダ名を取得
                        # rel_pathから実際のフォルダ名を取得（大文字小文字の違いを保持）
                        cat_folder_actual = self._get_actual_folder_name(rel_path, category_folders[current_category])
                        
                        # カテゴリフォルダから下のパス部分を取得（例: Props/StageProp.warudo または Props/StageProp/item.warudo）
                        category_rel_path = self._get_path_after_category(file_rel_path, cat_folder_actual)
                        
                        # 適切なプレフィックスを決定
                        prefix = self.protocols.get(current_category, "")
                        
                        # 複数のパスバリエーションを生成（単数形/複数形両方に対応）
                        path_variants = []
                        for folder_variant in self.category_paths[current_category]:
                            # 完全なパス (例: prop://data/Props/StageProp.warudo)
                            full_prefix_path = f"{prefix}data/{folder_variant}/{category_rel_path}"
                            path_variants.append(full_prefix_path)
                        
                        # サブフォルダ情報を追加
                        self.asset_files[current_category].append({
                            "name": os.path.splitext(file)[0],
                            "full_path": full_path,
                            "rel_path": file_rel_path,
                            "category_path": category_rel_path,
                            "asset_path": path_variants[0],  # 最初のバリエーションをデフォルトとして使用
                            "asset_path_variants": path_variants,  # すべてのパスバリエーション
                            "is_subfolder": is_subfolder,  # サブフォルダかどうか
                            "subfolder_name": subfolder_name if is_subfolder else ""  # サブフォルダの名前
                        })
                        
                        if self.debug_mode:
                            subfolder_info = f" (サブフォルダ: {subfolder_name})" if is_subfolder else ""
                            print(f"検出: {file_rel_path}{subfolder_info} -> {path_variants}")
    
    def _get_actual_folder_name(self, path, possible_folders):
        """パスから実際のフォルダ名を取得（大文字小文字の差異を保持）"""
        parts = path.split("/")
        for part in parts:
            for folder in possible_folders:
                if part.lower() == folder.lower():
                    return part
        return possible_folders[0]  # デフォルト値を返す
    
    def _get_path_after_category(self, path, category):
        """カテゴリフォルダ名の後のパス部分を取得"""
        parts = path.split('/')
        try:
            # カテゴリフォルダ名のインデックスを検索（大文字小文字を区別せず）
            index = -1
            for i, part in enumerate(parts):
                if part.lower() == category.lower():
                    index = i
                    break
                    
            if index >= 0 and index < len(parts) - 1:
                # カテゴリフォルダ以降のパス部分を結合
                return '/'.join(parts[index+1:])
            else:
                return path  # カテゴリがない場合はそのまま返す
        except:
            return path  # エラーの場合はそのまま返す
    
    def _normalize_asset_path(self, path, category):
        """アセットのパスを正規化（プロトコルとdata/を除去）"""
        if not path:
            return ""
            
        # プロトコル部分を取り除く
        for protocol in self.protocols.values():
            if path.startswith(protocol):
                path = path[len(protocol):]
                break
                
        # "data/"を取り除く
        if path.startswith("data/"):
            path = path[5:]
            
        # フォルダ名を正規化（Environment/EnvironmentsやProps/Propの違いを吸収）
        for prefix, variants in self.json_path_mapping.items():
            for variant in variants:
                if path.startswith(variant + "/"):
                    # 最初のバリアントに標準化
                    return variants[0] + path[len(variant):]
                
        return path
    
    def analyze_scene_data(self):
        if not self.scene_data:
            self._set_text_content(self.get_text("select_json_first"))
            return
            
        # ツリーをクリア
        for item in self.tree_widget.get_children():
            self.tree_widget.delete(item)
        
        # カテゴリ別にオブジェクトを整理
        environments = []
        props = []
        characters = []
        particles = []
        other_objects = []
        
        # JSONからオブジェクトを抽出
        self._extract_objects(self.scene_data, environments, props, characters, particles, other_objects)
        
        # 重複オブジェクトをまとめる
        env_counts = self._group_objects_by_path(environments)
        prop_counts = self._group_objects_by_path(props)
        char_counts = self._group_objects_by_path(characters)
        particle_counts = self._group_objects_by_path(particles)
        
        # ツリービューにカテゴリとアイテムを追加
        # 環境オブジェクト
        if env_counts:
            env_root = self.tree_widget.insert("", tk.END, text=self.get_text("env_category"), values=(self.get_text("env_category"), "", ""))
            self._add_objects_to_tree(env_root, env_counts, "Environment")
        
        # アイテム
        if prop_counts:
            prop_root = self.tree_widget.insert("", tk.END, text=self.get_text("prop_category"), values=(self.get_text("prop_category"), "", ""))
            self._add_objects_to_tree(prop_root, prop_counts, "Props")
        
        # キャラクター
        if char_counts:
            char_root = self.tree_widget.insert("", tk.END, text=self.get_text("char_category"), values=(self.get_text("char_category"), "", ""))
            self._add_objects_to_tree(char_root, char_counts, "Characters")
        
        # パーティクル
        if particle_counts:
            particle_root = self.tree_widget.insert("", tk.END, text=self.get_text("particle_category"), values=(self.get_text("particle_category"), "", ""))
            self._add_objects_to_tree(particle_root, particle_counts, "Particles")
        
        # その他のオブジェクト
        if other_objects:
            other_root = self.tree_widget.insert("", tk.END, text=self.get_text("other_category"), values=(self.get_text("other_category"), "", ""))
            for obj in other_objects:
                self.tree_widget.insert(other_root, tk.END, values=(obj.get('name', 'Unknown'), obj.get('path', ''), ""))
        
        # すべてのアイテムを展開
        for item in self.tree_widget.get_children():
            self.tree_widget.item(item, open=True)
        
        # サマリーを表示
        summary = self.get_text("analysis_results") + "\n"
        summary += self.get_text("env_count", total=len(environments), unique=len(env_counts)) + "\n"
        summary += self.get_text("prop_count", total=len(props), unique=len(prop_counts)) + "\n"
        summary += self.get_text("char_count", total=len(characters), unique=len(char_counts)) + "\n"
        summary += self.get_text("particle_count", total=len(particles), unique=len(particle_counts)) + "\n"
        summary += self.get_text("other_count", count=len(other_objects)) + "\n\n"
        
        # 問題があればそれも表示
        issues = []
        missing_files = []
        
        # サブフォルダの問題チェック
        self._check_for_subfolder_issues(environments, props, characters, particles, issues)
        
        # ファイル存在の問題チェック
        if self.verify_var.get() and self.streaming_assets_path:
            self._check_for_missing_files(environments, props, characters, particles, missing_files)
        
        if issues:
            summary += self.get_text("subfolder_issues") + "\n"
            for issue in issues:
                summary += f"- {issue}\n"
        
        if missing_files:
            summary += "\n" + self.get_text("missing_files") + "\n"
            for issue in missing_files:
                summary += f"- {issue}\n"
                
        if not issues and not missing_files:
            summary += self.get_text("no_issues")
            
        self._set_text_content(summary)
    
    def _group_objects_by_path(self, objects):
        """同じパスを持つオブジェクトをグループ化して、出現回数をカウントする"""
        path_count = defaultdict(int)
        path_name = {}
        
        for obj in objects:
            path = obj.get('path', '')
            name = obj.get('name', 'Unknown')
            path_count[path] += 1
            path_name[path] = name
            
        return [{
            'path': path,
            'name': path_name[path],
            'count': count
        } for path, count in path_count.items()]
    
    def _add_objects_to_tree(self, parent_item, object_counts, category):
        """オブジェクトとその出現回数をツリービューに追加する"""
        for obj in object_counts:
            name = obj['name']
            path = obj['path']
            count = obj['count']
            
            # 2回以上出現するオブジェクトは出現回数を表示
            display_name = name
            if count > 1:
                display_name = f"{name} ({self.get_text('usage_count', count=count)})"
                
            # 存在確認のためのステータス
            status = ""
            
            # ツリーアイテム作成
            item_id = self.tree_widget.insert(parent_item, tk.END, values=(display_name, path, status))
            
            # サブフォルダの確認（色付け）
            is_in_subfolder = self._check_subfolder(item_id, path)
            
            # ファイルが存在するかチェック
            if self.verify_var.get() and self.streaming_assets_path:
                file_exists = self._check_file_exists(path, category)
                
                if file_exists:
                    self.tree_widget.set(item_id, "status", self.get_text("file_verified"))
                else:
                    self.tree_widget.set(item_id, "status", self.get_text("file_not_found"))
                    # tkの場合は後でタグを使って色を設定
                    self.tree_widget.item(item_id, tags=("missing",))
        
        # 赤色のタグを定義
        self.tree_widget.tag_configure("missing", foreground=self.missing_file_color)
        # その他のタグも同様に定義
        self.tree_widget.tag_configure("workshop", background=self.workshop_color)
        for category, color in self.subfolder_colors.items():
            self.tree_widget.tag_configure(f"subfolder_{category.lower()}", background=color)
    
    def _extract_objects(self, data, environments, props, characters, particles, other_objects):
        """JSONデータを再帰的に処理して、関連するオブジェクトを抽出する"""
        if isinstance(data, dict):
            # valueキーがあり、文字列で、特定のプレフィックスを含む場合
            if "value" in data and isinstance(data["value"], str):
                value = data["value"].strip('"')
                
                # 環境
                if value.startswith("environment://"):
                    environments.append({
                        "name": self._get_name_from_path(value),
                        "path": value
                    })
                # アイテム
                elif value.startswith("prop://"):
                    props.append({
                        "name": self._get_name_from_path(value),
                        "path": value
                    })
                # キャラクター
                elif value.startswith("character://"):
                    characters.append({
                        "name": self._get_name_from_path(value),
                        "path": value
                    })
                # パーティクル
                elif value.startswith("particle://"):
                    particles.append({
                        "name": self._get_name_from_path(value),
                        "path": value
                    })
            
            # 再帰的に辞書のすべての値を処理
            for key, value in data.items():
                self._extract_objects(value, environments, props, characters, particles, other_objects)
        
        elif isinstance(data, list):
            # リスト内のすべてのアイテムを処理
            for item in data:
                self._extract_objects(item, environments, props, characters, particles, other_objects)
    
    def _get_name_from_path(self, path):
        """パスからオブジェクト名を抽出する"""
        if not path:
            return "Unknown"
        
        # パスの最後の部分を取得
        name = os.path.basename(path)
        
        # .warudoを取り除く
        if name.endswith(".warudo"):
            name = name[:-7]
            
        return name
    
    def _check_subfolder(self, item_id, path):
        """サブフォルダ内のオブジェクトかをチェック"""
        if not path:
            return False
            
        # "workshop/" はワークショップアイテム
        if "workshop/" in path:
            current_text = self.tree_widget.item(item_id, "values")[0]
            if f" ({self.get_text('workshop_label')})" not in current_text:
                self.tree_widget.set(item_id, "object", f"{current_text} ({self.get_text('workshop_label')})")
            self.tree_widget.item(item_id, tags=("workshop",))
            return False
            
        # 各種フォルダのサブフォルダチェックを統合
        folders_to_check = {
            "data/Props/": "Props",
            "data/Environment/": "Environment",
            "data/Characters/": "Characters",
            "data/Particles/": "Particles"
        }
        
        for folder_path, folder_name in folders_to_check.items():
            if folder_path in path and path.count('/') > 2:
                parts = path.split('/')
                if len(parts) > 3 and parts[2] == folder_name and len(parts) > 4:
                    subfolder_name = parts[3]
                    
                    # 表示テキストを更新
                    current_text = self.tree_widget.item(item_id, "values")[0]
                    if f" ({self.get_text('subfolder_label')}: {subfolder_name})" not in current_text:
                        self.tree_widget.set(item_id, "object", f"{current_text} ({self.get_text('subfolder_label')}: {subfolder_name})")
                    
                    # フォルダ名の列にもサブフォルダ名を表示
                    self.tree_widget.set(item_id, "status", f"{self.get_text('subfolder_label')}: {subfolder_name}")
                    
                    # タグを使用して色を設定
                    self.tree_widget.item(item_id, tags=(f"subfolder_{folder_name.lower()}",))
                    
                    return True
        
        return False
    def _check_file_exists(self, asset_path, category):
        """StreamingAssetsフォルダでファイルが存在するか確認"""
        if not self.streaming_assets_path or not asset_path:
            return True  # パスが設定されていない場合はチェックしない
        
        # パスを正規化（プロトコルとdata/を除去）
        normalized_asset_path = self._normalize_asset_path(asset_path, category)
        
        # カテゴリに対応するアセットリスト
        assets = self.asset_files.get(category, [])
        
        # サブフォルダを含むパスかどうかをチェック
        json_has_subfolder = False
        subfolder_path = None
        
        parts = normalized_asset_path.split('/')
        if len(parts) > 2:  # カテゴリ名の次にサブフォルダがある場合
            json_has_subfolder = True
            # サブフォルダを含むパス
            subfolder_path = '/'.join(parts)
            
            # デバッグモードの場合
            if self.debug_mode:
                print(f"JSONのサブフォルダパス検証: {subfolder_path}")
        
        # パスが一致するか確認
        for asset in assets:
            # アセットのパスバリエーション（複数形/単数形対応）をチェック
            asset_path_variants = asset.get('asset_path_variants', [asset.get('asset_path', '')])
            
            # 実際のファイルがサブフォルダ内にあるかどうか
            asset_is_in_subfolder = asset.get('is_subfolder', False)
            
            # デバッグモードの場合
            if self.debug_mode and asset_is_in_subfolder:
                print(f"アセットはサブフォルダにあります: {asset.get('name')} (subfolder: {asset.get('subfolder_name')})")
            
            # JSONパスとファイルシステムのパス構造が異なる場合（一方がサブフォルダ内、もう一方が直接カテゴリフォルダ内）
            # ファイルは存在するが、構造が異なるためチェックに失敗させる
            if json_has_subfolder != asset_is_in_subfolder:
                # ファイル名だけを比較して、同じファイルだけど構造が違う場合を検出
                json_filename = os.path.basename(normalized_asset_path)
                asset_filename = os.path.basename(asset.get('category_path', ''))
                
                if json_filename.lower() == asset_filename.lower():
                    if self.debug_mode:
                        print(f"ファイル名は一致するが構造が異なる: JSON={json_has_subfolder}, Asset={asset_is_in_subfolder}")
                        print(f"  - JSON path: {normalized_asset_path}")
                        print(f"  - Asset path: {asset.get('category_path')}")
                    # 同じファイル名だが構造が異なるので、falseではなくTrueを返す
                    # これにより、サブフォルダチェックで警告を出せる
                    return True
            
            # 元のパスでの完全一致チェック
            if asset_path in asset_path_variants:
                return True
                
            # カテゴリフォルダ以降のパス部分（StageProp.warudo など）
            asset_category_path = asset.get('category_path', '')
            
            # カテゴリフォルダ名のバリエーション
            folder_variants = self.category_paths.get(category, [category])
            
            # 各バリエーションで比較
            for folder in folder_variants:
                # カテゴリフォルダを含む完全なパス（Props/StageProp.warudo など）
                full_category_path = f"{folder}/{asset_category_path}"
                
                # 正規化パスの一致チェック
                if normalized_asset_path.lower() == full_category_path.lower():
                    return True
                    
                # サブフォルダを含む完全なパスでも検証
                if json_has_subfolder and subfolder_path.lower() == full_category_path.lower():
                    return True
            
            # ファイル名部分での一致チェック - ただしこれはあくまでファイル名のみの比較であり、パス構造は考慮しない
            asset_filename = os.path.basename(asset_category_path)
            json_filename = os.path.basename(normalized_asset_path)
            
            # ファイル名が一致した場合でも、パス構造が異なる場合は注意が必要
            if asset_filename.lower() == json_filename.lower():
                # サブフォルダ内のファイルと、直接カテゴリフォルダにあるファイルは区別する
                asset_parent = os.path.dirname(asset_category_path)
                norm_parent = os.path.dirname(normalized_asset_path)
                
                # パスの構造が異なる場合
                if (json_has_subfolder != asset_is_in_subfolder) or \
                   (json_has_subfolder and asset_is_in_subfolder and asset_parent.lower() != norm_parent.lower()):
                    if self.debug_mode:
                        print(f"サブフォルダ不一致: Asset={asset_parent}, JSON={norm_parent}")
                    # ファイルは存在するが、構造が異なるので警告を出す必要がある
                    # ここではTrueを返して、サブフォルダチェックのほうで警告する
                    return True
                
                # デバッグ情報
                if self.debug_mode:
                    print(f"ファイル名一致: {asset_filename} == {json_filename}")
                
                return True
                
            # デバッグモードの場合、比較情報を表示
            if self.debug_mode:
                print(f"比較: {normalized_asset_path.lower()} vs {asset_category_path.lower()}")
                
        # デバッグ用に詳細情報を表示
        if self.debug_mode:
            print(f"未検出アセット: {asset_path} (正規化: {normalized_asset_path})")
            
        return False
    
    def _check_for_subfolder_issues(self, environments, props, characters, particles, issues):
        """サブフォルダに関する問題点をチェックする"""
        # フォルダカテゴリごとのチェックを統合
        folders_to_check = [
            {"list": props, "path_parts": ["data/Props/", "data/Prop/"], "folder_idx": 2, "folder_name": "Props", "type_name": self.get_text("prop_category")},
            {"list": environments, "path_parts": ["data/Environment/", "data/Environments/"], "folder_idx": 2, "folder_name": "Environment", "type_name": self.get_text("env_category")},
            {"list": characters, "path_parts": ["data/Characters/", "data/Character/"], "folder_idx": 2, "folder_name": "Characters", "type_name": self.get_text("char_category")},
            {"list": particles, "path_parts": ["data/Particles/", "data/Particle/"], "folder_idx": 2, "folder_name": "Particles", "type_name": self.get_text("particle_category")}
        ]
        
        # 同じ問題を重複して報告しないためのセット
        reported_issues = set()
        
        for check in folders_to_check:
            for obj in check["list"]:
                path = obj.get('path', '')
                
                # 複数のパスパターンをチェック
                for path_part in check["path_parts"]:
                    if path_part in path:
                        parts = path.split('/')
                        folder_idx = check["folder_idx"]
                        
                        # フォルダ名のバリエーションをチェック
                        if (len(parts) > folder_idx and
                            (parts[folder_idx].lower() == check["folder_name"].lower() or
                             parts[folder_idx].lower() == check["folder_name"].rstrip('s').lower()) and
                            len(parts) > folder_idx + 1):
                            
                            issue_text = self.get_text("subfolder_move", type=check["type_name"], name=obj.get('name'), folder=parts[folder_idx+1], category=check["folder_name"])
                            
                            # 重複チェック
                            if issue_text not in reported_issues:
                                issues.append(issue_text)
                                reported_issues.add(issue_text)
                        break
    
    def _check_for_missing_files(self, environments, props, characters, particles, issues):
        """存在しないファイルの問題をチェック"""
        # カテゴリとリストのマッピング
        category_lists = {
            "Environment": environments,
            "Props": props,
            "Characters": characters,
            "Particles": particles
        }
        
        # カテゴリ名とその表示名
        category_names = {
            "Environment": self.get_text("env_category"),
            "Props": self.get_text("prop_category"),
            "Characters": self.get_text("char_category"),
            "Particles": self.get_text("particle_category")
        }
        
        # 各カテゴリのファイルをチェック
        for category, obj_list in category_lists.items():
            # 同じ問題を重複して報告しないためのセット
            reported_paths = set()
            
            for obj in obj_list:
                path = obj.get('path', '')
                name = obj.get('name', 'Unknown')
                
                # このパスがすでに報告済みかチェック
                if path in reported_paths:
                    continue
                    
                # ファイルが存在するかチェック
                if not self._check_file_exists(path, category):
                    # デバッグ情報を追加
                    debug_info = ""
                    if self.debug_mode:
                        normalized_path = self._normalize_asset_path(path, category)
                        debug_info = f" [正規化パス: {normalized_path}]"
                        
                    issues.append(self.get_text("file_missing", type=category_names.get(category, category), name=name, path=path, debug=debug_info))
                    reported_paths.add(path)


if __name__ == "__main__":
    app = WarudoSceneChecker()
    app.mainloop()
