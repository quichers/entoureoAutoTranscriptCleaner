from hugchat import hugchat
from hugchat.login import Login
from requests.cookies import RequestsCookieJar


class TextSmootherRepository:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def login(self) -> RequestsCookieJar:
        sign = Login(self.username, self.password)
        cookies = sign.login()
        cookie_path_dir = "./cookies_snapshot"
        sign.saveCookiesToDir(cookie_path_dir)
        return cookies
    

    def get_transcript(self, original_texts: list[str], preprompt: str) -> list[str]:
        cookies = self.login()
        
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        
        chatbot.chat(preprompt)

        results = []
        for text in original_texts:
            results.append(chatbot.chat(text))
        return results
    
    
    def start_conversation(self):
        if not self.username or not self.password:
            print(
                f"Found {self.username} for username and {self.password} for password. Need to set them in the .env file"
            )
            return

        sign = Login(self.username, self.password)
        cookies = sign.login()
        cookie_path_dir = "./cookies_snapshot"
        sign.saveCookiesToDir(cookie_path_dir)
        
        # Create a chatbot connection
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

        # New a conversation (ignore error)
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)

        # Intro message
        print("[[ Welcome to ChatPAL. Let's talk! ]]")
        print("'q' or 'quit' to exit")
        print("'c' or 'change' to change conversation")
        print("'n' or 'new' to start a new conversation")

        while True:
            user_input = input("> ")
            if user_input.lower() == "":
                pass
            elif user_input.lower() in ["q", "quit"]:
                break
            elif user_input.lower() in ["c", "change"]:
                print("Choose a conversation to switch to:")
                print(chatbot.get_conversation_list())
            elif user_input.lower() in ["n", "new"]:
                print("Clean slate!")
                id = chatbot.new_conversation()
                chatbot.change_conversation(id)
            else:
                print(chatbot.chat(user_input))
