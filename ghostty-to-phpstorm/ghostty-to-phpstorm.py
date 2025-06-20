#!/usr/bin/env python3
"""
Ghostty to PhpStorm Theme Converter

Converts Ghostty terminal themes to PhpStorm IDE themes.
Ghostty themes provide basic terminal colors, which are extended
to create comprehensive IDE themes with intelligent color derivation.

Usage:
    python ghostty-to-phpstorm.py [ghostty_theme_path] [output_dir]
    python ghostty-to-phpstorm.py --batch [ghostty_themes_dir] [output_dir]
    python ghostty-to-phpstorm.py --dir [ghostty_theme_path] [output_dir]  # Create theme directories instead of JAR files
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

        # Get accent colors from palette for icons
        accent_color = self.ghostty.palette.get(4, "#0078d4")  # Blue

        theme_json = {
            "name": theme_name,
            "dark": self.ghostty.is_dark,
            "author": "Ghostty Converter",
            "editorScheme": f"/{self.ghostty.name}.xml",
            "background": {
                "default": self.ghostty.background
            },
            "colors": {
                "primaryBackground": self.ghostty.background,
                "primaryForeground": self.ghostty.foreground,
                "selectionBackground": self.ghostty.selection_background,
                "selectionForeground": self.ghostty.selection_foreground,
                "accentColor": accent_color,
                "secondaryAccentColor": self.derivator.adjust_brightness(accent_color, -0.1 if self.ghostty.is_dark else 0.1)
            },
            "ui": ui_colors,
            "icons": {
                "ColorPalette": {
                    "Actions.Blue": accent_color,
                    "Actions.Green": self.ghostty.palette.get(2, "#00aa00"),
                    "Actions.Grey": self.derivator.adjust_brightness(self.ghostty.foreground, -0.3 if self.ghostty.is_dark else 0.3),
                    "Actions.Red": self.ghostty.palette.get(1, "#ff0000"),
                    "Actions.Yellow": self.ghostty.palette.get(3, "#ffaa00"),
                    "Objects.Blue": accent_color,
                    "Objects.Green": self.ghostty.palette.get(2, "#00aa00"),
                    "Objects.Grey": self.derivator.adjust_brightness(self.ghostty.foreground, -0.3 if self.ghostty.is_dark else 0.3),
                    "Objects.Pink": self.ghostty.palette.get(5, "#ff00ff"),
                    "Objects.Purple": self.ghostty.palette.get(5, "#ff00ff"),
                    "Objects.Red": self.ghostty.palette.get(1, "#ff0000"),
                    "Objects.Yellow": self.ghostty.palette.get(3, "#ffaa00"),
                    "Objects.BlackText": "#000000",
                    "Objects.WhiteText": "#ffffff"
                }
            }
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
            inactive_bg = self.derivator.adjust_brightness(bg, 0.05)
            highlight_bg = self.derivator.adjust_brightness(bg, 0.3)
            selection_inactive_bg = self.derivator.adjust_brightness(self.ghostty.selection_background, -0.2)
        else:
            # Light theme derivations
            panel_bg = self.derivator.adjust_brightness(bg, -0.05)
            border_color = self.derivator.adjust_brightness(bg, -0.15)
            hover_bg = self.derivator.adjust_brightness(bg, -0.1)
            pressed_bg = self.derivator.adjust_brightness(bg, -0.2)
            disabled_fg = self.derivator.adjust_brightness(fg, 0.4)
            inactive_bg = self.derivator.adjust_brightness(bg, -0.03)
            highlight_bg = self.derivator.adjust_brightness(bg, -0.1)
            selection_inactive_bg = self.derivator.adjust_brightness(self.ghostty.selection_background, 0.2)

        # Get accent colors from palette
        accent_color = self.ghostty.palette.get(4, "#0078d4")  # Blue
        error_color = self.ghostty.palette.get(1, "#ff0000")   # Red
        warning_color = self.ghostty.palette.get(3, "#ffaa00") # Yellow
        success_color = self.ghostty.palette.get(2, "#00aa00") # Green

        # Derive additional accent colors
        accent_secondary = self.derivator.adjust_brightness(accent_color, -0.1 if self.ghostty.is_dark else 0.1)
        accent_tertiary = self.derivator.adjust_brightness(accent_color, -0.2 if self.ghostty.is_dark else 0.2)

        # Create a few shades lighter than the background for borders
        lighter_bg = self.derivator.adjust_brightness(bg, 0.2 if self.ghostty.is_dark else -0.1)

        return {
            # Global defaults
            "*": {
                "background": bg,
                "foreground": fg,
                "infoForeground": self.derivator.adjust_brightness(fg, -0.3 if self.ghostty.is_dark else 0.3),
                "selectionBackground": self.ghostty.selection_background,
                "selectionForeground": self.ghostty.selection_foreground,
                "selectionInactiveBackground": selection_inactive_bg,
                "selectionBackgroundInactive": selection_inactive_bg,
                "disabledForeground": disabled_fg,
                "disabledBackground": self.derivator.adjust_brightness(bg, -0.05 if self.ghostty.is_dark else 0.05),
                "acceleratorForeground": accent_color,
                "acceleratorSelectionForeground": accent_color,
                "errorForeground": error_color,
                "borderColor": border_color,
                "disabledBorderColor": self.derivator.adjust_brightness(border_color, -0.3 if self.ghostty.is_dark else 0.3),
                "focusColor": accent_color,
                "focusedBorderColor": accent_color,
                "separatorColor": border_color
            },

            # Main window and panels
            "Window.background": bg,
            "Panel.background": panel_bg,
            "Window.border": lighter_bg,
            "Dialog.background": panel_bg,
            "Dialog.foreground": fg,
            "Dialog.borderColor": border_color,
            "DialogWrapper.southPanelBackground": panel_bg,
            "OnePixelDivider.background": border_color,
            "Borders.color": border_color,
            "Borders.ContrastBorderColor": lighter_bg,

            # Tool windows
            "ToolWindow.background": panel_bg,
            "ToolWindow.header.background": self.derivator.adjust_brightness(panel_bg, 0.05 if self.ghostty.is_dark else -0.05),
            "ToolWindow.header.active.background": self.derivator.adjust_brightness(panel_bg, 0.1 if self.ghostty.is_dark else -0.1),
            "ToolWindow.header.border.background": lighter_bg,
            "ToolWindow.header.closeButton.background": panel_bg,
            "ToolWindow.Button.selectedBackground": hover_bg,
            "ToolWindow.Button.hoverBackground": hover_bg,
            "ToolWindow.Button.selectedForeground": fg,
            "ToolWindow.HeaderTab.selectedBackground": self.derivator.adjust_brightness(panel_bg, 0.15 if self.ghostty.is_dark else -0.15),
            "ToolWindow.HeaderTab.selectedInactiveBackground": self.derivator.adjust_brightness(panel_bg, 0.05 if self.ghostty.is_dark else -0.05),
            "ToolWindow.HeaderTab.hoverBackground": hover_bg,
            "ToolWindow.HeaderTab.hoverInactiveBackground": self.derivator.adjust_brightness(hover_bg, -0.05 if self.ghostty.is_dark else 0.05),
            "ToolWindow.HeaderCloseButton.background": panel_bg,

            # Editor
            "Editor.background": bg,
            "EditorPane.background": bg,
            "EditorPane.inactiveBackground": inactive_bg,
            "EditorGroupsTabs.background": panel_bg,
            "EditorTabs.background": panel_bg,
            "EditorTabs.borderColor": border_color,
            "EditorTabs.underlineColor": accent_color,
            "EditorTabs.underlinedTabBackground": self.derivator.adjust_brightness(panel_bg, 0.1 if self.ghostty.is_dark else -0.1),
            "EditorTabs.hoverBackground": hover_bg,
            "EditorTabs.inactiveUnderlineColor": self.derivator.adjust_brightness(accent_color, -0.3 if self.ghostty.is_dark else 0.3),
            "FileColor.Yellow": self.derivator.blend_colors(bg, warning_color, 0.05),
            "FileColor.Green": self.derivator.blend_colors(bg, success_color, 0.05),
            "FileColor.Blue": self.derivator.blend_colors(bg, accent_color, 0.05),
            "FileColor.Violet": self.derivator.blend_colors(bg, "#9370DB", 0.05),  # Medium purple
            "FileColor.Orange": self.derivator.blend_colors(bg, "#FFA500", 0.05),  # Orange
            "FileColor.Rose": self.derivator.blend_colors(bg, "#FF007F", 0.05),    # Rose

            # Menus
            "Menu.background": panel_bg,
            "Menu.foreground": fg,
            "Menu.borderColor": border_color,
            "Menu.acceleratorForeground": self.derivator.adjust_brightness(fg, -0.2 if self.ghostty.is_dark else 0.2),
            "Menu.selectionBackground": hover_bg,
            "Menu.selectionForeground": fg,
            "MenuItem.acceleratorForeground": self.derivator.adjust_brightness(fg, -0.2 if self.ghostty.is_dark else 0.2),
            "MenuItem.selectionBackground": hover_bg,
            "MenuItem.selectionForeground": fg,
            "PopupMenu.background": panel_bg,
            "PopupMenu.borderColor": border_color,
            "MenuBar.background": bg,
            "MenuBar.borderColor": border_color,

            # UI Controls
            "Button.background": panel_bg,
            "Button.foreground": fg,
            "Button.hoverBackground": hover_bg,
            "Button.pressedBackground": pressed_bg,
            "Button.focusedBorderColor": accent_color,
            "Button.default.foreground": fg,
            "Button.default.background": accent_color,
            "Button.default.hoverBackground": self.derivator.adjust_brightness(accent_color, 0.1 if self.ghostty.is_dark else -0.1),
            "Button.default.pressedBackground": self.derivator.adjust_brightness(accent_color, -0.1 if self.ghostty.is_dark else 0.1),
            "Button.default.focusedBorderColor": self.derivator.adjust_brightness(accent_color, 0.2 if self.ghostty.is_dark else -0.2),
            "CheckBox.background": bg,
            "CheckBox.foreground": fg,
            "CheckBox.select": accent_color,
            "ComboBox.background": bg,
            "ComboBox.foreground": fg,
            "ComboBox.selectionBackground": hover_bg,
            "ComboBox.selectionForeground": fg,
            "ComboBox.disabledBackground": self.derivator.adjust_brightness(bg, -0.05 if self.ghostty.is_dark else 0.05),
            "ComboBox.ArrowButton.background": panel_bg,
            "ComboBox.ArrowButton.iconColor": fg,
            "Component.borderColor": border_color,
            "Component.focusedBorderColor": accent_color,
            "Component.disabledBorderColor": self.derivator.adjust_brightness(border_color, -0.3 if self.ghostty.is_dark else 0.3),
            "Component.errorFocusColor": error_color,
            "Component.inactiveErrorFocusColor": self.derivator.adjust_brightness(error_color, -0.3 if self.ghostty.is_dark else 0.3),
            "Component.warningFocusColor": warning_color,
            "Component.inactiveWarningFocusColor": self.derivator.adjust_brightness(warning_color, -0.3 if self.ghostty.is_dark else 0.3),
            "Link.activeForeground": accent_color,
            "Link.hoverForeground": accent_color,
            "Link.pressedForeground": accent_color,
            "Link.visitedForeground": self.derivator.adjust_brightness(accent_color, -0.2 if self.ghostty.is_dark else 0.2),
            "ToggleButton.background": panel_bg,
            "ToggleButton.foreground": fg,
            "ToggleButton.onBackground": accent_color,
            "ToggleButton.onForeground": "#FFFFFF" if self.ghostty.is_dark else "#000000",
            "ToggleButton.offBackground": self.derivator.adjust_brightness(panel_bg, -0.1 if self.ghostty.is_dark else 0.1),
            "ToggleButton.offForeground": fg,
            "ToggleButton.buttonColor": fg,

            # Trees and Lists
            "Tree.background": bg,
            "Tree.foreground": fg,
            "Tree.selectionBackground": self.ghostty.selection_background,
            "Tree.selectionForeground": self.ghostty.selection_foreground,
            "Tree.selectionInactiveBackground": selection_inactive_bg,
            "Tree.rowHeight": 20,
            "List.background": bg,
            "List.foreground": fg,
            "List.selectionBackground": self.ghostty.selection_background,
            "List.selectionForeground": self.ghostty.selection_foreground,
            "List.selectionInactiveBackground": selection_inactive_bg,
            "Table.background": bg,
            "Table.foreground": fg,
            "Table.selectionBackground": self.ghostty.selection_background,
            "Table.selectionForeground": self.ghostty.selection_foreground,
            "Table.stripeColor": self.derivator.adjust_brightness(bg, 0.05 if self.ghostty.is_dark else -0.05),
            "Table.gridColor": border_color,

            # Text fields
            "TextField.background": bg,
            "TextField.foreground": fg,
            "TextField.selectionBackground": self.ghostty.selection_background,
            "TextField.selectionForeground": self.ghostty.selection_foreground,
            "TextArea.background": bg,
            "TextArea.foreground": fg,
            "TextArea.selectionBackground": self.ghostty.selection_background,
            "TextArea.selectionForeground": self.ghostty.selection_foreground,
            "FormattedTextField.background": bg,
            "PasswordField.background": bg,
            "TextPane.background": bg,
            "TextPane.foreground": fg,
            "EditorPane.selectionBackground": self.ghostty.selection_background,

            # Separators and Borders
            "Separator.foreground": border_color,
            "Separator.separatorColor": border_color,
            "TabbedPane.tabSelectionHeight": 2,
            "TabbedPane.tabAreaBackground": panel_bg,
            "TabbedPane.background": bg,
            "TabbedPane.underlineColor": accent_color,
            "TabbedPane.hoverColor": hover_bg,
            "TabbedPane.contentAreaColor": border_color,

            # Status Bar
            "StatusBar.background": panel_bg,
            "StatusBar.foreground": fg,
            "StatusBar.borderColor": border_color,
            "StatusBar.hoverBackground": hover_bg,

            # Progress Bar
            "ProgressBar.background": panel_bg,
            "ProgressBar.foreground": accent_color,
            "ProgressBar.progressColor": accent_color,
            "ProgressBar.indeterminateStartColor": accent_color,
            "ProgressBar.indeterminateEndColor": accent_secondary,

            # Scroll Bar
            "ScrollBar.background": bg,
            "ScrollBar.thumbColor": self.derivator.adjust_brightness(bg, 0.3 if self.ghostty.is_dark else -0.3),
            "ScrollBar.thumbBorderColor": self.derivator.adjust_brightness(bg, 0.4 if self.ghostty.is_dark else -0.4),
            "ScrollBar.hoverThumbColor": self.derivator.adjust_brightness(bg, 0.4 if self.ghostty.is_dark else -0.4),
            "ScrollBar.hoverThumbBorderColor": self.derivator.adjust_brightness(bg, 0.5 if self.ghostty.is_dark else -0.5),
            "ScrollBar.trackColor": bg,
            "ScrollBar.Mac.hoverThumbColor": self.derivator.adjust_brightness(bg, 0.4 if self.ghostty.is_dark else -0.4),
            "ScrollBar.Mac.thumbColor": self.derivator.adjust_brightness(bg, 0.3 if self.ghostty.is_dark else -0.3),

            # Search
            "SearchEverywhere.background": panel_bg,
            "SearchEverywhere.foreground": fg,
            "SearchEverywhere.Tab.selectedBackground": hover_bg,
            "SearchEverywhere.Tab.selectedForeground": fg,
            "SearchEverywhere.SearchField.background": bg,
            "SearchEverywhere.SearchField.borderColor": border_color,
            "SearchEverywhere.List.separatorColor": border_color,
            "SearchMatch.startBackground": self.derivator.blend_colors(bg, accent_color, 0.3),
            "SearchMatch.endBackground": self.derivator.blend_colors(bg, accent_color, 0.1),

            # Notifications
            "Notification.background": panel_bg,
            "Notification.foreground": fg,
            "Notification.borderColor": border_color,
            "Notification.errorBackground": self.derivator.blend_colors(bg, error_color, 0.1),
            "Notification.errorBorderColor": error_color,
            "Notification.errorForeground": fg,
            "Notification.warningBackground": self.derivator.blend_colors(bg, warning_color, 0.1),
            "Notification.warningBorderColor": warning_color,
            "Notification.warningForeground": fg,
            "Notification.infoBackground": self.derivator.blend_colors(bg, accent_color, 0.1),
            "Notification.infoBorderColor": accent_color,
            "Notification.infoForeground": fg,

            # Tooltips
            "ToolTip.background": panel_bg,
            "ToolTip.foreground": fg,
            "ToolTip.borderColor": border_color,
            "ValidationTooltip.errorBackground": error_color,
            "ValidationTooltip.errorBorderColor": self.derivator.adjust_brightness(error_color, 0.2 if self.ghostty.is_dark else -0.2),
            "ValidationTooltip.warningBackground": warning_color,
            "ValidationTooltip.warningBorderColor": self.derivator.adjust_brightness(warning_color, 0.2 if self.ghostty.is_dark else -0.2),

            # Icons
            "Icons.foreground": fg,
            "Icons.greyForeground": self.derivator.adjust_brightness(fg, -0.3 if self.ghostty.is_dark else 0.3),
            "Icons.redForeground": error_color,
            "Icons.greenForeground": success_color,
            "Icons.blueForeground": accent_color,
            "Icons.yellowForeground": warning_color
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
  <category>UI</category>

  <description><![CDATA[
    <h2>{theme_name} Theme</h2>
    <p>A beautiful theme converted from the Ghostty terminal theme collection.</p>

    <p><strong>Features:</strong></p>
    <ul>
      <li>Complete UI theme with intelligent color derivation</li>
      <li>Editor color scheme optimized for code readability</li>
      <li>{"Dark" if self.ghostty.is_dark else "Light"} theme with harmonious color palette</li>
      <li>Syntax highlighting based on terminal ANSI colors</li>
      <li>Full styling for tool windows, borders, and all UI elements</li>
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
      <li>Full styling for tool windows, borders, and all UI elements</li>
    </ul>
  ]]></change-notes>

  <idea-version since-build="193" until-build="999.*"/>

  <depends>com.intellij.modules.platform</depends>

  <extensions defaultExtensionNs="com.intellij">
    <themeProvider id="{self.theme_id}" path="/{self.ghostty.name}.theme.json"/>
    <bundledColorScheme path="/{self.ghostty.name}.xml"/>
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


def convert_theme(input_file: Path, output_dir: Path, create_dir: bool = False):
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

    if create_dir:
        print(f"  ✓ Generated theme in {theme_dir}")
        return theme_dir
    else:
        jar_path = create_jar_file(theme_dir, output_dir)
        print(f"  ✓ Generated JAR: {jar_path.name}")
        return jar_path


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
    parser.add_argument('--dir', action='store_true', help='Create theme directories instead of JAR files')
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
                    convert_theme(theme_file, output_path, create_dir=args.dir)
                    converted += 1
            except Exception as e:
                print(f"  ✗ Failed to convert {theme_file.name}: {e}")

        print(f"\nConversion complete: {converted}/{len(theme_files)} themes converted")
        if not args.dir and not args.icls:
            print(f"\nJAR files are ready for PhpStorm installation:")
            print(f"Settings → Plugins → Install from disk → Select JAR file")
        elif args.dir:
            print(f"\nTheme directories are ready for packaging:")
            print(f"Zip the directories and install via Settings → Plugins → Install from disk")
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
            result = convert_theme(input_path, output_path, create_dir=args.dir)
            if not args.dir:
                print(f"\nInstall in PhpStorm:")
                print(f"Settings → Plugins → Install from disk → {result}")
                print(f"Then: Settings → Appearance → Theme → Select your theme")
            else:
                print(f"\nTheme directory created:")
                print(f"Zip the directory and install via Settings → Plugins → Install from disk")


if __name__ == '__main__':
    main()
