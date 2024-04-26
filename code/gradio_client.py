from gradio_client import Client

client = Client("dylanebert/multi-view-diffusion")
result = client.predict(
		"/download (3).jpg",	# filepath  in 'Image Input' Image component
		"Hello!!",	# str  in 'parameter_9' Textbox component
		api_name="/image_to_mv"
)