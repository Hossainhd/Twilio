#Copyright @ISmartCoder
#Updates Channel https://t.me/TheSmartDev
from app import app
from utils import LOGGER
from config import DEVELOPER_ID, check_channel_subscription, send_subscription_message, is_user_subscribed
from pyrogram import idle, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
import asyncio

async def handle_subscription_check(_, query):
    """Handle subscription check callback"""
    user_id = query.from_user.id
    not_joined = await check_channel_subscription(user_id, app)
    
    if not not_joined:
        await query.message.edit_text(
            "✅ **Subscription Verified!**\n\n"
            "You can now use the bot. Send /help to see available commands.",
            reply_markup=None
        )
    else:
        await query.answer(
            f"You still need to join: {', '.join(not_joined)}", 
            show_alert=True
        )

async def check_subscription_on_start(_, message):
    """Check subscription when user starts the bot"""
    user_id = message.from_user.id
    
    # Check if user is subscribed
    if await is_user_subscribed(user_id, app):
        # User is subscribed, show welcome message
        await message.reply_text(
            "🤖 **Welcome to Twilio SMS Bot!**\n\n"
            "Use /help to see available commands.\n"
            "Use /login to connect your Twilio account.",
            reply_markup=None
        )
    else:
        # User not subscribed, show join message
        await send_subscription_message(app, user_id)

async def main():
    # Add subscription check handler
    app.add_handler(MessageHandler(check_subscription_on_start, filters.command("start")))
    app.add_handler(CallbackQueryHandler(handle_subscription_check, filters.regex("^check_subscription$")))
    
    await app.start()
    LOGGER.info("Bot Successfully Started💥")
    
    if DEVELOPER_ID:
        try:
            await app.send_message(
                int(DEVELOPER_ID),
                "**Bot Successfully Started💥**\n"
                "Channel subscription system is active!"
            )
            LOGGER.info(f"Sent startup confirmation to DEVELOPER_ID: {DEVELOPER_ID}")
        except Exception as e:
            LOGGER.error(f"Could not send startup message to DEVELOPER_ID: {e}")
    
    await idle()
    await app.stop()
    LOGGER.info("Bot Stopped Successfully.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())