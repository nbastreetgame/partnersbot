import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ID администратора
ADMIN_ID = 7014721682

# Множество для хранения ID пользователей
registered_users = set()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение с кнопкой"""
    
    user = update.effective_user
    
    # Уведомляем администратора только о новых пользователях
    if user.id not in registered_users:
        registered_users.add(user.id)
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"👤 Новый пользователь:\n\n"
                     f"Имя: {user.first_name} {user.last_name or ''}\n"
                     f"Username: @{user.username or 'нет'}\n"
                     f"ID: {user.id}"
            )
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления админу: {e}")
    
    # Создаем кнопку
    keyboard = [
        [KeyboardButton("🔥 ПОДПИСКА НАВСЕГДА 🔥")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    await update.message.reply_text(
        "Добро пожаловать! 💋\n\n"
        "Получите пожизненный доступ к эксклюзивному контенту!",
        reply_markup=reply_markup
    )

# Обработчик кнопки подписки
async def show_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает информацию о подписке"""
    
    keyboard = [
        [KeyboardButton("💳 ОПЛАТИТЬ")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    response = (
        "🔥 ПОДПИСКА НАВСЕГДА 🔥\n\n"
        "Стоимость: 3 000.00 🇷🇺RUB\n"
        "Срок действия: Навсегда ♾️\n\n"
        "Вы получите доступ к:\n"
        "• 💋 NataFullPorn (канал)"
    )
    
    await update.message.reply_text(response, reply_markup=reply_markup)

# Обработчик кнопки "ОПЛАТИТЬ"
async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает реквизиты для оплаты"""
    
    payment_text = """Способ оплаты: На карту Т-Банк
К оплате: 3 000.00 🇷🇺RUB
Реквизиты для оплаты:
2200701046225592
Т-банк
Наталия💖
__________________________
Вы платите физическому лицу.
Деньги поступят на счёт получателя."""
    
    keyboard = [
        [KeyboardButton("⏳ Я ОПЛАТИЛ")],
        [KeyboardButton("👈 НАЗАД")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    await update.message.reply_text(payment_text, reply_markup=reply_markup)

# Обработчик кнопки "Я ОПЛАТИЛ"
async def handle_paid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запрашивает чек"""
    
    keyboard = [
        [KeyboardButton("🚫 ОТМЕНА")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    message_text = """🤷 Оплатили?

👌 Тогда отправьте сюда картинкой (не документом!) квитанцию платежа: скриншот или фото.

На квитанции должны быть четко видны: дата, время и сумма платежа.
__________________________
За спам вы можете быть заблокированы!"""
    
    await update.message.reply_text(message_text, reply_markup=reply_markup)

# Обработчик фото (чеков)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет чек администратору"""
    
    user = update.effective_user
    photo = update.message.photo[-1]
    
    try:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo.file_id,
            caption=f"💳 Новый чек об оплате:\n\n"
                    f"👤 Пользователь: {user.first_name} {user.last_name or ''}\n"
                    f"Username: @{user.username or 'нет'}\n"
                    f"ID: {user.id}\n"
                    f"Тариф: НАВСЕГДА (3000₽)"
        )
        
        await update.message.reply_text(
            "✅ Ваш чек получен!\n"
            "Ожидайте подтверждения от администратора."
        )
        
        await start(update, context)
        
    except Exception as e:
        logger.error(f"Ошибка отправки чека админу: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка. Попробуйте позже или свяжитесь с администратором."
        )

# Обработчик кнопки "НАЗАД" и "ОТМЕНА"
async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возвращает к началу"""
    await start(update, context)

def main() -> None:
    """Запуск бота"""
    
    # Токен бота
    TOKEN = "8544544839:AAFe5kbQoqR3dJXejS30n4jW9liYHcTws-A"
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    
    # Кнопки
    application.add_handler(MessageHandler(
        filters.Regex("^🔥 ПОДПИСКА НАВСЕГДА 🔥$"), 
        show_subscription
    ))
    application.add_handler(MessageHandler(
        filters.Regex("^💳 ОПЛАТИТЬ$"), 
        handle_payment
    ))
    application.add_handler(MessageHandler(
        filters.Regex("^⏳ Я ОПЛАТИЛ$"), 
        handle_paid
    ))
    application.add_handler(MessageHandler(
        filters.Regex("^(👈 НАЗАД|🚫 ОТМЕНА)$"), 
        handle_back
    ))
    
    # Обработчик фото
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
