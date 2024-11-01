from dotenv import load_dotenv
load_dotenv()

def get_text_length(text:str)->int:
    """text by character"""
    return len(text)
if __name__ == "__main__":
    print("hello")
    print(get_text_length("dog"))