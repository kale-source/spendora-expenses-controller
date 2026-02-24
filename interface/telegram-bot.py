from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá, sou a Spendora, sua assistente financeira. Você deseja criar seu controle financeiro por aqui?")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Para criar seu controle financeiro, basta enviar uma mensagem com /adicionar <valor> \nE seguir os proximos passos!")
    
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.split(" ")

    if len(user_text) == 1:
        await update.message.reply_text("Sera necessario adicionar um valor para salvar.")
        return None

    price = user_text[1]

    if int(price) <= 0:
        await update.message.reply_text("O valor da sua transação não pode ser negativo.")
        return None
    
    await update.message.reply_text(f"O valor da sua transação é: {price}")

app = Application.builder().token(bot_token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("adicionar", add))

app.run_polling()