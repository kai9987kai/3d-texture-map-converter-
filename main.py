import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Set up the Tkinter window
window = tk.Tk()
window.title("Texture Map Converter")

# Set up the input image
input_image = None
input_image_tk = None

# Set up the output image
output_image = Image.new("RGB", (300, 300), (255, 255, 255))
output_image_tk = ImageTk.PhotoImage(output_image)

# Add the input and output images to the Tkinter window
input_label = tk.Label(window, image=input_image_tk)
input_label.pack(side="left")
output_label = tk.Label(window, image=output_image_tk)
output_label.pack(side="right")

# Set up the file dialog button
def open_file_dialog():
    # Open the file dialog and get the selected file
    filepath = filedialog.askopenfilename()
    # Load the selected file as the input image
    global input_image
    input_image = Image.open(filepath)
    input_image = input_image.resize((300, 300), Image.ANTIALIAS)
    global input_image_tk
    input_image_tk = ImageTk.PhotoImage(input_image)
    # Update the input image in the Tkinter window
    input_label.configure(image=input_image_tk)

file_dialog_button = tk.Button(window, text="Select Input Image", command=open_file_dialog)
file_dialog_button.pack(side="top")

# Set up the conversion buttons
def normal_map():
    # Convert the input image to a normal map
    output_image = input_image.convert("RGB")
    # Update the output image in the Tkinter window
    output_image_tk.paste(output_image)
    output_label.configure(image=output_image_tk)

def height_map():
    # Convert the input image to a height map
    output_image = input_image.convert("L")
    # Update the output image in the Tkinter window
    output_image_tk.paste(output_image)
    output_label.configure(image=output_image_tk)

normal_button = tk.Button(window, text="Normal Map", command=normal_map)
normal_button.pack(side="bottom")
height_button = tk.Button(window, text="Height Map", command=height_map)
height_button.pack(side="bottom")

# Run the Tkinter loop
window.mainloop()
