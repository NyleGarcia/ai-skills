#!/usr/bin/env python3
import os
import sys

# Define target paths
TARGET_DIRS = [
    "/Users/nylegarcia/git/ai-skills/skills",
    "/Users/nylegarcia/git/ai-skills/plugins"
]

# Prompt injection / prompt poisoning keywords/phrases
KEYWORDS = [
    "ignore previous",
    "system override",
    "you must now",
    "do not perform",
    "override system prompt",
    "ignore all instructions",
    "ignore system rules",
    "ignore user rules",
    "bypass rules"
]

def scan_file(file_path):
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            # Case-insensitive checks
            content_lower = content.lower()
            for keyword in KEYWORDS:
                if keyword in content_lower:
                    # Find exact line numbers and contents
                    f.seek(0)
                    for line_idx, line in enumerate(f, 1):
                        if keyword in line.lower():
                            violations.append({
                                "keyword": keyword,
                                "line": line_idx,
                                "content": line.strip()
                            })
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return violations

def main():
    total_files = 0
    total_violations = 0
    
    print("Starting Skill Security & Prompt Poisoning Scan...")
    print(f"Target directories: {', '.join(TARGET_DIRS)}")
    print(f"Scanning for keywords: {', '.join(f'\"{kw}\"' for kw in KEYWORDS)}")
    print("-" * 60)
    
    for base_dir in TARGET_DIRS:
        if not os.path.exists(base_dir):
            print(f"Warning: Directory {base_dir} does not exist. Skipping.")
            continue
            
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    total_files += 1
                    violations = scan_file(file_path)
                    if violations:
                        total_violations += len(violations)
                        print(f"VIOLATION FOUND: {file_path}")
                        for v in violations:
                            print(f"  Line {v['line']}: Found keyword '{v['keyword']}' -> \"{v['content']}\"")
                        print("-" * 60)
                        
    print("Scan Summary:")
    print(f"  Total markdown files scanned: {total_files}")
    print(f"  Total violations found: {total_violations}")
    
    if total_violations > 0:
        print("FAIL: Prompt poisoning / prompt injection keywords detected in skill markdown files!")
        sys.exit(1)
    else:
        print("SUCCESS: No prompt injection or prompt poisoning keywords detected in skills.")
        sys.exit(0)

if __name__ == "__main__":
    main()
