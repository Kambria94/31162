import tkinter as tk

def save_values():
    # Function to save the entered values
    # elbow_angle_value = elbow_entry.get()
    print("Writing out configuration")
    file1 = open('parameters.txt', 'w')
    counter = 0
    for line in entries:
        line_str = labels[counter]+','+ str(line[0].get())+','+str(line[1].get())
        print(line_str)
        file1.write(line_str+"\n")
        counter += 1
    window.destroy()
    

# Create the main window
window = tk.Tk()
window.title("Pose Perfect - Set Parameters")

# Labels and initial values
labels = ["Elbow Angle", "Hip/Back Angle", "Left Knee Angle", "Right Knee Angle", "Heel Distance (Leg to length ratio)"]
min_values = [165, 0, 148, 161, 0.455]
max_values = [180, 180, 162, 172, 0.909]

label_font_str = 'Helvetica 12 bold'
# Header row
tk.Label(window, text="Configure", font=label_font_str).grid(row=0, column=0, pady=10)
tk.Label(window, text="Minimum", font=label_font_str).grid(row=0, column=1, pady=10)
tk.Label(window, text="Maximum", font=label_font_str).grid(row=0, column=2, pady=10)

# Create and place labels and entry widgets
entries = []
for label, min_value, max_value in zip(labels, min_values, max_values):
    tk.Label(window, text=label, font=label_font_str).grid(row=len(entries)+1, column=0, sticky="e")
    entry = tk.Entry(window)
    entry.insert(0, str(min_value))
    entry.grid(row=len(entries)+1, column=1, sticky="w")
    entry2 = tk.Entry(window)
    entry2.insert(0, str(max_value))
    entry2.grid(row=len(entries)+1, column=2, sticky="w")
    entries.append((entry, entry2))

# Button to save values
save_button = tk.Button(window, text="Save Configuration", command=save_values)
save_button.grid(row=len(entries)+2, columnspan=3, pady=20)

# Start the main loop
window.mainloop()
