"""
Generate project structure tree for progress assessment
Run: python show_project_structure.py
"""

import os
from pathlib import Path

# Directories/files to exclude
EXCLUDE = {
    '__pycache__', '.git', 'venv', 'env', '.venv',
    'chroma_db', 'test_chroma_db', '.pytest_cache',
    '.ipynb_checkpoints', 'node_modules', '.env'
}

EXCLUDE_EXTENSIONS = {'.pyc', '.pyo', '.pyd', '.so', '.dll'}

def should_exclude(path):
    """Check if path should be excluded"""
    if path.name in EXCLUDE:
        return True
    if path.suffix in EXCLUDE_EXTENSIONS:
        return True
    if path.name.startswith('.') and path.name not in {'.env.example', '.gitignore'}:
        return True
    return False

def print_tree(directory, prefix="", is_last=True, files_only=False):
    """Print directory tree structure"""
    try:
        path = Path(directory)
        
        # Get all items, excluding specified directories
        items = sorted([p for p in path.iterdir() if not should_exclude(p)],
                      key=lambda x: (not x.is_dir(), x.name.lower()))
        
        for i, item in enumerate(items):
            is_last_item = i == len(items) - 1
            current_prefix = "└── " if is_last_item else "├── "
            
            # Add file size for files
            if item.is_file():
                size = item.stat().st_size
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024*1024:
                    size_str = f"{size/1024:.1f}KB"
                else:
                    size_str = f"{size/(1024*1024):.1f}MB"
                print(f"{prefix}{current_prefix}{item.name} ({size_str})")
            else:
                print(f"{prefix}{current_prefix}{item.name}/")
            
            # Recurse into directories
            if item.is_dir():
                extension_prefix = "    " if is_last_item else "│   "
                print_tree(item, prefix + extension_prefix, is_last_item)
    
    except PermissionError:
        pass

def count_files_by_type(directory):
    """Count files by extension"""
    counts = {}
    total_size = 0
    
    for path in Path(directory).rglob('*'):
        if path.is_file() and not should_exclude(path):
            ext = path.suffix or 'no_extension'
            counts[ext] = counts.get(ext, 0) + 1
            total_size += path.stat().st_size
    
    return counts, total_size

def main():
    """Main function"""
    print("=" * 70)
    print("📁 RAG POLICY ASSISTANT - PROJECT STRUCTURE")
    print("=" * 70)
    print()
    
    project_root = Path.cwd()
    print(f"📂 {project_root.name}/")
    print_tree(project_root, "")
    
    print()
    print("=" * 70)
    print("📊 FILE STATISTICS")
    print("=" * 70)
    
    counts, total_size = count_files_by_type(project_root)
    
    # Sort by count
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nTotal Size: {total_size/(1024*1024):.2f} MB")
    print(f"\nFiles by type:")
    for ext, count in sorted_counts:
        print(f"  {ext:20s}: {count:3d} files")
    
    print()
    print("=" * 70)
    print("✅ REQUIRED FILES CHECKLIST")
    print("=" * 70)
    
    required_files = {
        'README.md': 'Project documentation',
        'requirements.txt': 'Dependencies',
        '.env.example': 'API key template',
        'app.py': 'Streamlit application',
        'src/document_processor.py': 'Document processing',
        'src/vector_store.py': 'Vector database',
        'src/rag_pipeline.py': 'RAG implementation',
        'data/policies/*.md': 'Policy documents (8 files)',
        '.github/workflows/*.yml': 'CI/CD pipeline',
        'design-and-evaluation.md': 'Design documentation',
        'ai-tooling.md': 'AI tools usage',
    }
    
    print("\nChecking required files...")
    for file_pattern, description in required_files.items():
        if '*' in file_pattern:
            # Handle wildcard patterns
            base_path = Path(file_pattern.split('*')[0])
            if base_path.exists():
                files = list(base_path.parent.glob(base_path.name + '*'))
                if files:
                    print(f"  ✅ {file_pattern:40s} - {description}")
                else:
                    print(f"  ❌ {file_pattern:40s} - {description}")
            else:
                print(f"  ❌ {file_pattern:40s} - {description}")
        else:
            if Path(file_pattern).exists():
                print(f"  ✅ {file_pattern:40s} - {description}")
            else:
                print(f"  ❌ {file_pattern:40s} - {description}")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()