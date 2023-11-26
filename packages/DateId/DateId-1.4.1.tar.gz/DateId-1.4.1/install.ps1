Write-Host "Running D:\Dropbox\Projects\BEE\DateId\install.ps1..." -ForegroundColor Yellow
if (Test-Path -Path $env:PROJECT_DIR\pyproject.toml) {pip install --no-cache-dir -e .[dev]}
