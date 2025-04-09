@echo off
rem 文字コードをUTF-8に設定
chcp 65001 > nul

rem 環境変数の遅延展開を有効化
setlocal enabledelayedexpansion

rem 仮想環境の存在確認
if not exist "venv" (
    echo [INFO] 仮想環境を作成しています...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Pythonがインストールされていないか、venvモジュールが使用できません。
        echo [ERROR] Pythonをインストールしてから再度実行してください。
        pause
        exit /b 1
    )
)

rem 仮想環境を有効化
echo [INFO] 仮想環境を有効化しています...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] 仮想環境の有効化に失敗しました。
    pause
    exit /b 1
)

rem 必要なパッケージをインストール
echo [INFO] パッケージをインストールしています...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] パッケージのインストールに失敗しました。
    echo [INFO] Pythonのバージョンを確認します...
    python --version
    pause
    exit /b 1
)

rem Pythonスクリプトを実行
echo [INFO] シーンチェッカーを起動しています...
python warudo_scene_checker.py
if errorlevel 1 (
    echo [ERROR] プログラムの実行中にエラーが発生しました。
    pause
    exit /b 1
)

rem 仮想環境を無効化
call venv\Scripts\deactivate.bat

echo [INFO] 処理が完了しました。
pause
exit /b 0