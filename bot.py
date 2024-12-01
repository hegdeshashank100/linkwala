import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# JSON file to store links
JSON_FILE = "links.json"

# Load links from JSON file
def load_links():
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save links to JSON file
def save_links(links):
    with open(JSON_FILE, "w") as file:
        json.dump(links, file, indent=4)

# Load existing links
links = load_links()

# States for conversation
ENTER_NAME, ENTER_LINK = range(2)

# Command: /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Hello! Send me a website name (in lowercase, without spaces), and I'll provide the link. "
        "If the link doesn't exist, you can add it using /add."
    )

# Handle user messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()
    response = links.get(user_message, "Sorry, I don't have a link for that website. Use /add to add it.")
    await update.message.reply_text(response)

# Add new link: /add
async def add(update: Update, context: CallbackContext):
    await update.message.reply_text("Please enter the name of the website you want to add:")
    return ENTER_NAME

# Step 1: User enters name
async def enter_name(update: Update, context: CallbackContext):
    context.user_data["website_name"] = update.message.text.lower()
    await update.message.reply_text("Now enter the URL of the website:")
    return ENTER_LINK

# Step 2: User enters link
async def enter_link(update: Update, context: CallbackContext):
    website_name = context.user_data["website_name"]
    website_link = update.message.text
    links[website_name] = website_link  # Add to the dictionary
    save_links(links)  # Save to the JSON file

    await update.message.reply_text(f"Website '{website_name}' has been added with the link: {website_link}")
    return ConversationHandler.END

# Cancel conversation
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Link addition canceled.")
    return ConversationHandler.END

# Main function to run the bot
def main():
    bot_token = "YOUR_BOT_TOKEN"
    application = Application.builder().token(bot_token).build()

    # Conversation handler for adding links
    add_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add)],
        states={
            ENTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_name)],
            ENTER_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_link)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(add_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
