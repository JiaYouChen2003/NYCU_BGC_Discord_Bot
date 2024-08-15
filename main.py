import discord
from discord.ext import tasks
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 機器人正在玩的遊戲
GAME_PLAYING = 'The best board game: Agricola'
# 機器人要在哪裡發言
DISCORD_ANNOUNCEMENT_CHANNEL_NAME = '麻瓜大廳'
# 機器人出錯會寫在哪裡
DISCORD_ERROR_CHANNEL_NAME = '測試'
# 出錯時幾分鐘後重試
MINUTES = 10

# 社團INSTAGRAM的網址
INSTAGRAM_URL = 'https://www.instagram.com/nycubgc/'
# INSTAGRAM公告前面要加的詞
INSTAGRAM_MESSAGE_PREFIX = '桌遊社Instagram有新貼文啦，快去看看吧\n貼文網址：'

# 測試時INSTAGRAM的公告
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
        if instagram_last_post_website == 0:
            return 0
        instagram_last_post_website_message = f'{INSTAGRAM_MESSAGE_PREFIX}{instagram_last_post_website}'
        print(instagram_last_post_website_message)
        return instagram_last_post_website_message
    
    @staticmethod
    def __getInstagramLastPostWebsiteByInstagramDriver(instagram_driver=None):
        if instagram_driver is None:
            instagram_last_post_website = TEST_INSTAGRAM_LAST_POST_WEBSITE
            
            print('TEST MODE: instagram driver is None')
            print(f'Last post website: {instagram_last_post_website}')
            return instagram_last_post_website
        else:
            new_post = instagram_driver.find_element(By.CLASS_NAME, '_aagu')
            instagram_last_post_website = new_post.find_element(By.XPATH, '..').get_attribute('href')
            if not instagram_last_post_website.startswith(INSTAGRAM_URL):
                return 0
            
            print(f'Last post website: {instagram_last_post_website}')
            return instagram_last_post_website


# Event library invocation
@client.event
# When the bot is ready
async def on_ready():
    print(f'Logged in as {client.user}')
    game = discord.Game(GAME_PLAYING)
    # discord.Status: online = 'online', offline = 'offline', idle = 'idle', dnd = 'dnd', do_not_disturb = 'dnd', invisible = 'invisible'
    await client.change_presence(status=discord.Status.online, activity=game)
    getNewAnnouncement.start()


@tasks.loop(minutes=MINUTES, count=2)
async def getNewAnnouncement():
    try:
        channel = discord.utils.get(client.get_all_channels(), name=DISCORD_ANNOUNCEMENT_CHANNEL_NAME)
        # Retrieve the last post website message from instagram
        instagram_last_post_website_message = Instagram_Functions.getInstagramLastPostWebsiteMessageByURL(url=INSTAGRAM_URL)
        assert instagram_last_post_website_message != 0, 'Instagram website structure have been changed'
        
        # Retrieve the last message sent by the bot in the channel
        last_bot_message = ''
        async for msg in channel.history():
            if msg.author == client.user:
                last_bot_message = msg.content
                break
        
        # If the last post website message is not same with the bot's last message, send the last post website message
        if instagram_last_post_website_message != last_bot_message or last_bot_message.startswith('An error occurred: '):
            await channel.send(instagram_last_post_website_message)
        
        getNewAnnouncement.stop()
    except Exception as e:
        channel = discord.utils.get(client.get_all_channels(), name=DISCORD_ERROR_CHANNEL_NAME)
        await channel.send(f'An error occurred: {str(e)}. Retry in {MINUTES} minutes')


def main():
    # optional: for task scheduler to find the bot token
    token_root = os.path.dirname(__file__)
    if token_root == '':
        token_root = '.'
    with open(token_root + '/token.txt', 'r') as token_file:
        token = token_file.read()
    client.run(token)


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        INSTAGRAM_URL = None
        main()
    elif sys.argv[1] == 'main':
        main()
