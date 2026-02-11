# Merge refactor/integrate-notebooks into merge_all_updates
# Run from project root: .\merge_branches.ps1

Set-Location $PSScriptRoot

Write-Host "Current branch:" -ForegroundColor Cyan
git branch --show-current

Write-Host "`nMerging refactor/integrate-notebooks..." -ForegroundColor Cyan
git merge refactor/integrate-notebooks

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nMerge has conflicts. Resolve them:" -ForegroundColor Yellow
    Write-Host "  - .ipynb files: Accept Incoming (Theirs)" -ForegroundColor Yellow
    Write-Host "  - src/*.py files: Accept Current (Ours)" -ForegroundColor Yellow
    Write-Host "Then run: git add . ; git commit -m 'Merge integrate-notebooks'" -ForegroundColor Yellow
} else {
    Write-Host "`nMerge complete." -ForegroundColor Green
}
