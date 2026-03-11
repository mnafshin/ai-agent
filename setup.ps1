# =============================================================
# AI Agent - One-Command Setup  (Windows PowerShell)
# Usage:  .\setup.ps1
#
# Auth resolution:
#   1. GITHUB_TOKEN (PAT) → GitHub Models API (covers GPT-4o for all 20 skills)
#   2. ANTHROPIC_KEY      → direct Claude API (optional, overrides GPT fallback)
#   3. OPENAI_KEY         → direct OpenAI API (optional, overrides GitHub Models)
# =============================================================

$ErrorActionPreference = "Stop"
$VenvDir  = ".venv"
$EnvFile  = ".env"
$ReqFile  = "requirements.txt"

Write-Host ""
Write-Host "+==========================================+" -ForegroundColor Cyan
Write-Host "|   AI Agent - Environment Setup           |" -ForegroundColor Cyan
Write-Host "+==========================================+" -ForegroundColor Cyan
Write-Host ""

# -- 1. Virtual environment ------------------------------------------------
if (-Not (Test-Path $VenvDir)) {
    Write-Host "[VENV] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv $VenvDir
} else {
    Write-Host "[OK] Virtual environment already exists." -ForegroundColor Green
}

# -- 2. Activate and upgrade pip -------------------------------------------
Write-Host "[PIP] Activating venv and upgrading pip..." -ForegroundColor Yellow
& "$VenvDir\Scripts\Activate.ps1"
python -m pip install --upgrade pip --quiet

# -- 3. Install dependencies -----------------------------------------------
Write-Host "[DEPS] Installing dependencies from $ReqFile..." -ForegroundColor Yellow
pip install -r $ReqFile --quiet

# -- 3b. Install CLI -------------------------------------------------------
Write-Host "[CLI] Installing agent CLI..." -ForegroundColor Yellow
pip install -e agent_core --quiet
Write-Host "   [OK] CLI installed: 'agent' command is now available" -ForegroundColor Green

# -- 4. Resolve API keys ---------------------------------------------------
Write-Host ""
Write-Host "[AUTH] Resolving auth keys..." -ForegroundColor Yellow

$GithubToken   = [Environment]::GetEnvironmentVariable("GITHUB_TOKEN",  "User")
$AnthropicKey  = [Environment]::GetEnvironmentVariable("ANTHROPIC_KEY", "User")
$OpenAIKey     = [Environment]::GetEnvironmentVariable("OPENAI_KEY",    "User")

# If nothing at all, prompt for the GitHub PAT
if (-Not $GithubToken -and -Not $AnthropicKey -and -Not $OpenAIKey) {
    Write-Host ""
    Write-Host "  No API keys found in environment." -ForegroundColor Yellow
    Write-Host "  A GitHub PAT with 'models' access covers GPT-4o for all 20 skills." -ForegroundColor Cyan
    Write-Host "  Create one at: https://github.com/settings/tokens" -ForegroundColor Cyan
    Write-Host ""
    $GithubToken = Read-Host "  Enter GITHUB_TOKEN (or press Enter to edit .env manually later)"
    if ($GithubToken) {
        [Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $GithubToken, "User")
        Write-Host "  [OK] GITHUB_TOKEN saved to user environment." -ForegroundColor Green
    }
}

Write-Host ""
if ($AnthropicKey) {
    Write-Host "  [OK] Claude  -> ANTHROPIC_KEY (direct Anthropic API)" -ForegroundColor Green
} elseif ($GithubToken) {
    Write-Host "  [OK] Claude  -> GPT fallback (via GitHub Models API)" -ForegroundColor Green
} else {
    Write-Host "  [WARN] Claude  -> no key (set GITHUB_TOKEN or ANTHROPIC_KEY)" -ForegroundColor Yellow
}

if ($OpenAIKey) {
    Write-Host "  [OK] GPT     -> OPENAI_KEY (direct OpenAI API)" -ForegroundColor Green
} elseif ($GithubToken) {
    Write-Host "  [OK] GPT     -> GITHUB_TOKEN (GitHub Models API)" -ForegroundColor Green
} else {
    Write-Host "  [WARN] GPT     -> no key (set GITHUB_TOKEN or OPENAI_KEY)" -ForegroundColor Yellow
}
Write-Host ""

# -- 5. Write .env ---------------------------------------------------------
if (-Not (Test-Path $EnvFile)) {
    $GhLine        = if ($GithubToken)  { "GITHUB_TOKEN=$GithubToken" }  else { "# GITHUB_TOKEN=ghp_your-token-here" }
    $AnthropicLine = if ($AnthropicKey) { "ANTHROPIC_KEY=$AnthropicKey" } else { "# ANTHROPIC_KEY=sk-ant-your-key-here  # optional" }
    $OpenAILine    = if ($OpenAIKey)    { "OPENAI_KEY=$OpenAIKey" }       else { "# OPENAI_KEY=sk-your-key-here          # optional" }

    @"
# AI Agent - Environment Variables
#
# GITHUB_TOKEN (PAT) gives access to GPT-4o via GitHub Models API.
# All 20 skills work with just this token.
# Optional: ANTHROPIC_KEY for real Claude, OPENAI_KEY for direct OpenAI.

$GhLine

$AnthropicLine
$OpenAILine
"@ | Out-File -FilePath $EnvFile -Encoding utf8

    Write-Host "[OK] Created .env template." -ForegroundColor Yellow
} else {
    Write-Host "[OK] .env already exists -- not overwritten." -ForegroundColor Cyan
}

# -- 6. Validate setup -----------------------------------------------------
Write-Host ""
Write-Host "[CHECK] Validating agent setup..." -ForegroundColor Yellow
python agent_core/tools/inspector.py agent_core --validate

# -- 7. Done ---------------------------------------------------------------
Write-Host ""
Write-Host "+==========================================+" -ForegroundColor Cyan
Write-Host "|  Setup complete!                         |" -ForegroundColor Cyan
Write-Host "|                                          |" -ForegroundColor Cyan
Write-Host "|  Next steps:                             |" -ForegroundColor Cyan
Write-Host "|  1. .\.venv\Scripts\Activate.ps1         |" -ForegroundColor Cyan
Write-Host "|  2. agent status                         |" -ForegroundColor Cyan
Write-Host "|  3. agent execute task.md                |" -ForegroundColor Cyan
Write-Host "+==========================================+" -ForegroundColor Cyan
Write-Host ""
