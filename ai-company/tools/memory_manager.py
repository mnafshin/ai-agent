#!/usr/bin/env python3
"""
Memory Manager - Handles memory indexing, lazy loading, and efficient access.
Prevents memory bottlenecks as project grows.
"""

import json
import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import yaml
import re

class MemoryIndex:
    """Fast lookup index for memory files."""
    
    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path)
        self.index_file = self.memory_path / "index.yaml"
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load index from file."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return yaml.safe_load(f) or {}
        return {
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_decisions": 0,
                "total_bugs": 0,
                "total_reviews": 0,
            },
            "recent_decisions": [],
            "recent_bugs": [],
            "recent_reviews": [],
            "summaries": {},
            "archives": {"available": []}
        }
    
    def save_index(self):
        """Save index to file."""
        self.index["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w') as f:
            yaml.dump(self.index, f, default_flow_style=False)
    
    def rebuild_index(self):
        """Rebuild index from memory files."""
        print("🔄 Rebuilding memory index...")
        
        self.index["recent_decisions"] = self._index_file("decisions.md", "decision")
        self.index["recent_bugs"] = self._index_file("debug_log.md", "bug")
        self.index["recent_reviews"] = self._index_file("review_log.md", "review")
        
        self.index["metadata"]["total_decisions"] = self._count_entries("decisions.md")
        self.index["metadata"]["total_bugs"] = self._count_entries("debug_log.md")
        self.index["metadata"]["total_reviews"] = self._count_entries("review_log.md")
        
        self.save_index()
        print("✅ Index rebuilt")
    
    def _index_file(self, filename: str, entry_type: str) -> List[Dict]:
        """Extract entries from memory file."""
        file_path = self.memory_path / filename
        if not file_path.exists():
            return []
        
        entries = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Find header lines and create quick references
        for i, line in enumerate(lines):
            if line.startswith("## "):
                # Extract date and topic
                match = re.match(r"## (\d{4}-\d{2}-\d{2}):(.*)", line)
                if match:
                    date = match.group(1)
                    topic = match.group(2).strip()
                    entries.append({
                        "date": date,
                        "topic": topic[:50],  # First 50 chars
                        "line": i + 1,
                        "entry_type": entry_type
                    })
        
        # Keep only last 20 for quick access
        return sorted(entries, key=lambda x: x["date"], reverse=True)[:20]
    
    def _count_entries(self, filename: str) -> int:
        """Count total entries in file."""
        file_path = self.memory_path / filename
        if not file_path.exists():
            return 0
        with open(file_path, 'r') as f:
            return sum(1 for line in f if line.startswith("## "))
    
    def search(self, keyword: str, file_type: str = "decisions") -> List[Dict]:
        """Search through memory files."""
        file_map = {
            "decisions": "decisions.md",
            "bugs": "debug_log.md",
            "reviews": "review_log.md"
        }
        
        filepath = self.memory_path / file_map.get(file_type, "decisions.md")
        if not filepath.exists():
            return []
        
        results = []
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                results.append({
                    "line": i + 1,
                    "content": line.strip()[:100],
                    "file": file_map[file_type]
                })
        
        return results[:10]  # Limit to 10 results


class MemoryManager:
    """Efficient memory access with lazy loading and caching."""
    
    def __init__(self, memory_path: Path, use_sqlite: bool = False):
        self.memory_path = Path(memory_path)
        self.index = MemoryIndex(memory_path)
        self.use_sqlite = use_sqlite
        self.cache = {}  # In-memory cache
        
        if use_sqlite:
            self.db_path = self.memory_path / "memory.db"
            self._init_sqlite()
    
    def _init_sqlite(self):
        """Initialize SQLite database for large-scale memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY,
                date TEXT,
                topic TEXT,
                content TEXT,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS debug_log (
                id INTEGER PRIMARY KEY,
                date TEXT,
                component TEXT,
                issue TEXT,
                resolution TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_log (
                id INTEGER PRIMARY KEY,
                date TEXT,
                file TEXT,
                score INTEGER,
                issues TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for fast queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_decisions_date ON decisions(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_debug_date ON debug_log(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_review_file ON review_log(file)")
        
        conn.commit()
        conn.close()
    
    def get_recent_decisions(self, limit: int = 10) -> List[Dict]:
        """Get recent decisions without loading entire file."""
        if "recent_decisions" in self.cache:
            return self.cache["recent_decisions"][:limit]
        
        decisions = []
        file_path = self.memory_path / "decisions.md"
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract decision headers
        entries = re.findall(r"## ([\d-]+): (.+?)\n(.*?)(?=##|\Z)", content, re.DOTALL)
        decisions = [
            {"date": date, "topic": topic.strip(), "content": content[:500]}
            for date, topic, content in entries[-limit:]
        ]
        
        self.cache["recent_decisions"] = decisions
        return decisions
    
    def get_recent_bugs(self, limit: int = 10) -> List[Dict]:
        """Get recent bugs without loading entire file."""
        if "recent_bugs" in self.cache:
            return self.cache["recent_bugs"][:limit]
        
        bugs = []
        file_path = self.memory_path / "debug_log.md"
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract bug entries
        entries = re.findall(r"## ([\d-]+): (.+?)\n(.*?)(?=##|\Z)", content, re.DOTALL)
        bugs = [
            {"date": date, "issue": topic.strip(), "resolution": content[:300]}
            for date, topic, content in entries[-limit:]
        ]
        
        self.cache["recent_bugs"] = bugs
        return bugs
    
    def get_recent_reviews(self, limit: int = 10) -> List[Dict]:
        """Get recent code reviews without loading entire file."""
        if "recent_reviews" in self.cache:
            return self.cache["recent_reviews"][:limit]
        
        reviews = []
        file_path = self.memory_path / "review_log.md"
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract review entries
        entries = re.findall(r"## ([\d-]+): (.+?) - Score: (\d+)(.*?)(?=##|\Z)", content, re.DOTALL)
        reviews = [
            {"date": date, "file": topic.strip(), "score": int(score), "notes": notes.strip()[:300]}
            for date, topic, score, notes in entries[-limit:]
        ]
        
        self.cache["recent_reviews"] = reviews
        return reviews
    
    def create_summary(self) -> Dict[str, str]:
        """Create concise summaries of key decisions."""
        summaries = {}
        
        # Decisions summary
        decisions = self.get_recent_decisions(5)
        if decisions:
            topics = ", ".join(d["topic"] for d in decisions[:3])
            summaries["decisions"] = f"Recent decisions: {topics}"
        
        # Bugs summary
        bugs = self.get_recent_bugs(5)
        if bugs:
            issues = ", ".join(b["issue"] for b in bugs[:3])
            summaries["bugs"] = f"Recent issues: {issues}"
        
        # Reviews summary
        reviews = self.get_recent_reviews(5)
        if reviews:
            avg_score = sum(r["score"] for r in reviews) / len(reviews)
            summaries["reviews"] = f"Recent quality score: {avg_score:.0f}/100"
        
        return summaries
    
    def get_context_for_agent(self) -> str:
        """Generate concise context for agent (tokens-efficient)."""
        context = "# Memory Context\n\n"
        
        # Add summaries instead of full history
        summaries = self.create_summary()
        for key, summary in summaries.items():
            context += f"## {key.title()}\n{summary}\n\n"
        
        # Add recent high-impact items
        context += "## Recent Decisions\n"
        for decision in self.get_recent_decisions(3):
            context += f"- {decision['date']}: {decision['topic']}\n"
        
        context += "\n## Recent Issues Fixed\n"
        for bug in self.get_recent_bugs(3):
            context += f"- {bug['date']}: {bug['issue']}\n"
        
        return context
    
    def get_stats(self) -> Dict[str, int]:
        """Get memory statistics."""
        return {
            "total_decisions": self.index.index["metadata"]["total_decisions"],
            "total_bugs": self.index.index["metadata"]["total_bugs"],
            "total_reviews": self.index.index["metadata"]["total_reviews"],
            "cache_size": len(self.cache)
        }


if __name__ == "__main__":
    # Example usage
    import sys
    
    memory_path = Path("memory")
    manager = MemoryManager(memory_path)
    
    print("🧠 Memory Manager")
    print(manager.get_context_for_agent())
    print("\n📊 Stats:", manager.get_stats())
