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


def getInstagramLastPostWebsiteByInstagramDriver(instagram_driver=None):
    if instagram_driver is None:
        instagram_last_post_webiste = 'https://www.instagram.com/nycubgc/p/C5yA0PqyA88/?img_index=1'
        
        print('TEST MODE: instagram driver is None')
        print(f'Last post website: {instagram_last_post_webiste}')
        return instagram_last_post_webiste
    else:
        post_list = instagram_driver.find_elements(By.TAG_NAME, 'a')[3:]
        instagram_last_post_webiste = post_list[0].get_attribute('href')
        
        print(f'Last post website: {instagram_last_post_webiste}')
        return instagram_last_post_webiste


def getInstagramLastPostWebsiteMessage():
    instagram_driver = getDriverByURL()
    instagram_last_post_website = getInstagramLastPostWebsiteByInstagramDriver(instagram_driver)
    instagram_last_post_website_message = f'New post: {instagram_last_post_website}'
    return instagram_last_post_website_message


# Event library invocation
@client.event
# When the bot is ready
async def on_ready():
    print(f'Logged in as {client.user}')
    game = discord.Game('The best board game: Agricola')
    # discord.Status: online = 'online', offline = 'offline', idle = 'idle', dnd = 'dnd', do_not_disturb = 'dnd', invisible = 'invisible'
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
# When a new message is sent in a channel
async def on_message(message):
    # Exclude messages from the bot itself to avoid infinite loops
    if message.author == client.user:
        return
    
    if message.content.startswith('!get'):
        try:
            # Retrieve the last post website message from instagram
            instagram_last_post_website_message = getInstagramLastPostWebsiteMessage()
            
            # Retrieve the last message sent by the bot in the channel
            async for msg in message.channel.history():
                if msg.author == client.user:
                    last_bot_message = msg.content
                    break
                else:
                    last_bot_message = None
            
            # If the last post website message is not same with the bot's last message, send the last post website message
            if instagram_last_post_website_message != last_bot_message:
                await message.channel.send(instagram_last_post_website_message)
        except Exception as e:
            await message.channel.send(f'An error occurred: {str(e)}')


def main():
    with open('token.txt', 'r') as token_file:
        token = token_file.read()
    client.run(token)


if __name__ == '__main__':
    main()
