#!/usr/bin/env python3
"""
Site Files Publisher

This script copies publish.css and publish.js to the vault's site files directory.
This is useful for publishing the vault with proper styling and functionality.
"""

import os
import shutil
from config_loader import get_paths

def copy_site_files():
    """Copy publish.css and publish.js to the vault's site files directory."""
    
    # Get configured paths
    paths = get_paths()
    
    # Define source files (in the current directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_css = os.path.join(script_dir, 'publish.css')
    source_js = os.path.join(script_dir, 'publish.js')
    
    # Define destination directory (site files in vault)
    site_files_dir = os.path.join(paths['output_base_dir'], 'site files')
    
    print("=" * 60)
    print("COPYING SITE FILES TO VAULT")
    print("=" * 60)
    
    # Create site files directory if it doesn't exist
    try:
        os.makedirs(site_files_dir, exist_ok=True)
        print(f"Created/verified site files directory: {site_files_dir}")
    except Exception as e:
        print(f"Error creating site files directory: {e}")
        return False
    
    # Copy CSS file
    try:
        if os.path.exists(source_css):
            dest_css = os.path.join(site_files_dir, 'publish.css')
            shutil.copy2(source_css, dest_css)
            print(f"✅ Copied: publish.css")
            print(f"   From: {source_css}")
            print(f"   To:   {dest_css}")
        else:
            print(f"❌ Source file not found: {source_css}")
            return False
    except Exception as e:
        print(f"❌ Error copying publish.css: {e}")
        return False
    
    # Copy JS file
    try:
        if os.path.exists(source_js):
            dest_js = os.path.join(site_files_dir, 'publish.js')
            shutil.copy2(source_js, dest_js)
            print(f"✅ Copied: publish.js")
            print(f"   From: {source_js}")
            print(f"   To:   {dest_js}")
        else:
            print(f"❌ Source file not found: {source_js}")
            return False
    except Exception as e:
        print(f"❌ Error copying publish.js: {e}")
        return False
    
    print("=" * 60)
    print("SITE FILES COPY COMPLETE")
    print("=" * 60)
    print("Site files are now ready for publishing!")
    print(f"Location: {site_files_dir}")
    
    return True

def main():
    """Main function."""
    import sys
    
    try:
        success = copy_site_files()
        if success:
            print("🎉 Site files copied successfully!")
            sys.exit(0)
        else:
            print("💥 Some operations failed. Check the output above.")
            sys.exit(1)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
