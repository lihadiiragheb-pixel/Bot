# main.py
import time
import schedule
from datetime import datetime
import signal
import sys

from config import Config
from exchange_client import ExchangeClient
from strategy import RSI_BB_Strategy
from risk_manager import RiskManager
from logger import BotLogger

class GoldTradingBot:
    """
    البوت الرئيسي لتداول الذهب
    """
    
    def __init__(self):
        self.config = Config()
        self.logger = BotLogger()
        self.exchange = ExchangeClient(self.config)
        self.strategy = RSI_BB_Strategy(self.config)
        self.risk_manager = RiskManager(self.config, self.exchange)
        
        self.is_running = False
        self.last_signal = 'HOLD'
        self.position = None
        
        # إشارة لإيقاف البوت
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        
        self.logger.info("🚀 بدء تشغيل بوت تداول الذهب")
        self.logger.info(f"⚙️ الإعدادات: {self.config.SYMBOL}, {self.config.TIMEFRAME}")
    
    def check_market(self):
        """
        التحقق من السوق واتخاذ القرار
        """
        try:
            # جلب البيانات
            df = self.exchange.fetch_ohlcv(limit=100)
            if df is None:
                return
            
            # حساب المؤشرات
            df = self.strategy.calculate_indicators(df)
            
            # توليد الإشارة
            signal = self.strategy.generate_signal(df)
            
            # التحقق من المخاطر
            if not self.risk_manager.check_daily_loss_limit():
                return
            
            # الحصول على الرصيد والسعر
            balance = self.exchange.get_balance()
            current_price = self.exchange.get_current_price()
            
            # تنفيذ الصفقة إذا كان هناك إشارة جديدة
            if signal != 'HOLD' and signal != self.last_signal:
                # حساب حجم الصفقة
                position_size = self.risk_manager.calculate_position_size(
                    balance, 
                    self.config.STOP_LOSS_PERCENT
                )
                
                # تنفيذ الأمر
                order = self.exchange.place_order(signal, position_size)
                
                if order:
                    self.logger.trade(signal, current_price, position_size)
                    self.last_signal = signal
                    
                    # تحديث المركز
                    if signal == 'BUY':
                        self.position = {'type': 'BUY', 'price': current_price, 'size': position_size}
                    elif signal == 'SELL':
                        self.position = {'type': 'SELL', 'price': current_price, 'size': position_size}
            
            # عرض حالة السوق
            self.display_market_status(df, signal, current_price)
            
        except Exception as e:
            self.logger.error(f"خطأ في التحقق من السوق: {e}")
    
    def display_market_status(self, df, signal, current_price):
        """
        عرض حالة السوق
        """
        latest = df.iloc[-1]
        print("\n" + "="*50)
        print(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💰 السعر الحالي: {current_price:.2f}")
        print(f"📊 RSI: {latest['rsi']:.2f}")
        print(f"📉 الحد السفلي BB: {latest['bb_lower']:.2f}")
        print(f"📈 الحد العلوي BB: {latest['bb_upper']:.2f}")
        print(f"🔔 الإشارة: {signal}")
        print("="*50)
    
    def run(self):
        """
        تشغيل البوت بشكل دوري
        """
        self.is_running = True
        
        # جدولة المهام
        schedule.every(5).minutes.do(self.check_market)  # كل 5 دقائق
        
        # تشغيل فوري عند البدء
        self.check_market()
        
        self.logger.info("✅ البوت يعمل - في انتظار الإشارات...")
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop(self, signum=None, frame=None):
        """
        إيقاف البوت
        """
        self.logger.info("🛑 إيقاف البوت...")
        self.is_running = False
        
        # إغلاق أي مراكز مفتوحة إذا لزم الأمر
        if self.position:
            self.logger.warning("⚠️ يوجد مركز مفتوح - يرجى الإغلاق يدوياً")
        
        sys.exit(0)

# نقطة الدخول الرئيسية
if __name__ == "__main__":
    bot = GoldTradingBot()
    bot.run()
