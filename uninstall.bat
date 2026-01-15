@echo off
:: タスクタイムスタンプ アンインストーラー
:: 管理者権限で実行する必要があります

echo ========================================
echo   タスクタイムスタンプ アンインストーラー
echo ========================================
echo.

:: 管理者権限チェック
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [エラー] 管理者権限で実行してください。
    echo.
    pause
    exit /b 1
)

set "INSTALL_DIR=C:\Program Files\TaskTimestamp"

if not exist "%INSTALL_DIR%" (
    echo インストールされていません。
    pause
    exit /b 0
)

echo インストール先: %INSTALL_DIR%
echo.

:: アンインストール確認
set /p CONFIRM="アンインストールしますか？ (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo キャンセルしました。
    pause
    exit /b 0
)

echo.
echo [1/2] ファイルを削除中...
rmdir /S /Q "%INSTALL_DIR%"

echo [2/2] ショートカットを削除中...
set "SHORTCUT=%USERPROFILE%\Desktop\タスクタイムスタンプ.lnk"
if exist "%SHORTCUT%" del "%SHORTCUT%"

echo.
echo ========================================
echo   アンインストール完了！
echo ========================================
echo.
pause
