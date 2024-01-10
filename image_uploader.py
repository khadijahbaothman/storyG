import streamlit as st
import os
import requests


API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
HEADERS = {"Authorization": "Bearer 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"}



def query_caption(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=HEADERS, data=data)
    print(response.json())
    return response.json()

def main():
    st.title("Abaad Story")

    uploaded_images = st.file_uploader("Upload up to 10 images", accept_multiple_files=True, key="fileuploader")

    captions = []

    if uploaded_images is not None and len(uploaded_images) > 0:
        st.header("Uploaded Images:")
        save_folder = "uploaded_images"

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        for i, image in enumerate(uploaded_images):
            image_path = os.path.join(save_folder, f"image_{i}.png")
            with open(image_path, "wb") as f:
                f.write(image.read())
            
            st.image(image, caption=f"Image {i + 1}")

            # Get caption using the API
            output = query_caption(image_path)
            
            captions.append(output[0]['generated_text'])
          

    st.header("Image Captions:")
    for i, caption in enumerate(captions):
        st.write(f"Image {i + 1}: {caption}")

if __name__ == "__main__":
    main()

