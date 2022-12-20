import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

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

def smooth_gaussian(image, sigma=1.0):
    # Create the Gaussian kernel
    size = int(6 * sigma + 1)
    kernel = np.zeros((size, size))
    center = size // 2
    for i in range(size):
        for j in range(size):
            kernel[i, j] = np.exp(-((i - center) ** 2 + (j - center) ** 2) / (2 * sigma ** 2))
    kernel /= kernel.sum()
    # Convolve the image with the kernel
    image_smooth = np.zeros_like(image)
    for i in range(1, image.shape[0] - 1):
        for j in range(1, image.shape[1] - 1):
            image_smooth[i, j] = (image[i-1:i+2, j-1:j+2] * kernel).sum()
    return image_smooth
def gradient(image):
    # Compute the gradient in the x-direction
    gradient_x = np.zeros_like(image)
    gradient_x[:, :-1] = image[:, 1:] - image[:, :-1]
    # Compute the gradient in the y-direction
    gradient_y = np.zeros_like(image)
    gradient_y[:-1, :] = image[1:, :] - image[:-1, :]
    return gradient_x, gradient_y
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
    # Convert the input image to grayscale
    input_image_gray = input_image.convert("L")
    # Apply Gaussian smoothing to the input image
    im_smooth = smooth_gaussian(np.array(input_image_gray), sigma=5)
    # Compute the gradient of the input image
    gradient_x, gradient_y = gradient(im_smooth)
    # Generate the normal map from the gradient
    normal_map = compute_normal_map(gradient_x, gradient_y)
    # Convert the normal map to an image
    output_image = Image.fromarray((normal_map * 255).astype(np.uint8))
    # Update the output image in the Tkinter window
    output_image_tk.paste(output_image)
    output_label.configure(image=output_image_tk)
def normal_map():
    # Convert the input image to grayscale
    input_image_gray = input_image.convert("L")
    # Apply Gaussian smoothing to the input image
    im_smooth = smooth_gaussian(np.array(input_image_gray), sigma=5)
    # Compute the gradient of the input image
    gradient_x, gradient_y = gradient(im_smooth)
    # Generate the normal map from the gradient
    normal_map = compute_normal_map(gradient_x, gradient_y)
    # Convert the normal map to an image
    output_image = Image.fromarray((normal_map * 255).astype(np.uint8))
    # Update the output image in the Tkinter window
    output_image_tk.paste(output_image)
    output_label.configure(image=output_image_tk)


file_dialog_button = tk.Button(window, text="Select Input Image", command=open_file_dialog)
file_dialog_button.pack(side="top")

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
