import cv2
import os
from PIL import Image as Img

def create_gif(images, output_gif_path, duration=500):
    # Save as GIF
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0  # 0 means infinite loop
    )

folder_name = "extracted_images"
os.makedirs(folder_name, exist_ok=True) 
img_name = 'output0 (1)'
image = cv2.imread(f'multi_images\{img_name}.png')
rows = 2
cols = 2

width = image.shape[1] // cols
height = image.shape[0] // rows
extracted_img = []

for y in range(rows):
    for x in range(cols):
        start_x = x * width
        start_y = y * height
        end_x = start_x + width
        end_y = start_y + height
        sub_image = image[start_y:end_y, start_x:end_x]
        pil_image = Img.fromarray(cv2.cvtColor(sub_image, cv2.COLOR_BGR2RGB))
        extracted_img.append(pil_image)
        filename = f"{folder_name}/cropped_img_{y}_{x}.jpg"
        pil_image.save(filename)



print(extracted_img)

print(f"Extracted images saved to folder: {folder_name}")
output_gif_path = f"outputs/{img_name}.gif"
# Create GIF
create_gif(extracted_img, output_gif_path)

print(f"GIF created and saved at {output_gif_path}")
