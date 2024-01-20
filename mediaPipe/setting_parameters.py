import tkinter as tk
import PIL.ImageTk as ImageTk
import PIL.Image as Image

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
#fg_color_str = "yellow2"
fg_color_str = "Gold2"
bg_color_str = "MediumOrchid4"
window.configure(bg=bg_color_str)
window.title("Pose Perfect - Set Parameters")

# Labels and initial values
labels = ["Elbow Angle (deg)", "Hip/Back Angle (deg)", "Left Knee Angle (deg)", "Right Knee Angle (deg)", "Heel Distance to Leg length Ratio"]
min_values = [165, 0, 148, 161, 0.455]
max_values = [180, 180, 162, 172, 0.909]

label_font_str = 'Helvetica 12 bold'
# Header row
image = Image.open("pose_perfect.png")
image = image.resize((116, 30), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)
tk.Label(window, image=photo).grid(row=0, column=1, padx=10, pady=10)

tk.Label(window, text="Parameter", font=label_font_str, fg=fg_color_str, bg=bg_color_str).grid(row=1, column=0, pady=10)
tk.Label(window, text="Minimum", font=label_font_str, fg=fg_color_str, bg=bg_color_str).grid(row=1, column=1, pady=10)
tk.Label(window, text="Maximum", font=label_font_str, fg=fg_color_str, bg=bg_color_str).grid(row=1, column=2, pady=10)
header_count = 2
# Create and place labels and entry widgets
entries = []
for label, min_value, max_value in zip(labels, min_values, max_values):
    tk.Label(window, text=label, font=label_font_str, fg=fg_color_str, bg=bg_color_str).grid(row=len(entries)+header_count, column=0, sticky="e")
    entry = tk.Entry(window)
    entry.insert(0, str(min_value))
    entry.grid(row=len(entries)+header_count, column=1, sticky="w")
    entry2 = tk.Entry(window)
    entry2.insert(0, str(max_value))
    entry2.grid(row=len(entries)+header_count, column=2, sticky="w")
    entries.append((entry, entry2))

# Button to save values
save_button = tk.Button(window, text="Save Configuration", command=save_values)
save_button.grid(row=len(entries)+2, columnspan=3, pady=20)

# Start the main loop
window.mainloop()
