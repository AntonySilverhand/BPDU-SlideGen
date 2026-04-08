#!/bin/bash

# BPDU SlideGen — Symlink Local Skills
# This script symlinks skills from this repository into your local Claude Code skills directory.

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SKILLS_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${BLUE}BPDU SlideGen — Installing skills...${NC}"

if [ ! -d "$SKILLS_DIR" ]; then
    echo -e "${YELLOW}Creating Claude Code skills directory: $SKILLS_DIR${NC}"
    mkdir -p "$SKILLS_DIR"
fi

# List of skills in this repo
SKILLS=("deep-analysis" "imagegen" "slide-export-tips" "slidegen" "slide-theme")

for SKILL in "${SKILLS[@]}"; do
    TARGET="$SKILLS_DIR/$SKILL"
    SOURCE="$REPO_DIR/skills/$SKILL"

    if [ -d "$SOURCE" ]; then
        # Remove existing file/symlink if it exists
        if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
            rm -rf "$TARGET"
        fi

        ln -s "$SOURCE" "$TARGET"
        echo -e "${GREEN}✓ Installed: $SKILL${NC}"
    else
        echo -e "${YELLOW}✗ Skill not found in repo: $SKILL${NC}"
    fi
done

echo -e "\n${BLUE}Installation complete!${NC}"
echo -e "You can now use these skills in Claude Code. Try asking:"
echo -e "${YELLOW}\"Analyze the motion...\"${NC} or ${YELLOW}\"Generate a slide deck on...\"${NC}"
