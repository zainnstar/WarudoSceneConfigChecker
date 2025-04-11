# WarudoSceneConfigChecker

This is a script that checks whether the assets in the warudo scene file are in the StreamingAssets folder.

このスクリプトは、warudo のシーンファイルに含まれるアセットが StreamingAssets フォルダに存在するかどうかを確認します。

## インストール方法

1. Python がインストールされていることを確認してください（tkinter が必要です）
2. このリポジトリをダウンロードしてください
3. `start_checker.bat` でアプリケーションを起動できます

## 使用方法

1. `start_checker.bat`を実行してアプリケーションを起動します
2. シーンファイルの読み込み：
   - 「シーンファイルを読み込む」ボタンをクリック
   - Warudo のシーンファイル（\*.json）を選択
3. StreamingAssets フォルダの設定：
   - 「StreamingAssets フォルダを設定」ボタンをクリック
   - Warudo の StreamingAssets フォルダを選択

オプション：

- 不足ファイルのチェック：シーンで参照されているが StreamingAssets にない未ファイルを検出
- 未使用ファイルのチェック：シーンで使用されていない StreamingAssets 内のファイルを検出
- サブディレクトリを含める：StreamingAssets のサブディレクトリ内のファイルもチェック

「解析」ボタンをクリックすると、チェックが開始され、結果がアプリケーションウィンドウに表示されます。

## 製作者

稲峰幸助 サークル GoodLuck
https://x.com/inamine55
