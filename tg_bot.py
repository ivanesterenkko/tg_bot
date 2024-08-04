import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


TOKEN = '7332551320:AAEONIMU3NfI8J-I9S0NnPBhLm64xBkpXDc' # Токен бота
GROUP_IDS = ['@qwerty_bot_21']  # Список групп

async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    bot = Bot(TOKEN)
    chat_member_statuses = []

    for group_id in GROUP_IDS:
        try:
            chat_member = await bot.get_chat_member(chat_id=group_id, user_id=user.id)
            chat_member_statuses.append((group_id, chat_member.status))
        except Exception as e:
            logger.error(f"Error checking group {group_id} for user {user.id}: {e}")
            chat_member_statuses.append((group_id, 'not_found'))

    member_statuses = ['member', 'administrator', 'creator']

    not_subscribed_groups = [group_id for group_id, status in chat_member_statuses if status not in member_statuses]

    if not_subscribed_groups:
        keyboard = [
            [InlineKeyboardButton("Проверить снова", callback_data='check_subscription')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f'Вы не подписаны на следующие группы: {", ".join(not_subscribed_groups)}. Пожалуйста, подпишитесь на них.', reply_markup=reply_markup)
    else:
        await update.message.reply_text('Вы подписаны на все необходимые группы!')

# Обработчик для callback_data
async def check_subscription(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Отвечаем на запрос, чтобы убрать часики ожидания

    user = query.from_user
    bot = Bot(TOKEN)
    chat_member_statuses = []

    for group_id in GROUP_IDS:
        try:
            chat_member = await bot.get_chat_member(chat_id=group_id, user_id=user.id)
            chat_member_statuses.append((group_id, chat_member.status))
        except Exception as e:
            logger.error(f"Error checking group {group_id} for user {user.id}: {e}")
            chat_member_statuses.append((group_id, 'not_found'))

    member_statuses = ['member', 'administrator', 'creator']

    not_subscribed_groups = [group_id for group_id, status in chat_member_statuses if status not in member_statuses]

    if not_subscribed_groups:
        keyboard = [
            [InlineKeyboardButton("Проверить снова", callback_data='check_subscription')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f'Вы не подписаны на следующие группы: {", ".join(not_subscribed_groups)}. Пожалуйста, подпишитесь на них.', reply_markup=reply_markup)
    else:
        await query.edit_message_text('Вы подписаны на все необходимые группы!')

# Команда /stop
async def stop(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Бот останавливается...')
    context.application.stop()  # Остановка приложения

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработка команды /start
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Обработка команды /stop
    stop_handler = CommandHandler("stop", stop)
    application.add_handler(stop_handler)

    # Обработка callback_data
    subscription_handler = CallbackQueryHandler(check_subscription, pattern='check_subscription')
    application.add_handler(subscription_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()