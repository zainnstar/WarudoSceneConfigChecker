# WarudoSceneConfigChecker

This is a script that checks whether the assets in the warudo scene file are in the StreamingAssets folder.

このスクリプトは、warudo のシーンファイルに含まれるアセットが StreamingAssets フォルダに存在するかどうかを確認します。

## Installation / インストール方法

1. Download and extract `WarudoSceneChecker.zip`
2. You can launch the application using `start_checker.bat` in the folder

3. `WarudoSceneChecker.zip` をダウンロードして展開してください
4. フォルダ内の `start_checker.bat` でアプリケーションを起動できます

Note: Python installation is required to run this application.
※ このアプリケーションの実行には Python のインストールが必要です。

## How to Use / 使用方法

1. Run `start_checker.bat` to launch the application
2. Load Scene File:
   - Click "Load Scene File" button
   - Select a Warudo scene file (\*.json)
3. Set StreamingAssets Folder:

   - Click "Set StreamingAssets Folder" button
   - Select Warudo's StreamingAssets folder

4. `start_checker.bat`を実行してアプリケーションを起動します
5. シーンファイルの読み込み：
   - 「シーンファイルを読み込む」ボタンをクリック
   - Warudo のシーンファイル（\*.json）を選択
6. StreamingAssets フォルダの設定：
   - 「StreamingAssets フォルダを設定」ボタンをクリック
   - Warudo の StreamingAssets フォルダを選択

Options / オプション：

- Missing File Check: Detect files referenced in the scene but not present in StreamingAssets
- Unused File Check: Detect files in StreamingAssets that are not used in the scene
- Include Subdirectories: Check files in subdirectories of StreamingAssets

- 不足ファイルのチェック：シーンで参照されているが StreamingAssets にない未ファイルを検出
- 未使用ファイルのチェック：シーンで使用されていない StreamingAssets 内のファイルを検出
- サブディレクトリを含める：StreamingAssets のサブディレクトリ内のファイルもチェック

Click the "Analyze" button to start checking, and the results will be displayed in the application window.
「解析」ボタンをクリックすると、チェックが開始され、結果がアプリケーションウィンドウに表示されます。

## Creator / 製作者

稲峰幸助 - Circle GoodLuck / サークル GoodLuck
https://x.com/inamine55
