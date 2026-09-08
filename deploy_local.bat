@echo off
setlocal EnableExtensions

rem Created: 2026-09-01 09:18 JST
rem Updated: 2026-09-09 06:17 JST
rem ============================================================
rem Bousai Blog local preview deploy
rem 1) Update this repository from GitHub main
rem 2) Synchronize reviewed Markdown into preview HTML temporarily
rem 3) Copy preview files to Apache htdocs\bousai_preview
rem 4) Restore tracked preview files and open the local preview
rem ============================================================

set "APACHE_ROOT=C:\server\Apache24\htdocs"
set "SITE_DIR=bousai_preview"
set "DST=%APACHE_ROOT%\%SITE_DIR%"
set "OPEN_URL=http://localhost/%SITE_DIR%/index.html"
set "PUSHD_OK=0"
set "PREVIEW_SYNCED=0"

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

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found.
    echo Python 3.11 or later is required to synchronize reviewed article text.
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
echo [1/4] Updating repository...
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

rem Do not overwrite a user's local preview edits when restoring generated files.
git diff --quiet -- preview
if errorlevel 1 (
    echo [ERROR] Local changes already exist under preview\.
    echo Commit, stash, or revert those changes before running this batch.
    goto :error
)

git diff --cached --quiet -- preview
if errorlevel 1 (
    echo [ERROR] Staged changes already exist under preview\.
    echo Commit or unstage them before running this batch.
    goto :error
)

rem ---- Synchronize reviewed Markdown ----------------------------
echo.
echo [2/4] Synchronizing reviewed Markdown into preview HTML...
set "PYTHONPATH=%SRC%\src;%PYTHONPATH%"
python "%SRC%\scripts\sync_previews_from_markdown.py"
if errorlevel 1 (
    echo [ERROR] Preview synchronization failed.
    git restore --worktree -- preview >nul 2>&1
    goto :error
)
set "PREVIEW_SYNCED=1"

rem ---- Prepare destination --------------------------------------
echo.
echo [3/4] Copying preview files...
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

rem Restore generated tracked previews after they have been copied locally.
if "%PREVIEW_SYNCED%"=="1" (
    git restore --worktree -- preview
    set "PREVIEW_SYNCED=0"
)

rem Robocopy codes 0-7 are success/informational. 8+ are failures.
if %ROBOCOPY_EXIT% GEQ 8 (
    echo [ERROR] Robocopy failed. Exit code: %ROBOCOPY_EXIT%
    goto :error
)

rem ---- Open browser ---------------------------------------------
echo.
echo [4/4] Opening local preview...
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
if "%PREVIEW_SYNCED%"=="1" (
    git restore --worktree -- preview >nul 2>&1
)
echo.
echo ========================================
echo Preview deploy stopped because of an error.
echo No Git reset or cleanup outside generated preview files was performed.
echo ========================================
echo.
if "%PUSHD_OK%"=="1" popd
pause
exit /b 1
