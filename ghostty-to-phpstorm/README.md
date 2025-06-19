# Ghostty to PhpStorm Theme Converter

Successfully converts Ghostty terminal themes to PhpStorm IDE themes with intelligent color derivation, creating full UI themes that appear in the "Preferred Theme" menu.

## Features

- **400+ themes converted** from Ghostty's theme collection
- **Smart color derivation** - extends basic terminal colors to comprehensive UI elements
- **Dark/light detection** - automatically determines theme type based on background luminance
- **Complete plugin structure** - generates proper PhpStorm plugin with JSON theme + XML color scheme
- **JAR packaging** - creates ready-to-install JAR files for PhpStorm
- **Batch processing** - convert entire theme directories at once
- **Full UI theming** - styles all UI elements including tool windows, borders, and panels
- **Appears in Preferred Theme menu** - themes are properly registered as UI themes

## Usage

### Single Theme Conversion
```bash
# Generate ready-to-install JAR file (default)
python3 ghostty-to-phpstorm.py "/path/to/ghostty/theme" "./output-dir"

# Generate theme directory instead of JAR
python3 ghostty-to-phpstorm.py --dir "/path/to/ghostty/theme" "./output-dir"
```

### Batch Conversion (All Themes)
```bash
# Generate all themes as JAR files (default)
python3 ghostty-to-phpstorm.py --batch "/Applications/Ghostty.app/Contents/Resources/ghostty/themes" "./jar-themes"

# Generate all theme directories instead of JARs
python3 ghostty-to-phpstorm.py --batch --dir "/Applications/Ghostty.app/Contents/Resources/ghostty/themes" "./all-themes"
```

## Installation in PhpStorm

### Method 1: JAR Installation (Default)
1. Run the converter (JAR files are created by default)
2. Go to **Settings → Plugins → ⚙️ → Install from disk**
3. Select the `.jar` file
4. Restart PhpStorm
5. Go to **Settings → Appearance → Theme** and select your theme

### Method 2: Manual Installation
1. Run the converter with `--dir` flag to generate theme directories
2. Zip the generated theme directory
3. Follow the same installation steps as Method 1

## Generated Structure

Each converted theme creates a complete PhpStorm plugin:

```
ThemeName-theme/
├── META-INF/
│   └── plugin.xml          # Plugin configuration
└── resources/
    ├── ThemeName.theme.json # Main theme definition
    └── ThemeName.xml        # Editor color scheme
```

By default, the script creates `ThemeName-theme.jar` files ready for installation. Use the `--dir` flag to only generate the directory structure.

## Color Mapping

| Ghostty Element | PhpStorm Usage |
|----------------|----------------|
| `background` | Editor background, main UI background, window background |
| `foreground` | Text color, labels, default foreground |
| `palette[0-15]` | Syntax highlighting, accent colors, notification colors |
| `selection-*` | Text selection colors, list/tree selections |
| `cursor-color` | Caret color |

## Intelligent Derivation

The converter automatically generates missing UI colors by:
- **Brightness adjustment** for panels, borders, hover states
- **Color blending** for notification backgrounds
- **Luminance analysis** for dark/light theme detection
- **Palette mapping** for syntax highlighting and UI accents
- **Border derivation** using lighter shades of background color
- **Icon coloring** based on terminal palette colors

## UI Elements Styled

The themes now style all UI elements including:

| UI Element | Styling |
|------------|---------|
| Tool Windows | Headers, tabs, buttons, backgrounds |
| Borders | Window borders, component borders, separators |
| Panels | Backgrounds, borders, hover states |
| Buttons | Normal, default, hover, pressed states |
| Menus | Backgrounds, selections, accelerators |
| Editor Tabs | Active, inactive, hover states |
| Lists & Trees | Backgrounds, selections, row styling |
| Notifications | Info, warning, error variants |
| Scroll Bars | Track, thumb, hover states |
| Status Bar | Background, borders |
| Icons | Action and object colors |

## Examples

Generated themes include:
- **Dracula** (dark theme with purple accents)
- **GitHub Light** (clean light theme)
- **Tokyo Night** (popular dark theme)
- **Catppuccin variants** (pastel themes)
- **Gruvbox** (retro themes)

All 394 Ghostty themes have been successfully converted and tested.
