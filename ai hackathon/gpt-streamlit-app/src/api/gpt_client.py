class GPTClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_response(self, user_input):
        if not self.api_key:
            raise ValueError("API key is not set.")
        
        # Here you would typically make a request to the GPT API
        # For example, using requests library:
        # response = requests.post("API_ENDPOINT", headers={"Authorization": f"Bearer {self.api_key}"}, json={"input": user_input})
        # return response.json().get("output")

        # Placeholder for actual API call
        return f"Response for input: {user_input}"  # This is a mock response for demonstration purposes.