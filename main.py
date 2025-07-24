import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()  # load token dari .env file

TOKEN = os.getenv("8405776515:AAHMnopWOecVZZi7gBx_oGSxG6ovVIlKyVU")
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"total": 0, "riwayat": []}
    await update.message.reply_text("Halo! Kirim /tambah [jumlah] [keterangan] untuk mencatat pengeluaranmu.")

async def tambah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {"total": 0, "riwayat": []}

    try:
        jumlah = int(context.args[0])
        keterangan = ' '.join(context.args[1:])
        user_data[user_id]["total"] += jumlah
        user_data[user_id]["riwayat"].append((jumlah, keterangan))
        await update.message.reply_text(f"✅ Dicatat: Rp{jumlah} - {keterangan}")
    except:
        await update.message.reply_text("Format salah. Gunakan: /tambah 10000 makan siang")

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    total = user_data.get(user_id, {}).get("total", 0)
    await update.message.reply_text(f"Total pengeluaranmu saat ini: Rp{total}")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"total": 0, "riwayat": []}
    await update.message.reply_text("🔄 Data pengeluaran direset.")

async def riwayat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    riwayat = user_data.get(user_id, {}).get("riwayat", [])
    if not riwayat:
        await update.message.reply_text("Belum ada pengeluaran yang dicatat.")
        return

    pesan = "🧾 Riwayat pengeluaran:\n"
    for jumlah, ket in riwayat:
        pesan += f"- Rp{jumlah} - {ket}\n"
    await update.message.reply_text(pesan)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tambah", tambah))
app.add_handler(CommandHandler("total", total))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("riwayat", riwayat))

print("Bot berjalan...")
app.run_polling()
