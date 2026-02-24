"""
Error Handler - Global error handling
"""
import logging
import traceback
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors in the bot"""
    logger.error("Exception while handling an update:", exc_info=context.error)
    
    # Get traceback
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    
    logger.error(f"Traceback:\n{tb_string}")
    
    # Notify user
    try:
        if isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again later.\n"
                "If the problem persists, contact support."
            )
    except Exception as e:
        logger.error(f"Failed to send error message to user: {e}")
