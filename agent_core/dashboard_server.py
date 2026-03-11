#!/usr/bin/env python3
"""
Dynamic Dashboard Server for Agent Core
Reads config files and allows in-place updates.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import yaml
import json
from pathlib import Path
from datetime import datetime
import os

# Load .env files (check both parent and agent_core directories)
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Base paths
BASE_PATH = Path(__file__).parent
CONFIG_PATH = BASE_PATH / "config.yaml"
MODELS_CONFIG_PATH = BASE_PATH / "config" / "models.yaml"
MEMORY_PATH = BASE_PATH / "memory"

# Load .env files in priority order:
# 1. agent_core/.env (local to dashboard)
# 2. parent/.env (project root)
load_dotenv(BASE_PATH / '.env')              # Load from agent_core/.env
load_dotenv(BASE_PATH.parent / '.env')       # Load from project root .env

print(f"📂 Loading environment variables from:")
print(f"   - {BASE_PATH / '.env'}")
print(f"   - {BASE_PATH.parent / '.env'}")


def load_config():
    """Load main config.yaml"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def load_models_config():
    """Load config/models.yaml"""
    if MODELS_CONFIG_PATH.exists():
        with open(MODELS_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def save_config(data):
    """Save main config.yaml"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def save_models_config(data):
    """Save config/models.yaml"""
    with open(MODELS_CONFIG_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def get_env_status():
    """Check environment variables for all supported providers."""
    return {
        "github_token":       bool(os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_COPILOT_TOKEN")),
        "anthropic_key":      bool(os.getenv("ANTHROPIC_KEY")),
        "openai_key":         bool(os.getenv("OPENAI_KEY")),
        "aws_bedrock":        bool(os.getenv("AWS_ACCESS_KEY_ID")),
        "gcp_vertex":         bool(os.getenv("GOOGLE_CLOUD_PROJECT")),
        "local_llm":          bool(os.getenv("LOCAL_LLM_URL")),
        "llm_provider":       os.getenv("LLM_PROVIDER", "auto"),
    }


def get_memory_stats():
    """Get memory folder statistics"""
    if not MEMORY_PATH.exists():
        return {"total_files": 0, "total_size": 0}

    files = list(MEMORY_PATH.glob("*.md"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())

    return {
        "total_files": len(files),
        "total_size": total_size,
        "files": [{"name": f.name, "size": f.stat().st_size} for f in files]
    }


def get_skills_list():
    """Get list of all skills from file system"""
    skills_path = BASE_PATH / "skills"
    skills = []

    if skills_path.exists():
        for team_dir in skills_path.iterdir():
            if team_dir.is_dir() and not team_dir.name.startswith('.'):
                for skill_dir in team_dir.iterdir():
                    if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                        skills.append({
                            "name": skill_dir.name,
                            "team": team_dir.name,
                            "path": str(skill_dir.relative_to(BASE_PATH))
                        })

    return skills


@app.route('/')
def index():
    """Serve dashboard"""
    return render_template('dashboard_dynamic.html')


@app.route('/api/status')
def api_status():
    """Get current system status"""
    config = load_config()
    models_config = load_models_config()
    env_status = get_env_status()
    memory_stats = get_memory_stats()
    skills = get_skills_list()

    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "config": config,
        "models": models_config,
        "env": env_status,
        "memory": memory_stats,
        "skills": skills,
        "status": "operational"
    })


@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """Get or update main config"""
    if request.method == 'GET':
        return jsonify(load_config())

    elif request.method == 'POST':
        try:
            new_config = request.json
            save_config(new_config)
            return jsonify({"success": True, "message": "Config updated successfully"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/models', methods=['GET', 'POST'])
def api_models():
    """Get or update models config"""
    if request.method == 'GET':
        return jsonify(load_models_config())

    elif request.method == 'POST':
        try:
            new_config = request.json
            save_models_config(new_config)
            return jsonify({"success": True, "message": "Models config updated successfully"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/config/skill_models', methods=['POST'])
def update_skill_model():
    """Update a single skill's model assignment"""
    try:
        data = request.json
        skill_name = data.get('skill')
        new_model = data.get('model')

        config = load_config()
        if 'skill_models' not in config:
            config['skill_models'] = {}

        config['skill_models'][skill_name] = new_model
        save_config(config)

        return jsonify({"success": True, "message": f"Updated {skill_name} to {new_model}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/config/critic', methods=['POST'])
def update_critic_config():
    """Update critic loop configuration"""
    try:
        data = request.json
        config = load_config()

        if 'critic_loop' not in config:
            config['critic_loop'] = {}

        config['critic_loop'].update(data)
        save_config(config)

        return jsonify({"success": True, "message": "Critic config updated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = BASE_PATH / 'templates'
    templates_dir.mkdir(exist_ok=True)

    print(f"""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║      AI Agent Dashboard Server                       ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

📊 Dashboard: http://localhost:5000
🔧 Config API: http://localhost:5000/api/config
🤖 Models API: http://localhost:5000/api/models

Starting server...
""")

    app.run(debug=True, host='0.0.0.0', port=5000)

