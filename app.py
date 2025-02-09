import vertexai
import streamlit as st
from google.cloud import speech
from vertexai.preview.vision_models import ImageGenerationModel
import os
import uuid
from datetime import datetime

# Initialize configuration
PROJECT_ID = "vital-cedar-443204-f3"
LOCATION = "us-central1"
IMAGE_FOLDER = "generated_images"

# Create the images directory if it doesn't exist
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Initialize session states
if 'step' not in st.session_state:
    st.session_state.step = 'audio_input'
if 'is_transcribing' not in st.session_state:
    st.session_state.is_transcribing = False
if 'audio_processed' not in st.session_state:
    st.session_state.audio_processed = False

def generate_unique_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"image_{timestamp}_{unique_id}.png"

def transcribe_audio(audio_bytes):
    try:
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=audio_bytes)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=48000,
            language_code="en-US",
            model="default"
        )
        
        response = client.recognize(config=config, audio=audio)
        
        if response and response.results and len(response.results) > 0:
            return response.results[0].alternatives[0].transcript
        return None
    except Exception as e:
        st.sidebar.error(f"Transcription error: {str(e)}")
        return None

def generate_image(prompt):
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="1:1"
        )
        
        filename = generate_unique_filename()
        output_file_path = os.path.join(IMAGE_FOLDER, filename)
        response[0].save(location=output_file_path)
        return output_file_path
        
    except Exception as e:
        st.error(f"Image generation error: {str(e)}")
        return None

def reset_flow():
    st.session_state.step = 'audio_input'
    st.session_state.is_transcribing = False
    st.session_state.audio_processed = False
    if 'transcript' in st.session_state:
        del st.session_state.transcript
    if 'current_image' in st.session_state:
        del st.session_state.current_image

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Speech to Image Generator",
        layout="wide"
    )

    # Sidebar
    with st.sidebar:
        st.title("Controls")
        st.markdown("---")
        
        # Audio Input Section
        st.subheader("🎤 Audio Input")
        audio_file = st.audio_input("Record your description", disabled=st.session_state.audio_processed)
        
        if audio_file is not None and not st.session_state.audio_processed:
            try:
                audio_bytes = audio_file.read()
                if len(audio_bytes) > 0 and not st.session_state.is_transcribing:
                    st.session_state.is_transcribing = True
                    with st.status("Transcribing audio..."):
                        transcript = transcribe_audio(audio_bytes)
                        if transcript:
                            st.session_state.transcript = transcript
                            st.session_state.step = 'show_transcript'
                            st.session_state.audio_processed = True
                            st.session_state.is_transcribing = False
                            st.rerun()
            except Exception as e:
                st.error(f"Error processing audio: {str(e)}")
                st.session_state.is_transcribing = False
        
        # Display transcript if available
        if hasattr(st.session_state, 'transcript'):
            st.markdown("---")
            st.subheader("📝 Transcript")
            st.write(st.session_state.transcript)
            if st.button("🎨 Generate Image", type="primary"):
                with st.status("Creating your image..."):
                    image_path = generate_image(st.session_state.transcript)
                    if image_path:
                        st.session_state.current_image = image_path
                        st.session_state.step = 'show_image'
                        st.rerun()
        
        # Reset button
        st.markdown("---")
        if st.button("🔄 Start Over"):
            reset_flow()
            st.rerun()

    # Main content area
    st.title("Speech to Image Generator")
    st.markdown("Transform your words into images using AI")
    
    # Main content container
    main_container = st.container(border=True)
    with main_container:
        if st.session_state.step == 'audio_input':
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("""
                    ### 👋 Welcome!
                    1. Use the sidebar to record your description
                    2. Review the transcript
                    3. Generate your image
                    """)
        
        elif st.session_state.step == 'show_image':
            if hasattr(st.session_state, 'current_image') and os.path.exists(st.session_state.current_image):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(st.session_state.current_image, use_container_width=True)
                    
                    # Download button container
                    download_container = st.container(border=True)
                    with download_container:
                        st.markdown("#### Download Options")
                        with open(st.session_state.current_image, "rb") as file:
                            st.download_button(
                                "⬇️ Download Image",
                                file,
                                file_name=os.path.basename(st.session_state.current_image),
                                mime="image/png",
                                type="primary"
                            )

if __name__ == "__main__":
    main()
