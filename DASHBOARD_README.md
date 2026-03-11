# 🎛️ AI Agent Dynamic Dashboard

A **live, editable dashboard** that reads directly from your config files and updates them in real-time.

## Features

✅ **Live Config Display** — Shows actual values from `config.yaml` and `config/models.yaml`  
✅ **In-Place Editing** — Update skill assignments, model configs, critic settings  
✅ **Auto-Refresh** — Refreshes every 30 seconds  
✅ **Environment Status** — Shows which API keys are set  
✅ **Memory Stats** — Displays memory folder statistics  
✅ **System Stats** — Shows total skills, status, and more  

## Quick Start

### Option 1: Windows
```bash
dashboard.bat
```

### Option 2: Linux/macOS
```bash
bash dashboard.sh
```

### Option 3: Manual
```bash
source .venv/bin/activate       # or: .\.venv\Scripts\Activate.ps1
cd agent_core
python dashboard_server.py
```

Then open: **http://localhost:5000**

---

## What You Can Do

### 1. View Current Configuration
- See all Claude 4 and GPT-5.4 models
- Check which models are assigned to which skills
- View critic loop settings
- Check environment variable status

### 2. Edit Skill Assignments
- Change which model a skill uses
- Click "Save All" to update `config.yaml`
- Changes persist immediately

### 3. Update Critic Configuration
- Enable/disable critic loop
- Change max iterations (1-10)
- Set quality threshold (0-100)
- Click "Save" to update `config.yaml`

### 4. Monitor System
- Memory folder size and file count
- Total skills configured
- System operational status

---

## API Endpoints

The dashboard server exposes REST APIs:

### GET /api/status
Returns full system status (config + models + env + memory + skills)

```bash
curl http://localhost:5000/api/status
```

### GET /api/config
Returns main `config.yaml` content

```bash
curl http://localhost:5000/api/config
```

### POST /api/config
Updates main `config.yaml`

```bash
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d @new_config.json
```

### GET /api/models
Returns `config/models.yaml` content

```bash
curl http://localhost:5000/api/models
```

### POST /api/models
Updates `config/models.yaml`

```bash
curl -X POST http://localhost:5000/api/models \
  -H "Content-Type: application/json" \
  -d @new_models.json
```

### POST /api/config/critic
Updates critic loop configuration

```bash
curl -X POST http://localhost:5000/api/config/critic \
  -H "Content-Type: application/json" \
  -d '{"enabled": true, "max_iterations": 5, "quality_threshold": 90}'
```

---

## Architecture

```
dashboard_server.py          # Flask server
├── Reads:
│   ├── config.yaml          # Main config
│   ├── config/models.yaml   # Model definitions
│   ├── memory/*.md          # Memory files
│   └── skills/*/*/SKILL.md  # Skill definitions
│
├── Writes (on save):
│   ├── config.yaml          # Updated config
│   └── config/models.yaml   # Updated models
│
└── Serves:
    └── templates/dashboard_dynamic.html  # Dynamic dashboard
```

---

## Configuration Files

### config.yaml
```yaml
auth:
  required: [GITHUB_COPILOT_TOKEN]
  optional_overrides: [ANTHROPIC_KEY, OPENAI_KEY]

critic_loop:
  enabled: true
  max_iterations: 5
  quality_threshold: 90
  adaptive_thresholds:
    hotfix: 75
    bug_fix: 85
    feature: 90

models:
  claude_haiku: claude-4-haiku-20260115
  claude_sonnet: claude-4-sonnet-20260201
  claude_opus: claude-4.6-opus-20260301
  gpt_5_4: gpt-5.4-2026-02-15

skill_models:
  gather_requirements: claude_sonnet
  write_spec: claude_opus
  implement_feature: claude_sonnet
  generate_tests: gpt_5_4
  # ... all 20 skills
```

### config/models.yaml
```yaml
models:
  claude:
    haiku:
      version: "4.0"
      id: "claude-4-haiku-20260115"
      cost: { input: 0.5, output: 2.5 }
    sonnet:
      version: "4.0"
      id: "claude-4-sonnet-20260201"
      cost: { input: 2, output: 10 }
    opus:
      version: "4.6"
      id: "claude-4.6-opus-20260301"
      cost: { input: 12, output: 60 }
  gpt:
    gpt-5.4:
      version: "5.4"
      id: "gpt-5.4-2026-02-15"
      cost: { input: 8, output: 24 }
```

---

## Example Workflow

### 1. View current config
```bash
# Start dashboard
dashboard.bat

# Open browser
http://localhost:5000
```

### 2. Change a skill's model
- Find "implement_feature" in Skill Assignments
- Change from `claude/sonnet` to `claude/opus`
- Click "Save All"
- Config file updates immediately

### 3. Update critic threshold
- Go to "Critic Loop Config"
- Change threshold from 90 to 85
- Click "Save"
- Changes apply instantly

### 4. Verify changes
```bash
# Check config file
cat agent_core/config.yaml

# Or refresh dashboard
```

---

## Troubleshooting

### Dashboard won't start
```bash
# Install dependencies
pip install flask flask-cors

# Or re-run setup
.\setup.ps1     # Windows
bash setup.sh   # Linux/macOS
```

### Can't save changes
- Check file permissions on `config.yaml`
- Make sure server has write access
- Check server console for error messages

### Port 5000 already in use
Edit `dashboard_server.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

---

## Static vs Dynamic Dashboard

### Old (Static)
- **File:** `dashboard.html`
- **Type:** Static HTML file
- **Data:** Hardcoded examples
- **Editing:** Not possible

### New (Dynamic) ✅
- **File:** `dashboard_server.py` + `templates/dashboard_dynamic.html`
- **Type:** Flask web app
- **Data:** Live from config files
- **Editing:** Yes — updates config files directly

**Use the dynamic dashboard for real work!**

---

## Security Note

⚠️ The dashboard server runs on **localhost only** by default and is intended for **local development use**.

Do not expose it to the internet without:
- Adding authentication
- Using HTTPS
- Implementing rate limiting
- Validating all inputs

---

## Next Steps

1. **Start dashboard:** `dashboard.bat` or `bash dashboard.sh`
2. **Open browser:** http://localhost:5000
3. **Update configs:** Edit skill assignments or critic settings
4. **Save changes:** Click "Save" buttons
5. **Verify:** Check `config.yaml` or refresh dashboard

**Your config files are now editable through a beautiful UI!** 🎉

