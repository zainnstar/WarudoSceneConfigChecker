# WarudoSceneConfigChecker

This is a script that checks whether the assets in the warudo scene file are in the StreamingAssets folder.

このスクリプトは、warudo のシーンファイルに含まれるアセットが StreamingAssets フォルダに存在するかどうかを確認します。

## Installation / インストール方法

### English

1. Make sure you have Python installed on your system
2. Clone or download this repository
3. Install required dependencies:

```
pip install -r requirements.txt
```

### 日本語

1. Python がインストールされていることを確認してください
2. このリポジトリをクローンまたはダウンロードしてください
3. 必要な依存関係をインストールします：

```
pip install -r requirements.txt
```

## Usage / 使用方法

### English

1. Launch the application by running `start_checker.bat`
2. Load Scene File:
   - Click "Load Scene File" button
   - Select your Warudo scene file (\*.json)
3. Set StreamingAssets Folder:
   - Click "Set StreamingAssets Folder" button
   - Select your Warudo's StreamingAssets folder

Options:

- Check missing files: Detects files referenced in the scene but missing from StreamingAssets
- Check unused files: Finds files in StreamingAssets that aren't used in the scene
- Include subdirectories: Also checks files in subdirectories of StreamingAssets

Click "Analyze" to start the check. Results will be displayed in the application window.

### 日本語

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
