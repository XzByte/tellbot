import os
import requests
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
from tenacity import retry, stop_after_attempt, wait_fixed

# Load environment variables from .env file
load_dotenv()

# Define a function to start the bot
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am your Telegram bot.')

# Define a function to get Jenkins build status for a specific job
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def jenkins_status(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a job name.")
        return

    job_name = context.args[0]
    jenkins_url = os.getenv("JENKINS_URL")
    user = os.getenv("JENKINS_USER")
    token = os.getenv("JENKINS_API_TOKEN")

    response = requests.get(f"{jenkins_url}/job/{job_name}/lastBuild/api/json", auth=(user, token))
    if response.status_code == 200:
        build_info = response.json()
        status = build_info['result']
        await update.message.reply_text(f"The last build status of {job_name} is: {status}")
    else:
        await update.message.reply_text(f"Failed to fetch Jenkins build status for job: {job_name}")

# Define a function to show the menu of available commands
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        ["/start", "/jenkins <job_name>"],
        ["/menu"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Choose a command:", reply_markup=reply_markup)

# Define the main function to run the bot
def main() -> None:
    # Get the bot token from environment variables
    bot_token = os.getenv("BOT_TOKEN")

    # Create an Application object with your bot's token
    application = Application.builder().token(bot_token).connect_timeout(60).read_timeout(60).build()

    # Register the command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jenkins", jenkins_status))
    application.add_handler(CommandHandler("menu", menu))

    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()