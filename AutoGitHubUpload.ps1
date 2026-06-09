# Decentralized Healthcare Management System - Automated GitHub Upload
# This script will handle the complete GitHub upload process

# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AUTOMATED GITHUB UPLOAD SYSTEM" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 This script will handle the complete GitHub upload process for you!" -ForegroundColor Green
Write-Host ""

Write-Host "📋 STEPS I WILL PERFORM:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣ Create GitHub repository" -ForegroundColor White
Write-Host "2️⃣ Install Git if needed" -ForegroundColor White
Write-Host "3️⃣ Initialize Git repository" -ForegroundColor White
Write-Host "4️⃣ Add all files to Git" -ForegroundColor White
Write-Host "5️⃣ Create initial commit" -ForegroundColor White
Write-Host "6️⃣ Push to GitHub" -ForegroundColor White
Write-Host "7️⃣ Enable GitHub Pages" -ForegroundColor White
Write-Host "8️⃣ Setup live demo" -ForegroundColor White
Write-Host ""

Write-Host "🔧 REQUIREMENTS:" -ForegroundColor Yellow
Write-Host "- GitHub account" -ForegroundColor White
Write-Host "- Internet connection" -ForegroundColor White
Write-Host "- Admin permissions (for Git install)" -ForegroundColor White
Write-Host ""

Write-Host "🎯 READY TO START?" -ForegroundColor Green
Read-Host "Press Enter to continue..."

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STEP 1: COLLECTING GITHUB INFORMATION" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$githubUsername = Read-Host "Please enter your GitHub username"
$githubToken = Read-Host "Please enter your GitHub token (create at github.com/settings/tokens)"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STEP 2: CREATING GITHUB REPOSITORY" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    $body = @{
        name = 'decentralized-healthcare-system'
        description = 'A Java-based decentralized healthcare management system with blockchain technology'
        private = $false
        auto_init = $false
    } | ConvertTo-Json

    $headers = @{
        'Authorization' = "token $githubToken"
        'Accept' = 'application/vnd.github.v3+json'
    }

    $response = Invoke-RestMethod -Uri 'https://api.github.com/user/repos' -Method POST -Headers $headers -Body $body
    Write-Host "✅ Repository created successfully!" -ForegroundColor Green
    Write-Host "Repository URL: $($response.html_url)" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Failed to create repository. Please check your credentials." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STEP 3: CHECKING/INSTALLING GIT" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    git --version | Out-Null
    Write-Host "✅ Git is already installed!" -ForegroundColor Green
}
catch {
    Write-Host "📦 Git not found. Installing Git..." -ForegroundColor Yellow
    
    try {
        # Try Chocolatey first
        choco --version | Out-Null
        Write-Host "Installing Git via Chocolatey..." -ForegroundColor Yellow
        choco install git -y --force
    }
    catch {
        Write-Host "Chocolatey not found. Installing Git directly..." -ForegroundColor Yellow
        
        # Download and install Git
        $gitInstaller = "Git-2.39.0.2-64-bit.exe"
        $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.39.0.windows.2/$gitInstaller"
        
        Write-Host "Downloading Git installer..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller
        
        Write-Host "Installing Git (this may take a few minutes)..." -ForegroundColor Yellow
        Start-Process -FilePath $gitInstaller -ArgumentList "/VERYSILENT /NORESTART" -Wait
        
        Remove-Item $gitInstaller -Force
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
    }
    
    # Verify Git installation
    try {
        git --version | Out-Null
        Write-Host "✅ Git installed successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Git installation failed. Please install Git manually from https://git-scm.com" -ForegroundColor Red
        Read-Host "Press Enter to exit..."
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STEP 4: INITIALIZING GIT REPOSITORY" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    git init
    git config user.name "Healthcare System Bot"
    git config user.email "healthcare@system.local"
    Write-Host "✅ Git repository initialized!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to initialize Git repository." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STEP 5: ADDING ALL FILES TO GIT" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    git add .
    Write-Host "✅ All files added to Git!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to add files to Git." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STEP 6: CREATING INITIAL COMMIT" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    $commitMessage = @"
🏥 Initial commit - Decentralized Healthcare Management System

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

🌐 Ready for deployment to GitHub Pages!
"@

    git commit -m $commitMessage
    Write-Host "✅ Initial commit created!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to create commit." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STEP 7: CONNECTING TO GITHUB" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    $repoUrl = "https://$githubUsername`:$githubToken@github.com/$githubUsername/decentralized-healthcare-system.git"
    git remote add origin $repoUrl
    Write-Host "✅ Connected to GitHub repository!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to connect to GitHub." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STEP 8: PUSHING TO GITHUB" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    git branch -M main
    git push -u origin main
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to push to GitHub. Please check your credentials." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STEP 9: ENABLING GITHUB PAGES" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    $pagesBody = @{
        source = @{
            branch = 'main'
            path = '/web'
        }
    } | ConvertTo-Json

    $pagesResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/$githubUsername/decentralized-healthcare-system/pages" -Method POST -Headers $headers -Body $pagesBody
    Write-Host "✅ GitHub Pages enabled!" -ForegroundColor Green
    Write-Host "Pages URL: $($pagesResponse.html_url)" -ForegroundColor Cyan
}
catch {
    Write-Host "⚠️ GitHub Pages may need to be enabled manually." -ForegroundColor Yellow
    Write-Host "Go to: https://github.com/$githubUsername/decentralized-healthcare-system/settings/pages" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🎉 UPLOAD COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🌐 Your repository is now live at:" -ForegroundColor Green
Write-Host "   https://github.com/$githubUsername/decentralized-healthcare-system" -ForegroundColor Cyan
Write-Host ""

Write-Host "🌐 Your live demo will be available at:" -ForegroundColor Green
Write-Host "   https://$githubUsername.github.io/decentralized-healthcare-system/" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 What's included:" -ForegroundColor Yellow
Write-Host "✅ Complete Java backend source code" -ForegroundColor White
Write-Host "✅ Modern web frontend application" -ForegroundColor White
Write-Host "✅ Comprehensive documentation" -ForegroundColor White
Write-Host "✅ MIT license" -ForegroundColor White
Write-Host "✅ Contribution guidelines" -ForegroundColor White
Write-Host "✅ GitHub Actions for CI/CD" -ForegroundColor White
Write-Host "✅ GitHub Pages deployment" -ForegroundColor White
Write-Host ""

Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "1. Visit your repository on GitHub" -ForegroundColor White
Write-Host "2. Wait 1-2 minutes for GitHub Pages to deploy" -ForegroundColor White
Write-Host "3. Access your live healthcare system demo" -ForegroundColor White
Write-Host "4. Share with others!" -ForegroundColor White
Write-Host ""

Write-Host "🏥 The Decentralized Healthcare Management System" -ForegroundColor Green
Write-Host "   is now available to the world!" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "           SUCCESS! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 Opening your repository in browser..." -ForegroundColor Yellow
Start-Process "https://github.com/$githubUsername/decentralized-healthcare-system"

Write-Host "🌐 Opening your live demo in browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
Start-Process "https://$githubUsername.github.io/decentralized-healthcare-system/"

Write-Host ""
Write-Host "🎉 All done! Your healthcare system is now live on GitHub!" -ForegroundColor Green
Read-Host "Press Enter to exit..."
