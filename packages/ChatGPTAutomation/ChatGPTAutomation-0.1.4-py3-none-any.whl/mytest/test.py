from chatgpt_automation.chatgpt_automation import ChatGPTAutomation

# Initialize with path to Chrome and ChromeDriver
chat_bot = ChatGPTAutomation(chrome_path="C:\Program Files\Google\Chrome\Application\chrome.exe", chrome_driver_path="C:\Program Files (x86)\chromedriver.exe")

chat_bot.send_prompt_to_chatgpt("Hello World")
import time

time.sleep(4)

chat_bot.send_prompt_to_chatgpt("Hello world")


all_responses = chat_bot.return_chatgpt_conversation()

print(all_responses)