#!/usr/bin/env python3
"""
AntSciHub Generate Vault - Main Runner

This script runs both the vault generation scripts:
1. generate_vault_commands.py - Generates individual command markdown files
2. generate_vault_cmd_index.py - Generates the hierarchical index file

Usage:
    python main.py
    python main.py --commands-only
    python main.py --index-only
    python main.py --help
"""

import sys
import argparse
from datetime import datetime

def run_commands():
    """Run the vault commands generation script."""
    print("=" * 60)
    print("GENERATING VAULT COMMANDS")
    print("=" * 60)
    
    try:
        from generate_vault_commands import generate_vault
        generate_vault()
        return True
    except Exception as e:
        print(f"Error running generate_vault_commands: {e}")
        return False

def run_index():
    """Run the vault index generation script."""
    print("=" * 60)
    print("GENERATING VAULT INDEX")
    print("=" * 60)
    
    try:
        from generate_vault_cmd_index import generate_vault_index
        generate_vault_index()
        return True
    except Exception as e:
        print(f"Error running generate_vault_cmd_index: {e}")
        return False

def main():
    """Main function to run the vault generation process."""
    parser = argparse.ArgumentParser(
        description="Generate AntSciHub knowledge vault from database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                 # Run both commands and index generation
  python main.py --commands-only # Run only commands generation
  python main.py --index-only    # Run only index generation
        """
    )
    
    parser.add_argument(
        '--commands-only', 
        action='store_true',
        help='Only generate command files, skip index generation'
    )
    
    parser.add_argument(
        '--index-only', 
        action='store_true',
        help='Only generate index file, skip commands generation'
    )
    
    args = parser.parse_args()
    
    # Check for conflicting arguments
    if args.commands_only and args.index_only:
        print("Error: Cannot use --commands-only and --index-only together")
        sys.exit(1)
    
    start_time = datetime.now()
    print("AntSciHub Vault Generation")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    success = True
    
    # Run commands generation
    if not args.index_only:
        if not run_commands():
            success = False
    
    # Add separator between operations
    if not args.commands_only and not args.index_only:
        print()
    
    # Run index generation
    if not args.commands_only:
        if not run_index():
            success = False
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"Finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time: {duration.total_seconds():.2f} seconds")
    
    if success:
        print("✅ All operations completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some operations failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
