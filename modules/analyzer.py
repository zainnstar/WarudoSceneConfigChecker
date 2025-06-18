# -*- coding: utf-8 -*-
"""
分析エンジンモジュール
シーンデータの分析を行います。
"""

import os
from collections import defaultdict


class SceneAnalyzer:
    """シーンデータ分析クラス"""
    
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
    
    def extract_objects(self, data):
        """JSONデータを再帰的に処理して、関連するオブジェクトを抽出する"""
        environments = []
        props = []
        characters = []
        particles = []
        other_objects = []
        
        self._extract_objects_recursive(data, environments, props, characters, particles, other_objects)
        
        return {
            "environments": environments,
            "props": props,
            "characters": characters,
            "particles": particles,
            "other_objects": other_objects
        }
    
    def _extract_objects_recursive(self, data, environments, props, characters, particles, other_objects):
        """再帰的にオブジェクトを抽出する内部メソッド"""
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
                self._extract_objects_recursive(value, environments, props, characters, particles, other_objects)
        
        elif isinstance(data, list):
            # リスト内のすべてのアイテムを処理
            for item in data:
                self._extract_objects_recursive(item, environments, props, characters, particles, other_objects)
    
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
    
    def group_objects_by_path(self, objects):
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
    
    def check_subfolder_issues(self, extracted_objects, get_text_func):
        """サブフォルダに関する問題点をチェックする"""
        issues = []
        
        # フォルダカテゴリごとのチェック設定
        folders_to_check = [
            {
                "list": extracted_objects["props"], 
                "path_parts": ["data/Props/", "data/Prop/"], 
                "folder_idx": 2, 
                "folder_name": "Props", 
                "type_name": get_text_func("prop_category")
            },
            {
                "list": extracted_objects["environments"], 
                "path_parts": ["data/Environment/", "data/Environments/"], 
                "folder_idx": 2, 
                "folder_name": "Environment", 
                "type_name": get_text_func("env_category")
            },
            {
                "list": extracted_objects["characters"], 
                "path_parts": ["data/Characters/", "data/Character/"], 
                "folder_idx": 2, 
                "folder_name": "Characters", 
                "type_name": get_text_func("char_category")
            },
            {
                "list": extracted_objects["particles"], 
                "path_parts": ["data/Particles/", "data/Particle/"], 
                "folder_idx": 2, 
                "folder_name": "Particles", 
                "type_name": get_text_func("particle_category")
            }
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
                            
                            issue_text = get_text_func("subfolder_move", 
                                                     type=check["type_name"], 
                                                     name=obj.get('name'), 
                                                     folder=parts[folder_idx+1], 
                                                     category=check["folder_name"])
                            
                            # 重複チェック
                            if issue_text not in reported_issues:
                                issues.append(issue_text)
                                reported_issues.add(issue_text)
                        break
        
        return issues
    
    def check_missing_files(self, extracted_objects, get_text_func):
        """存在しないファイルの問題をチェック"""
        issues = []
        
        # カテゴリとリストのマッピング
        category_lists = {
            "Environment": extracted_objects["environments"],
            "Props": extracted_objects["props"],
            "Characters": extracted_objects["characters"],
            "Particles": extracted_objects["particles"]
        }
        
        # カテゴリ名とその表示名
        category_names = {
            "Environment": get_text_func("env_category"),
            "Props": get_text_func("prop_category"),
            "Characters": get_text_func("char_category"),
            "Particles": get_text_func("particle_category")
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
                if not self.asset_manager.check_file_exists(path, category):
                    issues.append(get_text_func("file_missing", 
                                              type=category_names.get(category, category), 
                                              name=name, 
                                              path=path, 
                                              debug=""))
                    reported_paths.add(path)
        
        return issues
