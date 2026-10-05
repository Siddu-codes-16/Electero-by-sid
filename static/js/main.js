// Main JavaScript for Electero

// Utility: Show/hide elements
function show(element) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    if (element) element.classList.remove('hidden');
}

function hide(element) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    if (element) element.classList.add('hidden');
}

// Utility: Show alert message
function showAlert(message, type = 'error') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);

    setTimeout(() => alertDiv.remove(), 5000);
}

// Utility: Format numbers
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

// API call wrapper
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Request failed');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// LED Calculator
if (document.getElementById('led-form')) {
    document.getElementById('led-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const supplyVoltage = parseFloat(document.getElementById('supply-voltage').value);
        const ledVoltage = parseFloat(document.getElementById('led-voltage').value);
        const ledCurrent = parseFloat(document.getElementById('led-current').value);

        try {
            const result = await apiCall('/api/calculate/led', 'POST', {
                supply_voltage: supplyVoltage,
                led_voltage: ledVoltage,
                led_current: ledCurrent
            });

            if (result.error) {
                showAlert(result.error, 'error');
                return;
            }

            // Display results
            document.getElementById('calculated-resistance').textContent =
                `${result.calculated_resistance} Ω`;
            document.getElementById('standard-resistance').textContent =
                `${result.standard_resistance} Ω`;
            document.getElementById('actual-current').textContent =
                `${result.actual_current_ma} mA`;
            document.getElementById('power-dissipation').textContent =
                `${result.power_dissipation_w} W`;
            document.getElementById('recommended-wattage').textContent =
                `${result.recommended_wattage} W`;

            show('result-section');
            showAlert('Calculation complete!', 'success');

        } catch (error) {
            showAlert(error.message, 'error');
        }
    });
}

// Voltage Divider Calculator
if (document.getElementById('vd-form')) {
    document.getElementById('vd-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const vin = parseFloat(document.getElementById('vin').value);
        const vout = parseFloat(document.getElementById('vout').value);
        const r1 = document.getElementById('r1').value ?
            parseFloat(document.getElementById('r1').value) : null;
        const r2 = document.getElementById('r2').value ?
            parseFloat(document.getElementById('r2').value) : null;

        try {
            const result = await apiCall('/api/calculate/voltage-divider', 'POST', {
                vin, vout, r1, r2
            });

            if (result.error) {
                showAlert(result.error, 'error');
                return;
            }

            // Display results
            let html = '';
            if (result.r1_standard) {
                html += `<div class="result-item">
                    <span class="result-label">R1 (Calculated):</span>
                    <span class="result-value">${result.r1_calculated} Ω</span>
                </div>
                <div class="result-item">
                    <span class="result-label">R1 (Standard):</span>
                    <span class="result-value highlight">${result.r1_standard} Ω</span>
                </div>
                <div class="result-item">
                    <span class="result-label">R2:</span>
                    <span class="result-value">${result.r2} Ω</span>
                </div>`;
            } else if (result.r2_standard) {
                html += `<div class="result-item">
                    <span class="result-label">R1:</span>
                    <span class="result-value">${result.r1} Ω</span>
                </div>
                <div class="result-item">
                    <span class="result-label">R2 (Calculated):</span>
                    <span class="result-value">${result.r2_calculated} Ω</span>
                </div>
                <div class="result-item">
                    <span class="result-label">R2 (Standard):</span>
                    <span class="result-value highlight">${result.r2_standard} Ω</span>
                </div>`;
            } else {
                html += `<div class="result-item">
                    <span class="result-label">R1:</span>
                    <span class="result-value">${result.r1} Ω</span>
                </div>
                <div class="result-item">
                    <span class="result-label">R2:</span>
                    <span class="result-value">${result.r2} Ω</span>
                </div>`;
            }

            html += `<div class="result-item">
                <span class="result-label">Actual Output Voltage:</span>
                <span class="result-value highlight">${result.actual_vout || result.calculated_vout} V</span>
            </div>
            <div class="result-item">
                <span class="result-label">Current Draw:</span>
                <span class="result-value">${result.current_ma} mA</span>
            </div>
            <div class="result-item">
                <span class="result-label">Power Dissipation:</span>
                <span class="result-value">${result.power_dissipation_w} W</span>
            </div>`;

            document.getElementById('vd-results').innerHTML = html;
            show('vd-result-section');
            showAlert('Calculation complete!', 'success');

        } catch (error) {
            showAlert(error.message, 'error');
        }
    });
}

// Color Code Decoder/Encoder
if (document.getElementById('decode-form')) {
    const colors = ['black', 'brown', 'red', 'orange', 'yellow', 'green',
                   'blue', 'violet', 'grey', 'white'];
    const multiplierColors = [...colors, 'gold', 'silver'];
    const toleranceColors = ['brown', 'red', 'green', 'blue', 'violet',
                            'grey', 'gold', 'silver'];

    let selectedBands = {
        band1: 'brown',
        band2: 'black',
        band3: 'red',
        band4: 'gold'
    };

    // Create color selectors
    function createColorSelector(containerId, colorList, bandName) {
        const container = document.getElementById(containerId);
        colorList.forEach(color => {
            const div = document.createElement('div');
            div.className = `color-option color-${color}`;
            div.dataset.color = color;
            div.title = color.charAt(0).toUpperCase() + color.slice(1);

            if (selectedBands[bandName] === color) {
                div.classList.add('selected');
            }

            div.addEventListener('click', () => {
                container.querySelectorAll('.color-option').forEach(opt =>
                    opt.classList.remove('selected'));
                div.classList.add('selected');
                selectedBands[bandName] = color;
                updateResistorVisual();
            });

            container.appendChild(div);
        });
    }

    createColorSelector('band1-colors', colors, 'band1');
    createColorSelector('band2-colors', colors, 'band2');
    createColorSelector('band3-colors', multiplierColors, 'band3');
    createColorSelector('band4-colors', toleranceColors, 'band4');

    // Update visual resistor
    function updateResistorVisual() {
        document.getElementById('visual-band1').className =
            `resistor-band color-${selectedBands.band1}`;
        document.getElementById('visual-band2').className =
            `resistor-band color-${selectedBands.band2}`;
        document.getElementById('visual-band3').className =
            `resistor-band color-${selectedBands.band3}`;
        document.getElementById('visual-band4').className =
            `resistor-band color-${selectedBands.band4}`;
    }

    updateResistorVisual();

    // Decode color code
    document.getElementById('decode-btn').addEventListener('click', async () => {
        try {
            const result = await apiCall('/api/color-code/decode', 'POST', selectedBands);

            if (result.error) {
                showAlert(result.error, 'error');
                return;
            }

            document.getElementById('decoded-resistance').textContent =
                result.resistance_readable;
            document.getElementById('decoded-tolerance').textContent =
                `±${result.tolerance_percent}%`;

            show('decode-result');

        } catch (error) {
            showAlert(error.message, 'error');
        }
    });
}

// Encode resistance to color code
if (document.getElementById('encode-form')) {
    document.getElementById('encode-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const resistance = parseFloat(document.getElementById('encode-resistance').value);

        try {
            const result = await apiCall('/api/color-code/encode', 'POST', { resistance });

            if (result.error) {
                showAlert(result.error, 'error');
                return;
            }

            document.getElementById('encode-band1').textContent =
                result.band1.charAt(0).toUpperCase() + result.band1.slice(1);
            document.getElementById('encode-band2').textContent =
                result.band2.charAt(0).toUpperCase() + result.band2.slice(1);
            document.getElementById('encode-band3').textContent =
                result.band3.charAt(0).toUpperCase() + result.band3.slice(1);
            document.getElementById('encode-band4').textContent =
                result.band4.charAt(0).toUpperCase() + result.band4.slice(1);

            // Update visual
            document.getElementById('encode-visual-band1').className =
                `resistor-band color-${result.band1}`;
            document.getElementById('encode-visual-band2').className =
                `resistor-band color-${result.band2}`;
            document.getElementById('encode-visual-band3').className =
                `resistor-band color-${result.band3}`;
            document.getElementById('encode-visual-band4').className =
                `resistor-band color-${result.band4}`;

            show('encode-result');
            showAlert('Encoding complete!', 'success');

        } catch (error) {
            showAlert(error.message, 'error');
        }
    });
}

// Set active nav link
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
