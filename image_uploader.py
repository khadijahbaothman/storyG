import streamlit as st
import os
import requests
from openai import OpenAI

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
HEADERS = {"Authorization": "Bearer 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"}
client = openai.OpenAI(api_key="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")


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

    st.header("The Story:")
    prompt = "tell me a story aout makkah city and add this event"+captions+"then translated into arabic"
    # After each call, append the prompt and response to 'messages' to keep track of the conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi!"},
        {"role": "user", "content": prompt}
    ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  
    st.write(completion.choices[0].message.content)

if __name__ == "__main__":
    main()

