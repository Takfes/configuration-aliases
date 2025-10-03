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


class Colors:
    """ANSI color codes for terminal output"""

    # Basic colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    ITALIC = "\033[3m"

    # Reset
    RESET = "\033[0m"

    @staticmethod
    def strip_ansi(text: str) -> str:
        """Remove ANSI codes from text for length calculations"""
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", text)


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
            print(
                f"{Colors.BRIGHT_RED}❌ Alias file not found:{Colors.RESET} {Colors.DIM}{self.alias_file}{Colors.RESET}"
            )
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
        # Header with colors and box styling
        print(f"\n{Colors.CYAN}╭{'─' * 60}╮{Colors.RESET}")
        print(
            f"{Colors.CYAN}│{Colors.RESET} {Colors.BRIGHT_CYAN}📁 Source:{Colors.RESET} {Colors.DIM}{self.parser.alias_file}{Colors.RESET}{' ' * (60 - len(self.parser.alias_file) - 10)}{Colors.CYAN}│{Colors.RESET}"
        )
        print(
            f"{Colors.CYAN}│{Colors.RESET} {Colors.BRIGHT_YELLOW}🎯 {category.upper().replace('_', ' ')} ALIASES{Colors.RESET}{' ' * (60 - len(category.upper().replace('_', ' ')) - 12)}{Colors.CYAN}│{Colors.RESET}"
        )
        print(f"{Colors.CYAN}╰{'─' * 60}╯{Colors.RESET}\n")

        total_aliases = 0
        total_functions = 0

        for section_name in self.parser.section_order:
            items = self.parser.sections.get(section_name, [])
            if not items:
                continue

            # Section header with enhanced styling
            section_title = section_name.upper().replace("_", " ")
            print(f"{Colors.BRIGHT_BLUE}📦 {section_title}{Colors.RESET}")
            print(f"{Colors.BLUE}{'═' * (len(section_title) + 3)}{Colors.RESET}")

            for name, command, description in items:
                if command == "(function)":
                    # Function styling with icon
                    desc_text = (
                        f"{Colors.DIM} - {description}{Colors.RESET}"
                        if description
                        else ""
                    )
                    print(
                        f"   {Colors.BRIGHT_MAGENTA}⚡ {name:<11}{Colors.RESET} {Colors.YELLOW}▶{Colors.RESET} {Colors.CYAN}{command}{Colors.RESET}{desc_text}"
                    )
                    total_functions += 1
                else:
                    # Alias styling with icon
                    desc_text = (
                        f"{Colors.DIM} # {description}{Colors.RESET}"
                        if description
                        else ""
                    )
                    # Truncate long commands for readability
                    display_cmd = (
                        command if len(command) <= 50 else command[:47] + "..."
                    )
                    print(
                        f"   {Colors.BRIGHT_GREEN}🔧 {name:<11}{Colors.RESET} {Colors.YELLOW}▶{Colors.RESET} {Colors.WHITE}{display_cmd}{Colors.RESET}{desc_text}"
                    )
                    total_aliases += 1

            print()

        # Summary with enhanced styling
        print(f"{Colors.CYAN}╭{'─' * 40}╮{Colors.RESET}")
        print(
            f"{Colors.CYAN}│{Colors.RESET} {Colors.BRIGHT_CYAN}📊 Summary:{Colors.RESET} {Colors.BRIGHT_GREEN}{total_aliases} aliases{Colors.RESET}, {Colors.BRIGHT_MAGENTA}{total_functions} functions{Colors.RESET}{' ' * (40 - len(str(total_aliases)) - len(str(total_functions)) - 23)}{Colors.CYAN}│{Colors.RESET}"
        )
        print(f"{Colors.CYAN}╰{'─' * 40}╯{Colors.RESET}\n")

    def display_table(self, category: str) -> None:
        """Display aliases in compact table format"""
        # Header with colors
        print(
            f"\n{Colors.BRIGHT_CYAN}📁 Source:{Colors.RESET} {Colors.DIM}{self.parser.alias_file}{Colors.RESET}"
        )
        print(
            f"{Colors.BRIGHT_YELLOW}🎯 {category.upper().replace('_', ' ')} ALIASES{Colors.RESET}"
        )

        # Table borders with colors
        top_border = f"{Colors.CYAN}┌─────────────────────┬─────────────────────────────────────────────┐{Colors.RESET}"
        mid_border = f"{Colors.CYAN}├─────────────────────┼─────────────────────────────────────────────┤{Colors.RESET}"
        bottom_border = f"{Colors.CYAN}└─────────────────────┴─────────────────────────────────────────────┘{Colors.RESET}"

        print(top_border)

        for section_name in self.parser.section_order:
            items = self.parser.sections.get(section_name, [])
            if not items:
                continue

            section_printed = False

            for name, command, description in items:
                if not section_printed:
                    section_header = section_name.upper().replace("_", " ")
                    print(
                        f"{Colors.CYAN}│{Colors.RESET} {Colors.BRIGHT_BLUE}{section_header:<19}{Colors.RESET} {Colors.CYAN}│{Colors.RESET} {'':<43} {Colors.CYAN}│{Colors.RESET}"
                    )
                    print(mid_border)
                    section_printed = True

                # Truncate long commands and apply colors
                display_cmd = command
                if len(display_cmd) > 43:
                    display_cmd = display_cmd[:40] + "..."

                # Color code based on type
                if command == "(function)":
                    name_color = f"{Colors.BRIGHT_MAGENTA}{name}{Colors.RESET}"
                    cmd_color = f"{Colors.CYAN}{display_cmd}{Colors.RESET}"
                else:
                    name_color = f"{Colors.BRIGHT_GREEN}{name}{Colors.RESET}"
                    cmd_color = f"{Colors.WHITE}{display_cmd}{Colors.RESET}"

                # Calculate padding accounting for color codes
                name_padding = 19 - len(Colors.strip_ansi(name_color))
                cmd_padding = 43 - len(Colors.strip_ansi(cmd_color))

                print(
                    f"{Colors.CYAN}│{Colors.RESET} {name_color}{' ' * name_padding} {Colors.CYAN}│{Colors.RESET} {cmd_color}{' ' * cmd_padding} {Colors.CYAN}│{Colors.RESET}"
                )

            if section_printed:
                print(mid_border)

        print(bottom_border)

    def display_interactive(self, category: str) -> None:
        """Display interactive section menu"""
        print(
            f"\n{Colors.BRIGHT_CYAN}📁 Source:{Colors.RESET} {Colors.DIM}{self.parser.alias_file}{Colors.RESET}"
        )
        print(
            f"{Colors.BRIGHT_YELLOW}🎯 {category.upper().replace('_', ' ')} ALIASES{Colors.RESET} {Colors.GRAY}- Select a section:{Colors.RESET}\n"
        )

        section_map = {}
        i = 1

        for section_name in self.parser.section_order:
            items = self.parser.sections.get(section_name, [])
            if not items:
                continue

            alias_count = sum(1 for _, cmd, _ in items if cmd != "(function)")
            func_count = sum(1 for _, cmd, _ in items if cmd == "(function)")

            func_text = (
                f", {Colors.BRIGHT_MAGENTA}{func_count} functions{Colors.RESET}"
                if func_count > 0
                else ""
            )

            print(
                f"{Colors.YELLOW}[{i:2d}]{Colors.RESET} {Colors.BRIGHT_BLUE}📦 {section_name:<25}{Colors.RESET} {Colors.GRAY}({Colors.BRIGHT_GREEN}{alias_count} aliases{Colors.RESET}{func_text}{Colors.GRAY}){Colors.RESET}"
            )

            section_map[str(i)] = section_name
            i += 1

        print(
            f"\n{Colors.YELLOW}[{Colors.BRIGHT_RED} 0{Colors.YELLOW}]{Colors.RESET} {Colors.DIM}Return to main menu{Colors.RESET}\n"
        )

        try:
            choice = input(
                f"{Colors.BRIGHT_CYAN}Enter number or 'q' to quit:{Colors.RESET} "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.YELLOW}Exiting...{Colors.RESET}")
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
            print(
                f"{Colors.BRIGHT_RED}Invalid selection. Please try again.{Colors.RESET}"
            )
            self.display_interactive(category)

    def _display_selected_section(self, category: str, section_name: str) -> None:
        """Display only the selected section in cards format"""
        # Header with box styling
        section_title = section_name.upper().replace("_", " ")
        header_width = max(60, len(section_title) + 20)

        print(f"\n{Colors.CYAN}╭{'─' * header_width}╮{Colors.RESET}")
        print(
            f"{Colors.CYAN}│{Colors.RESET} {Colors.BRIGHT_CYAN}📁 Source:{Colors.RESET} {Colors.DIM}{self.parser.alias_file}{Colors.RESET}{' ' * (header_width - len(self.parser.alias_file) - 10)}{Colors.CYAN}│{Colors.RESET}"
        )
        print(
            f"{Colors.CYAN}│{Colors.RESET} {Colors.BRIGHT_YELLOW}🎯 {category.upper().replace('_', ' ')}{Colors.RESET} {Colors.GRAY}→{Colors.RESET} {Colors.BRIGHT_BLUE}{section_title}{Colors.RESET}{' ' * (header_width - len(category.upper().replace('_', ' ')) - len(section_title) - 14)}{Colors.CYAN}│{Colors.RESET}"
        )
        print(f"{Colors.CYAN}╰{'─' * header_width}╯{Colors.RESET}\n")

        items = self.parser.sections.get(section_name, [])
        for name, command, description in items:
            if command == "(function)":
                desc_text = (
                    f"{Colors.DIM} - {description}{Colors.RESET}" if description else ""
                )
                print(
                    f"   {Colors.BRIGHT_MAGENTA}⚡ {name:<11}{Colors.RESET} {Colors.YELLOW}▶{Colors.RESET} {Colors.CYAN}{command}{Colors.RESET}{desc_text}"
                )
            else:
                desc_text = (
                    f"{Colors.DIM} # {description}{Colors.RESET}" if description else ""
                )
                display_cmd = command if len(command) <= 50 else command[:47] + "..."
                print(
                    f"   {Colors.BRIGHT_GREEN}🔧 {name:<11}{Colors.RESET} {Colors.YELLOW}▶{Colors.RESET} {Colors.WHITE}{display_cmd}{Colors.RESET}{desc_text}"
                )

        print()

    def _show_help(self) -> None:
        """Show help information"""
        print(f"\n{Colors.BRIGHT_YELLOW}🎯 Enhanced Alias Display System{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 40}{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_CYAN}Usage:{Colors.RESET}")
        print(
            f"  {Colors.BRIGHT_GREEN}show <category>{Colors.RESET}        {Colors.GRAY}Show grouped cards view (default){Colors.RESET}"
        )
        print(
            f"  {Colors.BRIGHT_GREEN}show <category> -t{Colors.RESET}     {Colors.GRAY}Show compact table view{Colors.RESET}"
        )
        print(
            f"  {Colors.BRIGHT_GREEN}show <category> -i{Colors.RESET}     {Colors.GRAY}Show interactive section menu{Colors.RESET}"
        )
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
                f"{Colors.BRIGHT_RED}❌ Neither ALIASES_DIR nor CONFIG_PATH environment variables are set{Colors.RESET}"
            )
            sys.exit(1)

    if len(sys.argv) < 2:
        print(f"\n{Colors.BRIGHT_YELLOW}🎯 Enhanced Alias Display System{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 40}{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_CYAN}Usage:{Colors.RESET}")
        print(
            f"  {Colors.BRIGHT_GREEN}show <category>{Colors.RESET}        {Colors.GRAY}Show grouped cards view (default){Colors.RESET}"
        )
        print(
            f"  {Colors.BRIGHT_GREEN}show <category> -t{Colors.RESET}     {Colors.GRAY}Show compact table view{Colors.RESET}"
        )
        print(
            f"  {Colors.BRIGHT_GREEN}show <category> -i{Colors.RESET}     {Colors.GRAY}Show interactive section menu{Colors.RESET}"
        )
        print(f"\n{Colors.BRIGHT_CYAN}Available categories:{Colors.RESET}")

        # List available categories
        alias_files = Path(aliases_dir).glob(".alias_*")
        categories = [f.name.replace(".alias_", "") for f in alias_files if f.is_file()]

        if categories:
            for i, cat in enumerate(sorted(categories)):
                color = [
                    Colors.BRIGHT_GREEN,
                    Colors.BRIGHT_BLUE,
                    Colors.BRIGHT_MAGENTA,
                    Colors.BRIGHT_CYAN,
                ][i % 4]
                print(f"  {color}{cat}{Colors.RESET}", end="")
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
        print(
            f"{Colors.BRIGHT_RED}❌ Alias file not found:{Colors.RESET} {Colors.DIM}{alias_file}{Colors.RESET}"
        )
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
