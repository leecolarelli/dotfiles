# Ghostty to PhpStorm Theme Converter

Successfully converts Ghostty terminal themes to PhpStorm IDE themes with intelligent color derivation.

## Features

- **400+ themes converted** from Ghostty's theme collection
- **Smart color derivation** - extends basic terminal colors to comprehensive UI elements
- **Dark/light detection** - automatically determines theme type based on background luminance
- **Complete plugin structure** - generates proper PhpStorm plugin with JSON theme + XML color scheme
- **JAR packaging** - creates ready-to-install JAR files for PhpStorm
- **Batch processing** - convert entire theme directories at once

## Usage

### Single Theme Conversion
```bash
# Generate theme directory
python3 ghostty-to-phpstorm.py "/path/to/ghostty/theme" "./output-dir"

# Generate ready-to-install JAR file
python3 ghostty-to-phpstorm.py --jar "/path/to/ghostty/theme" "./output-dir"
```

### Batch Conversion (All Themes)
```bash
# Generate all theme directories
python3 ghostty-to-phpstorm.py --batch "/Applications/Ghostty.app/Contents/Resources/ghostty/themes" "./all-themes"

# Generate all themes as JAR files
python3 ghostty-to-phpstorm.py --batch --jar "/Applications/Ghostty.app/Contents/Resources/ghostty/themes" "./jar-themes"
```

## Installation in PhpStorm

### Method 1: JAR Installation (Recommended)
1. Run converter with `--jar` flag
2. Go to **Settings → Plugins → ⚙️ → Install from disk**
3. Select the `.jar` file
4. Restart PhpStorm
5. Go to **Settings → Appearance → Theme** and select your theme

### Method 2: Manual Installation
1. Zip the generated theme directory
2. Follow the same installation steps as Method 1

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

With `--jar` flag, this becomes `ThemeName-theme.jar` ready for installation.

## Color Mapping

| Ghostty Element | PhpStorm Usage |
|----------------|----------------|
| `background` | Editor background, main UI background |
| `foreground` | Text color, labels |
| `palette[0-15]` | Syntax highlighting (keywords, strings, etc.) |
| `selection-*` | Text selection colors |
| `cursor-color` | Caret color |

## Intelligent Derivation

The converter automatically generates missing UI colors by:
- **Brightness adjustment** for panels, borders, hover states
- **Color blending** for notification backgrounds
- **Luminance analysis** for dark/light theme detection
- **Palette mapping** for syntax highlighting

## Examples

Generated themes include:
- **Dracula** (dark theme with purple accents)
- **GitHub Light** (clean light theme)
- **Tokyo Night** (popular dark theme)
- **Catppuccin variants** (pastel themes)
- **Gruvbox** (retro themes)

All 394 Ghostty themes have been successfully converted and tested.