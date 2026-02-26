#!/bin/bash
# OpenClawMD Skill Installer for Agent Deck
# 
# This script installs all OpenClawMD skills into Agent Deck.
# 
# Usage:
#   ./install_skills.sh              # Install all skills
#   ./install_skills.sh --list       # List available skills
#   ./install_skills.sh --clean      # Remove all installed skills
#   ./install_skills.sh build-exact  # Install specific skill
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ZIPS_DIR="${SCRIPT_DIR}/zips"
AGENT_DECK_SKILLS_DIR="$HOME/.agent-deck/skill-db/official"

# Helper functions
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# Print header
print_header() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║         OpenClawMD Skill Installer                       ║"
    echo "║         For Agent Deck                                   ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
}

# List available skills
list_skills() {
    log_info "Available skills in $SKILLS_ZIPS_DIR:"
    echo ""
    
    if [ ! -d "$SKILLS_ZIPS_DIR" ]; then
        log_error "Skills directory not found: $SKILLS_ZIPS_DIR"
        exit 1
    fi
    
    count=0
    for zip_file in "$SKILLS_ZIPS_DIR"/*.zip; do
        if [ -f "$zip_file" ]; then
            skill_name=$(basename "$zip_file" .zip)
            echo "  • $skill_name"
            ((count++))
        fi
    done
    
    echo ""
    log_info "Total: $count skills available"
}

# Install a single skill
install_skill() {
    local skill_name=$1
    local zip_file="$SKILLS_ZIPS_DIR/${skill_name}.zip"
    local install_dir="$AGENT_DECK_SKILLS_DIR/${skill_name}"
    
    if [ ! -f "$zip_file" ]; then
        log_error "Skill not found: $skill_name"
        echo "  Available skills:"
        list_skills
        return 1
    fi
    
    # Create install directory
    mkdir -p "$install_dir"
    
    # Extract skill
    unzip -o -q "$zip_file" -d "$install_dir"
    
    if [ $? -eq 0 ]; then
        log_success "Installed: $skill_name"
        echo "  → $install_dir"
        return 0
    else
        log_error "Failed to install: $skill_name"
        return 1
    fi
}

# Install all skills
install_all() {
    log_info "Installing all skills to Agent Deck..."
    echo ""
    
    if [ ! -d "$SKILLS_ZIPS_DIR" ]; then
        log_error "Skills directory not found: $SKILLS_ZIPS_DIR"
        echo ""
        echo "Please make sure you're running this script from the OC-skills directory:"
        echo "  cd /path/to/OC-skills"
        echo "  ./install_skills.sh"
        exit 1
    fi
    
    # Create Agent Deck skills directory
    mkdir -p "$AGENT_DECK_SKILLS_DIR"
    
    installed=0
    failed=0
    
    for zip_file in "$SKILLS_ZIPS_DIR"/*.zip; do
        if [ -f "$zip_file" ]; then
            skill_name=$(basename "$zip_file" .zip)
            if install_skill "$skill_name"; then
                ((installed++))
            else
                ((failed++))
            fi
        fi
    done
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                    Installation Complete                 ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    log_success "Installed: $installed skills"
    if [ $failed -gt 0 ]; then
        log_error "Failed: $failed skills"
    fi
    echo ""
    log_info "Skills location: $AGENT_DECK_SKILLS_DIR"
    echo ""
    log_info "Next steps:"
    echo "  1. Start Agent Deck: agent-deck"
    echo "  2. Press 's' to open Skills Manager"
    echo "  3. Your skills should be listed there"
    echo ""
}

# Clean all installed skills
clean_all() {
    log_warn "This will remove all installed OpenClawMD skills from Agent Deck!"
    echo ""
    read -p "Are you sure? (y/N) " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        log_info "Removing skills..."
        
        for zip_file in "$SKILLS_ZIPS_DIR"/*.zip; do
            if [ -f "$zip_file" ]; then
                skill_name=$(basename "$zip_file" .zip)
                install_dir="$AGENT_DECK_SKILLS_DIR/${skill_name}"
                
                if [ -d "$install_dir" ]; then
                    rm -rf "$install_dir"
                    log_info "Removed: $skill_name"
                fi
            fi
        done
        
        echo ""
        log_success "All skills removed!"
        echo ""
    else
        log_info "Cancelled"
    fi
}

# Show help
show_help() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  (none)           Install all skills (default)"
    echo "  --list           List available skills"
    echo "  --clean          Remove all installed skills"
    echo "  --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                       # Install all skills"
    echo "  $0 --list                # List available skills"
    echo "  $0 build-exact           # Install specific skill"
    echo "  $0 --clean               # Remove all skills"
    echo ""
}

# Main
print_header

case "${1:-}" in
    --list|-l)
        list_skills
        ;;
    --clean)
        clean_all
        ;;
    --help|-h)
        show_help
        ;;
    *)
        if [ -n "${1:-}" ]; then
            # Install specific skill
            install_skill "$1"
        else
            # Install all skills
            install_all
        fi
        ;;
esac
