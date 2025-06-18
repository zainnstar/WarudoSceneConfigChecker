# -*- coding: utf-8 -*-
"""
メインUIモジュール
アプリケーションのメインユーザーインターフェースを提供します。
"""

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

from .translations import get_text
from .dialogs import LanguageDialog


class MainUI(tk.Tk):
    """メインUIクラス"""
    
    def __init__(self, config_manager, asset_manager, analyzer):
        super().__init__()
        
        self.config_manager = config_manager
        self.asset_manager = asset_manager
        self.analyzer = analyzer
        
        # データ保存用
        self.current_file_path = None
        self.scene_data = None
        
        # 色の定義
        self.workshop_color = "#90EE90"
        self.missing_file_color = "#FF0000"
        self.subfolder_colors = {
            "Props": "#FFC800",
            "Environment": "#87CEFA",
            "Characters": "#FFA07A",
            "Particles": "#DDA0DD"
        }
          # UIの初期化
        self._setup_window()
        self._create_menu_bar()
        self._setup_ui()
        
        # 保存されたStreamingAssetsパスを読み込み
        self._load_streaming_assets_path()
    
    def _setup_window(self):
        """ウィンドウの基本設定"""
        self.title(self.get_text("window_title"))
        self.geometry("1000x700")
    
    def get_text(self, key, **kwargs):
        """翻訳テキストを取得"""
        return get_text(self.config_manager.get_language(), key, **kwargs)
    
    def _create_menu_bar(self):
        """メニューバーを作成"""
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # 設定メニュー
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(
            label=self.get_text("menu_language"), 
            command=self._show_language_dialog
        )
        self.menu_bar.add_cascade(label=self.get_text("menu_settings"), menu=settings_menu)
    
    def _show_language_dialog(self):
        """言語設定ダイアログを表示"""
        dialog = LanguageDialog(self, self.config_manager.get_language(), self.get_text)
        self.wait_window(dialog)
        
        new_language = dialog.get_selected_language()
        if new_language and new_language != self.config_manager.get_language():
            self.config_manager.set_language(new_language)
            self._update_ui_texts()
            # メニューバーも更新
            self.menu_bar.destroy()
            self._create_menu_bar()
    
    def _update_ui_texts(self):
        """UI全体のテキストを現在の言語で更新"""
        self.title(self.get_text("window_title"))
        
        # 各UI要素のテキストを更新
        if hasattr(self, 'file_path_label'):
            if self.current_file_path:
                self.file_path_label["text"] = os.path.basename(self.current_file_path)
            else:
                self.file_path_label["text"] = self.get_text("json_not_selected")

        if hasattr(self, 'assets_path_label'):
            if self.asset_manager.streaming_assets_path:
                self.assets_path_label["text"] = os.path.basename(self.asset_manager.streaming_assets_path)
            else:
                self.assets_path_label["text"] = self.get_text("folder_not_selected")

        # その他のUI要素も更新
        ui_elements = [
            ('json_group', 'json_group'),
            ('assets_group', 'assets_group'),
            ('options_group', 'options_group'),
            ('file_select_button', 'select_json'),
            ('assets_select_button', 'select_assets'),
            ('verify_files_cb', 'verify_files'),
            ('debug_cb', 'show_debug'),
            ('analyze_button', 'analyze_button')
        ]
        
        for attr_name, text_key in ui_elements:
            if hasattr(self, attr_name):
                getattr(self, attr_name)["text"] = self.get_text(text_key)

        # ツリービューの列ヘッダーも更新
        if hasattr(self, 'tree_widget'):
            self.tree_widget.heading("#1", text=self.get_text("column_object"))
            self.tree_widget.heading("#2", text=self.get_text("column_path"))
            self.tree_widget.heading("#3", text=self.get_text("column_status"))
    
    def _setup_ui(self):
        """メインUIをセットアップ"""
        # メインフレーム
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ファイル選択エリア
        self._create_file_selection_area(main_frame)
        
        # ペインウィンドウ（分割ビュー）
        paned = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # ツリービューエリア
        self._create_tree_view_area(paned)
        
        # テキスト表示エリア
        self._create_text_area(paned)

        # 分析ボタン
        self.analyze_button = ttk.Button(
            main_frame, 
            text=self.get_text("analyze_button"), 
            command=self._analyze_scene_data
        )
        self.analyze_button.pack(fill=tk.X)
    
    def _create_file_selection_area(self, parent):
        """ファイル選択エリアを作成"""
        file_frame = ttk.Frame(parent)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        # JSON選択グループ
        self.json_group = ttk.LabelFrame(file_frame, text=self.get_text("json_group"))
        self.json_group.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        json_inner_frame = ttk.Frame(self.json_group, padding=5)
        json_inner_frame.pack(fill=tk.X, expand=True)

        self.file_path_label = ttk.Label(json_inner_frame, text=self.get_text("json_not_selected"))
        self.file_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.file_select_button = ttk.Button(json_inner_frame, text=self.get_text("select_json"), command=self._select_file)
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
            command=self._select_streaming_assets
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
    
    def _create_tree_view_area(self, parent):
        """ツリービューエリアを作成"""
        tree_frame = ttk.Frame(parent)
        parent.add(tree_frame, weight=3)

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
        
        # タグの設定
        self._setup_tree_tags()
    
    def _setup_tree_tags(self):
        """ツリービューのタグを設定"""
        self.tree_widget.tag_configure("missing", foreground=self.missing_file_color)
        self.tree_widget.tag_configure("workshop", background=self.workshop_color)
        for category, color in self.subfolder_colors.items():
            self.tree_widget.tag_configure(f"subfolder_{category.lower()}", background=color)
    
    def _create_text_area(self, parent):
        """テキスト表示エリアを作成"""
        text_frame = ttk.Frame(parent)
        parent.add(text_frame, weight=1)

        # テキストウィジェットとスクロールバー
        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_edit = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD)
        self.text_edit.pack(fill=tk.BOTH, expand=True)
        self.text_edit.config(state=tk.DISABLED)
        
        text_scroll.config(command=self.text_edit.yview)
        self.text_edit.config(yscrollcommand=text_scroll.set)
    
    def _toggle_debug_mode(self):
        """デバッグモードの切り替え"""
        self.debug_mode = self.debug_var.get()
        self.asset_manager.debug_mode = self.debug_mode
        self.analyzer.debug_mode = self.debug_mode
    
    def _select_file(self):
        """JSONファイルを選択"""
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
    def _select_streaming_assets(self):
        """StreamingAssetsフォルダを選択"""
        folder_path = filedialog.askdirectory(title="StreamingAssetsフォルダを選択")
        if folder_path:
            self.asset_manager.set_streaming_assets_path(folder_path)
            self.assets_path_label["text"] = os.path.basename(folder_path) or folder_path
            
            # パスを設定に保存
            self.config_manager.set_streaming_assets_path(folder_path)
            
            # 見つかったファイルの情報を表示
            asset_summary = self.get_text("scan_results") + "\n"
            summary = self.asset_manager.get_asset_summary()
            
            for category, count in summary.items():
                asset_summary += self.get_text("files_detected", category=category, count=count) + "\n"
                    
            self._set_text_content(asset_summary)
    
    def _load_streaming_assets_path(self):
        """保存されたStreamingAssetsパスを読み込み"""
        saved_path = self.config_manager.get_streaming_assets_path()
        if saved_path and os.path.exists(saved_path):
            self.asset_manager.set_streaming_assets_path(saved_path)
            self.assets_path_label["text"] = os.path.basename(saved_path) or saved_path
            
            # 見つかったファイルの情報を表示
            asset_summary = self.get_text("scan_results") + "\n"
            summary = self.asset_manager.get_asset_summary()
            
            for category, count in summary.items():
                asset_summary += self.get_text("files_detected", category=category, count=count) + "\n"
                    
            self._set_text_content(asset_summary)
    
    def _set_text_content(self, text):
        """テキストエディタの内容を設定"""
        self.text_edit.config(state=tk.NORMAL)
        self.text_edit.delete(1.0, tk.END)
        self.text_edit.insert(tk.END, text)
        self.text_edit.config(state=tk.DISABLED)
    
    def _analyze_scene_data(self):
        """シーンデータを分析"""
        if not self.scene_data:
            self._set_text_content(self.get_text("select_json_first"))
            return
        
        # ツリーをクリア
        for item in self.tree_widget.get_children():
            self.tree_widget.delete(item)
        
        # オブジェクトを抽出
        extracted_objects = self.analyzer.extract_objects(self.scene_data)
        
        # 重複オブジェクトをまとめる
        env_counts = self.analyzer.group_objects_by_path(extracted_objects["environments"])
        prop_counts = self.analyzer.group_objects_by_path(extracted_objects["props"])
        char_counts = self.analyzer.group_objects_by_path(extracted_objects["characters"])
        particle_counts = self.analyzer.group_objects_by_path(extracted_objects["particles"])
        
        # ツリービューにカテゴリとアイテムを追加
        self._add_category_to_tree(env_counts, "env_category", "Environment")
        self._add_category_to_tree(prop_counts, "prop_category", "Props")
        self._add_category_to_tree(char_counts, "char_category", "Characters")
        self._add_category_to_tree(particle_counts, "particle_category", "Particles")
        
        # その他のオブジェクト
        if extracted_objects["other_objects"]:
            other_root = self.tree_widget.insert("", tk.END, text=self.get_text("other_category"), 
                                                values=(self.get_text("other_category"), "", ""))
            for obj in extracted_objects["other_objects"]:
                self.tree_widget.insert(other_root, tk.END, 
                                      values=(obj.get('name', 'Unknown'), obj.get('path', ''), ""))
        
        # すべてのアイテムを展開
        for item in self.tree_widget.get_children():
            self.tree_widget.item(item, open=True)
        
        # サマリーを生成して表示
        self._generate_analysis_summary(extracted_objects, env_counts, prop_counts, char_counts, particle_counts)
    
    def _add_category_to_tree(self, object_counts, category_key, category):
        """カテゴリをツリーに追加"""
        if object_counts:
            category_root = self.tree_widget.insert("", tk.END, text=self.get_text(category_key), 
                                                   values=(self.get_text(category_key), "", ""))
            self._add_objects_to_tree(category_root, object_counts, category)
    
    def _add_objects_to_tree(self, parent_item, object_counts, category):
        """オブジェクトをツリーに追加"""
        for obj in object_counts:
            name = obj['name']
            path = obj['path']
            count = obj['count']
            
            # 2回以上出現するオブジェクトは出現回数を表示
            display_name = name
            if count > 1:
                display_name = f"{name} ({self.get_text('usage_count', count=count)})"
            
            # ツリーアイテム作成
            item_id = self.tree_widget.insert(parent_item, tk.END, values=(display_name, path, ""))
            
            # サブフォルダの確認（色付け）
            self._check_subfolder_display(item_id, path)
            
            # ファイルが存在するかチェック
            if self.verify_var.get() and self.asset_manager.streaming_assets_path:
                file_exists = self.asset_manager.check_file_exists(path, category)
                
                if file_exists:
                    self.tree_widget.set(item_id, "status", self.get_text("file_verified"))
                else:
                    self.tree_widget.set(item_id, "status", self.get_text("file_not_found"))
                    self.tree_widget.item(item_id, tags=("missing",))
    
    def _check_subfolder_display(self, item_id, path):
        """サブフォルダ内のオブジェクトの表示を調整"""
        if not path:
            return False
            
        # "workshop/" はワークショップアイテム
        if "workshop/" in path:
            current_text = self.tree_widget.item(item_id, "values")[0]
            if f" ({self.get_text('workshop_label')})" not in current_text:
                self.tree_widget.set(item_id, "object", f"{current_text} ({self.get_text('workshop_label')})")
            self.tree_widget.item(item_id, tags=("workshop",))
            return False
            
        # 各種フォルダのサブフォルダチェック
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
                        self.tree_widget.set(item_id, "object", 
                                           f"{current_text} ({self.get_text('subfolder_label')}: {subfolder_name})")
                    
                    # ステータスにもサブフォルダ名を表示
                    self.tree_widget.set(item_id, "status", f"{self.get_text('subfolder_label')}: {subfolder_name}")
                    
                    # タグを使用して色を設定
                    self.tree_widget.item(item_id, tags=(f"subfolder_{folder_name.lower()}",))
                    
                    return True
        
        return False
    
    def _generate_analysis_summary(self, extracted_objects, env_counts, prop_counts, char_counts, particle_counts):
        """分析結果のサマリーを生成"""
        summary = self.get_text("analysis_results") + "\n"
        summary += self.get_text("env_count", total=len(extracted_objects["environments"]), unique=len(env_counts)) + "\n"
        summary += self.get_text("prop_count", total=len(extracted_objects["props"]), unique=len(prop_counts)) + "\n"
        summary += self.get_text("char_count", total=len(extracted_objects["characters"]), unique=len(char_counts)) + "\n"
        summary += self.get_text("particle_count", total=len(extracted_objects["particles"]), unique=len(particle_counts)) + "\n"
        summary += self.get_text("other_count", count=len(extracted_objects["other_objects"])) + "\n\n"
        
        # 問題チェック
        issues = []
        missing_files = []
        
        # サブフォルダの問題チェック
        issues = self.analyzer.check_subfolder_issues(extracted_objects, self.get_text)
        
        # ファイル存在の問題チェック
        if self.verify_var.get() and self.asset_manager.streaming_assets_path:
            missing_files = self.analyzer.check_missing_files(extracted_objects, self.get_text)
        
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
