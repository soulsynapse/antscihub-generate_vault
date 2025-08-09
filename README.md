# AntSciHub Generate Vault

This tool generates markdown files from a database of community responses for the AntSciHub knowledge vault.

## Configuration

The tool uses a flexible configuration system with the following priority order:

1. **Default values** - Built-in defaults using "./output" folder (only used if config.json is missing)
2. **config.json** - Main configuration file with project-specific paths
3. **config.local.json** - Local overrides (ignored by git)

### Configuration Options

- `database_path`: Path to the SQLite database file (default: "responses.db")
- `output_base_dir`: Base directory for generated files (default: "./output")
- `commands_subdir`: Subdirectory name for command files (default: "Commands")
- `index_filename`: Name of the index file (default: "Index.md")

### Setup

1. Copy `config.local.json.example` to `config.local.json`
2. Modify `config.local.json` with your local paths
3. The local config file is ignored by git, so you can customize it without affecting the repository

### Example config.local.json

```json
{
    "database_path": "responses.db",
    "output_base_dir": "C:\\Users\\YourUsername\\Documents\\YourVault\\Community Knowledge",
    "commands_subdir": "Commands",
    "index_filename": "Index.md"
}
```

## Usage

### Quick Start

Run both scripts with a single command:

```bash
python main.py
```

### Individual Scripts

Run the scripts directly:

```bash
python generate_vault_commands.py
python generate_vault_cmd_index.py
```

### Advanced Usage

The main script supports several options:

```bash
# Run both commands and index generation (default)
python main.py

# Run only command files generation
python main.py --commands-only

# Run only index generation
python main.py --index-only

# Show help
python main.py --help
```

The tool will automatically:
1. Load configuration from available config files
2. Create output directories if they don't exist
3. Generate markdown files from the database entries
