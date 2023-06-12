
import logging
from datetime import datetime

from telegram.ext import CommandHandler, ContextTypes, ApplicationBuilder
from telegram import Update
from typing import Final

from curency_api_iran import i_convert_currency_price_to_irr


BOT_TOKEN: Final = ''
DEV_IDS = ['']

logging.basicConfig(format='%(levelname)s - (%(asctime)s) - %(message)s - (Line: %(lineno)d) -[%(filename)s]',
                    datefmt='%H:%M:%S',
                    encoding='utf-8',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


async def stat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You can use This bot with following pattern :\n"
             "/set <int><base> -> Send You a base to IRR converted Price after <int> seconds ",
        reply_to_message_id=update.effective_message.id,
    )


async def set_for_currency_alert_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        job_name = str(update.effective_user.id)
        base = str(context.args[1])
        due = float(context.args[0])
        if due < 5:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Pls Insert a Number greater or equal to 5!",
                reply_to_message_id=update.effective_message.id
            )
            return
        removed_job = remove_job_if_exist(job_name, context)
        context.job_queue.run_repeating(
            currency_alert_job,
            chat_id=update.effective_chat.id,
            interval=due,
            name=job_name,
            data={
                "base": base,
                "due": due
            }
        )
        text = "Your Job was created"
        if removed_job:
            text += "\n All Other Jobs Deleted Successfully!"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )
    except(IndexError, ValueError):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You set my job Wrong!!",
            reply_to_message_id=update.effective_message.id,
        )


async def unset_alert_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name(str(update.effective_user.id))
    for job in jobs:
        job.schedule_removal()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="all Jobs Deleted!!"
        )


async def currency_alert_job(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    base = context.job.data["base"]
    due = context.job.data["due"]
    price = i_convert_currency_price_to_irr(base)
    current_time = datetime.now().strftime("%H:%M")
    await context.bot.send_message(
        chat_id=job.chat_id,
        text=f"At {current_time}  (Iran Standard Time)  {base} to IRR price is: {price} Rial \n "
             f" I will notify you after {due} seconds again ! "
    )


def remove_job_if_exist(name: str, context: ContextTypes.DEFAULT_TYPE):
    all_jobs = context.job_queue.get_jobs_by_name(name)
    if not all_jobs:
        return False
    for job in all_jobs:
        job.schedule_removal()
    return True


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler(['start', 'help'], stat_handler))
    bot.add_handler(CommandHandler('set', set_for_currency_alert_handler))
    bot.add_handler(CommandHandler('unset', unset_alert_handler))
    bot.run_polling()
