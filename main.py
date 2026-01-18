import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\n"
        "📥 YouTube / TikTok / Instagram link yubor\n"
        "🎬 Video yuklab beraman"
    )

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    msg = await update.message.reply_text("⏳ Yuklanmoqda...")

    ydl_opts = {
        "format": "mp4",
        "outtmpl": "video.%(ext)s",
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(
            video=open("video.mp4", "rb"),
            caption="✅ Tayyor"
        )

        os.remove("video.mp4")
        await msg.delete()

    except Exception as e:
        await msg.edit_text("❌ Xatolik yuz berdi")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, downloader))

    app.run_polling()

if __name__ == "__main__":
    main()
