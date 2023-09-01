import logging
import random
import os
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from bs4 import BeautifulSoup

# Set your Telegram bot token here
TOKEN = 'BOT_TOKEN_HERE'

## Set the list of allowed admin chat IDs
ALLOWED_ADMIN_IDS = [CHATID_HERE, NEW_CHATID_HERE]  # Replace CHATID_HERE and NEW_CHATID_HERE with actual chat IDs of allowed admins


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your Dork Scraper bot. Send me /dork followed by a query to scrape domains.')

def dork(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id not in ALLOWED_ADMIN_IDS:
        update.message.reply_text('You are not authorized to use this command.')
        return

    query = context.args
    if not query:
        update.message.reply_text('Please provide a query after /dork.')
        return

    search_query = ' '.join(query)
    search_url = f'https://www.google.com/search?q={search_query}&num=200'
    
    try:
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        domains = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.startswith('/url?q='):
                domain = href.split('/url?q=')[1].split('&')[0]
                if domain.startswith('http') and 'google.com' not in domain:
                    domains.append(domain)
        
        unique_domains = list(set(domains))
        random_number = random.randint(1, 10000)
        filename = f'random_{random_number}.txt'
        with open(filename, 'w') as file:
            file.write('\n'.join(unique_domains))
        update.message.reply_document(document=open(filename, 'rb'))
    except Exception as e:
        update.message.reply_text('An error occurred while fetching and scraping data.')


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("dork", dork))
    
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
