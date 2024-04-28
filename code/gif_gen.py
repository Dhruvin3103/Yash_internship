import cv2
from PIL import Image as Img
from io import BytesIO
import replicate
from decouple import config
import cloudinary.uploader
import requests

# replicate = replicate.Client(api_token=config('REPLICATE_API_TOKEN'))
cloudinary.config( 
			cloud_name = config('CLOUD_NAME'), 
			api_key = config('API_KEY'), 
			api_secret = config('API_SECRET')
		)
def enhance(img):
    print(img)
    print('running','gif wala ')
    output = replicate.run(
        "batouresearch/magic-image-refiner:507ddf6f977a7e30e46c0daefd30de7d563c72322f9e4cf7cbac52ef0f667b13",
        input={
                "hdr": 1,
                "image": img,
                "steps": 30,
                "prompt": "a fashion model posing for a photoshoot",
                "scheduler": "K_EULER_ANCESTRAL",
                "creativity": 0.40,
                "guess_mode": False,
                "resolution": "2048",
                "resemblance": 0.70,
                "guidance_scale": 7,
                "negative_prompt": "ugly face , malformed hands,teeth, tooth, open mouth, longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, mutant"
            }
    )
    print(output[0],'enhance wala ')
    return output[0]

def create_gif(image_path, duration=500):
    print('okey dokey : )')
    upload_result = cloudinary.uploader.upload(image_path)["secure_url"]
    image_path = enhance(upload_result)
    # image_data = response.content  
    images = crop_image(image_path)
    # images = crop_image(upload_result)
    gif_bytes = BytesIO()
    images[0].save(
        gif_bytes,
        format='GIF',
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    gif_bytes.seek(0)
    with open('output3.gif', 'wb') as f:
        f.write(gif_bytes.getvalue())
    return gif_bytes.getvalue()
    
    
def crop_image(image_url):
    # Load the image using PIL
    response = requests.get(image_url, stream=True)
    image = Img.open(response.raw)
    
    # Get dimensions of the image
    width, height = image.size
    
    # Define rows and columns for cropping
    rows, cols = 2, 3 
    
    # Calculate the width and height of each sub-image
    sub_width = width // cols
    sub_height = height // rows
    
    extracted_img = []
    
    # Iterate over each row and column
    for y in range(rows):
        for x in range(cols):
            # Calculate coordinates for cropping
            left = x * sub_width
            upper = y * sub_height
            right = left + sub_width
            lower = upper + sub_height
            
            # Crop the image
            sub_image = image.crop((left, upper, right, lower))
            
            # Append the cropped image to the list
            extracted_img.append(sub_image)
    
    return extracted_img


# def crop_image(image):
#     image = Img.open(requests.get('https://replicate.delivery/pbxt/LNlaHFaMILrOG9OHL5PZKJJFPZZhiMlpPbqIAwPZa7F71krE/out-0.png', stream=True).raw)
#     print(type(image),image)
#     # image = cv2.imread(image)
#     width, height = image.size
    
#     # Define rows and columns for cropping
#     rows, cols = 2, 2
#     # Calculate the width and height of each sub-image
#     sub_width = width // cols
#     sub_height = height // rows
#     extracted_img = []
#     for y in range(rows):
#         for x in range(cols):
#             start_x = x * sub_width
#             start_y = y * sub_height
#             end_x = start_x + sub_width
#             end_y = start_y + sub_height
#             sub_image = image.crop((left, upper, right, lower))
#             pil_image = Img.fromarray(cv2.cvtColor(sub_image, cv2.COLOR_BGR2RGB))
#             extracted_img.append(pil_image)
#     return extracted_img

# output_gif = create_gif('test_case/image.png')


# st.image(output_gif_bytes, caption="Output GIF")
# Now you have the GIF in output_gif variable, you can use it as needed.
