import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


TOKEN = '7332551320:AAEONIMU3NfI8J-I9S0NnPBhLm64xBkpXDc' # Токен бота
GROUP_IDS = ['@qwerty_bot_21']  # Список групп

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    not_subscribed_groups = [group_id for group_id, status in chat_member_statuses if status != 'member']

    if not_subscribed_groups:
        await update.message.reply_text(f'Вы не подписаны на следующие группы: {", ".join(not_subscribed_groups)}. Пожалуйста, подпишитесь на них.')
    else:
        await update.message.reply_text('Вы подписаны на все необходимые группы!')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработка команды /start
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()

if __name__ == '__main__':
    main()