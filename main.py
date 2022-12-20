import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math

# Create the main window
root = tk.Tk()
root.title("Image Converter")

# Create a frame to hold the image
image_frame = tk.Frame(root)
image_frame.pack()

# Create a label to display the image
image_label = tk.Label(image_frame)
image_label.pack()
# Create a function to open an image file and display it
def open_image():
  file_path = filedialog.askopenfilename()
  image = Image.open(file_path)
  image = ImageTk.PhotoImage(image)
  image_label.config(image=image)
  image_label.image = image

# Create a button to open an image file
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

# Create a function to convert the image to a normal map
def convert_to_normal_map():
  # Convert the image to grayscale
  grayscale_image = image.convert("L")

  # Create an empty image to hold the normal map
  normal_map = Image.new(image.mode, image.size)

  # Iterate over the pixels in the image
  for x in range(image.width):
    for y in range(image.height):
      # Calculate the normal vector for the pixel at (x, y)
      # using the pixel values of the surrounding pixels
      dx = grayscale_image.getpixel((x+1, y)) - grayscale_image.getpixel((x-1, y))
      dy = grayscale_image.getpixel((x, y+1)) - grayscale_image.getpixel((x, y-1))
      dz = 255
      normal = (dx, dy, dz)

      # Normalize the normal vector
      length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
      normal = (normal[0]/length, normal[1]/length, normal[2]/length)

      # Set the pixel value in the normal map to the normalized normal vector
      normal_map.putpixel((x, y), normal)

  # Display the normal map
  normal_map = ImageTk.PhotoImage(normal_map)
  image_label.config(image=normal_map)
  image_label.image = normal_map

# Create a button to convert the image to a normal map
normal_button = tk.Button(root, text="Convert to Normal Map", command=convert_to_normal_map)
normal_button.pack()
# Create a function to convert the image to a height map
def convert_to_height_map():
  # Convert the image to grayscale
  grayscale_image = image.convert("L")

  # Create an empty image to hold the height map
  height_map = Image.new(image.mode, image.size)

  # Iterate over the pixels in the image
  for x in range(image.width):
    for y in range(image.height):
      # Set the pixel value in the height map to the grayscale value of the pixel
      height_map.putpixel((x, y), grayscale_image.getpixel((x, y)))

  # Display the height map
  height_map = ImageTk.PhotoImage(height_map)
  image_label.config(image=height_map)
  image_label.image = height_map

# Create a button to convert the image to a height map
height_button = tk.Button(root, text="Convert to Height Map", command=convert_to_height_map)
height_button.pack()
normal_button = tk.Button(root, text="Convert to Normal Map", command=convert_to_normal_map)
normal_button.pack()
# Run the main loop
root.mainloop()
