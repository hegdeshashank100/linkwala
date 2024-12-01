from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Dictionary of website names and links
website_links = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "baidu": "https://www.baidu.com",
    "wikipedia": "https://www.wikipedia.org",
    "amazon": "https://www.amazon.com",
    "reddit": "https://www.reddit.com",
    "yahoo": "https://www.yahoo.com",
    "instagram": "https://www.instagram.com",
    "twitter": "https://www.twitter.com",
    "linkedin": "https://www.linkedin.com",
    "t.co": "https://www.t.co",
    "tumblr": "https://www.tumblr.com",
    "netflix": "https://www.netflix.com",
    "qq": "https://www.qq.com",
    "pinterest": "https://www.pinterest.com",
    "office": "https://www.office.com",
    "microsoft": "https://www.microsoft.com",
    "apple": "https://www.apple.com",
    "stackoverflow": "https://www.stackoverflow.com",
    "github": "https://www.github.com",
    "espn": "https://www.espn.com",
    "sina": "https://www.sina.com.cn",
    "etsy": "https://www.etsy.com",
    "vk": "https://www.vk.com",
    "naver": "https://www.naver.com",
    "alibaba": "https://www.alibaba.com",
    "twitch": "https://www.twitch.tv",
    "imdb": "https://www.imdb.com",
    "cnn": "https://www.cnn.com",
    "sohu": "https://www.sohu.com",
    "samsung": "https://www.samsung.com",
    "bing": "https://www.bing.com",
    "reuters": "https://www.reuters.com",
    "microsoftonline": "https://www.microsoftonline.com",
    "foxnews": "https://www.foxnews.com",
    "huffpost": "https://www.huffpost.com",
    "flickr": "https://www.flickr.com",
    "scribd": "https://www.scribd.com",
    "pandora": "https://www.pandora.com",
    "bbc": "https://www.bbc.com",
    "weibo": "https://www.weibo.com",
    "paypal": "https://www.paypal.com",
    "nytimes": "https://www.nytimes.com",
    "cnbc": "https://www.cnbc.com",
    "dailymotion": "https://www.dailymotion.com",
    "mercadolibre": "https://www.mercadolibre.com",
    "bilibili": "https://www.bilibili.com",
    "walmart": "https://www.walmart.com",
    "target": "https://www.target.com",
    "indeed": "https://www.indeed.com",
    "tripadvisor": "https://www.tripadvisor.com",
    "quora": "https://www.quora.com",
    "foxsports": "https://www.foxsports.com",
    "mashable": "https://www.mashable.com",
    "redditfunny": "https://www.reddit.com/r/funny",
    "ok": "https://www.ok.ru",
    "nike": "https://www.nike.com",
    "zoho": "https://www.zoho.com",
    "kickstarter": "https://www.kickstarter.com",
    "businessinsider": "https://www.businessinsider.com",
    "spiegel": "https://www.spiegel.de",
    "autotrader": "https://www.autotrader.com",
    "usatoday": "https://www.usatoday.com",
    "news": "https://www.news.yahoo.com",
    "craigslist": "https://www.craigslist.org",
    "britannica": "https://www.britannica.com",
    "msn": "https://www.msn.com",
    "washingtonpost": "https://www.washingtonpost.com",
    "lazada": "https://www.lazada.com",
    "pornhub": "https://www.pornhub.com",
    "cambridge": "https://www.cambridge.org",
    "smh": "https://www.smh.com.au",
    "vimeo": "https://www.vimeo.com",
    "chaturbate": "https://www.chaturbate.com",
    "asos": "https://www.asos.com",
    "coursera": "https://www.coursera.org",
    "godaddy": "https://www.godaddy.com",
    "express": "https://www.express.co.uk",
    "upwork": "https://www.upwork.com",
    "airbnb": "https://www.airbnb.com",
    "weather": "https://www.weather.com",
    "rottentomatoes": "https://www.rottentomatoes.com",
    "yellowpages": "https://www.yellowpages.com",
    "bbc.co.uk": "https://www.bbc.co.uk",
    "pokerstars": "https://www.pokerstars.com",
    "weebly": "https://www.weebly.com",
    "spotify": "https://www.spotify.com",
    "flipkart": "https://www.flipkart.com",
    "aliexpress": "https://www.aliexpress.com",
    "zappos": "https://www.zappos.com",
    "lowes": "https://www.lowes.com",
    "bestbuy": "https://www.bestbuy.com",
    "snapchat": "https://www.snapchat.com",
    "zoom": "https://www.zoom.us",
    "dropbox": "https://www.dropbox.com",
    "telegram": "https://www.telegram.org",
    "slack": "https://www.slack.com",
    "skype": "https://www.skype.com",
    "behance": "https://www.behance.net",
    "yandex": "https://www.yandex.com",
    "forbes": "https://www.forbes.com",
    "soundcloud": "https://www.soundcloud.com",
    "bitbucket": "https://www.bitbucket.org",
    "codepen": "https://www.codepen.io",
    "edx": "https://www.edx.org",
    "theverge": "https://www.theverge.com",
    "redbubble": "https://www.redbubble.com",
    "swiggy": "https://www.swiggy.com",
    "dominos": "https://www.dominos.com",
    "yelp": "https://www.yelp.com",
    "uber": "https://www.uber.com",
    "lyft": "https://www.lyft.com",
    "zoominfo": "https://www.zoominfo.com",
    "webmd": "https://www.webmd.com",
    "dictionary": "https://www.dictionary.com",
    "wikihow": "https://www.wikihow.com",
    "techcrunch": "https://www.techcrunch.com",
    "thedailybeast": "https://www.thedailybeast.com",
    "businessweek": "https://www.businessweek.com",
    "theguardian": "https://www.theguardian.com",
    "ft": "https://www.ft.com",
    "time": "https://www.time.com",
    "bloomberg": "https://www.bloomberg.com",
    "bbcnews": "https://www.bbcnews.com",
    "huffpost": "https://www.huffpost.com",
    "thehill": "https://www.thehill.com",
    "independent": "https://www.independent.co.uk",
    "washingtontimes": "https://www.washingtontimes.com",
    "theatlantic": "https://www.theatlantic.com",
    "barrons": "https://www.barrons.com",
    "usatoday": "https://www.usatoday.com",
    "theeconomist": "https://www.economist.com",
    "worldometers": "https://www.worldometers.info",
    "tmz": "https://www.tmz.com",
    "people": "https://www.people.com",
    "gq": "https://www.gq.com",
    "vogue": "https://www.vogue.com",
    "zomato": "https://www.zomato.com",
    "jiocinema": "https://www.jiocinema.com",
    "myntra": "https://www.myntra.com",
    "swiggy": "https://www.swiggy.com",
    "hotstar":"https://www.hotstar.com/in/home"
    "whatsapp": "https://web.whatsapp.com"
}



# Function to handle incoming messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()
    response = website_links.get(user_message, "Sorry, I don't have a link for that website.")
    await update.message.reply_text(response)

# Function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! Send me a website name(In Lower Case without Space), and I'll provide you with the link.")

# Main function to start the bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = "7625370821:AAEUgkhMJKkKpIrWKFtwG3pBRxgnyCP_VhU"
    application = Application.builder().token(bot_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
