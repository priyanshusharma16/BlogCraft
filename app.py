import streamlit as st
import os
import google.generativeai as genai
from apikey import google_gemini_api_key    

genai.configure(api_key=google_gemini_api_key)   

# Create the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

# Setting up our model
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config
)

# Set the app to wide mode
st.set_page_config(layout="wide")

# Title of our app
st.title('BlogCraft: Your AI Writing Companion')

# Create a subheader
st.subheader("Now you can craft perfect blogs with the help of AI - BlogCraft is your new AI Blog Companion")

# Subheader for user input
with st.sidebar:
    st.title("Input your blog details")
    st.subheader("Enter details of the Blog you want to generate")
    
    # Blog title
    blog_title = st.text_input("Blog Title")
    
    # Keywords input
    keywords = st.text_area("Keywords (comma-separated)") 
    
    # Number of words
    num_words = st.slider("Number of Words", min_value=100, max_value=5000, step=250)
    
    
    # Submit button
    submit_button = st.button("Generate Blog")

# Main logic: Generate the blog when the button is clicked
if submit_button and blog_title and keywords:
    # Create the input message for the model
    input_message = (
        f'Generate a comprehensive, engaging blog post relevant to the given title "{blog_title}" '
        f'and keywords "{keywords}". Make sure to incorporate these keywords in the blog post. '
        f'The blog should be approximately {num_words} words in length, suitable for an online audience. '
        'Ensure the content is original, informative, and maintains a consistent tone throughout.'
    )
    
    # Start the chat session to generate the blog
    chat_session = model.start_chat(history=[])  # Start with an empty history
    
    try:
        # The model responds with the generated blog
        response = chat_session.send_message(input_message)
        generated_blog = response.text

        # Display the generated blog in the app
        st.header(f'Generated Blog: {blog_title}')
        st.write(generated_blog)
        
        # Optionally, save the blog to a text file
        if st.button("Download Blog"):
            with open(f"{blog_title}.txt", "w") as f:
                f.write(generated_blog)
            st.success(f"Blog saved as {blog_title}.txt")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        generated_blog = "Failed to generate blog due to an internal error."
else:
    st.warning("Please fill in the blog title and keywords before generating the blog.")
