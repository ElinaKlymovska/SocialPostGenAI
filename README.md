# AI Social Media Text Generator with Corrections

## Overview
This project is an AI-powered application designed to generate and refine creative social media texts. It leverages **Amazon Bedrock** for text generation, **AWS Rekognition** for image-based keyword extraction, and **Streamlit** for a user-friendly interface. The app allows users to iteratively refine generated texts with multi-turn conversations.

---

## Features

### 🎯 **Key Features**
1. **Multi-turn Conversation Support**
   - Uses Amazon Bedrock's **Converse API** to enable iterative refinement of social media texts.

2. **Image Analysis for Keyword Extraction**
   - Extracts relevant keywords from uploaded images using **AWS Rekognition**.

3. **Prompt Optimization**
   - Supports multiple languages: **English**, **Ukrainian**, **Polish**, and **Italian**.
   - Offers tone options: **Friendly**, **Formal**, **Neutral**, and **Creative**.

4. **Real-time Corrections**
   - Allows users to edit generated text and resubmit it for further refinement.

5. **Streamlined Interface**
   - Provides a simple and intuitive interface using **Streamlit**.

6. **Error Handling and Logging**
   - Includes detailed logs for debugging API requests.
   - Implements error handling for conversation role alternation and Bedrock API responses.

---

## Installation

### Prerequisites
- Python 3.8+
- AWS account with access to **Amazon Bedrock** and **AWS Rekognition**

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ElinaKlymovska/SocialPostGenAI.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials:**
   Ensure your `~/.aws/credentials` file contains:
   ```plaintext
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   region = us-east-1
   ```

4. **Run the application:**
   ```bash
   streamlit run app/main.py
   ```

---

## Usage

1. **Upload an Image**
   - The app extracts keywords from the image using **AWS Rekognition**.

2. **Set Language and Tone**
   - Choose from supported languages: English, Ukrainian, Polish, or Italian.
   - Select a tone: Friendly, Formal, Neutral, or Creative.

3. **Generate Text**
   - The app generates text using Amazon Bedrock's Converse API.

4. **Edit and Refine**
   - Modify the generated text in the app and resubmit it for further refinements.

---

## Technologies Used
- **Amazon Bedrock:** Text generation via Titan models.
- **AWS Rekognition:** Keyword extraction from images.
- **Streamlit:** Web application framework.
- **Python:** Core development language.
- **Deep Translator:** Language translation for prompt optimization.

---

## Folder Structure
```plaintext
.
├── app/
│   ├── main.py          # Main Streamlit app
│   ├── utils.py         # Utility functions for Bedrock and Rekognition
│   └── prepare_prompt.py # Prompt preparation and language translation
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Contributing
Contributions are welcome! Please fork the repository, create a new branch for your feature, and submit a pull request.

---


---

## Acknowledgments
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) for advanced generative AI models.
- [AWS Rekognition](https://aws.amazon.com/rekognition/) for image analysis.
- [Streamlit](https://streamlit.io/) for providing a seamless UI experience.

