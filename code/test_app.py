import streamlit as st
import replicate
from PIL import Image
import requests
from io import BytesIO
import tempfile

# Set page title
st.set_page_config(page_title="SOTA VTON")

# Title
st.title("State Of The Art VTON")

# Sidebar
with st.sidebar:
    # Image input fields
    garment_image = st.file_uploader("Garment Image", type=["jpg", "png", "jpeg"])
    model_image = st.file_uploader("Model Image", type=["jpg", "png", "jpeg"])

    # Radio button for category selection
    category = st.radio("Select Category", ["upper_body", "lower_body", "dresses"])

    # Text input box for garment description
    garment_description = st.text_input("Garment Description")

    # Run button
    run_button = st.button("Run")

# Output area
output_area = st.empty()

# Display uploaded garment image
if garment_image:
    col1, col2 = st.columns(2)
    with col1:
        st.image(garment_image, caption="Garment Image", use_column_width=True)

# Display uploaded model image
if model_image:
    if 'col1' not in locals() or 'col2' not in locals():
        col1, col2 = st.columns(2)
    with col2:
        st.image(model_image, caption="Model Image", use_column_width=True)

# Run the Replicate API when the run button is clicked
if run_button and garment_image and model_image:
    with st.spinner("Running the model..."):
        # Save garment image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_garment_img:
            tmp_garment_img.write(garment_image.read())
            garment_img_path = tmp_garment_img.name

        # Save model image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_model_img:
            tmp_model_img.write(model_image.read())
            model_img_path = tmp_model_img.name

        output = replicate.run(
            "cuuupid/idm-vton:5c6712b51ff45af53bba0e88d4a5ec33fad0a85de32462e3d3cbcf51b53d5d37",
            input={
                "seed": 42,
                "steps": 30,
                "category": category,
                "garm_img": open(garment_img_path, "rb"),
                "human_img": open(model_img_path, "rb"),
                "garment_des": garment_description,
            },
        )

        # Display output image
        output_area.image(output, use_column_width=True, caption="Output Image")
