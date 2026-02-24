"""
Admin Handler - Handles administrative commands
"""
import logging
import shutil
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from managers.user_manager import UserManager
from config import Config

logger = logging.getLogger(__name__)


class AdminHandler:
    """Handles admin-only commands"""
    
    def __init__(self, user_manager: UserManager, config: Config):
        self.user_manager = user_manager
        self.config = config
    
    def _is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id == self.config.ADMIN_ID
    
    async def backup_db(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Backup database file"""
        user_id = update.effective_user.id
        
        if not self._is_admin(user_id):
            await update.message.reply_text("⛔️ Unauthorized. Admin only.")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backups/language_bot_backup_{timestamp}.db"
            
            # Create backup directory if not exists
            import os
            os.makedirs("backups", exist_ok=True)
            
            # Copy database
            shutil.copy2(self.config.DB_PATH, backup_path)
            
            # Send backup file
            with open(backup_path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename=f"backup_{timestamp}.db",
                    caption=f"✅ Database backup created\n{timestamp}"
                )
            
            logger.info(f"✅ Admin {user_id} created database backup")
        
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            await update.message.reply_text(f"❌ Backup failed: {str(e)}")
    
    async def restore_db(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Restore database from file"""
        user_id = update.effective_user.id
        
        if not self._is_admin(user_id):
            await update.message.reply_text("⛔️ Unauthorized. Admin only.")
            return
        
        # Check if message has document
        if not update.message.document:
            await update.message.reply_text(
                "📎 Please send the backup file with /restore command."
            )
            return
        
        try:
            # Download file
            file = await context.bot.get_file(update.message.document.file_id)
            restore_path = "restore_temp.db"
            await file.download_to_drive(restore_path)
            
            # Backup current database
            backup_current = f"backups/before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            import os
            os.makedirs("backups", exist_ok=True)
            shutil.copy2(self.config.DB_PATH, backup_current)
            
            # Restore
            shutil.copy2(restore_path, self.config.DB_PATH)
            
            # Cleanup
            os.remove(restore_path)
            
            await update.message.reply_text(
                "✅ Database restored successfully!\n"
                f"Previous database backed up to:\n{backup_current}"
            )
            
            logger.info(f"✅ Admin {user_id} restored database")
        
        except Exception as e:
            logger.error(f"❌ Restore failed: {e}")
            await update.message.reply_text(f"❌ Restore failed: {str(e)}")
