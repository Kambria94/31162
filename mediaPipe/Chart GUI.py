import tkinter as tk
from tkinter import font
import colorsys
import random

def save_values():
    # Save the entered values to variables and update the duplicate chart
    for i, label in enumerate(labels):
        value_min = int(entry_values_min[i].get())
        value_max = int(entry_values_max[i].get())

        # Store values in variables
        variable_min[label] = value_min
        variable_max[label] = value_max

        # Update the duplicate chart with the new values
        label_duplicate_min[i].config(text=value_min)
        label_duplicate_max[i].config(text=value_max)

def load_defaults():
    # Load default values into the entry boxes and update the duplicate chart
    for i, label in enumerate(labels):
        saved_value_min = variable_min.get(label, default_values_min[label])
        saved_value_max = variable_max.get(label, default_values_max[label])

        entry_values_min[i].delete(0, tk.END)
        entry_values_min[i].insert(0, saved_value_min)

        entry_values_max[i].delete(0, tk.END)
        entry_values_max[i].insert(0, saved_value_max)

        # Update the duplicate chart with the default values
        label_duplicate_min[i].config(text=default_values_min[label])
        label_duplicate_max[i].config(text=default_values_max[label])

def increase_value(entry):
    # Increase the value in the entry box by 1
    current_value = int(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, str(current_value + 1))

def decrease_value(entry):
    # Decrease the value in the entry box by 1
    current_value = int(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, str(current_value - 1))

# Create the main window
window = tk.Tk()
window.title("PosePerfect Parameters Display")

# Make the window fullscreen
window.attributes("-fullscreen", True)

# Retrieve screen resolution
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Halve the size of the UI
ui_scale_factor = 0.5
window_width = int(screen_width * ui_scale_factor)
window_height = int(screen_height * ui_scale_factor)

# Set the window size limit
window.minsize(width=window_width, height=window_height)

# Randomly select fonts for customization
font_family = "Helvetica Now"

# Styling
font_title = font.Font(family=font_family, size=int(window_width / 40), weight="bold")
font_label = font.Font(family=font_family, size=int(window_width / 50), weight="bold")
font_button = font.Font(family=font_family, size=int(window_width / 50), weight="bold")

# Create a Canvas for the smooth and random gradient background
canvas = tk.Canvas(window, width=screen_width, height=screen_height, highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

# Generate random number of steps for each gradient
num_gradients = 5  # You can adjust the number of gradients
for _ in range(num_gradients):
    num_steps = random.randint(50, 200)  # Randomize the number of steps in each gradient

    # Generate random starting and ending colors for each gradient
    start_color = (random.random(), 1.0, 1.0)  # Random hue, full saturation, full brightness
    end_color = (random.random(), 1.0, 1.0)

    # Convert to RGB format
    start_rgb = [int(c * 255) for c in colorsys.hsv_to_rgb(*start_color)]
    end_rgb = [int(c * 255) for c in colorsys.hsv_to_rgb(*end_color)]

    # Create the gradient
    for i in range(num_steps):
        # Interpolate between start and end colors
        ratio = i / (num_steps - 1)
        current_color = [
            int(start_rgb[j] + ratio * (end_rgb[j] - start_rgb[j])) for j in range(3)
        ]
        color_hex = "#{:02X}{:02X}{:02X}".format(*current_color)

        y0 = int((i / num_steps) * screen_height)
        y1 = int(((i + 1) / num_steps) * screen_height)

        canvas.create_rectangle(0, y0, screen_width, y1, fill=color_hex, outline=color_hex)

# Labels
labels = ["Punch Time", "Elbow Angle", "Shoulder Angle", "Hip/Back Angle", "Left Knee Angle", "Right Knee Angle", "Feet Distance"]

# Default values
default_values_min = {"Punch Time": 1, "Elbow Angle": 2, "Shoulder Angle": 3, "Hip/Back Angle": 4, "Left Knee Angle": 5, "Right Knee Angle": 6, "Feet Distance": 7}
default_values_max = {"Punch Time": 8, "Elbow Angle": 9, "Shoulder Angle": 10, "Hip/Back Angle": 11, "Left Knee Angle": 12, "Right Knee Angle": 13, "Feet Distance": 14}

# Column headers for the original chart (Configure)
tk.Label(window, text="Configure", font=font_title).grid(row=0, column=2, padx=int(window_width / 50), pady=int(window_width / 100), sticky=tk.W)
tk.Label(window, text="Minimum", font=font_label).grid(row=0, column=3, padx=int(window_width / 50), pady=int(window_width / 100), sticky=tk.W)
tk.Label(window, text="Maximum", font=font_label).grid(row=0, column=5, padx=int(window_width / 50), pady=int(window_width / 100), sticky=tk.W)

# Entry widgets for the original chart (Configure)
entry_values_min = []
entry_values_max = []
for i, label in enumerate(labels):
    tk.Label(window, text=label, font=font_label).grid(row=i+1, column=2, padx=int(window_width / 50), pady=int(window_width / 100), sticky=tk.W)

    # Up arrow for increasing value
    up_arrow_min = tk.Button(window, text="⬆", font=font_button, command=lambda i=i: increase_value(entry_values_min[i]))
    up_arrow_min.grid(row=i+1, column=3, padx=int(window_width / 100), pady=int(window_width / 100), sticky=tk.W)

    entry_min = tk.Entry(window, font=font_label)
    entry_min.grid(row=i+1, column=4, padx=int(window_width / 50), pady=int(window_width / 100))
    entry_values_min.append(entry_min)

    # Down arrow for decreasing value
    down_arrow_min = tk.Button(window, text="⬇", font=font_button, command=lambda i=i: decrease_value(entry_values_min[i]))
    down_arrow_min.grid(row=i+1, column=4, padx=int(window_width / 100), pady=int(window_width / 100), sticky=tk.E)

    # Up arrow for increasing value
    up_arrow_max = tk.Button(window, text="⬆", font=font_button, command=lambda i=i: increase_value(entry_values_max[i]))
    up_arrow_max.grid(row=i+1, column=5, padx=int(window_width / 100), pady=int(window_width / 100), sticky=tk.W)

    entry_max = tk.Entry(window, font=font_label)
    entry_max.grid(row=i+1, column=6, padx=int(window_width / 50), pady=int(window_width / 100))
    entry_values_max.append(entry_max)

    # Down arrow for decreasing value
    down_arrow_max = tk.Button(window, text="⬇", font=font_button, command=lambda i=i: decrease_value(entry_values_max[i]))
    down_arrow_max.grid(row=i+1, column=6, padx=int(window_width / 100), pady=int(window_width / 100), sticky=tk.E)

# Save button
save_button = tk.Button(window, text="Save", font=font_button, command=save_values)
save_button.grid(row=len(labels)+1, column=4, pady=int(window_width / 50))

# Load Defaults button
load_defaults_button = tk.Button(window, text="Load Defaults", font=font_button, command=load_defaults)
load_defaults_button.grid(row=len(labels)+1, column=5, pady=int(window_width / 50))

# Variables to store values for the original chart (Configure)
variable_min = {}
variable_max = {}

# Separator between the charts
tk.Label(window, text="").grid(row=0, column=7)

# Column headers for the duplicate chart (Preset Default)
tk.Label(window, text="Preset Default", font=font_title).grid(row=0, column=8, padx=int(window_width / 50), pady=int(window_width / 100), sticky=tk.W)
tk.Label(window, text="Minimum", font=font_label).grid(row=0, column=9, padx=int(window_width / 50), pady=int(window_width / 100), sticky=tk.W)
tk.Label(window, text="Maximum", font=font_label).grid(row=0, column=10, padx=int(window_width / 50), pady=int(window_width / 100), sticky=tk.W)

# Labels for the duplicate chart (Preset Default)
label_duplicate_min = []
label_duplicate_max = []
for i, label in enumerate(labels):
    tk.Label(window, text=label, font=font_label).grid(row=i+1, column=8, padx=int(window_width / 50), pady=int(window_width / 100), sticky=tk.W)

    label_min = tk.Label(window, text=default_values_min[label], font=font_label)
    label_min.grid(row=i+1, column=9, padx=int(window_width / 50), pady=int(window_width / 100))
    label_duplicate_min.append(label_min)

    label_max = tk.Label(window, text=default_values_max[label], font=font_label)
    label_max.grid(row=i+1, column=10, padx=int(window_width / 50), pady=int(window_width / 100))
    label_duplicate_max.append(label_max)

# GO! button
go_button = tk.Button(window, text="GO!", font=font_button, command=window.destroy)
go_button.grid(row=len(labels)+1, column=8, columnspan=3, pady=int(window_width / 50))

# Run the main loop
window.mainloop()
