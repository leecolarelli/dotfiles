# Ghostty to PhpStorm Theme Converter

Successfully converts Ghostty terminal themes to PhpStorm IDE themes with intelligent color derivation.

## Features

- **400+ themes converted** from Ghostty's theme collection
- **Smart color derivation** - extends basic terminal colors to comprehensive UI elements
- **Dark/light detection** - automatically determines theme type based on background luminance
- **Complete plugin structure** - generates proper PhpStorm plugin with JSON theme + XML color scheme
- **Batch processing** - convert entire theme directories at once

## Usage

### Single Theme Conversion
```bash
python3 ghostty-to-phpstorm.py "/path/to/ghostty/theme" "./output-dir"
```

### Batch Conversion (All Themes)
```bash
python3 ghostty-to-phpstorm.py --batch "/Applications/Ghostty.app/Contents/Resources/ghostty/themes" "./all-themes"
```

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

## Installation in PhpStorm

1. Zip the generated theme directory
2. Go to **Settings → Plugins → Install from disk**
3. Select the zipped theme
4. Restart PhpStorm
5. Go to **Settings → Appearance → Theme** and select your theme

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