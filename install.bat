@echo off
:: タスクタイムスタンプ インストーラー
:: 管理者権限で実行する必要があります

echo ========================================
echo   タスクタイムスタンプ インストーラー
echo ========================================
echo.

:: 管理者権限チェック
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [エラー] 管理者権限で実行してください。
    echo.
    echo このファイルを右クリックして
    echo 「管理者として実行」を選択してください。
    echo.
    pause
    exit /b 1
)

set "INSTALL_DIR=C:\Program Files\TaskTimestamp"

echo インストール先: %INSTALL_DIR%
echo.

:: インストール確認
set /p CONFIRM="インストールしますか？ (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo キャンセルしました。
    pause
    exit /b 0
)

:: フォルダ作成
echo.
echo [1/3] フォルダを作成中...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

:: ファイルコピー
echo [2/3] ファイルをコピー中...
copy /Y "TaskTimestamp.exe" "%INSTALL_DIR%\" >nul
if exist "data" (
    xcopy /E /I /Y "data" "%INSTALL_DIR%\data" >nul
)
if exist "マニュアル.md" (
    copy /Y "マニュアル.md" "%INSTALL_DIR%\" >nul
)

:: デスクトップショートカット作成
echo [3/3] ショートカットを作成中...
set "SHORTCUT=%USERPROFILE%\Desktop\タスクタイムスタンプ.lnk"
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%INSTALL_DIR%\TaskTimestamp.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

echo.
echo ========================================
echo   インストール完了！
echo ========================================
echo.
echo インストール先: %INSTALL_DIR%
echo デスクトップにショートカットを作成しました。
echo.
pause
