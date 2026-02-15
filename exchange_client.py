# exchange_client.py
import ccxt
import pandas as pd
from datetime import datetime

class ExchangeClient:
    """
    الاتصال بمنصة التداول وتنفيذ الأوامر
    """
    
    def __init__(self, config):
        self.config = config
        self.exchange = None
        self.connect()
        
    def connect(self):
        """
        الاتصال بالمنصة
        """
        try:
            # استخدام Binance كمثال (يمكن تغييره)
            self.exchange = ccxt.binance({
                'apiKey': self.config.EXCHANGE_API_KEY,
                'secret': self.config.EXCHANGE_SECRET_KEY,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',  # أو 'future' للعقود الآجلة
                }
            })
            
            # تفعيل وضع الاختبار (sandbox)
            if self.config.TEST_MODE:
                self.exchange.set_sandbox_mode(True)
                print("🧪 وضع الاختبار مفعل - لا توجد أموال حقيقية")
            
            # اختبار الاتصال
            self.exchange.fetch_balance()
            print(f"✅ متصل بالمنصة: {self.exchange.name}")
            
        except Exception as e:
            print(f"❌ فشل الاتصال: {e}")
            raise e
    
    def fetch_ohlcv(self, limit=100):
        """
        جلب بيانات الشموع اليابانية
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(
                self.config.SYMBOL, 
                timeframe=self.config.TIMEFRAME, 
                limit=limit
            )
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"❌ فشل جلب البيانات: {e}")
            return None
    
    def get_balance(self):
        """
        الحصول على الرصيد
        """
        try:
            balance = self.exchange.fetch_balance()
            usdt_balance = balance['USDT']['free'] if 'USDT' in balance['free'] else 0
            return usdt_balance
        except:
            return 10000  # قيمة افتراضية للاختبار
    
    def place_order(self, signal, amount):
        """
        تنفيذ أمر شراء أو بيع
        """
        try:
            if signal == 'BUY':
                order = self.exchange.create_market_buy_order(
                    self.config.SYMBOL, 
                    amount
                )
                print(f"✅ أمر شراء: {amount} {self.config.SYMBOL}")
                
            elif signal == 'SELL':
                order = self.exchange.create_market_sell_order(
                    self.config.SYMBOL, 
                    amount
                )
                print(f"✅ أمر بيع: {amount} {self.config.SYMBOL}")
            else:
                return None
            
            return order
            
        except Exception as e:
            print(f"❌ فشل تنفيذ الأمر: {e}")
            return None
    
    def get_current_price(self):
        """
        الحصول على السعر الحالي
        """
        try:
            ticker = self.exchange.fetch_ticker(self.config.SYMBOL)
            return ticker['last']
        except:
            return 2000  # قيمة افتراضية للاختبار
