import tkinter as tk
from tkinter import ttk
import serial
import threading
import keyboard
import json
import os

# === CONFIG ===
APP_NAME        = "NIFFTYSWIGGLE-KEYPAD"
PROFILE_DIR     = './profiles/'
SERIAL_PORT     = 'COM3'
BAUD_RATE       = 9600
DEFAULT_PROFILE = 'default'
# ==============

# === THEMES ===
LIGHT_THEME = {
    "bg": "#f0f0f0", "fg": "#000000",
    "highlight": "#0078D7",
    "listbox_bg": "#ffffff", "listbox_fg": "#000000"
}

DARK_THEME = {
    "bg": "#1e1e1e", "fg": "#d4d4d4",
    "highlight": "#569CD6",
    "listbox_bg": "#252526", "listbox_fg": "#d4d4d4"
}

current_theme = LIGHT_THEME
os.makedirs(PROFILE_DIR, exist_ok=True)

default_map = {
    '1': 'i', '2': 'b', '3': 'l', 'A': 'ctrl+z',
    '4': 'e', '5': 'z', '6': 'x', 'B': 'ctrl+s',
    '7': 'h', '8': 't', '9': 'g', 'C': 'ctrl+c',
    '*': 'enter', '0': 'ctrl+0', '#': 'ctrl+x', 'D': 'ctrl+v'
}

# === PROFILE FUNCTIONS ===
def load_profile(name):
    path = os.path.join(PROFILE_DIR, f"{name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default_map.copy()

def save_profile(name):
    if name:
        with open(os.path.join(PROFILE_DIR, f"{name}.json"), "w") as f:
            json.dump(keymap, f)
        status.set(f"✅ Saved profile: {name}")
        update_profile_list()
        profile_selector.set(name)
        new_profile_name.delete(0, tk.END)
    else:
        status.set("⚠️ Enter a profile name to save.")

def get_profiles():
    return [f.replace('.json', '') for f in os.listdir(PROFILE_DIR) if f.endswith('.json')]

def update_profile_list():
    profiles = get_profiles()
    profile_selector['values'] = profiles
    if current_profile not in profiles:
        profile_selector.set(DEFAULT_PROFILE)

def load_selected_profile(event=None):
    global keymap, current_profile
    selected = profile_selector.get().strip()
    if selected:
        current_profile = selected
        keymap = load_profile(current_profile)
        status.set(f"📂 Loaded profile: {current_profile}")
        refresh_layout()
        update_mapping_list()
        apply_theme()

# === REMAPPING ===
def remap_key(key):
    def save_new_mapping():
        keymap[key] = entry.get()
        status.set(f"{key} → {entry.get()} (unsaved)")
        update_mapping_list()
        remap_win.destroy()

    remap_win = tk.Toplevel(root)
    remap_win.title(f"Remap {key}")
    remap_win.resizable(False, False)
    remap_win.configure(bg=current_theme["bg"])
    tk.Label(remap_win, text=f"Current Mapping: {keymap.get(key, '')}",
             bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=5)
    entry = tk.Entry(remap_win, width=20)
    entry.insert(0, keymap.get(key, ''))
    entry.pack(padx=10, pady=5)
    tk.Button(remap_win, text="Update", command=save_new_mapping).pack(pady=5)

# === SERIAL ===
def listen_serial():
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        status.set("🟢 Arduino Connected.")
        while True:
            try:
                if arduino.in_waiting:
                    key = arduino.readline().decode().strip()
                    action = keymap.get(key)
                    if action:
                        keyboard.send(action)
                        status.set(f"🔘 {key} → {action}")
                        root.after(700, lambda: status.set(""))
                    else:
                        status.set(f"⚠️ Unmapped key: {key}")
                        root.after(700, lambda: status.set(""))
            except Exception as e:
                status.set(f"Serial error: {e}")
    except Exception as err:
        status.set(f"🔌 Connection failed: {err}")

# === THEMING ===
def toggle_theme():
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    apply_theme()

def apply_theme():
    root.configure(bg=current_theme["bg"])
    mapping_list.configure(bg=current_theme["listbox_bg"], fg=current_theme["listbox_fg"])
    button_frame.configure(bg=current_theme["bg"])
    for widget in root.winfo_children():
        try: widget.configure(bg=current_theme["bg"], fg=current_theme["fg"])
        except: pass
    for widget in button_frame.winfo_children():
        try: widget.configure(bg=current_theme["bg"], fg=current_theme["fg"])
        except: pass

# === GUI ===
def refresh_layout():
    for widget in button_frame.winfo_children():
        widget.destroy()
    layout_keys = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
    ]
    for r, row in enumerate(layout_keys):
        for c, key in enumerate(row):
            btn = tk.Button(button_frame, text=key, width=6, command=lambda k=key: remap_key(k))
            btn.grid(row=r, column=c, padx=4, pady=4)

def update_mapping_list():
    mapping_list.delete(0, tk.END)
    for key in sorted(keymap):
        mapping_list.insert(tk.END, f"{key} → {keymap[key]}")

# === INIT ===
current_profile = DEFAULT_PROFILE
keymap = load_profile(current_profile)

root = tk.Tk()
root.title(APP_NAME)
root.geometry("400x680")
root.resizable(False, False)

status = tk.StringVar()
tk.Label(root, text=APP_NAME, font=("Segoe UI", 16, "bold")).pack(pady=(10, 0))
tk.Label(root, textvariable=status, font=("Segoe UI", 10)).pack(pady=4)

# Profile Manager
profile_frame = tk.Frame(root)
profile_frame.pack(pady=5)
tk.Label(profile_frame, text="Current Profile:").grid(row=0, column=0, padx=4)
profile_selector = ttk.Combobox(profile_frame, width=18, state="readonly")
profile_selector.grid(row=0, column=1, padx=4)
profile_selector.bind("<<ComboboxSelected>>", load_selected_profile)

tk.Label(profile_frame, text="New Profile Name:").grid(row=1, column=0, padx=4)
new_profile_name = tk.Entry(profile_frame, width=20)
new_profile_name.grid(row=1, column=1, padx=4)

tk.Button(profile_frame, text="💾 Save", command=lambda: save_profile(new_profile_name.get().strip())).grid(row=2, column=0, columnspan=2, pady=6)

tk.Button(root, text="🌓 Toggle Theme", command=toggle_theme).pack(pady=4)

# Keypad + Mappings
tk.Label(root, text="Remap Keys", font=("Segoe UI", 11, "bold")).pack(pady=(8, 2))
button_frame = tk.Frame(root)
button_frame.pack()
refresh_layout()

tk.Label(root, text="Key Mappings", font=("Segoe UI", 11, "bold")).pack(pady=(10, 2))
mapping_list = tk.Listbox(root, width=30, height=14, font=("Courier", 10))
mapping_list.pack()
update_mapping_list()
update_profile_list()
profile_selector.set(current_profile)

apply_theme()
threading.Thread(target=listen_serial, daemon=True).start()
root.mainloop()