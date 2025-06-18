# -*- coding: utf-8 -*-
"""
アセット管理モジュール
StreamingAssetsフォルダのスキャンと管理を行います。
"""

import os
from collections import defaultdict


class AssetManager:
    """アセット管理クラス"""
    
    def __init__(self):
        pass
        self.streaming_assets_path = None
        self.asset_files = {
            "Environment": [],
            "Props": [],
            "Characters": [],
            "Particles": []
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
            "Environment": ["Environment", "Environments"],
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
    
    def set_streaming_assets_path(self, path):
        """StreamingAssetsのパスを設定"""
        self.streaming_assets_path = path
        if path:
            self.scan_streaming_assets()
    
    def scan_streaming_assets(self):
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
                        cat_folder_actual = self._get_actual_folder_name(rel_path, category_folders[current_category])
                        
                        # カテゴリフォルダから下のパス部分を取得
                        category_rel_path = self._get_path_after_category(file_rel_path, cat_folder_actual)
                        
                        # 適切なプレフィックスを決定
                        prefix = self.protocols.get(current_category, "")
                        
                        # 複数のパスバリエーションを生成（単数形/複数形両方に対応）
                        path_variants = []
                        for folder_variant in self.category_paths[current_category]:
                            # 完全なパス
                            full_prefix_path = f"{prefix}data/{folder_variant}/{category_rel_path}"
                            path_variants.append(full_prefix_path)
                        
                        # サブフォルダ情報を追加
                        self.asset_files[current_category].append({
                            "name": os.path.splitext(file)[0],
                            "full_path": full_path,
                            "rel_path": file_rel_path,
                            "category_path": category_rel_path,
                            "asset_path": path_variants[0],                            "asset_path_variants": path_variants,
                            "is_subfolder": is_subfolder,
                            "subfolder_name": subfolder_name if is_subfolder else ""
                        })
    
    def _get_actual_folder_name(self, path, possible_folders):
        """パスから実際のフォルダ名を取得（大文字小文字の差異を保持）"""
        parts = path.split("/")
        for part in parts:
            for folder in possible_folders:
                if part.lower() == folder.lower():
                    return part
        return possible_folders[0]
    
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
                return path
        except:
            return path
    
    def normalize_asset_path(self, path, category):
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
            
        # フォルダ名を正規化
        for prefix, variants in self.json_path_mapping.items():
            for variant in variants:
                if path.startswith(variant + "/"):
                    return variants[0] + path[len(variant):]
                
        return path
    
    def check_file_exists(self, asset_path, category):
        """StreamingAssetsフォルダでファイルが存在するか確認（サブフォルダまで厳密チェック）"""
        if not self.streaming_assets_path or not asset_path:
            return True
        
        # パスを正規化
        normalized_asset_path = self.normalize_asset_path(asset_path, category)
        
        # カテゴリに対応するアセットリスト
        assets = self.asset_files.get(category, [])
        
        # JSONのパス構造を解析
        json_parts = normalized_asset_path.split('/')
        json_has_subfolder = len(json_parts) > 2  # カテゴリ名の後にサブフォルダがあるか
        json_subfolder = json_parts[1] if json_has_subfolder else ""
        json_filename = json_parts[-1]  # ファイル名部分
        
        # 各アセットとの厳密な比較
        for asset in assets:
            asset_category_path = asset.get('category_path', '')
            asset_is_in_subfolder = asset.get('is_subfolder', False)
            asset_subfolder_name = asset.get('subfolder_name', '')
              # アセットのパス構造を解析
            asset_parts = asset_category_path.split('/')
            asset_filename = asset_parts[-1] if asset_parts else ''
            
            # ファイル名が一致しない場合はスキップ
            if json_filename.lower() != asset_filename.lower():
                continue
            
            # 1. 両方ともサブフォルダにない場合（直接カテゴリフォルダ内）
            if not json_has_subfolder and not asset_is_in_subfolder:
                return True
              # 2. 両方ともサブフォルダ内にある場合
            elif json_has_subfolder and asset_is_in_subfolder:
                # サブフォルダ名まで一致するかチェック
                if json_subfolder.lower() == asset_subfolder_name.lower():
                    return True
              # 3. 構造が異なる場合（一方がサブフォルダ、もう一方が直接）
            else:
                # 構造が異なる場合は一致しないとみなす
                continue
        
        return False
    
    def get_asset_summary(self):
        """アセットの概要を取得"""
        summary = {}
        for category, files in self.asset_files.items():
            summary[category] = len(files)
        return summary
