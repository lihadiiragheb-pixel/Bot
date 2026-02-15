# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys (تخزن في .env)
    EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY')
    EXCHANGE_SECRET_KEY = os.getenv('EXCHANGE_SECRET_KEY')
    
    # إعدادات التداول
    SYMBOL = 'XAU/USDT'  # زوج الذهب
    TIMEFRAME = '5m'      # الإطار الزمني
    LOT_SIZE = 0.01       # حجم الصفقة
    
    # استراتيجية RSI
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    
    # استراتيجية Bollinger Bands
    BB_PERIOD = 20
    BB_STD = 2.0
    
    # إدارة المخاطر
    MAX_RISK_PERCENT = 2.0      # 2% من رأس المال كحد أقصى للخسارة
    STOP_LOSS_PERCENT = 0.5     # 0.5% وقف الخسارة
    TAKE_PROFIT_PERCENT = 1.0   # 1% جني الأرباح
    MAX_DAILY_LOSS = 5.0        # 5% كحد أقصى للخسارة اليومية
    
    # إعدادات Render
    PORT = int(os.getenv('PORT', 10000))
    RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL', 'http://localhost:5000')
    
    # وضع الاختبار
    TEST_MODE = True  # True = حساب تجريبي، False = حساب حقيقي
