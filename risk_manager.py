# risk_manager.py
import pandas as pd
from datetime import datetime, timedelta

class RiskManager:
    """
    إدارة المخاطر وحماية رأس المال
    """
    
    def __init__(self, config, exchange_client):
        self.config = config
        self.exchange = exchange_client
        self.daily_trades = []
        self.daily_pnl = 0
        self.last_reset = datetime.now()
        
    def reset_daily_stats(self):
        """
        إعادة تعيين الإحصائيات اليومية
        """
        now = datetime.now()
        if now.date() > self.last_reset.date():
            self.daily_trades = []
            self.daily_pnl = 0
            self.last_reset = now
            print(f"📊 تم إعادة تعيين الإحصائيات اليومية - التاريخ: {now.date()}")
    
    def check_daily_loss_limit(self):
        """
        التحقق من حد الخسارة اليومي
        """
        self.reset_daily_stats()
        
        # حساب نسبة الخسارة من رأس المال
        balance = self.exchange.get_balance()
        loss_percent = (self.daily_pnl / balance) * 100 if balance > 0 else 0
        
        if loss_percent <= -self.config.MAX_DAILY_LOSS:
            print(f"⚠️ تم تجاوز حد الخسارة اليومي ({loss_percent:.2f}%) - إيقاف التداول")
            return False
        return True
    
    def calculate_position_size(self, balance, stop_loss_percent):
        """
        حساب حجم الصفقة بناءً على نسبة المخاطرة
        """
        risk_amount = balance * (self.config.MAX_RISK_PERCENT / 100)
        position_size = risk_amount / (balance * stop_loss_percent / 100)
        
        # تطبيق حدود الحد الأدنى والأقصى
        min_size = 0.001
        max_size = 1.0
        
        position_size = max(min_size, min(position_size, max_size))
        
        print(f"📈 حجم الصفقة المحسوب: {position_size:.4f} (المخاطرة: ${risk_amount:.2f})")
        return position_size
    
    def add_trade(self, trade_result):
        """
        إضافة صفقة للإحصائيات
        """
        self.daily_trades.append(trade_result)
        if 'pnl' in trade_result:
            self.daily_pnl += trade_result['pnl']
        
        print(f"📝 تم إضافة الصفقة - إجمالي اليوم: ${self.daily_pnl:.2f}")
