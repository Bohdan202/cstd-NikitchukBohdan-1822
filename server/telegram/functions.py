from config import bot, creator_id


def log(message, type, result):
    text = (message.from_user.first_name or '???') + ' (' + (message.from_user.username or '???') + '): ' + type + ' "' + message.text + '" -> "' + result + '"'

    print(text)
    if message.chat.id != creator_id:
        bot.send_message(creator_id, text)