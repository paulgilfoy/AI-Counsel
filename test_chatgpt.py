from chatgpt import ChatGPT

def main():
    # Initialize ChatGPT
    chat = ChatGPT()
    
    # Send a hello world message
    response = chat.get_response("Hello, world! Please respond with a greeting.")
    print("Response:", response)

if __name__ == "__main__":
    main() 