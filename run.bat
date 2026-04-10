@echo off
REM ========================================
REM To-Do List Project - Quick Run Script
REM ========================================

echo.
echo ======================================
echo  To-Do List Project
echo ======================================
echo.
echo Choose what to run:
echo.
echo 1. Start FastAPI Server
echo 2. Start Mobile App (Flet)
echo 3. Run Database Setup
echo 4. Test API Endpoints
echo 5. Run Both (API + Mobile)
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting FastAPI Server...
    echo.
    call env\Scripts\activate.bat
    uvicorn to_do_list:app --reload --host 0.0.0.0 --port 8000
) else if "%choice%"=="2" (
    echo.
    echo Starting Mobile App...
    echo.
    call env\Scripts\activate.bat
    python mobile_app.py
) else if "%choice%"=="3" (
    echo.
    echo Running Database Setup...
    echo.
    call env\Scripts\activate.bat
    python setup_database.py
) else if "%choice%"=="4" (
    echo.
    echo Running API Tests...
    echo.
    call env\Scripts\activate.bat
    python test_api.py
) else if "%choice%"=="5" (
    echo.
    echo Starting both API and Mobile App...
    echo Making sure dependencies are installed...
    echo.
    call env\Scripts\pip install -r requirements.txt
    echo.
    echo Starting FastAPI Server in new window...
    start "FastAPI Server" cmd /k "cd /d %CD% && call env\Scripts\activate.bat && uvicorn to_do_list:app --reload --host 0.0.0.0 --port 8000"
    echo.
    timeout /t 3 /nobreak
    echo.
    echo Starting Mobile App...
    call env\Scripts\activate.bat
    python mobile_app.py
) else (
    echo Invalid choice. Please run the script again.
    pause
    exit /b 1
)

pause
