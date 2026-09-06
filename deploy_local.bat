@echo off
setlocal EnableExtensions

rem Created: 2026-09-01 09:18 JST
rem ============================================================
rem Bousai Blog local preview deploy
rem 1) Update this repository from GitHub main
rem 2) Copy preview files to Apache htdocs\bousai_preview
rem 3) Open the local preview in the default browser
rem ============================================================

set "APACHE_ROOT=C:\server\Apache24\htdocs"
set "SITE_DIR=bousai_preview"
set "DST=%APACHE_ROOT%\%SITE_DIR%"
set "OPEN_URL=http://localhost/%SITE_DIR%/index.html"
set "PUSHD_OK=0"

pushd "%~dp0"
if errorlevel 1 (
    echo [ERROR] Could not open the repository folder.
    goto :error
)
set "PUSHD_OK=1"
set "SRC=%CD%"

echo.
echo ========================================
echo Bousai Blog local preview deploy
echo ========================================
echo Repository : %SRC%
echo Preview src: %SRC%\preview
echo Apache dst : %DST%
echo URL        : %OPEN_URL%
echo.

rem ---- Check Git ------------------------------------------------
where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git was not found.
    echo Install Git for Windows and run this batch again.
    goto :error
)

rem ---- Check repository -----------------------------------------
if not exist "%SRC%\.git\" (
    echo [ERROR] This folder is not a Git repository.
    echo Clone the repository once, then run deploy_local.bat from that folder.
    goto :error
)

rem ---- Check Apache root ----------------------------------------
if not exist "%APACHE_ROOT%\" (
    echo [ERROR] Apache htdocs was not found:
    echo         %APACHE_ROOT%
    goto :error
)

rem ---- Update main ----------------------------------------------
echo [1/3] Updating repository...
git switch main
if errorlevel 1 (
    echo [ERROR] Could not switch to main.
    goto :error
)

git pull --ff-only origin main
if errorlevel 1 (
    echo [ERROR] git pull failed.
    echo Resolve local changes or GitHub authentication, then retry.
    goto :error
)

rem Pull may have updated the preview directory, so check it afterwards.
if not exist "%SRC%\preview\index.html" (
    echo [ERROR] Preview index was not found:
    echo         %SRC%\preview\index.html
    goto :error
)

rem ---- Prepare destination --------------------------------------
echo.
echo [2/3] Copying preview files...
if not exist "%DST%\" (
    mkdir "%DST%"
    if errorlevel 1 (
        echo [ERROR] Could not create preview destination:
        echo         %DST%
        goto :error
    )
)

rem /MIR is safe here because DST is a dedicated bousai_preview directory.
robocopy "%SRC%\preview" "%DST%" /MIR /R:2 /W:1 /NFL /NDL /NJH /NJS /NP
set "ROBOCOPY_EXIT=%ERRORLEVEL%"

rem Robocopy codes 0-7 are success/informational. 8+ are failures.
if %ROBOCOPY_EXIT% GEQ 8 (
    echo [ERROR] Robocopy failed. Exit code: %ROBOCOPY_EXIT%
    goto :error
)

rem ---- Open browser ---------------------------------------------
echo.
echo [3/3] Opening local preview...
start "" "%OPEN_URL%"
if errorlevel 1 (
    echo [WARN] Could not open the browser automatically.
    echo Open this URL manually:
    echo   %OPEN_URL%
)

echo.
echo ========================================
echo Preview deploy completed successfully.
echo ========================================
echo Open:
echo   %OPEN_URL%
echo.
if "%PUSHD_OK%"=="1" popd
pause
exit /b 0

:error
echo.
echo ========================================
echo Preview deploy stopped because of an error.
echo No Git reset or cleanup was performed.
echo ========================================
echo.
if "%PUSHD_OK%"=="1" popd
pause
exit /b 1
