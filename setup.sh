#!/usr/bin/env bash
# =============================================================
# AI Agent – One-Command Setup  (Linux / macOS)
# Usage:  bash setup.sh
#
# Auth resolution:
#   1. Uses ANTHROPIC_KEY / OPENAI_KEY if already set in environment
#   2. Falls back to GitHub Copilot OAuth (auto device-flow login on first run)
# =============================================================
set -e

VENV_DIR=".venv"
ENV_FILE=".env"
REQUIREMENTS="requirements.txt"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   AI Agent – Environment Setup           ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── 1. Virtual environment ───────────────────────────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
  echo "🐍 Creating Python virtual environment..."

  # Try python3 first, then python
  if command -v python3 &> /dev/null; then
    python3 -m venv "$VENV_DIR"
  elif command -v python &> /dev/null; then
    python -m venv "$VENV_DIR"
  else
    echo "❌ Error: Python not found. Please install Python 3.9 or higher."
    exit 1
  fi

  # Verify venv was created
  if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "❌ Error: Virtual environment creation failed."
    echo "   Please install python3-venv package:"
    echo "   sudo apt install python3-venv  (Ubuntu/Debian)"
    echo "   sudo yum install python3-venv  (RedHat/CentOS)"
    exit 1
  fi

  echo "   ✅ Virtual environment created successfully"
else
  echo "✅ Virtual environment already exists."
fi

# ── 2. Activate and upgrade pip ──────────────────────────────────────────────
echo "⬆️  Activating venv and upgrading pip..."

# Verify activate script exists
if [ ! -f "$VENV_DIR/bin/activate" ]; then
  echo "❌ Error: $VENV_DIR/bin/activate not found"
  echo "   Removing corrupt venv directory..."
  rm -rf "$VENV_DIR"
  echo "   Please run setup.sh again"
  exit 1
fi

source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip --quiet

# ── 3. Install dependencies ──────────────────────────────────────────────────
echo "📦 Installing dependencies from $REQUIREMENTS..."
pip install -r "$REQUIREMENTS" --quiet

# ── 3b. Install CLI ──────────────────────────────────────────────────────────
echo "🔧 Installing agent CLI (makes 'agent' command available)..."
pip install -e agent_core --quiet
echo "   ✅ CLI installed: 'agent' command is now available"

# ── 4. Resolve API keys ──────────────────────────────────────────────────────
echo ""
echo "🔑 Resolving auth keys..."

ANTHROPIC_KEY="${ANTHROPIC_KEY:-}"
OPENAI_KEY="${OPENAI_KEY:-}"

echo ""
if [ -n "$ANTHROPIC_KEY" ]; then
  echo "  ✅ Claude  → ANTHROPIC_KEY (direct API)"
else
  echo "  ✅ Claude  → will use Copilot (auto-login on first run)"
fi

if [ -n "$OPENAI_KEY" ]; then
  echo "  ✅ GPT     → OPENAI_KEY (direct API)"
else
  echo "  ✅ GPT     → will use Copilot (auto-login on first run)"
fi

echo ""
echo "  Auth note: On first 'agent' run, if no direct API keys are found,"
echo "  the tool will start a GitHub OAuth login in your browser (one-time)."
echo "  This uses the same Copilot access as your IDE."
echo ""

# ── 5. Write .env ─────────────────────────────────────────────────────────────
if [ ! -f "$ENV_FILE" ]; then
  {
    echo "# AI Agent – Environment Variables"
    echo "#"
    echo "# Auth priority (per provider):"
    echo "#   1. ANTHROPIC_KEY / OPENAI_KEY  (direct API — overrides Copilot for that provider)"
    echo "#   2. GitHub Copilot OAuth        (automatic — device flow login on first run)"
    echo "#"
    echo "# For most users, no keys are needed here. The agent will authenticate"
    echo "# via GitHub Copilot using an OAuth browser login (one-time)."
    echo "#"
    echo "# Set direct keys only if you want to bypass Copilot for a specific provider:"
    echo ""

    if [ -n "$ANTHROPIC_KEY" ]; then
      echo "ANTHROPIC_KEY=$ANTHROPIC_KEY"
    else
      echo "# ANTHROPIC_KEY=sk-ant-your-key-here  # optional: direct Anthropic API"
    fi

    if [ -n "$OPENAI_KEY" ]; then
      echo "OPENAI_KEY=$OPENAI_KEY"
    else
      echo "# OPENAI_KEY=sk-your-key-here          # optional: direct OpenAI API"
    fi
  } > "$ENV_FILE"

  echo "📄 Created .env template."
else
  echo "✅ .env already exists — not overwritten."
fi

# ── 6. Validate setup ────────────────────────────────────────────────────────
echo ""
echo "🔍 Validating agent setup..."
python agent_core/tools/inspector.py agent_core --validate || true

# ── 7. Done ──────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  ✅  Setup complete!                     ║"
echo "║                                          ║"
echo "║  Next steps:                             ║"
echo "║  1. Review .env (optional, for overrides)║"
echo "║  2. source .venv/bin/activate            ║"
echo "║                                          ║"
echo "║  Run orchestrator:                       ║"
echo "║    python agent_core/orchestrator.py 001 ║"
echo "║                                          ║"
echo "║  Or use CLI:                             ║"
echo "║    agent execute task.md                 ║"
echo "║    agent review --help                   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

