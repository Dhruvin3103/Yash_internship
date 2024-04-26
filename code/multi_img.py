from gradio_client import Client

client = Client("dylanebert/multi-view-diffusion")
result = client.predict(
		"test_case/download (3).jpg",	# filepath  in 'Image Input' Image component
		"a lady wearing a outfit high quality",	# str  in 'parameter_9' Textbox component
		api_name="/image_to_mv"
)
from PIL import Image
image = Image.open(result)
# plt.imshow(image)
# plt.axis('off')  
# plt.show()
image.save("output_image.png")