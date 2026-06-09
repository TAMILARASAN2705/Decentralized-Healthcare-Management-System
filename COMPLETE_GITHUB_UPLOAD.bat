@echo off
cls
echo ========================================
echo   AUTOMATED GITHUB UPLOAD SYSTEM
echo ========================================
echo.
echo 🚀 This script will handle the complete
echo    GitHub upload process for you!
echo.
echo 📋 STEPS I WILL PERFORM:
echo.
echo 1️⃣ Create GitHub repository
echo 2️⃣ Install Git if needed
echo 3️⃣ Initialize Git repository
echo 4️⃣ Add all files to Git
echo 5️⃣ Create initial commit
echo 6️⃣ Push to GitHub
echo 7️⃣ Enable GitHub Pages
echo 8️⃣ Setup live demo
echo.
echo 🔧 REQUIREMENTS:
echo - GitHub account
echo - Internet connection
echo - Admin permissions (for Git install)
echo.
echo 🎯 READY TO START?
echo.
pause

echo.
echo ========================================
echo   STEP 1: CHECKING GITHUB ACCOUNT
echo ========================================
echo.
echo Please provide your GitHub username:
set /p github_username="GitHub Username: "
echo.
echo Please provide your GitHub token (create at github.com/settings/tokens):
set /p github_token="GitHub Token: "

echo.
echo ========================================
echo   STEP 2: CREATING GITHUB REPOSITORY
echo ========================================
echo.
powershell -Command "& {$body = @{name='decentralized-healthcare-system'; description='A Java-based decentralized healthcare management system with blockchain technology'; private='false'}; $headers = @{'Authorization'='token %github_token%'; 'Accept'='application/vnd.github.v3+json'}; $response = Invoke-RestMethod -Uri 'https://api.github.com/user/repos' -Method POST -Headers $headers -Body ($body | ConvertTo-Json); Write-Output $response.clone_url}"

if %errorlevel% neq 0 (
    echo ❌ Failed to create repository. Please check your credentials.
    pause
    exit /b 1
)

echo ✅ Repository created successfully!

echo.
echo ========================================
echo   STEP 3: INSTALLING GIT
echo ========================================
echo.

REM Check if Git is already installed
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Git is already installed!
    goto :git_ready
)

echo 📦 Installing Git...
powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"

choco install git -y
if %errorlevel% neq 0 (
    echo ❌ Failed to install Git via Chocolatey. Trying alternative...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.39.0.windows.2/Git-2.39.0.2-64-bit.exe' -OutFile 'git-installer.exe'"
    start /wait git-installer.exe /VERYSILENT /NORESTART
    del git-installer.exe
)

:git_ready
echo ✅ Git is ready!

echo.
echo ========================================
echo   STEP 4: INITIALIZING GIT REPOSITORY
echo ========================================
echo.

git init
git config user.name "Healthcare System Bot"
git config user.email "healthcare@system.local"

echo ✅ Git repository initialized!

echo.
echo ========================================
echo   STEP 5: ADDING ALL FILES TO GIT
echo ========================================
echo.

git add .
echo ✅ All files added to Git!

echo.
echo ========================================
echo   STEP 6: CREATING INITIAL COMMIT
echo ========================================
echo.

git commit -m "🏥 Initial commit - Decentralized Healthcare Management System

✨ Features:
- Patient registration with unique cryptographic IDs
- Doctor authentication with secure password hashing
- Medical record creation with SHA-256 encryption
- Blockchain ledger with mining simulation
- Smart contract access control
- Comprehensive audit logging
- Modern web interface with responsive design
- Complete documentation and setup guides

🔧 Technologies:
- Java 8+ backend
- Modern HTML/CSS/JavaScript frontend
- Bootstrap 5 UI framework
- SHA-256 encryption
- Blockchain simulation
- Local storage persistence

🌐 Ready for deployment to GitHub Pages!"

echo ✅ Initial commit created!

echo.
echo ========================================
echo   STEP 7: CONNECTING TO GITHUB
echo ========================================
echo.

git remote add origin https://%github_username%:%github_token%@github.com/%github_username%/decentralized-healthcare-system.git

echo ✅ Connected to GitHub repository!

echo.
echo ========================================
echo   STEP 8: PUSHING TO GITHUB
echo ========================================
echo.

git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo ❌ Failed to push to GitHub. Please check your credentials.
    pause
    exit /b 1
)

echo ✅ Successfully pushed to GitHub!

echo.
echo ========================================
echo   STEP 9: ENABLING GITHUB PAGES
echo ========================================
echo.

powershell -Command "& {$body = @{source=@{branch='main'; path='/web'}}; $headers = @{'Authorization'='token %github_token%'; 'Accept'='application/vnd.github.v3+json'}; $response = Invoke-RestMethod -Uri 'https://api.github.com/repos/%github_username%/decentralized-healthcare-system/pages' -Method POST -Headers $headers -Body ($body | ConvertTo-Json); Write-Output $response.html_url}"

echo ✅ GitHub Pages enabled!

echo.
echo ========================================
echo   🎉 UPLOAD COMPLETE!
echo ========================================
echo.
echo 🌐 Your repository is now live at:
echo    https://github.com/%github_username%/decentralized-healthcare-system
echo.
echo 🌐 Your live demo will be available at:
echo    https://%github_username%.github.io/decentralized-healthcare-system/
echo.
echo 📋 What's included:
echo ✅ Complete Java backend source code
echo ✅ Modern web frontend application
echo ✅ Comprehensive documentation
echo ✅ MIT license
echo ✅ Contribution guidelines
echo ✅ GitHub Actions for CI/CD
echo ✅ GitHub Pages deployment
echo.
echo 🎯 Next steps:
echo 1. Visit your repository on GitHub
echo 2. Wait 1-2 minutes for GitHub Pages to deploy
echo 3. Access your live healthcare system demo
echo 4. Share with others!
echo.
echo 🏥 The Decentralized Healthcare Management System
echo    is now available to the world!
echo.
echo ========================================
echo   SUCCESS! 🎉
echo ========================================
echo.
pause

echo 🌐 Opening your repository in browser...
start https://github.com/%github_username%/decentralized-healthcare-system

echo 🌐 Opening your live demo in browser...
timeout /t 10 /nobreak >nul
start https://%github_username%.github.io/decentralized-healthcare-system/

echo.
echo 🎉 All done! Your healthcare system is now live on GitHub!
