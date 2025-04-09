@echo off
rem ウィンドウが一瞬で閉じるのを防ぐためのタイトル設定
title WarudoSceneConfigChecker 起動ツール

rem 文字コードをUTF-8に設定
chcp 65001 > nul
setlocal enabledelayedexpansion

rem バッチファイル実行開始メッセージ
echo [開始] バッチファイルを実行しています...
echo.

rem Pythonの存在確認
echo [確認] Pythonがインストールされているか確認しています...
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [エラー] Pythonが見つかりません。
    echo [エラー] Pythonをインストールしてから再実行してください。
    goto :ERROR
)

rem Python バージョン表示
echo [情報] Pythonバージョン:
python --version
echo.

rem 仮想環境の存在確認
if not exist "venv" (
    echo [実行] 仮想環境を作成しています...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [エラー] 仮想環境の作成に失敗しました。
        echo [エラー] Pythonのバージョンが3.5以上か確認してください。
        goto :ERROR
    )
)

rem 仮想環境を有効化
echo [実行] 仮想環境を有効化しています...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo [エラー] 仮想環境の有効化に失敗しました。
    goto :ERROR
)

rem 必要なパッケージをインストール
echo [実行] パッケージをインストールしています...
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo [エラー] pipのアップグレードに失敗しました。
    goto :ERROR
)

python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [エラー] パッケージのインストールに失敗しました。
    echo [情報] requirements.txt ファイルの存在を確認してください。
    goto :ERROR
)

rem Pythonスクリプトを実行
echo [実行] シーンチェッカーを起動しています...
python warudo_scene_checker.py
if %ERRORLEVEL% neq 0 (
    echo [エラー] プログラムの実行中にエラーが発生しました。
    goto :ERROR
)

rem 仮想環境を無効化
call venv\Scripts\deactivate.bat

echo.
echo [完了] 処理が正常に終了しました。
goto :END

:ERROR
echo.
echo [終了] エラーが発生したため、処理を中断しました。
echo.

:END
echo.
echo 終了するには何かキーを押してください...
pause > nul
exit /b 0