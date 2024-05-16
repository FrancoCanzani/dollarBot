from dotenv import load_dotenv
from textblob import TextBlob
import os
import praw
import logging
from telegram import Update
from telegram.ext import (
    MessageHandler,
    ContextTypes,
    CommandHandler,
    Application,
    filters,
)


# Load environment variables from .env file
load_dotenv()


def Average(lst):
    return sum(lst) / len(lst)


reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    user_agent=os.getenv("user_agent"),
)


def handle_subreddit_analysis(subreddit: str):
    try:
        polarity_scores = []
        subjectivity = []
        posts = []

        for submission in reddit.subreddit(subreddit).hot(limit=5):
            submission_text = submission.title + " " + submission.selftext
            blob = TextBlob(submission_text)
            submission_polarity = [
                sentence.sentiment.polarity for sentence in blob.sentences
            ]
            submission_subjectivity = [
                sentence.sentiment.subjectivity for sentence in blob.sentences
            ]
            posts.append(f"{submission.title}")
            polarity_scores.extend(submission_polarity)
            subjectivity.extend(submission_subjectivity)

        # Calculate the average polarity score for all submissions
        polarity_average = round(Average(polarity_scores), 3)
        subjectivity_average = round(Average(subjectivity), 3)

        # Format the results for better presentation
        result = (
            f"Subreddit: {subreddit}\n"
            f"Last 5 posts (hot):\n{'\n'.join(posts)}\n"
            f"Total Average Polarity Score: {polarity_average}\n"
            f"Total Average Subjectivity Score: {subjectivity_average}\n"
            "The polarity score is a float within the range [-1.0, 1.0]. "
            "The subjectivity is a float within the range [0.0, 1.0] where "
            "0.0 is very objective and 1.0 is very subjective."
        )
        return result

    except Exception as e:
        return f"An error occurred: {e}"


# Logging module to know when (and why) things don't work as expected
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Commands


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """Hello! Reddit Sentiment Bot is a Telegram bot that provides sentiment analysis for Reddit posts from various subreddits. It analyzes the sentiment (positive/negative) and subjectivity (objective/subjective) of the latest posts in a specified subreddit.

🔍 How to Use:

Analyze Subreddit: To analyze the sentiment of posts from a subreddit, simply type the name of the subreddit. For example: nba

Subreddit Restrictions: Please note that the subreddit name should be entered as a single word without spaces.

📊 Understanding Results:

Polarity Score: A float value within the range [-1.0, 1.0], where negative values indicate negative sentiment and positive values indicate positive sentiment.
Subjectivity Score: A float value within the range [0.0, 1.0], where 0.0 represents objectivity and 1.0 represents subjectivity."""

    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Please type the name of a subreddit so I can analyze it!"
    )


# Responses


def handle_response(input: str) -> str:
    processed = input.lower()

    if len(processed.split()) > 1:
        return "The Subreddit should be one word. Check the list of subreddits: https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits/"

    return handle_subreddit_analysis(input)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}')

    if message_type == "group":
        if os.getenv("bot_username") in text:
            new_text = text.replace(os.getenv("bot_username"), "").strip()
            response = handle_response(new_text)
        else:
            return

    else:
        response = handle_response(text)

    print("Bot: ", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    app = Application.builder().token(os.getenv("telegram_token")).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=5)
