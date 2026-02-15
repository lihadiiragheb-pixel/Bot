# strategy.py
import pandas as pd
import ta

class RSI_BB_Strategy:
    """
    استراتيجية التداول باستخدام RSI و Bollinger Bands
    """
    
    def __init__(self, config):
        self.config = config
        self.rsi_period = config.RSI_PERIOD
        self.bb_period = config.BB_PERIOD
        self.bb_std = config.BB_STD
        
    def calculate_indicators(self, df):
        """
        حساب المؤشرات الفنية
        """
        # حساب RSI
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=self.rsi_period).rsi()
        
        # حساب Bollinger Bands
        bb = ta.volatility.BollingerBands(
            df['close'], 
            window=self.bb_period, 
            window_dev=self.bb_std
        )
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()
        
        return df
    
    def generate_signal(self, df):
        """
        توليد إشارات التداول
        """
        if len(df) < max(self.rsi_period, self.bb_period):
            return 'HOLD'
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # شروط الشراء
        buy_conditions = (
            latest['close'] <= latest['bb_lower'] and  # السعر عند الحد السفلي
            latest['rsi'] < self.config.RSI_OVERSOLD and  # RSI في ذروة البيع
            latest['close'] > prev['close']  # بداية ارتداد
        )
        
        # شروط البيع
        sell_conditions = (
            latest['close'] >= latest['bb_upper'] and  # السعر عند الحد العلوي
            latest['rsi'] > self.config.RSI_OVERBOUGHT and  # RSI في ذروة الشراء
            latest['close'] < prev['close']  # بداية هبوط
        )
        
        if buy_conditions:
            return 'BUY'
        elif sell_conditions:
            return 'SELL'
        else:
            return 'HOLD'
