# NIFFTYSWIGGLE-KEYPAD 🎛️🌀  
A custom macro pad powered by an Arduino and Python GUI. Press hardware buttons to trigger keyboard shortcuts, switch between saved profiles, and automate your PC like a boss.

---

## 📦 What Is It?

NIFFTYSWIGGLE-KEYPAD is a DIY gadget made from:

- 🧱 A matrix-style keypad (like a 4×4 button grid)
- 💡 An Arduino board (to read buttons + send messages)
- 🧠 A Python desktop app with remapping and profiles

It lets you assign keyboard shortcuts (like `ctrl+s` or `alt+f4`) to physical buttons, create profiles for different tasks, and launch a user-friendly GUI to control it all.

---

## 🧰 What You’ll Need

| Part              | Example                    |
|-------------------|----------------------------|
| Arduino board      | Uno, Nano, Leonardo        |
| 4×4 keypad module  | Usually 8-pin matrix pad   |
| Jumper wires       | Male-to-male or breadboard |
| USB cable          | To connect Arduino to PC   |
| Windows PC         | To run the GUI             |

✅ No soldering required if you're using a breadboard or pre-wired pad.

---

## 🔌 Wiring the Keypad to Arduino

4×4 keypads typically use **8 pins**, arranged in 4 rows and 4 columns. You’ll connect each pin to a digital input on your Arduino.

### Sample Wiring:

| Keypad Pin | Connect To |
|------------|------------|
| Pin 1      | D2         |
| Pin 2      | D3         |
| Pin 3      | D4         |
| Pin 4      | D5         |
| Pin 5      | D6         |
| Pin 6      | D7         |
| Pin 7      | D8         |
| Pin 8      | D9         |

💡 This assumes the standard keypad layout used by the Keypad Arduino library. Adjust as needed for your specific hardware.

---

## 🚀 Step-by-Step: Arduino Setup

1. Download and install the **Arduino IDE**:  
   [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)

2. Open this sketch from the repo:  
   `arduino/arduino_keyboard.ino`

3. Connect your Arduino via USB

4. In the IDE, choose:
   - Board: Arduino Uno (or your model)
   - Port: COM3 (or the detected port)

5. Click **Upload (✓)** to flash the sketch

Once uploaded, your Arduino will listen for keypad presses and send them to the Python app over Serial.

---

## 🖥️ How to Run the Desktop App

### ✅ Option A: Run the `.exe` (Easy Mode)

1. Go to the [Releases](https://github.com/NifftySwiggle/NifftySwiggle-Keypad/releases)
2. Download `NIFFTYSWIGGLE-KEYPAD.exe`
3. Double-click to launch!

Features:
- Auto-connects to Arduino
- GUI for live key remapping
- Profile save/load system
- Light/dark theme toggle

You’re ready to Swiggle!

---

### 💡 Option B: Run the Python Script

For users who want to customize or build the app from source.

#### Step-by-Step Guide

1. **Install Python**  
   [https://www.python.org/downloads](https://www.python.org/downloads)  
   ✅ Be sure to check “Add Python to PATH” during install

2. **Open NIFFTYSWIGGLE-KEYPAD.py**

3. **Install Required Packages**

   Open Command Prompt and run:

   ```bash
   pip install pyserial keyboard

4. **Run .py**

   ```bash
   python NIFFTYSWIGGLE-KEYPAD.py
