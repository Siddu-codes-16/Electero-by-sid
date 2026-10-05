# Quick Start Guide - Electero

## Installation & Setup

### Windows Users:
```bash
# Just double-click start.bat
# OR run in terminal:
start.bat
```

### Mac/Linux Users:
```bash
# Make the script executable
chmod +x start.sh

# Run it
./start.sh
```

### Manual Setup:
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python init_db.py

# 5. Run the app
python app.py
```

## Access the Application
Open your browser and go to: **http://localhost:5000**

## Features Overview

### 💡 LED Resistor Calculator
- Input: Supply voltage, LED voltage, desired current
- Output: Required resistor value with standard E24 series recommendation
- Includes power dissipation and wattage recommendation

### ⚡ Voltage Divider Calculator
- Design voltage divider networks
- Calculate R1, R2, or both based on your inputs
- Shows actual output voltage with standard component values

### 🎨 Resistor Color Code
- **Decoder**: Select color bands → Get resistance value
- **Encoder**: Enter resistance → Get color bands
- Visual resistor display with color bands

### 📊 RC Filter Designer
- Design low-pass or high-pass filters
- Interactive frequency response Bode plot
- Standard capacitor value recommendations

### 📜 Calculation History
- All calculations saved to SQLite database
- View, search, and delete past calculations
- Export-ready data format

## Project Structure
```
Electero/
├── app.py                 # Flask application & API endpoints
├── models.py              # Database models
├── calculators.py         # Core calculation logic
├── init_db.py            # Database initialization
├── requirements.txt       # Python dependencies
├── start.bat             # Windows startup script
├── start.sh              # Mac/Linux startup script
├── static/
│   ├── css/
│   │   └── style.css     # Modern dark theme styling
│   └── js/
│       └── main.js       # Frontend logic
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Home page
    ├── led.html          # LED calculator
    ├── voltage_divider.html
    ├── color_code.html
    ├── filter.html       # RC filter designer
    └── history.html      # Calculation history
```

## API Endpoints
All calculators expose REST APIs:

- `POST /api/calculate/led` - LED calculation
- `POST /api/calculate/voltage-divider` - Voltage divider
- `POST /api/calculate/filter` - Filter design
- `POST /api/color-code/decode` - Decode color bands
- `POST /api/color-code/encode` - Encode resistance
- `GET /api/history` - Get calculation history
- `DELETE /api/history/{id}` - Delete calculation

## Adding to GitHub

```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/Electero.git
git branch -M main
git push -u origin main
```

## Future Enhancements
- Ohm's Law calculator
- 555 Timer calculator
- Op-Amp gain calculators
- PCB trace width calculator
- Dark/light mode toggle
- PDF export functionality
- User authentication

## Technologies Used
- **Backend**: Python 3.8+ with Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Visualization**: Chart.js
- **Math Libraries**: NumPy, SciPy

## License
MIT License - See LICENSE file

---
Built with ❤️ for electronics students and engineers
