#!/usr/bin/env python3
"""
Ghostty to PhpStorm Theme Converter

Converts Ghostty terminal themes to PhpStorm IDE themes.
Ghostty themes provide basic terminal colors, which are extended
to create comprehensive IDE themes with intelligent color derivation.

Usage:
    python ghostty-to-phpstorm.py [ghostty_theme_path] [output_dir]
    python ghostty-to-phpstorm.py --batch [ghostty_themes_dir] [output_dir]
"""

import os
import sys
import json
import uuid
import argparse
import colorsys
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


class GhosttyTheme:
    """Represents a parsed Ghostty theme"""
    
    def __init__(self, name: str):
        self.name = name
        self.palette: Dict[int, str] = {}
        self.background = "#000000"
        self.foreground = "#ffffff"
        self.cursor_color = "#ffffff"
        self.cursor_text = "#000000"
        self.selection_background = "#ffffff"
        self.selection_foreground = "#000000"
    
    @property
    def is_dark(self) -> bool:
        """Determine if theme is dark based on background luminance"""
        return self._get_luminance(self.background) < 0.5
    
    def _get_luminance(self, hex_color: str) -> float:
        """Calculate relative luminance of a hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        
        # Convert to linear RGB
        def to_linear(c):
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r_lin, g_lin, b_lin = map(to_linear, [r, g, b])
        return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


class ColorDerivator:
    """Derives additional colors from base theme colors"""
    
    @staticmethod
    def adjust_brightness(hex_color: str, factor: float) -> str:
        """Adjust color brightness by factor (-1.0 to 1.0)"""
        hex_color = hex_color.lstrip('#')
        r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        v = max(0, min(1, v + factor))
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    @staticmethod
    def adjust_saturation(hex_color: str, factor: float) -> str:
        """Adjust color saturation by factor (-1.0 to 1.0)"""
        hex_color = hex_color.lstrip('#')
        r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        s = max(0, min(1, s + factor))
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    @staticmethod
    def blend_colors(color1: str, color2: str, ratio: float = 0.5) -> str:
        """Blend two hex colors with given ratio (0.0 = color1, 1.0 = color2)"""
        c1 = color1.lstrip('#')
        c2 = color2.lstrip('#')
        
        r1, g1, b1 = [int(c1[i:i+2], 16) for i in (0, 2, 4)]
        r2, g2, b2 = [int(c2[i:i+2], 16) for i in (0, 2, 4)]
        
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        
        return f"#{r:02x}{g:02x}{b:02x}"


class GhosttyParser:
    """Parses Ghostty theme files"""
    
    @staticmethod
    def parse_theme_file(file_path: Path) -> GhosttyTheme:
        """Parse a Ghostty theme file"""
        theme = GhosttyTheme(file_path.name)
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == 'palette':
                        # Extract palette number and color
                        parts = value.split('=', 1)
                        if len(parts) == 2:
                            try:
                                palette_num = int(parts[0])
                                color = parts[1].strip()
                                theme.palette[palette_num] = color
                            except ValueError:
                                continue
                    elif key == 'background':
                        theme.background = value
                    elif key == 'foreground':
                        theme.foreground = value
                    elif key == 'cursor-color':
                        theme.cursor_color = value
                    elif key == 'cursor-text':
                        theme.cursor_text = value
                    elif key == 'selection-background':
                        theme.selection_background = value
                    elif key == 'selection-foreground':
                        theme.selection_foreground = value
        
        return theme


class PhpStormThemeGenerator:
    """Generates PhpStorm theme files from Ghostty themes"""
    
    def __init__(self, ghostty_theme: GhosttyTheme):
        self.ghostty = ghostty_theme
        self.derivator = ColorDerivator()
        self.theme_id = str(uuid.uuid4())
    
    def generate_theme_json(self) -> Dict:
        """Generate the main theme JSON structure"""
        theme_name = self.ghostty.name.replace('_', ' ').title()
        
        # Derive UI colors from base theme
        ui_colors = self._derive_ui_colors()
        
        theme_json = {
            "name": theme_name,
            "dark": self.ghostty.is_dark,
            "author": "Ghostty Converter",
            "editorScheme": f"/{self.ghostty.name}.xml",
            "colors": {
                "primaryBackground": self.ghostty.background,
                "primaryForeground": self.ghostty.foreground,
                "selectionBackground": self.ghostty.selection_background,
                "selectionForeground": self.ghostty.selection_foreground
            },
            "ui": ui_colors
        }
        
        return theme_json
    
    def _derive_ui_colors(self) -> Dict:
        """Derive comprehensive UI colors from base theme"""
        bg = self.ghostty.background
        fg = self.ghostty.foreground
        
        if self.ghostty.is_dark:
            # Dark theme derivations
            panel_bg = self.derivator.adjust_brightness(bg, 0.1)
            border_color = self.derivator.adjust_brightness(bg, 0.2)
            hover_bg = self.derivator.adjust_brightness(bg, 0.15)
            pressed_bg = self.derivator.adjust_brightness(bg, -0.1)
            disabled_fg = self.derivator.adjust_brightness(fg, -0.4)
        else:
            # Light theme derivations
            panel_bg = self.derivator.adjust_brightness(bg, -0.05)
            border_color = self.derivator.adjust_brightness(bg, -0.15)
            hover_bg = self.derivator.adjust_brightness(bg, -0.1)
            pressed_bg = self.derivator.adjust_brightness(bg, -0.2)
            disabled_fg = self.derivator.adjust_brightness(fg, 0.4)
        
        # Get accent colors from palette
        accent_color = self.ghostty.palette.get(4, "#0078d4")  # Blue
        error_color = self.ghostty.palette.get(1, "#ff0000")   # Red
        warning_color = self.ghostty.palette.get(3, "#ffaa00") # Yellow
        success_color = self.ghostty.palette.get(2, "#00aa00") # Green
        
        return {
            "*": {
                "background": bg,
                "foreground": fg
            },
            "Panel.background": panel_bg,
            "Menu.background": panel_bg,
            "MenuBar.background": bg,
            "ToolWindow.background": panel_bg,
            "Editor.background": bg,
            "EditorTabs.background": panel_bg,
            "Tree.background": bg,
            "List.background": bg,
            "Table.background": bg,
            "TextField.background": bg,
            "Button.background": panel_bg,
            "Button.foreground": fg,
            "Button.hoverBackground": hover_bg,
            "Button.pressedBackground": pressed_bg,
            "Component.borderColor": border_color,
            "Component.focusedBorderColor": accent_color,
            "Component.disabledForeground": disabled_fg,
            "Link.activeForeground": accent_color,
            "Link.hoverForeground": accent_color,
            "Link.pressedForeground": accent_color,
            "Label.disabledForeground": disabled_fg,
            "Separator.foreground": border_color,
            "TabbedPane.tabSelectionHeight": 2,
            "StatusBar.background": panel_bg,
            "ProgressBar.progressColor": accent_color,
            "ScrollBar.thumbColor": self.derivator.adjust_brightness(bg, 0.3 if self.ghostty.is_dark else -0.3),
            "SearchEverywhere.background": panel_bg,
            "Notification.background": panel_bg,
            "Notification.errorBackground": self.derivator.blend_colors(bg, error_color, 0.1),
            "Notification.warningBackground": self.derivator.blend_colors(bg, warning_color, 0.1),
            "ValidationTooltip.errorBackground": error_color,
            "ValidationTooltip.warningBackground": warning_color
        }
    
    def generate_editor_scheme_xml(self) -> str:
        """Generate editor color scheme XML"""
        scheme = Element('scheme')
        scheme.set('name', self.ghostty.name)
        scheme.set('version', '142')
        scheme.set('parent_scheme', 'Darcula' if self.ghostty.is_dark else 'Default')
        
        # Add colors section
        colors = SubElement(scheme, 'colors')
        self._add_color_option(colors, 'BACKGROUND', self.ghostty.background)
        self._add_color_option(colors, 'FOREGROUND', self.ghostty.foreground)
        self._add_color_option(colors, 'CARET_COLOR', self.ghostty.cursor_color)
        self._add_color_option(colors, 'SELECTION_BACKGROUND', self.ghostty.selection_background)
        self._add_color_option(colors, 'SELECTION_FOREGROUND', self.ghostty.selection_foreground)
        
        # Add derived colors
        line_number_color = self.derivator.adjust_brightness(self.ghostty.foreground, -0.3)
        self._add_color_option(colors, 'LINE_NUMBERS_COLOR', line_number_color)
        self._add_color_option(colors, 'GUTTER_BACKGROUND', self.ghostty.background)
        
        # Add attributes for syntax highlighting
        attributes = SubElement(scheme, 'attributes')
        self._add_syntax_colors(attributes)
        
        # Pretty print XML
        rough_string = tostring(scheme, 'unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def _add_color_option(self, parent: Element, name: str, value: str):
        """Add a color option to XML"""
        option = SubElement(parent, 'option')
        option.set('name', name)
        option.set('value', value.upper())
    
    def _add_syntax_colors(self, attributes: Element):
        """Add syntax highlighting colors based on terminal palette"""
        # Map syntax elements to terminal colors
        syntax_mappings = [
            ('DEFAULT_KEYWORD', self.ghostty.palette.get(5, '#ff00ff')),      # Magenta
            ('DEFAULT_STRING', self.ghostty.palette.get(2, '#00ff00')),       # Green
            ('DEFAULT_NUMBER', self.ghostty.palette.get(1, '#ff0000')),       # Red
            ('DEFAULT_COMMENT', self.ghostty.palette.get(8, '#555555')),      # Bright Black
            ('DEFAULT_IDENTIFIER', self.ghostty.foreground),
            ('DEFAULT_FUNCTION_DECLARATION', self.ghostty.palette.get(4, '#0000ff')), # Blue
            ('DEFAULT_CLASS_NAME', self.ghostty.palette.get(3, '#ffff00')),   # Yellow
            ('DEFAULT_CONSTANT', self.ghostty.palette.get(6, '#00ffff')),     # Cyan
        ]
        
        for syntax_type, color in syntax_mappings:
            option = SubElement(attributes, 'option')
            option.set('name', syntax_type)
            value = SubElement(option, 'value')
            foreground = SubElement(value, 'option')
            foreground.set('name', 'FOREGROUND')
            foreground.set('value', color.upper().lstrip('#'))
    
    def generate_plugin_xml(self) -> str:
        """Generate plugin.xml configuration"""
        theme_name = self.ghostty.name.replace('_', ' ').title()
        plugin_id = f"com.ghostty.theme.{self.ghostty.name.lower().replace(' ', '_').replace('-', '_')}"
        
        return f'''<idea-plugin>
  <id>{plugin_id}</id>
  <name>{theme_name} Theme</name>
  <version>1.0.0</version>
  <vendor email="noreply@anthropic.com" url="https://github.com/anthropics/claude-code">Ghostty Converter</vendor>
  
  <description><![CDATA[
    <h2>{theme_name} Theme</h2>
    <p>A beautiful theme converted from the Ghostty terminal theme collection.</p>
    
    <p><strong>Features:</strong></p>
    <ul>
      <li>Complete UI theme with intelligent color derivation</li>
      <li>Editor color scheme optimized for code readability</li>
      <li>{"Dark" if self.ghostty.is_dark else "Light"} theme with harmonious color palette</li>
      <li>Syntax highlighting based on terminal ANSI colors</li>
    </ul>
    
    <p>Original Ghostty theme: <code>{self.ghostty.name}</code></p>
    
    <p><em>Generated with Claude Code's Ghostty to PhpStorm theme converter.</em></p>
  ]]></description>
  
  <change-notes><![CDATA[
    <h3>Version 1.0.0</h3>
    <ul>
      <li>Initial release</li>
      <li>Complete UI theme implementation</li>
      <li>Editor color scheme with syntax highlighting</li>
      <li>Intelligent color derivation from terminal palette</li>
    </ul>
  ]]></change-notes>
  
  <idea-version since-build="193" until-build="999.*"/>
  
  <depends>com.intellij.modules.platform</depends>
  
  <extensions defaultExtensionNs="com.intellij">
    <themeProvider id="{self.theme_id}" path="/{self.ghostty.name}.theme.json"/>
  </extensions>
  
  <applicationListeners>
  </applicationListeners>
</idea-plugin>'''


def create_jar_file(theme_dir: Path, output_dir: Path) -> Path:
    """Package theme directory into a JAR file"""
    jar_name = f"{theme_dir.name}.jar"
    jar_path = output_dir / jar_name
    
    with zipfile.ZipFile(jar_path, 'w', zipfile.ZIP_DEFLATED) as jar:
        for file_path in theme_dir.rglob('*'):
            if file_path.is_file():
                # Calculate relative path from theme directory
                relative_path = file_path.relative_to(theme_dir)
                jar.write(file_path, relative_path)
    
    return jar_path


def convert_theme(input_file: Path, output_dir: Path, create_jar: bool = False):
    """Convert a single Ghostty theme to PhpStorm format"""
    print(f"Converting {input_file.name}...")
    
    # Parse Ghostty theme
    ghostty_theme = GhosttyParser.parse_theme_file(input_file)
    
    # Generate PhpStorm theme
    generator = PhpStormThemeGenerator(ghostty_theme)
    
    # Create output directory
    theme_dir = output_dir / f"{ghostty_theme.name}-theme"
    theme_dir.mkdir(parents=True, exist_ok=True)
    
    # Create resources directory
    resources_dir = theme_dir / "resources"
    resources_dir.mkdir(exist_ok=True)
    
    # Create META-INF directory
    meta_inf_dir = theme_dir / "META-INF"
    meta_inf_dir.mkdir(exist_ok=True)
    
    # Write theme JSON
    theme_json = generator.generate_theme_json()
    with open(resources_dir / f"{ghostty_theme.name}.theme.json", 'w') as f:
        json.dump(theme_json, f, indent=2)
    
    # Write editor scheme XML
    scheme_xml = generator.generate_editor_scheme_xml()
    with open(resources_dir / f"{ghostty_theme.name}.xml", 'w') as f:
        f.write(scheme_xml)
    
    # Write plugin.xml
    plugin_xml = generator.generate_plugin_xml()
    with open(meta_inf_dir / "plugin.xml", 'w') as f:
        f.write(plugin_xml)
    
    if create_jar:
        jar_path = create_jar_file(theme_dir, output_dir)
        print(f"  ✓ Generated JAR: {jar_path.name}")
        return jar_path
    else:
        print(f"  ✓ Generated theme in {theme_dir}")
        return theme_dir


def create_icls_file(ghostty_theme: GhosttyTheme, output_dir: Path) -> Path:
    """Create .icls color scheme file for direct PhpStorm import"""
    generator = PhpStormThemeGenerator(ghostty_theme)
    icls_content = generator.generate_editor_scheme_xml()
    
    # Remove XML declaration and change root element
    lines = icls_content.split('\n')
    # Skip XML declaration and find scheme element
    scheme_start = -1
    for i, line in enumerate(lines):
        if '<scheme' in line:
            scheme_start = i
            break
    
    if scheme_start >= 0:
        # Remove the <?xml> declaration and get clean scheme content
        clean_content = '\n'.join(lines[scheme_start:])
        icls_path = output_dir / f"{ghostty_theme.name}.icls"
        with open(icls_path, 'w') as f:
            f.write(clean_content)
        return icls_path
    
    return None


def main():
    parser = argparse.ArgumentParser(description='Convert Ghostty themes to PhpStorm themes')
    parser.add_argument('input', help='Input Ghostty theme file or directory')
    parser.add_argument('output', help='Output directory for PhpStorm themes')
    parser.add_argument('--batch', action='store_true', help='Convert all themes in directory')
    parser.add_argument('--jar', action='store_true', help='Package themes as JAR files ready for PhpStorm installation')
    parser.add_argument('--icls', action='store_true', help='Create .icls color scheme files for direct import')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"Error: Input path {input_path} does not exist")
        sys.exit(1)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    if args.batch:
        if not input_path.is_dir():
            print("Error: --batch requires input to be a directory")
            sys.exit(1)
        
        theme_files = list(input_path.iterdir())
        theme_files = [f for f in theme_files if f.is_file()]
        
        print(f"Converting {len(theme_files)} themes...")
        converted = 0
        
        for theme_file in theme_files:
            try:
                if args.icls:
                    ghostty_theme = GhosttyParser.parse_theme_file(theme_file)
                    icls_path = create_icls_file(ghostty_theme, output_path)
                    if icls_path:
                        print(f"  ✓ Generated ICLS: {icls_path.name}")
                    converted += 1
                else:
                    convert_theme(theme_file, output_path, create_jar=args.jar)
                    converted += 1
            except Exception as e:
                print(f"  ✗ Failed to convert {theme_file.name}: {e}")
        
        print(f"\nConversion complete: {converted}/{len(theme_files)} themes converted")
        if args.jar:
            print(f"\nJAR files are ready for PhpStorm installation:")
            print(f"Settings → Plugins → Install from disk → Select JAR file")
        elif args.icls:
            print(f"\nICLS files are ready for PhpStorm import:")
            print(f"Settings → Editor → Color Scheme → ⚙️ → Import Scheme → Select ICLS file")
    else:
        if input_path.is_dir():
            print("Error: Use --batch flag to convert directory of themes")
            sys.exit(1)
        
        if args.icls:
            ghostty_theme = GhosttyParser.parse_theme_file(input_path)
            icls_path = create_icls_file(ghostty_theme, output_path)
            if icls_path:
                print(f"✓ Generated ICLS: {icls_path}")
                print(f"\nInstall in PhpStorm:")
                print(f"Settings → Editor → Color Scheme → ⚙️ → Import Scheme → {icls_path}")
        else:
            result = convert_theme(input_path, output_path, create_jar=args.jar)
            if args.jar:
                print(f"\nInstall in PhpStorm:")
                print(f"Settings → Plugins → Install from disk → {result}")
                print(f"Then: Settings → Appearance → Theme → Select your theme")


if __name__ == '__main__':
    main()