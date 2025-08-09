import sqlite3
import json
import os
import glob
from datetime import datetime
from config_loader import get_paths

def generate_vault():
    """Generate markdown files from database entries for AntSciHub vault."""
    
    # Get configured paths
    paths = get_paths()
    output_dir = paths['commands_dir']
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Delete all existing files in the folder first
    print("Clearing existing files...")
    for file_path in glob.glob(os.path.join(output_dir, "*")):
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    
    # Connect to database
    conn = sqlite3.connect(paths['database_path'])
    cursor = conn.cursor()
    
    # Get all entries from the database
    cursor.execute("""
        SELECT entry, response, userid, helpers, related_cmds, call_count, up, updated_at
        FROM responses
    """)
    
    entries = cursor.fetchall()
    conn.close()
    
    print(f"Processing {len(entries)} entries...")
    
    for entry_data in entries:
        entry, response, userid, helpers_json, related_json, call_count, up_json, updated_at = entry_data
        
        # Parse JSON fields, handle empty/null values
        try:
            helpers = json.loads(helpers_json) if helpers_json else []
        except (json.JSONDecodeError, TypeError):
            helpers = []
        
        try:
            related = json.loads(related_json) if related_json else []
        except (json.JSONDecodeError, TypeError):
            related = []
        
        try:
            up = json.loads(up_json) if up_json else []
        except (json.JSONDecodeError, TypeError):
            up = []
        
        # Format helpers list for markdown (YAML array format)
        helpers_formatted = ""
        if helpers:
            helpers_formatted = "\n" + "\n".join([f'  - "[[{helper}]]"' for helper in helpers])
        
        # Format related list for markdown (YAML array format)
        related_formatted = ""
        if related:
            related_formatted = "\n" + "\n".join([f'  - "[[{rel}]]"' for rel in related])
        
        # Format up list for markdown (YAML array format)
        up_formatted = ""
        if up:
            up_formatted = "\n" + "\n".join([f'  - "[[{u}]]"' for u in up])
        
        # Format lists for the info callout section
        up_display = ', '.join([f'[[{u}]]' for u in up]) if up else 'None'
        related_display = ', '.join([f'[[{rel}]]' for rel in related]) if related else 'None'
        helpers_display = ', '.join([f'[[{helper}]]' for helper in helpers]) if helpers else 'None'
        
        # Use last edited time from database
        last_edited_time = updated_at if updated_at else "Unknown"
        
        # Create markdown content
        markdown_content = f"""---
up:{up_formatted}
author:
  - "[[{userid}]]"
helpers:{helpers_formatted}
calls: {call_count}
related:{related_formatted}
---

{response}

>[!info]
>**Up:** {up_display}
>**Related**: {related_display}
>**Author:** [[{userid}]]
>**Volunteers:** {helpers_display}
>**Last Edited:** {last_edited_time}
"""
        
        # Create filename (sanitize entry name for filesystem)
        filename = f"{entry}.md"
        # Remove or replace invalid filename characters
        filename = filename.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        
        filepath = os.path.join(output_dir, filename)
        
        # Write markdown file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Created: {filename}")
        except Exception as e:
            print(f"Error creating {filename}: {e}")
    
    print(f"Vault generation complete! Files saved to: {output_dir}")

if __name__ == "__main__":
    generate_vault()
