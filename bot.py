import json
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# GitHub Details
GITHUB_REPO = 'hegdeshashank100/linkwala'
GITHUB_FILE_PATH = 'links.json'
GITHUB_TOKEN = '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'  # Replace with your GitHub personal access token

# JSON file to store links (locally and remotely)
JSON_FILE = "links.json"

# Flask app
app = Flask(__name__)

# Load links from GitHub
def load_links_from_github():
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_content = response.json()['content']
        return json.loads(requests.utils.base64.b64decode(file_content).decode())
    return {}

# Save links to GitHub
def save_links_to_github(links):
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    # Fetch the file info to get the sha for updating
    file_info_response = requests.get(url, headers=headers)
    if file_info_response.status_code == 200:
        sha = file_info_response.json()['sha']
        
        data = {
            'message': 'Update links.json with new link',
            'content': requests.utils.base64.b64encode(json.dumps(links).encode()).decode(),
            'sha': sha
        }
        
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Successfully updated links.json on GitHub.")
        else:
            print("Failed to update links.json on GitHub:", response.text)
    else:
        print("Failed to fetch file info from GitHub.")

# Load links from local JSON file or GitHub
def load_links():
    links = load_links_from_github()  # Load from GitHub
    if not links:
        try:
            with open(JSON_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    return links

# Save links to the local JSON file
def save_links(links):
    with open(JSON_FILE, "w") as file:
        json.dump(links, file, indent=4)
    save_links_to_github(links)  # Also update GitHub

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
    save_links(links)  # Save to both the local file and GitHub

    await update.message.reply_text(f"Website '{website_name}' has been added with the link: {website_link}")
    return ConversationHandler.END

# Cancel conversation
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Link addition canceled.")
    return ConversationHandler.END

# Webhook route for Telegram updates
@app.route(f"/{bot_token}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json.loads(json_str), bot)
    application.process_update(update)
    return 'OK', 200

# Main function to run the bot
if __name__ == "__main__":
    bot_token = "7625370821:AAEUgkhMJKkKpIrWKFtwG3pBRxgnyCP_VhU"  # Replace with your bot's token
    application = Application.builder().token(bot_token).build()

    # Load existing links
    global links
    links = load_links()

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

    # Run webhook
    app.run(host="0.0.0.0", port=5000)  # Use a suitable port for the server
