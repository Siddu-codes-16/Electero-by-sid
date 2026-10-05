#!/bin/bash
echo "========================================"
echo "   Electero - Electronics Design Assistant"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Initialize database
echo "Initializing database..."
python init_db.py
echo ""

# Run the application
echo "Starting Electero..."
echo "Open your browser at: http://localhost:5000"
echo ""
python app.py
