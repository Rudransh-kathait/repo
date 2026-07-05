# gpt-streamlit-app

## Overview
This project is a Streamlit application that integrates GPT functionality to provide users with AI-generated responses based on their input. The application leverages the OpenAI GPT API to generate text responses, making it a powerful tool for various applications such as chatbots, content generation, and more.

## Project Structure
```
gpt-streamlit-app
├── src
│   ├── gemini.py          # Main entry point for the Streamlit app
│   ├── api
│   │   └── gpt_client.py  # Contains the GPTClient class for API interaction
│   ├── ui
│   │   └── components.py   # UI components for the Streamlit app
│   └── utils
│       └── config.py      # Configuration settings and API key management
├── tests
│   └── test_gpt_client.py  # Unit tests for the GPTClient class
├── .env.example            # Example environment variables
├── .gitignore              # Files and directories to ignore in version control
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd gpt-streamlit-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and add your API key:
     ```
     API_KEY=your_api_key_here
     ```

## Usage
To run the Streamlit application, execute the following command:
```
streamlit run src/gemini.py
```

## GPT Integration
The application uses the `GPTClient` class from `src/api/gpt_client.py` to interact with the GPT API. Users can input text, and the application will return AI-generated responses.

## Testing
To run the unit tests for the `GPTClient` class, use:
```
pytest tests/test_gpt_client.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.