import sqlite3
import json
import os
from datetime import datetime
from config_loader import get_paths

def get_children(parent_entry, conn):
    """Get all entries that have parent_entry in their 'up' column."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT entry FROM responses 
        WHERE up LIKE ? OR up LIKE ? OR up LIKE ? OR up = ?
        ORDER BY entry
    """, (f'%"{parent_entry}"%', f"%['{parent_entry}'%", f"%'{parent_entry}'%", f'["{parent_entry}"]'))
    results = cursor.fetchall()
    return [entry[0] for entry in results]

def generate_nested_list(entry, conn, visited=None, indent_level=0):
    """Recursively generate nested markdown list."""
    if visited is None:
        visited = set()
    
    # Prevent infinite loops
    if entry in visited:
        return ""
    
    visited.add(entry)
    
    # Create the current entry line with proper indentation
    indent = "\t" * indent_level  # 1 tab per level
    result = f"{indent}- [[{entry}]]\n"
    
    # Get all children of this entry
    children = get_children(entry, conn)
    
    # Recursively add children
    for child in children:
        result += generate_nested_list(child, conn, visited.copy(), indent_level + 1)
    
    return result

def generate_callout_section(entry, conn, visited=None):
    """Generate a callout section for a top-level entry."""
    if visited is None:
        visited = set()
    
    # Prevent infinite loops
    if entry in visited:
        return ""
    
    visited.add(entry)
    
    # Start the callout (foldable with linked title)
    result = f"\n>[!note]+ [[{entry}]]\n"
    
    # Get all children of this entry
    children = get_children(entry, conn)
    
    if children:
        # Add children as a nested list inside the callout
        for child in children:
            result += f">- [[{child}]]\n"
            # Get grandchildren and add them with additional indentation (1 tab)
            grandchildren = get_children(child, conn)
            for grandchild in grandchildren:
                if grandchild not in visited:
                    result += f">\t- [[{grandchild}]]\n"
                    # Get great-grandchildren (2 tabs)
                    great_grandchildren = get_children(grandchild, conn)
                    for ggchild in great_grandchildren:
                        if ggchild not in visited:
                            result += f">\t\t- [[{ggchild}]]\n"
                            # Get great-great-grandchildren (3 tabs)
                            ggrandchildren = get_children(ggchild, conn)
                            for gggchild in ggrandchildren:
                                if gggchild not in visited:
                                    result += f">\t\t\t- [[{gggchild}]]\n"
    else:
        result += f">No sub-entries found.\n"
    
    return result

def find_orphaned_entries(conn):
    """Find entries that don't eventually trace back to 'm'."""
    cursor = conn.cursor()
    
    # Get all entries
    cursor.execute("SELECT entry FROM responses ORDER BY entry")
    all_entries = [row[0] for row in cursor.fetchall()]
    
    # Find all entries that are connected to 'm' (directly or indirectly)
    connected_to_m = set()
    
    def trace_to_m(entry, visited=None):
        if visited is None:
            visited = set()
        if entry in visited:
            return False
        visited.add(entry)
        
        if entry == 'm':
            return True
        
        # Check if this entry has 'm' in its up chain
        cursor.execute("SELECT up FROM responses WHERE entry=?", (entry,))
        result = cursor.fetchone()
        if result and result[0]:
            try:
                up_list = json.loads(result[0])
                for up_entry in up_list:
                    if up_entry == 'm' or trace_to_m(up_entry, visited.copy()):
                        return True
            except (json.JSONDecodeError, TypeError):
                pass
        return False
    
    # Check each entry
    for entry in all_entries:
        if trace_to_m(entry):
            connected_to_m.add(entry)
    
    # Return entries not connected to 'm'
    orphaned = [entry for entry in all_entries if entry not in connected_to_m]
    return orphaned

def generate_vault_index():
    """Generate hierarchical index markdown file from database entries."""
    
    # Get configured paths
    paths = get_paths()
    output_path = paths['index_path']
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(paths['database_path'])
    
    print("Generating hierarchical index starting from 'm'...")
    
    # Get direct children of 'm' for callout sections
    m_children = get_children('m', conn)
    
    # Generate callout sections for each child of 'm'
    callout_content = ""
    for child in m_children:
        callout_content += generate_callout_section(child, conn)
    
    # Find orphaned entries (not connected to 'm')
    orphaned = find_orphaned_entries(conn)
    
    # Generate orphaned entries list
    orphaned_content = ""
    if orphaned:
        orphaned_content = "\n## Unconnected Entries\n\nThe following entries are not connected to the main knowledge tree:\n\n"
        for entry in orphaned:
            orphaned_content += f"- [[{entry}]]\n"
    
    # Get current date and time for generation timestamp
    generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create markdown content
    markdown_content = f"""---
title: "Community Knowledge Index"
generated: "{generation_time}"
---

# Community Knowledge Index

This is a hierarchical index of all community knowledge entries, organized by their relationships in the database.

## Knowledge Categories

{callout_content}

{orphaned_content}

---

*Generated on {generation_time} from responses.db*
"""
    
    # Write markdown file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Index generated successfully: {output_path}")
    except Exception as e:
        print(f"Error creating index file: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    generate_vault_index()
