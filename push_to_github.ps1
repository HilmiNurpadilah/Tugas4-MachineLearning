# Script PowerShell untuk Push ke GitHub
# Jalankan dengan: .\push_to_github.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PUSH PROJECT KE GITHUB" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Git add
Write-Host "1. Adding files..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Git add failed!" -ForegroundColor Red
    exit 1
}
Write-Host "   ✅ Files added" -ForegroundColor Green
Write-Host ""

# 2. Git commit
Write-Host "2. Committing..." -ForegroundColor Yellow
git commit -m "Update app for Railway deployment"
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ⚠️  Nothing to commit or commit failed" -ForegroundColor Yellow
}
else {
    Write-Host "   ✅ Committed" -ForegroundColor Green
}
Write-Host ""

# 3. Set branch to main
Write-Host "3. Setting branch to main..." -ForegroundColor Yellow
git branch -M main
Write-Host "   ✅ Branch set to main" -ForegroundColor Green
Write-Host ""

# 4. Push to GitHub
Write-Host "4. Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "⚠️  Push failed! Trying force push..." -ForegroundColor Yellow
    git push -u origin main --force
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ Push failed!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Possible solutions:" -ForegroundColor Yellow
        Write-Host "1. Check your internet connection" -ForegroundColor White
        Write-Host "2. Check GitHub credentials" -ForegroundColor White
        Write-Host "3. Make sure repository exists: https://github.com/HilmiNurpadilah/Tugas4-MachineLearning" -ForegroundColor White
        exit 1
    }
}
Write-Host "   ✅ Pushed to GitHub" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ SUCCESS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository: https://github.com/HilmiNurpadilah/Tugas4-MachineLearning" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://railway.app" -ForegroundColor White
Write-Host "2. Login with GitHub" -ForegroundColor White
Write-Host "3. Create New Project → Deploy from GitHub" -ForegroundColor White
Write-Host "4. Select: HilmiNurpadilah/Tugas4-MachineLearning" -ForegroundColor White
Write-Host "5. Wait for build (~3-5 minutes)" -ForegroundColor White
Write-Host "6. Generate Domain in Settings → Networking" -ForegroundColor White
Write-Host ""
Write-Host "Read DEPLOY_RAILWAY.md for detailed instructions!" -ForegroundColor Cyan
Write-Host ""
