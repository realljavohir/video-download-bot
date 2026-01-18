from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import yt_dlp
import os

# 🔑 TOKENNI BU YERGA QO‘Y
TOKEN = "8383539672:AAH6P243Io-0o7bbP2d15-VMlAtXViLVjts"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\n\n"
        "📥 YouTube / TikTok / Instagram link yubor\n"
        "🎬 Video yuklab beraman"
    )

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    url = update.message.text.strip()

    if not any(x in url for x in ["youtube.com", "youtu.be", "tiktok.com", "instagram.com"]):
        await update.message.reply_text("❌ To‘g‘ri YouTube / TikTok / Instagram link yubor!")
        return

    msg = await update.message.reply_text("⏳ Yuklanmoqda, kuting...")

    ydl_opts = {
      "outtmpl": "%(title).50s.%(ext)s",
      "format": "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/mp4",
      "noplaylist": True,
      "quiet": True,
      "merge_output_format": "mp4",
  }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(
            video=open(filename, "rb"),
            caption="✅ Yuklab olindi"
        )

        os.remove(filename)
        await msg.delete()

    except Exception as e:
        await msg.edit_text("❌ Xatolik yuz berdi. Boshqa link bilan urinib ko‘ring.")
        print("XATO:", e)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, downloader))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
