# Importing functions from python-telegram-bot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import logging

# Importing own functions
from resources.db import canteens
import main as m
import algo as a

# Bot token
API_KEY = "TOKEN"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

ACTION, CRITERIA, DISTANCE = range(3)


def start(bot, update):
    update.message.reply_text(
        m.actionMsg,
        reply_markup=ReplyKeyboardMarkup([m.actionList], one_time_keyboard=True))
    return ACTION


def action(bot, update):
    user = update.message.from_user
    msg = update.message.text
    logger.info("Action of {}: {}".format(user.first_name, msg))

    # Checks if user wants to find a canteen
    if msg == m.actionList[0]:
        update.message.reply_text(
            m.criteriaMsg,
            reply_markup=ReplyKeyboardMarkup([m.criteriaList], one_time_keyboard=True))
        return CRITERIA

    # Checks if user wants to update a canteen
    elif msg == m.actionList[1]:
        m.updateCanteen(None, None)
        return ConversationHandler.END

    return ConversationHandler.END

def criteria(bot, update):
    user = update.message.from_user
    msg = update.message.text
    logger.info("Criteria of {}: {}".format(user.first_name, msg))

    # Checks if user wants to find a canteen by distance
    if msg == m.criteriaList[0]:
        update.message.reply_text('Send me your location so we can find the shortest distance!')
        return DISTANCE

    # Checks if user wants to update a canteen by price
    elif msg == m.criteriaList[1]:
        pass

    # Checks if user wants to update a canteen by rank
    elif msg == m.criteriaList[2]:
        pass

    return ConversationHandler.END

def distance(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of {}: {} / {}".format(user.first_name, user_location.latitude,
                user_location.longitude))
    update.message.reply_text('Alright, give me some time while I find the nearest canteens...')


    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(API_KEY)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ACTION: [RegexHandler('(Find a canteen|Update information)', action)],

            CRITERIA: [RegexHandler('(Distance|Price|Rank)', criteria)],

            DISTANCE: [MessageHandler(Filters.location, distance)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
