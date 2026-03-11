#!/usr/bin/env python3
"""
Archive Memory Script - Rotates old memory entries to archives.
Run this monthly to keep working memory lean.
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
import shutil
from typing import Tuple

class MemoryArchiver:
    """Archives old memory entries to prevent unbounded growth."""
    
    def __init__(self, memory_path: Path, archive_threshold_days: int = 90):
        self.memory_path = Path(memory_path)
        self.archive_threshold_days = archive_threshold_days
        self.cutoff_date = datetime.now() - timedelta(days=archive_threshold_days)
    
    def archive_memory(self):
        """Archive old entries from all memory files."""
        print(f"🗂️  Archiving memory entries older than {self.cutoff_date.date()}\n")
        
        archived_count = 0
        archived_count += self._archive_file("decisions.md")
        archived_count += self._archive_file("debug_log.md")
        archived_count += self._archive_file("review_log.md")
        archived_count += self._archive_file("decisions.md")
        
        if archived_count > 0:
            print(f"\n✅ Archived {archived_count} entries")
            self._update_index()
        else:
            print("✅ No entries to archive")
    
    def _archive_file(self, filename: str) -> int:
        """Archive entries from a single file."""
        file_path = self.memory_path / filename
        if not file_path.exists():
            return 0
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Find cutoff line
        cutoff_line = 0
        for i, line in enumerate(lines):
            # Look for date headers like "## 2024-01-15: ..."
            if line.startswith("## ") and "-" in line:
                try:
                    date_str = line.split(":")[0].replace("## ", "").strip()
                    # Parse date
                    entry_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if entry_date < self.cutoff_date:
                        cutoff_line = i
                        break
                except ValueError:
                    continue
        
        if cutoff_line == 0:
            print(f"  {filename}: No old entries (keeping all)")
            return 0
        
        # Separate old and new entries
        new_entries = lines[cutoff_line:]
        old_entries = lines[:cutoff_line]
        
        # Create archive file
        archive_name = self._get_archive_name(filename)
        archive_path = self.memory_path / archive_name
        
        # Append to archive
        if archive_path.exists():
            with open(archive_path, 'a') as f:
                f.writelines(old_entries)
        else:
            with open(archive_path, 'w') as f:
                f.writelines(old_entries)
        
        # Keep only new entries in active file
        with open(file_path, 'w') as f:
            f.writelines(new_entries)
        
        archived_count = len(old_entries)
        print(f"  {filename}: Archived {archived_count} lines → {archive_name}")
        
        return archived_count
    
    def _get_archive_name(self, filename: str) -> str:
        """Get archive filename based on current date."""
        now = datetime.now()
        year = now.year
        quarter = (now.month - 1) // 3 + 1
        
        base_name = filename.replace(".md", "")
        return f"archive_{base_name}_{year}_q{quarter}.md"
    
    def _update_index(self):
        """Update index file with archive information."""
        index_path = self.memory_path / "index.yaml"
        
        # Scan for archives
        archives = sorted([
            f for f in os.listdir(self.memory_path) 
            if f.startswith("archive_") and f.endswith(".md")
        ])
        
        if index_path.exists():
            import yaml
            with open(index_path, 'r') as f:
                index = yaml.safe_load(f) or {}
            
            index["archives"] = {
                "available": [
                    {"name": archive, "entries": self._count_lines(archive)}
                    for archive in archives
                ]
            }
            
            with open(index_path, 'w') as f:
                yaml.dump(index, f)
    
    def _count_lines(self, filename: str) -> int:
        """Count lines in file."""
        file_path = self.memory_path / filename
        try:
            with open(file_path, 'r') as f:
                return len([l for l in f if l.startswith("## ")])
        except:
            return 0
    
    def restore_from_archive(self, archive_name: str, filename: str):
        """Restore entries from archive to active memory."""
        archive_path = self.memory_path / archive_name
        file_path = self.memory_path / filename
        
        if not archive_path.exists():
            print(f"❌ Archive not found: {archive_name}")
            return
        
        # Append archive to active file
        with open(archive_path, 'r') as f:
            archive_content = f.read()
        
        with open(file_path, 'a') as f:
            f.write("\n# Restored from archive\n")
            f.write(archive_content)
        
        print(f"✅ Restored {archive_name} to {filename}")
    
    def show_archive_stats(self):
        """Show archive statistics."""
        print("📊 Archive Statistics\n")
        
        for filename in ["decisions.md", "debug_log.md", "review_log.md"]:
            file_path = self.memory_path / filename
            if file_path.exists():
                active_lines = len([
                    l for l in open(file_path).readlines() 
                    if l.startswith("## ")
                ])
                print(f"Active {filename}: {active_lines} entries")
        
        print("\nArchives:")
        archives = sorted([
            f for f in os.listdir(self.memory_path) 
            if f.startswith("archive_")
        ])
        
        for archive in archives:
            archive_path = self.memory_path / archive
            size_kb = os.path.getsize(archive_path) / 1024
            lines = len([l for l in open(archive_path).readlines() if l.startswith("## ")])
            print(f"  {archive}: {lines} entries ({size_kb:.1f} KB)")


if __name__ == "__main__":
    import sys
    
    memory_path = Path("memory")
    archiver = MemoryArchiver(memory_path, archive_threshold_days=90)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stats":
            archiver.show_archive_stats()
        elif sys.argv[1] == "--restore" and len(sys.argv) > 3:
            archiver.restore_from_archive(sys.argv[2], sys.argv[3])
        else:
            print("Usage:")
            print("  python archive_memory.py                    # Run archival")
            print("  python archive_memory.py --stats            # Show stats")
            print("  python archive_memory.py --restore ARCHIVE FILE  # Restore from archive")
    else:
        archiver.archive_memory()
