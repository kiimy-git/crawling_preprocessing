from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openai
import re, time

MAX_HISTORY = 10
MODEL = "gpt-3.5-turbo" # (gpt-3.5-turbo, gpt-4)

# os.environ["OPENAI_API_KEY"] = "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"
openai.api_type = "azure"
openai.api_base = "https://{resource-name}.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "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"

"""
Selenium 크롤링 할 때, 현재 창에서 크롤링하는 방법(Debugging Mode)
https://melonicedlatte.com/2023/01/01/193400.html

## 실행창
C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
"""
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(executable_path= r"C:\Users\yhunkim\Downloads\chromedriver_win32 (2)\chromedriver.exe", options=options)

driver.get("https://nutty.chat/channels")

driver.implicitly_wait(2)

# # Join chatroom
# driver.find_element(By.XPATH, "//*[@id='nutty']/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]")
driver.find_element(By.XPATH, "//*[@id='nutty']/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div[2]/img").click()
# time.sleep(3)
driver.implicitly_wait(3)

messages = [{
    "role": "system",
    "content": (
        "너는 나의 가장 친한 친구야. 현재 채팅방에서 채팅중이야. 아래 규칙을 반드시 지키면서 대답해야 해.\n"
        "1. 할 말이 없거나 지루하다 싶을 때는 농담을 던지거나 궁금한 것을 먼저 물어본다.\n"
        "2. 네가 이미 말했던 비슷한 의미의 대답을 반복하지 않는다.\n"
        "3. 반드시 반말로 대답한다.\n"
        "4. 너무 길게 말하지 않는다."
    )
}]
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
while True:
    try:
        # Get the last text (REPLACE CLASS NAMES of yours)
        xpath = "//div[@class='css-1rynq56 r-ubezar r-16dba41 r-oam9g7 r-1aittka r-cqee49']"
        luda_texts = driver.find_elements(By.XPATH, f"{xpath}")

        # Retrieve last 5 messages we missed
        for i, luda_text in enumerate(reversed(luda_texts[:5])):
            luda_text = luda_text.text.strip()

            if luda_text:
                is_text_exist = False

                for message in messages:
                    if luda_text in message.values():
                        is_text_exist = True
                        break

                if not is_text_exist:
                    messages.append({
                        "role": "user",
                        "content": luda_text
                    })
                    print(f"🙆🏻‍♀️이루다: {luda_text}")

        # Remove old messages, but keep system message
        if len(messages) > MAX_HISTORY:
            messages = messages[0:1] + messages[-10:]

        # ChatCompletion
        res = openai.Completion.create(

            engine=MODEL,
            messages=messages)
        
        gpt_text = res["choices"][0]["message"]["content"]

        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)
        gpt_text = emoji_pattern.sub(r'', gpt_text) # no emoji

        print(f"🤖ChatGPT: {gpt_text}")

        input_box = driver.find_element(By.XPATH, "//textarea")

        time.sleep(1)
        input_box.send_keys(gpt_text) # Cannot send emojis in Chrome
        time.sleep(1)
        input_box.send_keys(Keys.ENTER) # Enter

        messages.append({
            "role": "assistant", # ChatGPT
            "content": gpt_text
        })
    except Exception as e:
        print(e, "ERRRRRRRR")
    finally:
        time.sleep(10)