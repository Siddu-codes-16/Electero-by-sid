# Electero 🔌⚡

**Electero** is a comprehensive web-based electronics design assistant built for students and engineers. Calculate component values, design filters, decode resistor codes, and more — all with an intuitive interface.

## Features

- **LED Resistor Calculator** - Calculate the perfect resistor for your LED circuit
- **Voltage Divider Calculator** - Design voltage divider networks with standard component values
- **Resistor Color Code** - Decode and encode resistor color bands
- **RC Filter Designer** - Design low-pass/high-pass filters with frequency response plots
- **Standard Values Finder** - Find nearest E12/E24/E96 series resistor and capacitor values
- **Calculation History** - Save and revisit your past calculations

## Tech Stack

- **Backend:** Python 3.8+ with Flask
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Visualization:** Chart.js for frequency response plots
- **Calculations:** NumPy, SciPy

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Electero.git
cd Electero
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### LED Resistor Calculator
Enter your supply voltage, LED forward voltage, and desired current. Electero calculates the required resistor value and suggests the nearest standard value.

### Voltage Divider
Design voltage dividers with real-time output voltage calculation and power dissipation warnings.

### RC Filter Designer
Design filters by entering your cutoff frequency and impedance. View the frequency response with interactive Bode plots.

### Resistor Color Code
Decode: Select color bands to see the resistance value.
Encode: Enter a resistance value to see the color code.

## Project Structure

```
Electero/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── calculators.py         # Core calculation logic
├── init_db.py            # Database initialization
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── main.js       # Frontend logic
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── led.html          # LED calculator
│   ├── voltage_divider.html
│   ├── color_code.html
│   ├── filter.html       # RC filter designer
│   └── history.html      # Calculation history
└── README.md
```

## API Endpoints

All calculators expose REST API endpoints:

- `POST /api/calculate/led` - LED resistor calculation
- `POST /api/calculate/voltage-divider` - Voltage divider calculation
- `POST /api/calculate/filter` - Filter design calculation
- `GET /api/standard-value/{value}/{series}` - Find nearest standard value
- `GET /api/history` - Retrieve calculation history
- `DELETE /api/history/{id}` - Delete a calculation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Ohm's Law calculator with power calculations
- [ ] Inductor energy storage calculator
- [ ] PCB trace width calculator
- [ ] 555 Timer calculator
- [ ] Operational amplifier gain calculators
- [ ] Dark mode toggle
- [ ] Export calculations to PDF
- [ ] User authentication and cloud sync

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Built with ❤️ by an electronics enthusiast

## Acknowledgments

- Standard component values based on IEC 60063
- Circuit theory formulas from standard electronics textbooks
- Inspired by the needs of electronics students worldwide
