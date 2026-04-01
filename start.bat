@echo off
title Liturgy Slide Remote
echo.
echo ============================================
echo   LITURGY SLIDE REMOTE CONTROL
echo ============================================
echo.
echo IMPORTANT: Open your PowerPoint first!
echo Then tap buttons from your phone.
echo.
echo Starting server...
echo.
cd /d "%~dp0"
:: Run server using local python
"%~dp0python\python.exe" "%~dp0server.py"

echo.
echo Server stopped.
pause
