# logger.py
import logging
import os
from datetime import datetime

class BotLogger:
    """
    تسجيل جميع عمليات البوت
    """
    
    def __init__(self, log_file='trading_bot.log'):
        self.logger = logging.getLogger('TradingBot')
        self.logger.setLevel(logging.INFO)
        
        # إنشاء مجلد logs إذا لم يكن موجوداً
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # ملف تسجيل مع التاريخ
        log_filename = f"logs/{datetime.now().strftime('%Y%m%d')}_{log_file}"
        
        # إعداد الملف
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)
        
        # إعداد الكونسول
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # تنسيق الرسائل
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def trade(self, action, price, amount, pnl=None):
        """
        تسجيل صفقة
        """
        msg = f"TRADE - {action} | السعر: {price} | الكمية: {amount}"
        if pnl:
            msg += f" | الربح/الخسارة: {pnl}"
        self.logger.info(msg)
