#!/usr/bin/env python3
"""
Consolidate Memory Script - Merges request findings into global memory.
Run after request completes to persist important discoveries.
"""

import os
from pathlib import Path
from typing import Optional
from datetime import datetime

class MemoryConsolidator:
    """Merges request-scoped memory into global memory."""
    
    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path)
    
    def consolidate_request(self, request_id: str):
        """Consolidate findings from a completed request."""
        request_memory_path = self.memory_path.parent / "tasks" / f"request_{request_id}" / "memory"
        
        if not request_memory_path.exists():
            print(f"❌ Request memory not found: {request_memory_path}")
            return
        
        print(f"🔄 Consolidating findings from request {request_id}\n")
        
        consolidated_count = 0
        consolidated_count += self._merge_file(request_memory_path, "decisions.md", "Decisions")
        consolidated_count += self._merge_file(request_memory_path, "debug_log.md", "Bug fixes")
        consolidated_count += self._merge_file(request_memory_path, "review_log.md", "Code reviews")
        
        if consolidated_count > 0:
            print(f"\n✅ Consolidated {consolidated_count} entries")
            print(f"📝 Request-scoped memory archived for historical reference")
        else:
            print("✅ No new findings to consolidate")
    
    def _merge_file(self, request_path: Path, filename: str, label: str) -> int:
        """Merge entries from request memory into global memory."""
        request_file = request_path / filename
        global_file = self.memory_path / filename
        
        if not request_file.exists():
            return 0
        
        with open(request_file, 'r') as f:
            request_content = f.read().strip()
        
        if not request_content:
            print(f"  {label}: No entries (skipped)")
            return 0
        
        # Check if already in global memory (avoid duplicates)
        if global_file.exists():
            with open(global_file, 'r') as f:
                global_content = f.read()
            
            # Simple dedup: if content appears in global, skip
            if request_content in global_content:
                print(f"  {label}: Already exists in global memory (skipped)")
                return 0
        
        # Append request findings to global memory
        with open(global_file, 'a') as f:
            f.write("\n\n")
            f.write(f"# Consolidated from request_{request_id}\n")
            f.write(f"# Date: {datetime.now().isoformat()}\n")
            f.write(request_content)
        
        line_count = request_content.count("\n")
        print(f"  {label}: Merged from request → {filename} (+{line_count} lines)")
        
        return line_count
    
    def interactive_consolidate(self, request_id: str):
        """Interactively choose what to consolidate."""
        request_memory_path = self.memory_path.parent / "tasks" / f"request_{request_id}" / "memory"
        
        if not request_memory_path.exists():
            print(f"❌ Request memory not found: {request_memory_path}")
            return
        
        print(f"📋 Review findings from request {request_id}\n")
        
        # Show decisions
        decisions_file = request_memory_path / "decisions.md"
        if decisions_file.exists():
            print("=" * 60)
            print("DECISIONS MADE DURING REQUEST:")
            print("=" * 60)
            with open(decisions_file, 'r') as f:
                print(f.read())
            
            if input("\n✓ Consolidate these decisions? (y/n): ").lower() == 'y':
                self._merge_file(request_memory_path, "decisions.md", "Decisions")
        
        # Show bugs
        debug_file = request_memory_path / "debug_log.md"
        if debug_file.exists():
            print("\n" + "=" * 60)
            print("ISSUES FIXED DURING REQUEST:")
            print("=" * 60)
            with open(debug_file, 'r') as f:
                print(f.read())
            
            if input("\n✓ Consolidate these bug fixes? (y/n): ").lower() == 'y':
                self._merge_file(request_memory_path, "debug_log.md", "Bug fixes")
        
        # Show reviews
        review_file = request_memory_path / "review_log.md"
        if review_file.exists():
            print("\n" + "=" * 60)
            print("CODE QUALITY FINDINGS:")
            print("=" * 60)
            with open(review_file, 'r') as f:
                print(f.read())
            
            if input("\n✓ Consolidate these reviews? (y/n): ").lower() == 'y':
                self._merge_file(request_memory_path, "review_log.md", "Code reviews")
        
        print("\n✅ Consolidation complete")
    
    def archive_request_memory(self, request_id: str):
        """Archive request memory to historical records."""
        request_path = self.memory_path.parent / "tasks" / f"request_{request_id}"
        archive_path = self.memory_path.parent / "archived_requests" / f"request_{request_id}_memory"
        
        if not request_path.exists():
            return
        
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy request memory to archive
        import shutil
        if (request_path / "memory").exists():
            shutil.copytree(request_path / "memory", archive_path, dirs_exist_ok=True)
            print(f"📦 Archived request memory → {archive_path}")


if __name__ == "__main__":
    import sys
    
    memory_path = Path("memory")
    consolidator = MemoryConsolidator(memory_path)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python consolidate_memory.py REQUEST_ID           # Auto-merge all findings")
        print("  python consolidate_memory.py REQUEST_ID --review  # Interactive review first")
        print("  python consolidate_memory.py REQUEST_ID --archive # Archive for historical reference")
    else:
        request_id = sys.argv[1]
        
        if len(sys.argv) > 2 and sys.argv[2] == "--review":
            consolidator.interactive_consolidate(request_id)
        elif len(sys.argv) > 2 and sys.argv[2] == "--archive":
            consolidator.archive_request_memory(request_id)
        else:
            consolidator.consolidate_request(request_id)
            consolidator.archive_request_memory(request_id)
