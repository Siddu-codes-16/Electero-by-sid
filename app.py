"""
Flask application for Electero - Electronics Design Assistant
"""
from flask import Flask, render_template, request, jsonify
from models import Database
from calculators import (
    LEDCalculator, VoltageDividerCalculator, FilterCalculator,
    ColorCodeCalculator, find_nearest_standard_value
)

app = Flask(__name__)
db = Database()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/led')
def led_calculator():
    """LED resistor calculator page"""
    return render_template('led.html')


@app.route('/voltage-divider')
def voltage_divider():
    """Voltage divider calculator page"""
    return render_template('voltage_divider.html')


@app.route('/color-code')
def color_code():
    """Resistor color code page"""
    return render_template('color_code.html')


@app.route('/filter')
def filter_designer():
    """RC filter designer page"""
    return render_template('filter.html')


@app.route('/history')
def history():
    """Calculation history page"""
    return render_template('history.html')


# API Endpoints

@app.route('/api/calculate/led', methods=['POST'])
def calculate_led():
    """Calculate LED resistor value"""
    try:
        data = request.json
        supply_voltage = float(data.get('supply_voltage'))
        led_voltage = float(data.get('led_voltage'))
        led_current = float(data.get('led_current'))

        result = LEDCalculator.calculate(supply_voltage, led_voltage, led_current)

        if 'error' not in result:
            # Save to history
            db.save_calculation('LED Resistor', {
                'supply_voltage': supply_voltage,
                'led_voltage': led_voltage,
                'led_current_ma': led_current
            }, result)

        return jsonify(result)

    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input values'}), 400


@app.route('/api/calculate/voltage-divider', methods=['POST'])
def calculate_voltage_divider():
    """Calculate voltage divider values"""
    try:
        data = request.json
        vin = float(data.get('vin'))
        vout = float(data.get('vout'))
        r1 = data.get('r1')
        r2 = data.get('r2')

        if r1:
            r1 = float(r1)
        if r2:
            r2 = float(r2)

        result = VoltageDividerCalculator.calculate(vin, vout, r1, r2)

        if 'error' not in result:
            db.save_calculation('Voltage Divider', {
                'vin': vin,
                'vout': vout,
                'r1': r1,
                'r2': r2
            }, result)

        return jsonify(result)

    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input values'}), 400


@app.route('/api/calculate/filter', methods=['POST'])
def calculate_filter():
    """Calculate RC filter"""
    try:
        data = request.json
        filter_type = data.get('filter_type', 'lowpass')
        cutoff_freq = float(data.get('cutoff_freq'))
        impedance = float(data.get('impedance', 10000))

        if filter_type == 'lowpass':
            result = FilterCalculator.calculate_lowpass(cutoff_freq, impedance)
        else:
            result = FilterCalculator.calculate_highpass(cutoff_freq, impedance)

        if 'error' not in result:
            db.save_calculation(f'RC Filter ({filter_type})', {
                'cutoff_freq': cutoff_freq,
                'impedance': impedance
            }, {
                'resistor': result['resistor'],
                'capacitor': result['standard_capacitor_readable'],
                'actual_cutoff_hz': result['actual_cutoff_hz']
            })

        return jsonify(result)

    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input values'}), 400


@app.route('/api/color-code/decode', methods=['POST'])
def decode_color_code():
    """Decode resistor color code"""
    try:
        data = request.json
        band1 = data.get('band1')
        band2 = data.get('band2')
        band3 = data.get('band3')
        band4 = data.get('band4', 'gold')

        result = ColorCodeCalculator.decode(band1, band2, band3, band4)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/color-code/encode', methods=['POST'])
def encode_color_code():
    """Encode resistance value to color code"""
    try:
        data = request.json
        resistance = float(data.get('resistance'))

        result = ColorCodeCalculator.encode(resistance)

        return jsonify(result)

    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid resistance value'}), 400


@app.route('/api/standard-value/<value>/<series>')
def get_standard_value(value, series):
    """Find nearest standard value"""
    try:
        value = float(value)
        nearest = find_nearest_standard_value(value, series.upper())
        return jsonify({'nearest': nearest})

    except ValueError:
        return jsonify({'error': 'Invalid value'}), 400


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get calculation history"""
    limit = request.args.get('limit', 50, type=int)
    history = db.get_history(limit)
    return jsonify(history)


@app.route('/api/history/<int:calc_id>', methods=['DELETE'])
def delete_history(calc_id):
    """Delete a calculation from history"""
    db.delete_calculation(calc_id)
    return jsonify({'success': True})


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """Clear all calculation history"""
    db.clear_history()
    return jsonify({'success': True})


if __name__ == '__main__':
    # Initialize database on first run
    db.init_db()
    print("Electero is running!")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
