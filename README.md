# Speech to Image Generator 🎤➡️🖼️

A Streamlit application that converts spoken descriptions into images using Google Cloud Speech-to-Text and Vertex AI's Image Generation Model.

## Features

- 🎤 Audio Recording: Record your voice description directly in the browser
- 🔄 Speech-to-Text: Convert spoken words to text using Google Cloud Speech API
- 🎨 Image Generation: Transform text descriptions into images using Vertex AI
- 📥 Download Options: Save generated images locally
- 🎯 User-Friendly Interface: Clean and intuitive design with step-by-step guidance

## Project Structure

```
speech-to-image-generator/
│
├── app.py                  # Main application file
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
└── generated_images/      # Directory for storing generated images
```

## Dependencies

- streamlit
- google-cloud-speech
- vertexai
- python-uuid
- datetime

## Prerequisites

- Python 3.10
- Google Cloud Platform Account
- Required API Access:
  - Google Cloud Speech-to-Text API
  - Vertex AI API
- Project credentials configured

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kakarlapudiakhilvarma1/Speech-to-Image-Generation-using-Vertex-AI.git
```
```bash
cd Speech-to-Image-Generation-using-Vertex-AI
```
2. Create virtual environment using conda
```bash
conda create -p myenv python==3.10 -y
```
```bash
conda activate myenv/
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Authorize & Initializing the gcloud CLI to use Vertex AI Services:
```bash
https://cloud.google.com/sdk/docs/initializing
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Navigate to the provided local URL (typically http://localhost:8501)

3. Follow the steps in the application:
   - Record your description using the microphone
   - Review the transcribed text
   - Generate the image
   - Download the result if desired

## Screenshots

#### Initial Interface
![image](https://github.com/user-attachments/assets/10c59691-21ea-43e5-af1b-3651c6720145)

#### Recording and Transcription Process
![image](https://github.com/user-attachments/assets/c1d494bd-ea3c-42ea-ba5e-758119966557)

#### After Transcription
![image](https://github.com/user-attachments/assets/dde7e165-1184-4799-bd03-62a9f1325eb9)
---
![image](https://github.com/user-attachments/assets/43115477-e62c-4ca6-b875-e0ab98c5612c)

#### Finally after Image Generation
![image](https://github.com/user-attachments/assets/9b6626d8-218c-4cd2-ade1-ca8e35782300)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Cloud Platform for Speech-to-Text API
- Vertex AI for Image Generation
- Streamlit for the web framework

## Support

For support, please open an issue in the GitHub repository or contact kakarlapudiakhilvarma1@gmail.com
