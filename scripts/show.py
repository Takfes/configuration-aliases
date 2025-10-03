#!/usr/bin/env python3
"""
Enhanced Alias Display - Python Implementation
Parses alias files with section annotations and displays in various formats
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


class AliasParser:
    def __init__(self, alias_file: str):
        self.alias_file = alias_file
        self.sections: Dict[
            str, List[Tuple[str, str, str]]
        ] = {}  # section -> [(name, command, description)]
        self.section_order: List[str] = []

    def parse(self) -> bool:
        """Parse the alias file and extract sections with aliases and functions"""
        try:
            with open(self.alias_file, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"❌ Alias file not found: {self.alias_file}")
            return False

        current_section = None
        in_section = False
        equals_count = 0

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines
            if not line:
                i += 1
                continue

            # Section name: # > section name
            if line.startswith("#") and ">" in line:
                section_match = re.search(r"#\s*>\s*(.+)", line)
                if section_match:
                    current_section = section_match.group(1).strip()
                    self.section_order.append(current_section)
                    self.sections[current_section] = []
                    equals_count = 0
                    in_section = False
                    i += 1
                    continue

            # Section boundary: # ========= (at least 5 equals)
            if line.startswith("#") and "=====" in line:
                equals_count += 1
                if equals_count == 1:
                    in_section = True
                elif equals_count == 2:
                    in_section = False
                    current_section = None
                i += 1
                continue

            # Skip if not in section or no current section
            if not in_section or not current_section:
                i += 1
                continue

            # Skip commented lines (but not inline comments)
            if line.startswith("#") and "alias" not in line:
                i += 1
                continue

            # Parse alias
            alias_match = re.match(r"alias\s+([^=]+)=(.+)", line)
            if alias_match:
                name = alias_match.group(1).strip()
                command_with_comment = alias_match.group(2).strip()

                # Extract command and inline comment
                command, description = self._extract_command_and_description(
                    command_with_comment
                )
                self.sections[current_section].append((name, command, description))
                i += 1
                continue

            # Parse function
            func_match = re.match(
                r"(?:function\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\)\s*\{?", line
            )
            if func_match:
                func_name = func_match.group(1)

                # Look for description in previous lines (comments before function)
                description = self._get_function_description(lines, i)

                self.sections[current_section].append(
                    (func_name, "(function)", description)
                )
                i += 1
                continue

            i += 1

        return True

    def _extract_command_and_description(
        self, command_with_comment: str
    ) -> Tuple[str, str]:
        """Extract command and description from alias definition"""
        # Remove quotes
        command = command_with_comment.strip("'\"")

        # Look for inline comment
        comment_match = re.search(r"#\s*(.+)$", command)
        if comment_match:
            description = comment_match.group(1).strip()
            command = re.sub(r"\s*#.*$", "", command).strip("'\"")
        else:
            description = ""

        return command, description

    def _get_function_description(self, lines: List[str], func_line_idx: int) -> str:
        """Get function description from comments before function definition"""
        # Look backwards for comments
        for i in range(func_line_idx - 1, max(0, func_line_idx - 5), -1):
            line = lines[i].strip()
            if line.startswith("#") and not line.startswith("#="):
                # Extract description from comment
                desc_match = re.search(r"#\s*(.+)", line)
                if desc_match:
                    return desc_match.group(1).strip()
            elif line and not line.startswith("#"):
                break
        return ""


class AliasDisplay:
    def __init__(self, parser: AliasParser):
        self.parser = parser

    def display_cards(self, category: str) -> None:
        """Display aliases in grouped cards format (default)"""
        print(f"\n📁 Source: {self.parser.alias_file}")
        print(f"🎯 {category.upper().replace('_', ' ')} ALIASES\n")

        total_aliases = 0
        total_functions = 0

        for section_name in self.parser.section_order:
            items = self.parser.sections.get(section_name, [])
            if not items:
                continue

            print(f"📦 {section_name.upper().replace('_', ' ')}")

            for name, command, description in items:
                if command == "(function)":
                    desc_text = f" - {description}" if description else ""
                    print(f"   {name:<8} → {command}{desc_text}")
                    total_functions += 1
                else:
                    desc_text = f" # {description}" if description else ""
                    print(f"   {name:<8} → {command}{desc_text}")
                    total_aliases += 1

            print()

        print(f"📊 Total: {total_aliases} aliases, {total_functions} functions\n")

    def display_table(self, category: str) -> None:
        """Display aliases in compact table format"""
        print(f"\n📁 Source: {self.parser.alias_file}")
        print(f"🎯 {category.upper().replace('_', ' ')} ALIASES")
        print("┌─────────────────────┬─────────────────────────────────────────────┐")

        for section_name in self.parser.section_order:
            items = self.parser.sections.get(section_name, [])
            if not items:
                continue

            section_printed = False

            for name, command, description in items:
                if not section_printed:
                    section_header = section_name.upper().replace("_", " ")
                    print(f"│ {section_header:<19} │ {'':<43} │")
                    print(
                        "├─────────────────────┼─────────────────────────────────────────────┤"
                    )
                    section_printed = True

                # Truncate long commands
                display_cmd = command
                if len(display_cmd) > 43:
                    display_cmd = display_cmd[:40] + "..."

                print(f"│ {name:<19} │ {display_cmd:<43} │")

            if section_printed:
                print(
                    "├─────────────────────┼─────────────────────────────────────────────┤"
                )

        print("└─────────────────────┴─────────────────────────────────────────────┘\n")

    def display_interactive(self, category: str) -> None:
        """Display interactive section menu"""
        print(f"\n📁 Source: {self.parser.alias_file}")
        print(f"🎯 {category.upper().replace('_', ' ')} ALIASES - Select a section:\n")

        section_map = {}
        i = 1

        for section_name in self.parser.section_order:
            items = self.parser.sections.get(section_name, [])
            if not items:
                continue

            alias_count = sum(1 for _, cmd, _ in items if cmd != "(function)")
            func_count = sum(1 for _, cmd, _ in items if cmd == "(function)")

            func_text = f", {func_count} functions" if func_count > 0 else ""
            print(f"[{i:2d}] 📦 {section_name:<25} ({alias_count} aliases{func_text})")

            section_map[str(i)] = section_name
            i += 1

        print("\n[0] Return to main menu\n")

        try:
            choice = input("Enter number or 'q' to quit: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            return

        if choice.lower() == "q":
            return
        elif choice == "0":
            self._show_help()
            return
        elif choice in section_map:
            selected_section = section_map[choice]
            self._display_selected_section(category, selected_section)
        else:
            print("Invalid selection. Please try again.")
            self.display_interactive(category)

    def _display_selected_section(self, category: str, section_name: str) -> None:
        """Display only the selected section in cards format"""
        print(f"\n📁 Source: {self.parser.alias_file}")
        print(
            f"🎯 {category.upper().replace('_', ' ')} → {section_name.upper().replace('_', ' ')}\n"
        )

        items = self.parser.sections.get(section_name, [])
        for name, command, description in items:
            if command == "(function)":
                desc_text = f" - {description}" if description else ""
                print(f"   {name:<8} → {command}{desc_text}")
            else:
                desc_text = f" # {description}" if description else ""
                print(f"   {name:<8} → {command}{desc_text}")

        print()

    def _show_help(self) -> None:
        """Show help information"""
        print("\n🎯 Enhanced Alias Display System")
        print("────────────────────────────────────────")
        print("\nUsage:")
        print("  show <category>        Show grouped cards view (default)")
        print("  show <category> -t     Show compact table view")
        print("  show <category> -i     Show interactive section menu")
        print()


def main():
    # Get ALIASES_DIR from environment or use default
    aliases_dir = os.environ.get("ALIASES_DIR")

    # If not in environment, try to get from CONFIG_PATH
    if not aliases_dir:
        config_path = os.environ.get("CONFIG_PATH")
        if config_path:
            aliases_dir = os.path.join(config_path, "aliases")
        else:
            print(
                "❌ Neither ALIASES_DIR nor CONFIG_PATH environment variables are set"
            )
            sys.exit(1)

    if len(sys.argv) < 2:
        print("\n🎯 Enhanced Alias Display System")
        print("────────────────────────────────────────")
        print("\nUsage:")
        print("  show <category>        Show grouped cards view (default)")
        print("  show <category> -t     Show compact table view")
        print("  show <category> -i     Show interactive section menu")
        print("\nAvailable categories:")

        # List available categories
        alias_files = Path(aliases_dir).glob(".alias_*")
        categories = [f.name.replace(".alias_", "") for f in alias_files if f.is_file()]

        if categories:
            for i, cat in enumerate(sorted(categories)):
                print(f"  {cat}", end="")
                if (i + 1) % 4 == 0:
                    print()
            if len(categories) % 4 != 0:
                print()
        print()
        sys.exit(0)

    category = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else None

    # Find alias file
    alias_file = Path(aliases_dir) / f".alias_{category}"

    if not alias_file.exists():
        print(f"❌ Alias file not found: {alias_file}")
        sys.exit(1)

    # Parse and display
    parser = AliasParser(str(alias_file))
    if not parser.parse():
        sys.exit(1)

    display = AliasDisplay(parser)

    if mode == "-t":
        display.display_table(category)
    elif mode == "-i":
        display.display_interactive(category)
    else:
        display.display_cards(category)


if __name__ == "__main__":
    main()
