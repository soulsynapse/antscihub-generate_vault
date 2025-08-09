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

# Copy publish.css and publish.js to vault site files directory
python main.py --site-files

# Show help
python main.py --help
```

### Site Files Management

Use the site files script to copy publishing assets to the vault:

```bash
# Copy publish.css and publish.js to vault/site files/
python copy_site_files.py
```

This creates a "site files" directory in the vault with the CSS and JavaScript files needed for enhanced web publishing.

The tool will automatically:
1. Load configuration from available config files
2. Create output directories if they don't exist
3. Generate markdown files from the database entries

## Publishing Files

The repository includes ready-to-use publishing assets:

### `publish.css`
Empty css currently.

### `publish.js`
Empty JavaScript file as of currently.

## Advanced Customization

### Using CSS Sprite Sheets

For advanced styling and iconography, we can use CSS sprite sheets in the `publish.css` file. Sprite sheets are efficient ways to manage multiple icons or graphics in a single image file.

#### Setting up a CSS Sprite Sheet

1. **Create your sprite sheet image** - Combine all your icons into a single PNG or SVG file
2. **Define the sprite base class** in `publish.css`:

```css
.sprite {
    background-image: url('path/to/your-spritesheet.png');
    background-repeat: no-repeat;
    display: inline-block;
}
```

3. **Define individual sprite positions**:

```css
.sprite.icon-command {
    width: 16px;
    height: 16px;
    background-position: 0 0;
}

.sprite.icon-category {
    width: 16px;
    height: 16px;
    background-position: -16px 0;
}

.sprite.icon-info {
    width: 16px;
    height: 16px;
    background-position: -32px 0;
}
```

#### Using Sprites in Your Vault

Once defined, you can use sprites in your markdown by adding HTML elements:

```html
<span class="sprite icon-command"></span> Command Name
<span class="sprite icon-category"></span> Category
```

Alternatively we can add them the way that old reddit used to, with tags after the link, which may scale better.