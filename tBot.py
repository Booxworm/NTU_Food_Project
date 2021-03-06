# Importing functions from python-telegram-bot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import logging

# Importing own functions
import main
import algo
import db

# Bot token
API_KEY = "746454645:AAFOJ8q1TQVug9tyQGvydGiDhShCvVHwF7c"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOICE, FOOD, PRICE, DIST = range(4)

def start(bot, update, user_data):
    """
    Start state of bot
    Asks if the user wants to list out all canteens
    Sends user to CHOICE state
    """
    user_data.clear()
    update.message.reply_text(
        main.actionMsg,
        reply_markup=ReplyKeyboardMarkup([[main.actionList[0]]], one_time_keyboard=True, resize_keyboard=True))
    return CHOICE


def choice(bot, update, user_data):
    """
    Handles users choices
    Returns various states depending on user choice
    """
    user = update.message.from_user
    msg = update.message.text
    logger.info("Action of {}: {}".format(user.first_name, msg))

    # Checks if user wants to find a canteen
    if msg == main.actionList[0]:
        update.message.reply_text(
            "Please enter the food you want to eat. Press /done when you are finished. If left empty, will return all foods.",
            reply_markup=ReplyKeyboardRemove())
        return FOOD

    # Sort by distance
    elif msg == main.sortList[0]:
        update.message.reply_text("Send me your location, so I can help you find the nearest canteens. If you decide to search by rank instead, click /change",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(text="Send Location", request_location=True)]],
                one_time_keyboard=True,
                resize_keyboard=True))
        return DIST

    # Sort by rank
    elif msg == main.sortList[1]:
        return rank(bot, update, user_data)

    return ConversationHandler.END

def food(bot, update, user_data):
    """
    Adds new food to foodList
    Returns back to FOOD state once added
    """
    user = update.message.from_user
    msg = update.message.text
    msg = ''.join(msg.lower().split())
    logger.info("Adding {} to {}'s list".format(msg, user.first_name))

    # Appends food to food list
    if 'foodList' not in user_data: user_data['foodList'] = []
    user_data['foodList'].append(msg)

    return FOOD

def foodDone(bot, update, user_data):
    """
    User done with choosing food
    Checks if food chosen is in the database
    If yes, sends user to PRICE state
    Else, sends user back to FOOD state
    """
    user = update.message.from_user

    if 'foodList' not in user_data:
        update.message.reply_text("You did not input anything, so there will be no filter on the food")
        logger.info("{}'s list contains everything!".format(user.first_name))
        update.message.reply_text('Okay now choose an upper price range')
        user_data['canteens'] = db.readFile()
        return PRICE

    logger.info("Adding to list")

    user_data['canteens'] = algo.searchByFood(user_data['foodList'])
    if not len(user_data['canteens']):
        user_data['foodList'] = []
        update.message.reply_text("Sorry, looks like the food you chose cannot be found. Please choose again. Type /done when finished")
        return FOOD
    else:
        logger.info("{}'s list contains {}".format(user.first_name, user_data['foodList']))
        update.message.reply_text('Okay now choose an upper price range')
        return UPPER

def price(bot, update, user_data):
    """
    Lets users choose upper limit of price
    Sends user to CHOICE state, where they will choose either to be sorted by distance or rank
    """
    user = update.message.from_user
    msg = update.message.text

    try:
        if msg == '': msg = '-inf'
        msg = float(msg)
        logger.info("{} chose {}".format(user.first_name, msg))
        user_data['upper'] = msg
        temp = algo.searchByPrice(
            user_data['upper'],
            user_data['canteens'])
        if not len(temp):
            update.message.reply_text("No food within that price range, please choose an upper price range again")
            return PRICE
        else:
            user_data['canteens'] = temp
            update.message.reply_text(
                main.sortMsg,
                reply_markup=ReplyKeyboardMarkup([[sort] for sort in main.sortList], one_time_keyboard=True, resize_keyboard=True))
            return CHOICE

    except ValueError:
        update.message.reply_text("Sorry that is not a valid input, please enter a number")
        return LOWER

def dist(bot, update, user_data):
    """
    Extracts the latitude and longtitude
    Sorts the canteens by distance
    """
    user = update.message.from_user
    loc = update.message.location
    logger.info("Location of {}: {} / {}".format(user.first_name, loc.latitude,
                loc.longitude))
    update.message.reply_text('Give me some time while I find the nearest canteens...',
        reply_markup=ReplyKeyboardRemove())

    latlong = loc.latitude, loc.longitude
    user_data['canteens'] = algo.sortByDist(latlong, user_data['canteens'], True)

    logger.info(user_data['canteens'])
    update.message.reply_text(algo.formatCanteens(user_data['canteens']))
    return exit(bot, update)

def distChange(bot, update, user_data):
    """
    User decides to change from distance to rank
    Redirects the user to sort by rank
    """
    logger.info("Changing to rank")
    update.message.reply_text("Since you dont want to sort by distance, I'll sort it by rank instead")
    return rank(bot, update, user_data)

def rank(bot, update, user_data):
    """
    Sorts the canteens by rank
    """
    msg = update.message.text

    update.message.reply_text(
        'Give me some time while I find the best canteens...',
        reply_markup=ReplyKeyboardRemove())
    user_data['canteens'] = algo.sortByRank(user_data['canteens'])
    logger.info(user_data['canteens'])
    update.message.reply_text(algo.formatCanteens(user_data['canteens']))
    return exit(bot, update)

def exit(bot, update):
    """
    User has finished or cancelled the convo
    Ends the Conversation
    """
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Thanks for trying our bot!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """
    Log Errors caused by Updates
    """
    logger.warning('Update "%s" caused error "%s"', update, error)


def tMain():
    """
    Main function for telegram bot
    Contains all the states and conditions to move to next state
    """
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(API_KEY)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start,
                      pass_user_data=True)],

        states={
            CHOICE: [RegexHandler('^(Find a canteen|Distance|Rank)$', choice,
                     pass_user_data=True)],

            FOOD: [MessageHandler(Filters.text, food,
                   pass_user_data=True),
                   CommandHandler('done', foodDone,
                   pass_user_data=True)],

            PRICE: [MessageHandler(Filters.text, price,
                    pass_user_data=True)],

            DIST: [MessageHandler(Filters.location, dist,
                   pass_user_data=True),
                   CommandHandler('change', distChange,
                   pass_user_data=True)]
        },

        fallbacks=[CommandHandler('exit', exit)]
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
    tMain()
