# ========================================
# To-Do List Project - Quick Run Script
# ========================================

Write-Host "`n======================================"
Write-Host " To-Do List Project"
Write-Host "======================================`n" -ForegroundColor Cyan

Write-Host "Choose what to run:`n" -ForegroundColor Green

Write-Host "1. Start FastAPI Server"
Write-Host "2. Start Mobile App (Flet)"
Write-Host "3. Start Modern Mobile App with Login"
Write-Host "4. Start Mobile App with Login (Flet)"
Write-Host "5. Run Database Setup"
Write-Host "6. Test API Endpoints"
Write-Host "7. Run Both (API + Mobile)"
Write-Host "8. Run All (API + Modern Mobile with Login)"
Write-Host "9. Install/Update Dependencies`n"

$choice = Read-Host "Enter your choice (1-9)"

switch ($choice) {
    "1" {
        Write-Host "`nStarting FastAPI Server...`n" -ForegroundColor Yellow
        & .\env\Scripts\Activate.ps1
        uvicorn to_do_list:app --reload --host 0.0.0.0 --port 8000
    }
    "2" {
        Write-Host "`nStarting Mobile App (Flet)...`n" -ForegroundColor Yellow
        & .\env\Scripts\Activate.ps1
        python mobile_app.py
    }
    "3" {
        Write-Host "`nStarting Modern Mobile App with Login...`n" -ForegroundColor Yellow
        & .\env\Scripts\Activate.ps1
        python -c "
import flet as ft
from login_app import main as login_main
page = ft.Page()
login_main(page)
" # Will use login_app which redirects to modern_app
    }
    "4" {
        Write-Host "`nStarting Mobile App with Login...`n" -ForegroundColor Yellow
        & .\env\Scripts\Activate.ps1
        python login_app.py
    }
    "5" {
        Write-Host "`nRunning Database Setup...`n" -ForegroundColor Yellow
        & .\env\Scripts\Activate.ps1
        python setup_database.py
    }
    "6" {
        Write-Host "`nRunning API Tests...`n" -ForegroundColor Yellow
        & .\env\Scripts\Activate.ps1
        python test_api.py
    }
    "7" {
        Write-Host "`nStarting both API and Mobile App...`n" -ForegroundColor Yellow
        
        Write-Host "Starting FastAPI Server in new window...`n" -ForegroundColor Cyan
        $apiProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; & .\env\Scripts\Activate.ps1; uvicorn to_do_list:app --reload --host 0.0.0.0 --port 8000"
        
        Write-Host "Waiting for API server to start (3 seconds)...`n" -ForegroundColor Cyan
        Start-Sleep -Seconds 3
        
        Write-Host "Starting Mobile App...`n" -ForegroundColor Cyan
        & .\env\Scripts\Activate.ps1
        python mobile_app.py
    }
    "8" {
        Write-Host "`nStarting API and Modern Mobile App with Login...`n" -ForegroundColor Yellow
        
        Write-Host "Starting FastAPI Server in new window...`n" -ForegroundColor Cyan
        $apiProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; & .\env\Scripts\Activate.ps1; uvicorn to_do_list:app --reload --host 0.0.0.0 --port 8000"
        
        Write-Host "Waiting for API server to start (3 seconds)...`n" -ForegroundColor Cyan
        Start-Sleep -Seconds 3
        
        Write-Host "Starting Modern Mobile App with Login...`n" -ForegroundColor Cyan
        & .\env\Scripts\Activate.ps1
        python modern_app.py
    }
    "9" {
        Write-Host "`nInstalling/Updating Dependencies...`n" -ForegroundColor Yellow
        & .\env\Scripts\Activate.ps1
        pip install -r requirements.txt
        Write-Host "`nDependencies installed successfully!`n" -ForegroundColor Green
    }
    default {
        Write-Host "Invalid choice. Please run the script again." -ForegroundColor Red
        exit 1
    }
}
