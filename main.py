import logging
import os
from os.path import join, dirname

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

dotenv_path = join(dirname(__file__), ".env")
crawler_path = join(dirname(__file__), '..', "amiami_crawler")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
N_CH_ID = os.environ.get("N_CH_ID")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def figures(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Проверяю наличие интересных фигурок")
    os.system(f"cd {crawler_path} && npm run execute")
    results = open(join(f"{crawler_path}", "results.txt"),
                   "r", encoding="utf-8")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=results.read())
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Вот список на сегодня")

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    figures_handler = CommandHandler("figures", figures)

    application.add_handler(figures_handler)

    application.run_polling()
