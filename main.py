import discord
from discord.ext import tasks
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

GAME_PLAYING = 'The best board game: Agricola'
INSTAGRAM_URL = 'https://www.instagram.com/nycubgc/'
INSTAGRAM_MESSAGE_PREFIX = '桌遊社Instagram有新貼文啦，快去看看吧\n貼文網址：'

TEST_INSTAGRAM_LAST_POST_WEBSITE = 'https://www.instagram.com/nycubgc/p/C5yA0PqyA88/?img_index=1'

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
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(sleep_time)
        return driver


class Instagram_Functions():
    @staticmethod
    def getInstagramLastPostWebsiteMessageByURL(url=None):
        instagram_driver = getDriverByURL(url=url)
        instagram_last_post_website = Instagram_Functions.__getInstagramLastPostWebsiteByInstagramDriver(instagram_driver)
        instagram_last_post_website_message = f'{INSTAGRAM_MESSAGE_PREFIX}{instagram_last_post_website}'
        print(instagram_last_post_website_message)
        return instagram_last_post_website_message
    
    @staticmethod
    def __getInstagramLastPostWebsiteByInstagramDriver(instagram_driver=None):
        if instagram_driver is None:
            instagram_last_post_webiste = TEST_INSTAGRAM_LAST_POST_WEBSITE
            
            print('TEST MODE: instagram driver is None')
            print(f'Last post website: {instagram_last_post_webiste}')
            return instagram_last_post_webiste
        else:
            post_list = instagram_driver.find_elements(By.TAG_NAME, 'a')[3:]
            instagram_last_post_webiste = post_list[0].get_attribute('href')
            
            print(f'Last post website: {instagram_last_post_webiste}')
            return instagram_last_post_webiste


# Event library invocation
@client.event
# When the bot is ready
async def on_ready():
    print(f'Logged in as {client.user}')
    game = discord.Game(GAME_PLAYING)
    # discord.Status: online = 'online', offline = 'offline', idle = 'idle', dnd = 'dnd', do_not_disturb = 'dnd', invisible = 'invisible'
    await client.change_presence(status=discord.Status.online, activity=game)
    getNewAnnouncement.start()


@tasks.loop(minutes=10)
async def getNewAnnouncement():
    with open('channel_id.txt', 'r') as channel_id_file:
        channel_id = channel_id_file.read()
    channel = client.get_channel(int(channel_id))
    try:
        # Retrieve the last post website message from instagram
        instagram_last_post_website_message = Instagram_Functions.getInstagramLastPostWebsiteMessageByURL(url=INSTAGRAM_URL)
        
        # Retrieve the last message sent by the bot in the channel
        async for msg in channel.history():
            if msg.author == client.user:
                last_bot_message = msg.content
                break
            else:
                last_bot_message = None
        
        # If the last post website message is not same with the bot's last message, send the last post website message
        if instagram_last_post_website_message != last_bot_message:
            await channel.send(instagram_last_post_website_message)
    except Exception as e:
        await channel.send(f'An error occurred: {str(e)}')


def main():
    with open('token.txt', 'r') as token_file:
        token = token_file.read()
    client.run(token)


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        INSTAGRAM_URL = None
        main()
    elif sys.argv[1] == 'main':
        main()
