#!/usr/bin/env python3
"""Setup configuration for Agent CLI."""

from pathlib import Path
from setuptools import setup, find_packages

# Try to read README from parent dir or current dir
readme = Path(__file__).parent.parent / "README.md"
if not readme.exists():
    readme = Path(__file__).parent / "README.md"

long_description = readme.read_text(encoding="utf-8") if readme.exists() else "AI Agent CLI"

setup(
    name="ai-agent-cli",
    version="1.0.0",
    author="Afshin",
    description="CLI interface for orchestrating AI agents - piping ready for gh/glab integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["cli", "orchestrator", "copilot_models"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "click>=8.1.0",
        "anthropic>=0.25.0",
        "openai>=1.30.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "agent=cli:cli",
        ],
    },
    include_package_data=True,
)
