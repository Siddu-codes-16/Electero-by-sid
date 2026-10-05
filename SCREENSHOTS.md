# 📸 Screenshot Guide for GitHub

When you run Electero, take these screenshots to showcase on GitHub:

## Recommended Screenshots

### 1. Home Page
- **File**: `screenshot-home.png`
- **What to capture**: The landing page with all calculator cards
- **Shows**: Clean UI, project overview, navigation

### 2. LED Calculator in Action
- **File**: `screenshot-led-calculator.png`
- **What to capture**: LED calculator with filled inputs and displayed results
- **Example values**: 
  - Supply Voltage: 5V
  - LED Voltage: 2V
  - LED Current: 20mA
- **Shows**: Calculation results, standard value recommendation, power dissipation

### 3. Resistor Color Code Decoder
- **File**: `screenshot-color-code.png`
- **What to capture**: Color code page with visual resistor display
- **Shows**: Interactive color band selector, visual representation

### 4. RC Filter Designer with Plot
- **File**: `screenshot-filter-designer.png`
- **What to capture**: Filter designer with frequency response plot visible
- **Example values**:
  - Type: Low-Pass
  - Cutoff: 1000 Hz
  - Impedance: 10000 Ω
- **Shows**: Data visualization, frequency response curve

### 5. Calculation History
- **File**: `screenshot-history.png`
- **What to capture**: History page with several saved calculations
- **Shows**: Database functionality, data persistence

## How to Take Screenshots

### Windows
- **Full window**: Press `Alt + PrtScn`
- **Snipping Tool**: Search for "Snipping Tool" in Start menu

### Mac
- **Full window**: Press `Cmd + Shift + 4`, then `Space`, click window
- **Selection**: Press `Cmd + Shift + 4`, drag to select area

### Linux
- **gnome-screenshot** or **Spectacle** (depending on desktop environment)

## Adding to README

Update your README.md with screenshots like this:

```markdown
## Screenshots

### Home Page
![Home Page](screenshots/screenshot-home.png)

### LED Resistor Calculator
![LED Calculator](screenshots/screenshot-led-calculator.png)

### Resistor Color Code
![Color Code](screenshots/screenshot-color-code.png)

### RC Filter Designer
![Filter Designer](screenshots/screenshot-filter-designer.png)
```

## Directory Structure

Create a screenshots folder:
```
Electero/
├── screenshots/
│   ├── screenshot-home.png
│   ├── screenshot-led-calculator.png
│   ├── screenshot-color-code.png
│   ├── screenshot-filter-designer.png
│   └── screenshot-history.png
├── app.py
├── ...
```

## Tips for Great Screenshots

1. **Use a clean browser window** - Close unnecessary tabs and bookmarks bar
2. **Full window capture** - Show the complete interface
3. **Realistic data** - Use practical values that electronics engineers would use
4. **Highlight results** - Make sure calculated values are visible
5. **Good lighting** - If capturing your screen, ensure no glare
6. **Consistent size** - Try to keep all screenshots at similar dimensions (1920x1080 or 1280x720)

## Optional: Create a Demo GIF

Use tools like:
- **ScreenToGif** (Windows) - https://www.screentogif.com/
- **Kap** (Mac) - https://getkap.co/
- **Peek** (Linux) - https://github.com/phw/peek

Record a 10-15 second demo showing:
1. Opening the app
2. Selecting a calculator
3. Entering values
4. Viewing results

Add to README:
```markdown
## Demo
![Electero Demo](screenshots/demo.gif)
```

---

**Pro Tip**: Screenshots make your GitHub project stand out! Recruiters and fellow developers can immediately see what your project does without running it.
