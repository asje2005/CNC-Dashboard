@echo off
setlocal

REM Opens the Caregiver Dashboard mobile prototype files in VS Code.
REM Run this file from Windows Explorer or from a Command Prompt.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo Opening Caregiver Dashboard mobile prototype files...
echo Project folder: %PROJECT_DIR%
echo.

where code >nul 2>nul
if errorlevel 1 (
    echo VS Code command-line launcher "code" was not found.
    echo.
    echo To fix this in VS Code:
    echo   1. Press Ctrl+Shift+P
    echo   2. Run: Shell Command: Install 'code' command in PATH
    echo   3. Re-run this batch file
    echo.
    echo You can still open the files manually from this folder:
    echo   mobile\README.md
    echo   mobile\App.js
    echo   mobile\App.android.jsx
    echo   mobile\App.ios.jsx
    echo   mobile\src\CaregiverMobileApp.jsx
    echo   mobile\src\components\DashboardCard.jsx
    echo   mobile\src\data\sampleCare.js
    echo   mobile\src\theme\tokens.js
    pause
    exit /b 1
)

code "%PROJECT_DIR%"
code --reuse-window "%PROJECT_DIR%mobile\README.md"
code --reuse-window "%PROJECT_DIR%mobile\App.js"
code --reuse-window "%PROJECT_DIR%mobile\App.android.jsx"
code --reuse-window "%PROJECT_DIR%mobile\App.ios.jsx"
code --reuse-window "%PROJECT_DIR%mobile\src\CaregiverMobileApp.jsx"
code --reuse-window "%PROJECT_DIR%mobile\src\components\DashboardCard.jsx"
code --reuse-window "%PROJECT_DIR%mobile\src\data\sampleCare.js"
code --reuse-window "%PROJECT_DIR%mobile\src\theme\tokens.js"

echo Done. The mobile prototype files should now be open in VS Code.
echo.
echo To run the mobile prototype later:
echo   cd mobile
echo   npm install
echo   npm run web
echo.
pause
