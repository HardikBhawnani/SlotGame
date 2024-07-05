from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import random

# Replace 'YOUR_API_TOKEN' with your actual API token
API_TOKEN = '6979753535:AAET2BRoGxNnOyumK0k8RzSMMLfsnQdmVzg'

# Dictionary to store user balances
user_balances = {}

# Symbols for the slot machine
symbols = ['🍒', '🍋', '🍊', '🍉', '🍇', '🔔', '⭐', '7️⃣']

def get_user_key(update: Update) -> str:
    """Generate a unique key for the user based on chat_id and user_id"""
    return f"{update.effective_chat.id}_{update.message.from_user.id}"

async def start(update: Update, context: CallbackContext) -> None:
    user_key = get_user_key(update)
    if user_key not in user_balances:
        user_balances[user_key] = 100  # Starting balance
    await update.message.reply_text('Welcome to the Slot Machine Bot! Type /spin to play. Your starting balance is 100.')

async def spin(update: Update, context: CallbackContext) -> None:
    user_key = get_user_key(update)
    bet = 10  # Fixed bet amount
    if user_balances[user_key] < bet:
        await update.message.reply_text('You do not have enough balance to play. Please start a new game with /start.')
        return
    
    result = [random.choice(symbols) for _ in range(3)]
    result_text = ' | '.join(result)
    await update.message.reply_text(result_text)
    
    if len(set(result)) == 1:
        win_amount = bet * 10
        user_balances[user_key] += win_amount
        await update.message.reply_text(f'Jackpot! 🎉 You won {win_amount} credits. Your new balance is {user_balances[user_key]}.')
    elif len(set(result)) == 2:
        win_amount = bet * 2
        user_balances[user_key] += win_amount
        await update.message.reply_text(f'Close! You won {win_amount} credits. Your new balance is {user_balances[user_key]}.')
    else:
        user_balances[user_key] -= bet
        await update.message.reply_text(f'Try again! You lost {bet} credits. Your new balance is {user_balances[user_key]}.')

async def balance(update: Update, context: CallbackContext) -> None:
    user_key = get_user_key(update)
    if user_key in user_balances:
        await update.message.reply_text(f'Your current balance is {user_balances[user_key]}.')
    else:
        await update.message.reply_text('You do not have a balance. Start a new game by typing /start.')

def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spin", spin))
    application.add_handler(CommandHandler("balance", balance))

    application.run_polling()

if __name__ == '__main__':
    main()
