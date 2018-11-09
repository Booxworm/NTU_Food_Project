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

CHOICE, FOOD, UPPER, LOWER, DIST = range(5)

def start(bot, update, user_data):
    user_data.clear()
    update.message.reply_text(
        main.actionMsg,
        reply_markup=ReplyKeyboardMarkup([[action] for action in main.actionList], one_time_keyboard=True))
    return CHOICE


def choice(bot, update, user_data):
    user = update.message.from_user
    msg = update.message.text
    logger.info("Action of {}: {}".format(user.first_name, msg))

    # Checks if user wants to find a canteen
    if msg == main.actionList[0]:
        update.message.reply_text(
            "Please enter the food you want to eat. Press /done when you are finished",
            reply_markup=ReplyKeyboardRemove())
        return FOOD

    # Checks if user wants to update a canteen
    elif msg == main.actionList[1]:
        return ConversationHandler.END

    # Sort by distance
    elif msg == main.sortList[0]:
        update.message.reply_text("Send me your location, so I can help you find the nearest canteens. If you decide to search by rank instead, click /change",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(text="Send Location", request_location=True)]],
                one_time_keyboard=True))
        return DIST

    # Sort by rank
    elif msg == main.sortList[1]:
        return rank(bot, update, user_data)

    return ConversationHandler.END

def food(bot, update, user_data):
    user = update.message.from_user
    msg = update.message.text
    msg = ''.join(msg.lower().split())
    logger.info("Adding {} to {}'s list".format(msg, user.first_name))

    # Appends food to food list
    if 'foodList' not in user_data: user_data['foodList'] = []
    user_data['foodList'].append(msg)

    return FOOD

def foodDone(bot, update, user_data):
    user = update.message.from_user

    if 'foodList' not in user_data:
        update.message.reply_text("Please go choose a food before typing /done")
        return FOOD

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

def upper(bot, update, user_data):
    user = update.message.from_user
    msg = update.message.text

    try:
        if msg == '': msg = 'inf'
        msg = float(msg)
        logger.info("{} chose {}".format(user.first_name, msg))
        user_data['upper'] = msg
        update.message.reply_text("Choose a lower price range")
        return LOWER
    except ValueError:
        update.message.reply_text("Sorry that is not a valid input, please enter a number")
        return UPPER


def lower(bot, update, user_data):
    user = update.message.from_user
    msg = update.message.text

    try:
        if msg == '': msg = '-inf'
        msg = float(msg)
        logger.info("{} chose {}".format(user.first_name, msg))
        user_data['lower'] = msg
        temp = algo.searchByPrice(
            user_data['lower'],
            user_data['upper'],
            user_data['canteens'])
        if not len(temp):
            update.message.reply_text("No food within that price range, please choose an upper price range again")
            return UPPER
        else:
            user_data['canteens'] = temp
            update.message.reply_text(
                main.sortMsg,
                reply_markup=ReplyKeyboardMarkup([[sort] for sort in main.sortList], one_time_keyboard=True))
            return CHOICE

    except ValueError:
        update.message.reply_text("Sorry that is not a valid input, please enter a number")
        return LOWER

def dist(bot, update, user_data):
    user = update.message.from_user
    loc = update.message.location
    logger.info("Location of {}: {} / {}".format(user.first_name, loc.latitude,
                loc.longitude))
    update.message.reply_text('Give me some time while I find the nearest canteens...',
        reply_markup=ReplyKeyboardRemove())

    latlong = loc.latitude, loc.longitude
    user_data['canteens'] = algo.sortByDist(latlong, user_data['canteens'])

    logger.info(user_data['canteens'])
    sendCanteens(update, user_data['canteens'])
    return exit(bot, update)

def distChange(bot, update, user_data):
    logger.info("Changing to rank")
    update.message.reply_text("Since you dont want to sort by distance, I'll sort it by rank instead")
    return rank(bot, update, user_data)

def rank(bot, update, user_data):
    msg = update.message.text

    update.message.reply_text(
        'Give me some time while I find the best canteens...',
        reply_markup=ReplyKeyboardRemove())
    user_data['canteens'] = algo.sortByRank(user_data['canteens'])
    logger.info(user_data['canteens'])
    sendCanteens(update, user_data['canteens'])
    return exit(bot, update)

def sendCanteens(update, canteens):
    """
    Sends out a list of canteens
    Accepts an optional argument list of canteens to print out
    """
    msg = ""
    for c in canteens:
        msg += "{}\n".format(c['name'])
        msg += "  Coordinates - {}\n".format(c['coords'])
        if 'dist' in c:
            msg += "  Distance - {}\n".format(c['dist'])
        msg += "  Rank - {}\n".format(c['rank'])
        msg += "  Opening hours - {}\n".format(c['opening_hours'])
        msg += "  Food:\n"
        for food, price in c['food'].items():
            msg += "    {0} - ${1:0.2f}\n".format(food, price)
        msg += "\n"
    update.message.reply_text(msg)

def exit(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Thanks for trying our bot!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def tMain():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(API_KEY)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start,
                      pass_user_data=True)],

        states={
            CHOICE: [RegexHandler('^(Find a canteen|Update information|Distance|Rank)$', choice,
                     pass_user_data=True)],

            FOOD: [MessageHandler(Filters.text, food,
                   pass_user_data=True),
                   CommandHandler('done', foodDone,
                   pass_user_data=True)],

            UPPER: [MessageHandler(Filters.text, upper,
                    pass_user_data=True)],

            LOWER: [MessageHandler(Filters.text, lower,
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
