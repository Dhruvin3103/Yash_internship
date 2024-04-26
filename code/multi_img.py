import streamlit as st
from gradio_client import Client
from PIL import Image
from io import BytesIO
import io
import cloudinary.uploader
from decouple import config

class MultiViewDiffusionModel:
    def __init__(self):
        self.client = Client("dylanebert/multi-view-diffusion")
    def make_prediction(self, image_url, text_input):
        result = self.client.predict(image_url, text_input, api_name="/image_to_mv")
        output_image = Image.open(result)
        return output_image
 
def main():
    st.title("Multi-View Diffusion App")
    model = MultiViewDiffusionModel()
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        cloudinary.config( 
			cloud_name = config('CLOUD_NAME'), 
			api_key = config('API_KEY'), 
			api_secret = config('API_SECRET')
		)
        upload_result = cloudinary.uploader.upload(uploaded_image)
        print(upload_result)
        text_input = st.text_input("Description")

        if st.button("Generate Output"):
            if text_input:
                image_url = upload_result["secure_url"]
                output_image = model.make_prediction(image_url, text_input)
                st.image(output_image, caption="Output Image", use_column_width=True)
            else:
                st.warning("Please provide a description.")
    else:
        st.warning("Please upload an image.")


if __name__ == "__main__":
    main()
