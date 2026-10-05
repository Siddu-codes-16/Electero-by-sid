"""
Core calculation logic for Electero
All electronics formulas and algorithms
"""
import numpy as np
from scipy import signal


# Standard resistor values (E12, E24, E96 series)
E12_VALUES = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
E24_VALUES = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]
E96_VALUES = [
    100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143,
    147, 150, 154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210,
    215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309,
    316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453,
    464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665,
    681, 698, 715, 732, 750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976
]

# Color code mappings
COLOR_CODES = {
    'black': 0, 'brown': 1, 'red': 2, 'orange': 3, 'yellow': 4,
    'green': 5, 'blue': 6, 'violet': 7, 'grey': 8, 'white': 9
}

MULTIPLIER_COLORS = {
    'black': 1, 'brown': 10, 'red': 100, 'orange': 1000, 'yellow': 10000,
    'green': 100000, 'blue': 1000000, 'violet': 10000000, 'grey': 100000000,
    'white': 1000000000, 'gold': 0.1, 'silver': 0.01
}

TOLERANCE_COLORS = {
    'brown': 1, 'red': 2, 'green': 0.5, 'blue': 0.25, 'violet': 0.1,
    'grey': 0.05, 'gold': 5, 'silver': 10, 'none': 20
}


class LEDCalculator:
    """LED resistor calculator"""

    @staticmethod
    def calculate(supply_voltage, led_voltage, led_current_ma):
        """
        Calculate LED resistor value

        Args:
            supply_voltage: Supply voltage (V)
            led_voltage: LED forward voltage (V)
            led_current_ma: Desired LED current (mA)

        Returns:
            dict with calculated values
        """
        led_current_a = led_current_ma / 1000.0

        # Ohm's Law: R = (Vs - Vf) / I
        voltage_drop = supply_voltage - led_voltage

        if voltage_drop <= 0:
            return {
                'error': 'Supply voltage must be greater than LED forward voltage'
            }

        if led_current_a <= 0:
            return {
                'error': 'LED current must be greater than 0'
            }

        resistor_value = voltage_drop / led_current_a
        power_dissipation = voltage_drop * led_current_a

        # Find nearest standard value (E24 series)
        standard_value = find_nearest_standard_value(resistor_value, 'E24')
        actual_current = voltage_drop / standard_value * 1000  # mA
        actual_power = voltage_drop * (actual_current / 1000)

        # Recommend resistor wattage
        recommended_wattage = recommend_wattage(actual_power)

        return {
            'calculated_resistance': round(resistor_value, 2),
            'standard_resistance': standard_value,
            'actual_current_ma': round(actual_current, 2),
            'power_dissipation_w': round(actual_power, 3),
            'recommended_wattage': recommended_wattage,
            'voltage_drop': round(voltage_drop, 2)
        }


class VoltageDividerCalculator:
    """Voltage divider calculator"""

    @staticmethod
    def calculate(vin, vout, r1=None, r2=None):
        """
        Calculate voltage divider values

        Args:
            vin: Input voltage (V)
            vout: Desired output voltage (V)
            r1: First resistor (optional)
            r2: Second resistor (optional)

        Returns:
            dict with calculated values
        """
        if vout >= vin:
            return {'error': 'Output voltage must be less than input voltage'}

        if r1 and r2:
            # Calculate output voltage from given resistors
            calculated_vout = vin * r2 / (r1 + r2)
            current = vin / (r1 + r2) * 1000  # mA
            power = (vin ** 2) / (r1 + r2)

            return {
                'r1': r1,
                'r2': r2,
                'calculated_vout': round(calculated_vout, 3),
                'current_ma': round(current, 3),
                'power_dissipation_w': round(power, 3)
            }

        elif r1:
            # Calculate R2 from R1
            r2_calculated = (r1 * vout) / (vin - vout)
            r2_standard = find_nearest_standard_value(r2_calculated, 'E24')
            actual_vout = vin * r2_standard / (r1 + r2_standard)
            current = vin / (r1 + r2_standard) * 1000
            power = (vin ** 2) / (r1 + r2_standard)

            return {
                'r1': r1,
                'r2_calculated': round(r2_calculated, 2),
                'r2_standard': r2_standard,
                'actual_vout': round(actual_vout, 3),
                'current_ma': round(current, 3),
                'power_dissipation_w': round(power, 3)
            }

        else:
            # Calculate both resistors (assume R2 = 10k as starting point)
            r2_assumed = 10000
            r1_calculated = r2_assumed * ((vin / vout) - 1)
            r1_standard = find_nearest_standard_value(r1_calculated, 'E24')
            actual_vout = vin * r2_assumed / (r1_standard + r2_assumed)
            current = vin / (r1_standard + r2_assumed) * 1000
            power = (vin ** 2) / (r1_standard + r2_assumed)

            return {
                'r1_calculated': round(r1_calculated, 2),
                'r1_standard': r1_standard,
                'r2': r2_assumed,
                'actual_vout': round(actual_vout, 3),
                'current_ma': round(current, 3),
                'power_dissipation_w': round(power, 3)
            }


class FilterCalculator:
    """RC filter calculator and frequency response"""

    @staticmethod
    def calculate_lowpass(cutoff_freq, impedance=10000):
        """
        Calculate RC low-pass filter

        Args:
            cutoff_freq: Cutoff frequency in Hz
            impedance: Desired impedance (default 10k)

        Returns:
            dict with component values and frequency response
        """
        # fc = 1 / (2 * π * R * C)
        # C = 1 / (2 * π * R * fc)

        capacitance = 1 / (2 * np.pi * impedance * cutoff_freq)

        # Find standard capacitor value
        c_standard = find_nearest_capacitor_value(capacitance)
        actual_cutoff = 1 / (2 * np.pi * impedance * c_standard)

        # Generate frequency response
        frequencies = np.logspace(0, 6, 100)  # 1 Hz to 1 MHz
        response = calculate_lowpass_response(frequencies, impedance, c_standard)

        return {
            'resistor': impedance,
            'calculated_capacitor_f': capacitance,
            'standard_capacitor_f': c_standard,
            'standard_capacitor_readable': format_capacitance(c_standard),
            'actual_cutoff_hz': round(actual_cutoff, 2),
            'frequencies': frequencies.tolist(),
            'magnitude_db': response.tolist()
        }

    @staticmethod
    def calculate_highpass(cutoff_freq, impedance=10000):
        """
        Calculate RC high-pass filter

        Args:
            cutoff_freq: Cutoff frequency in Hz
            impedance: Desired impedance (default 10k)

        Returns:
            dict with component values and frequency response
        """
        capacitance = 1 / (2 * np.pi * impedance * cutoff_freq)
        c_standard = find_nearest_capacitor_value(capacitance)
        actual_cutoff = 1 / (2 * np.pi * impedance * c_standard)

        frequencies = np.logspace(0, 6, 100)
        response = calculate_highpass_response(frequencies, impedance, c_standard)

        return {
            'resistor': impedance,
            'calculated_capacitor_f': capacitance,
            'standard_capacitor_f': c_standard,
            'standard_capacitor_readable': format_capacitance(c_standard),
            'actual_cutoff_hz': round(actual_cutoff, 2),
            'frequencies': frequencies.tolist(),
            'magnitude_db': response.tolist()
        }


class ColorCodeCalculator:
    """Resistor color code decoder/encoder"""

    @staticmethod
    def decode(band1, band2, band3, band4='gold'):
        """
        Decode resistor color bands to resistance value

        Args:
            band1, band2: Digit bands
            band3: Multiplier band
            band4: Tolerance band (default gold = 5%)

        Returns:
            dict with resistance value and tolerance
        """
        try:
            digit1 = COLOR_CODES[band1.lower()]
            digit2 = COLOR_CODES[band2.lower()]
            multiplier = MULTIPLIER_COLORS[band3.lower()]
            tolerance = TOLERANCE_COLORS[band4.lower()]

            resistance = (digit1 * 10 + digit2) * multiplier

            return {
                'resistance': resistance,
                'resistance_readable': format_resistance(resistance),
                'tolerance_percent': tolerance
            }
        except KeyError as e:
            return {'error': f'Invalid color: {e}'}

    @staticmethod
    def encode(resistance):
        """
        Encode resistance value to color bands

        Args:
            resistance: Resistance in ohms

        Returns:
            dict with color bands
        """
        if resistance < 10 or resistance > 99e9:
            return {'error': 'Resistance out of range (10Ω - 99GΩ)'}

        # Find appropriate multiplier
        multiplier_power = 0
        value = resistance

        while value >= 100:
            value /= 10
            multiplier_power += 1

        # Get two significant digits
        digit1 = int(value // 10)
        digit2 = int(value % 10)

        # Find color names
        colors_reverse = {v: k for k, v in COLOR_CODES.items()}
        multipliers_reverse = {v: k for k, v in MULTIPLIER_COLORS.items() if isinstance(v, int)}

        band1 = colors_reverse[digit1]
        band2 = colors_reverse[digit2]
        band3 = multipliers_reverse.get(10 ** multiplier_power, 'unknown')

        return {
            'band1': band1,
            'band2': band2,
            'band3': band3,
            'band4': 'gold',
            'tolerance_percent': 5
        }


# Helper functions

def find_nearest_standard_value(value, series='E24'):
    """Find nearest standard resistor value"""
    series_values = {
        'E12': E12_VALUES,
        'E24': E24_VALUES,
        'E96': E96_VALUES
    }

    base_values = series_values.get(series, E24_VALUES)

    # Determine the decade
    decade = 10 ** np.floor(np.log10(value))
    normalized = value / decade

    # Find closest value in the series
    closest = min(base_values, key=lambda x: abs(x / 10 - normalized))

    return closest / 10 * decade


def find_nearest_capacitor_value(capacitance):
    """Find nearest standard capacitor value"""
    # Common capacitor values (pF, nF, uF)
    standard_caps = [
        1e-12, 1.5e-12, 2.2e-12, 3.3e-12, 4.7e-12, 6.8e-12,
        10e-12, 15e-12, 22e-12, 33e-12, 47e-12, 68e-12,
        100e-12, 150e-12, 220e-12, 330e-12, 470e-12, 680e-12,
        1e-9, 1.5e-9, 2.2e-9, 3.3e-9, 4.7e-9, 6.8e-9,
        10e-9, 15e-9, 22e-9, 33e-9, 47e-9, 68e-9,
        100e-9, 150e-9, 220e-9, 330e-9, 470e-9, 680e-9,
        1e-6, 1.5e-6, 2.2e-6, 3.3e-6, 4.7e-6, 6.8e-6,
        10e-6, 15e-6, 22e-6, 33e-6, 47e-6, 68e-6,
        100e-6, 150e-6, 220e-6, 330e-6, 470e-6, 680e-6,
        1000e-6, 1500e-6, 2200e-6, 3300e-6, 4700e-6
    ]

    return min(standard_caps, key=lambda x: abs(x - capacitance))


def format_capacitance(capacitance):
    """Format capacitance in human-readable form"""
    if capacitance >= 1e-6:
        return f"{capacitance * 1e6:.1f} µF"
    elif capacitance >= 1e-9:
        return f"{capacitance * 1e9:.1f} nF"
    else:
        return f"{capacitance * 1e12:.1f} pF"


def format_resistance(resistance):
    """Format resistance in human-readable form"""
    if resistance >= 1e6:
        return f"{resistance / 1e6:.2f} MΩ"
    elif resistance >= 1e3:
        return f"{resistance / 1e3:.2f} kΩ"
    else:
        return f"{resistance:.2f} Ω"


def recommend_wattage(power):
    """Recommend resistor wattage rating"""
    # Use 2x safety factor
    safe_power = power * 2

    standard_wattages = [0.125, 0.25, 0.5, 1, 2, 5]

    for wattage in standard_wattages:
        if safe_power <= wattage:
            return wattage

    return standard_wattages[-1]


def calculate_lowpass_response(frequencies, resistance, capacitance):
    """Calculate frequency response for RC low-pass filter"""
    omega = 2 * np.pi * frequencies
    magnitude = 1 / np.sqrt(1 + (omega * resistance * capacitance) ** 2)
    magnitude_db = 20 * np.log10(magnitude)
    return magnitude_db


def calculate_highpass_response(frequencies, resistance, capacitance):
    """Calculate frequency response for RC high-pass filter"""
    omega = 2 * np.pi * frequencies
    magnitude = (omega * resistance * capacitance) / np.sqrt(1 + (omega * resistance * capacitance) ** 2)
    magnitude_db = 20 * np.log10(magnitude)
    return magnitude_db
