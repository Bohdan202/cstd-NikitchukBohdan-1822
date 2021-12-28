from config import bot


@bot.message_handler(commands=['game'])
def start_game(call):
    bot.send_game(call.chat.id, 'prostogame')


@bot.callback_query_handler(func=lambda callback_query: callback_query.game_short_name == 'prostogame')
def game(call):
    bot.answer_callback_query(callback_query_id=call.id, url='https://www.google.com.ua')
    # bot.answer_callback_query(callback_query_id=call.id, show_alert=True, url='https://agar.io/#ffa')
    # bot.answer_callback_query(callback_query_id=call.id, show_alert=True, url='https://manunkasnjegowick.wixsite.com/wineandcocoaknights/post/1-2-сезон-2-серия')
    # bot.answer_callback_query(callback_query_id=call.id, show_alert=True, url='https://manunkasnjegowick.wixsite.com/wineandcocoaknights/post/1-2-%D1%81%D0%B5%D0%B7%D0%BE%D0%BD-2-%D1%81%D0%B5%D1%80%D0%B8%D1%8F')
    