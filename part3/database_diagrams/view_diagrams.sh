#!/bin/bash

# Safe script to view database diagrams
# This script helps avoid zsh parse errors when viewing Mermaid diagrams

echo "================================================"
echo "HBnB Database Diagrams Viewer"
echo "================================================"

echo ""
echo "Available diagram files:"
echo "1. hbnb_er_diagram.md - Main ER diagram"
echo "2. hbnb_extended_er_diagram.md - Extended schema"
echo "3. relationship_types_diagram.md - Relationship types"
echo "4. diagram_examples.md - Examples and testing"
echo "5. README.md - Documentation"
echo ""

echo "IMPORTANT: These are Mermaid.js diagrams in markdown format."
echo "Do NOT try to execute them directly in the shell!"
echo ""

echo "How to view the diagrams:"
echo "------------------------"
echo "1. View on GitHub/GitLab (recommended):"
echo "   - Open the .md files directly in your browser"
echo "   - GitHub/GitLab render Mermaid diagrams automatically"
echo ""
echo "2. Use Mermaid Live Editor:"
echo "   - Go to https://mermaid.live/"
echo "   - Copy the diagram code from the .md files"
echo "   - Paste into the editor"
echo ""
echo "3. Use VS Code with Mermaid extension:"
echo "   - Install 'Mermaid Markdown Syntax Highlighting'"
echo "   - Open .md files and use preview mode"
echo ""
echo "4. Export as images:"
echo "   - Use mermaid-cli: npm install -g @mermaid-js/mermaid-cli"
echo "   - Run: mmdc -i hbnb_er_diagram.md -o hbnb_er_diagram.png"
echo ""

echo "To avoid zsh parse errors:"
echo "- Always view .md files in proper markdown viewers"
echo "- Never execute Mermaid diagram code directly in shell"
echo "- Use this script to get viewing instructions"
echo ""

echo "Choose a file to display information about:"
read -p "Enter 1-5 or 'q' to quit: " choice

case $choice in
    1)
        echo ""
        echo "=== Main ER Diagram (hbnb_er_diagram.md) ==="
        echo "This file contains the core database schema with:"
        echo "- USERS, PLACES, REVIEWS, AMENITIES, PLACE_AMENITY entities"
        echo "- All primary relationships"
        echo "- Complete attribute definitions"
        echo "- Business rule constraints"
        echo ""
        echo "To view: Open hbnb_er_diagram.md in GitHub or Mermaid Live Editor"
        ;;
    2)
        echo ""
        echo "=== Extended Schema (hbnb_extended_er_diagram.md) ==="
        echo "This file contains the expanded schema with:"
        echo "- All core entities plus BOOKINGS, PAYMENTS, MESSAGES"
        echo "- Booking system relationships"
        echo "- Payment processing entities"
        echo "- User communication system"
        echo ""
        echo "To view: Open hbnb_extended_er_diagram.md in GitHub or Mermaid Live Editor"
        ;;
    3)
        echo ""
        echo "=== Relationship Types (relationship_types_diagram.md) ==="
        echo "This educational file explains:"
        echo "- Mermaid.js relationship notation"
        echo "- One-to-many, many-to-many relationships"
        echo "- Foreign key constraints"
        echo "- Unique constraints"
        echo ""
        echo "To view: Open relationship_types_diagram.md in GitHub or Mermaid Live Editor"
        ;;
    4)
        echo ""
        echo "=== Examples (diagram_examples.md) ==="
        echo "This file contains:"
        echo "- Simple test diagrams"
        echo "- Data flow examples"
        echo "- SQL query examples"
        echo "- Learning exercises"
        echo ""
        echo "To view: Open diagram_examples.md in GitHub or Mermaid Live Editor"
        ;;
    5)
        echo ""
        echo "=== Documentation (README.md) ==="
        echo "This file contains:"
        echo "- Complete usage instructions"
        echo "- Mermaid.js syntax reference"
        echo "- Viewing methods"
        echo "- Best practices"
        echo ""
        echo "To view: Open README.md in any markdown viewer"
        ;;
    q|Q)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        ;;
esac

echo ""
echo "Remember: Always view these files in proper markdown viewers!"
echo "Never execute Mermaid diagram code directly in the shell."
