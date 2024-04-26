import cv2
import os
from PIL import Image as Img

def create_gif(images, output_gif_path, duration=500):
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )


def crop_image(fold_name,img_path):
    os.makedirs(fold_name, exist_ok=True) 
    image = cv2.imread(img_path)
    print(image)
    rows, cols = 2,2
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
            filename = f"{fold_name}/cropped_img_{y}_{x}.jpg"
            pil_image.save(filename)
    return extracted_img

output_gif_path = f"outputs/testcase1.gif"
create_gif(crop_image('extracted_img','test_case\multi_img.png'), output_gif_path)
print(f"GIF created and saved at {output_gif_path}")