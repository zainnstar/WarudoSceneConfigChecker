# -*- coding: utf-8 -*-
"""
UIダイアログモジュール
各種ダイアログクラスを提供します。
"""

import tkinter as tk
from tkinter import ttk


class LanguageDialog(tk.Toplevel):
    """言語選択ダイアログ"""
    
    def __init__(self, parent=None, current_language="ja", get_text_func=None):
        super().__init__(parent)
        self.parent = parent
        self.current_language = current_language
        self.get_text = get_text_func
        self.result = None
        self.setup_ui()
        
        # モーダルダイアログにする
        self.transient(parent)
        self.grab_set()
        
    def setup_ui(self):
        """UIをセットアップ"""
        self.title(self.get_text("dialog_language"))
        
        # 言語選択用のラジオボタン
        self.language_var = tk.StringVar(value=self.current_language)
        
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 日本語
        ttk.Radiobutton(frame, text=self.get_text("japanese"),
                        variable=self.language_var, value="ja").pack(anchor=tk.W)
        
        # 英語
        ttk.Radiobutton(frame, text=self.get_text("english"),
                        variable=self.language_var, value="en").pack(anchor=tk.W)
        
        # ボタンレイアウト
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # OKボタン
        ok_button = ttk.Button(button_frame, text=self.get_text("dialog_ok"), 
                               command=self.ok_clicked)
        ok_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # キャンセルボタン
        cancel_button = ttk.Button(button_frame, text=self.get_text("dialog_cancel"), 
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
        """OKボタンがクリックされた時の処理"""
        self.result = self.language_var.get()
        self.destroy()
        
    def cancel_clicked(self):
        """キャンセルボタンがクリックされた時の処理"""
        self.destroy()
    
    def get_selected_language(self):
        """選択された言語を取得"""
        return self.result
