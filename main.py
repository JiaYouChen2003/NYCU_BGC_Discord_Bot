import discord
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

INSTAGRAM_URL = 'https://www.instagram.com/nycubgc/'

# client connects to Discord, intents specify bot permissions
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def getDriverByURL(url=None, sleep_time=10):
    if url is None:
        print('TEST MODE: url is None')
        return None
    else:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(sleep_time)
        return driver


def getInstagramFirstPostWebsiteByInstagramDriver(instagram_driver=None):
    if instagram_driver is None:
        instagram_first_post_webiste = 'https://www.instagram.com/nycubgc/p/C5yA0PqyA88/?img_index=1'
        
        print('TEST MODE: instagram driver is None')
        print(f'First post website: {instagram_first_post_webiste}')
        return instagram_first_post_webiste
    else:
        post_list = instagram_driver.find_elements(By.TAG_NAME, 'a')[3:]
        instagram_first_post_webiste = post_list[0].get_attribute('href')
        
        print(f'First post website: {instagram_first_post_webiste}')
        return instagram_first_post_webiste

# # Event library invocation
# @client.event
# # When the bot is ready
# async def on_ready():
#     print(f'Logged in as {client.user}')


# @client.event
# # When a new message is sent in a channel
# async def on_message(message):
#     # Exclude messages from the bot itself to avoid infinite loops
#     if message.author == client.user:
#         return
    
#     if message.content.startswith('!getimage'):
#         try:
#             soup = getSoupByURL(INSTAGRAM_URL)
#             nrec_list = soup.find_all('a', {'role' : 'link'})
#             # Check if the response content is an image
#             if 'image' in response.headers['Content-Type']:
#                 # Send the image back to the same channel
#                 await message.channel.send(file=discord.File(response.content, 'image.png'))
#             else:
#                 await message.channel.send("The provided URL doesn't point to an image.")
#         except Exception as e:
#             await message.channel.send(f"An error occurred: {str(e)}")


def main():
    # with open('token.txt', 'r') as token_file:
    #     token = token_file.read()
    # client.run(token)
    
    instagram_driver = getDriverByURL()
    instagram_first_post_website = getInstagramFirstPostWebsiteByInstagramDriver(instagram_driver)


if __name__ == '__main__':
    main()
