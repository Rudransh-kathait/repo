def load_config():
    import os
    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from a .env file if it exists

    api_key = os.getenv("GPT_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the GPT_API_KEY environment variable.")

    return {
        "api_key": api_key
    }