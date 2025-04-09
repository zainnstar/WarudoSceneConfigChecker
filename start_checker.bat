@echo off
chcp 65001
setlocal enabledelayedexpansion

REM 仮想環境の存在確認
if not exist "venv" (
    echo 仮想環境を作成しています...
    python -m venv venv
    if errorlevel 1 (
        echo Pythonがインストールされていないか、venvモジュールが使用できません。
        echo Pythonをインストールしてから再度実行してください。
        pause
        exit /b 1
    )
)

REM 仮想環境を有効化
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo 仮想環境の有効化に失敗しました。
    pause
    exit /b 1
)

REM 必要なパッケージをインストール
echo パッケージをインストールしています...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo パッケージのインストールに失敗しました。
    echo Pythonのバージョンが要件を満たしているか確認してください。
    echo 現在のPythonバージョン:
    python --version
    pause
    exit /b 1
)

REM Pythonスクリプトを実行
echo シーンチェッカーを起動しています...
python warudo_scene_checker.py
if errorlevel 1 (
    echo プログラムの実行中にエラーが発生しました。
    pause
    exit /b 1
)

REM 仮想環境を無効化
call venv\Scripts\deactivate.bat

pause
exit /b 0