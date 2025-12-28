"""
Email Sending Service via Gmail SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from utils.i18n import get_translation, DEFAULT_LANGUAGE


class EmailService:
    def __init__(self,
                 smtp_email: str = None,
                 smtp_password: str = None,
                 smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587):
        self._email = smtp_email or os.environ.get('SMTP_EMAIL', '')
        self._password = smtp_password or os.environ.get('SMTP_PASSWORD', '')
        self._server = smtp_server
        self._port = smtp_port
        self._enabled = bool(self._email and self._password)

        if not self._enabled:
            print("[EmailService] WARNING: Email not configured. Notifications will be console-only.")

    @property
    def is_enabled(self) -> bool:
        """Checks if email is configured."""
        return self._enabled

    def send(self, to_email: str, subject: str, body: str, html: bool = False) -> bool:
        print(f"[Email] Sending to {to_email}")
        print(f"  Subject: {subject}")

        if not self._enabled:
            print("  [SIMULATION] Email not configured, message not sent")
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self._email
            msg['To'] = to_email
            msg['Subject'] = subject

            content_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, content_type, 'utf-8'))

            with smtplib.SMTP(self._server, self._port) as server:
                server.starttls()
                server.login(self._email, self._password)
                server.send_message(msg)

            print(f"  [SUCCESS] Email sent to {to_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            print("  [ERROR] Invalid Gmail email or password")
            return False
        except smtplib.SMTPException as e:
            print(f"  [ERROR] SMTP error: {e}")
            return False
        except Exception as e:
            print(f"  [ERROR] Unknown error: {e}")
            return False

    def send_order_confirmation(self, order) -> bool:
        lang = getattr(order, 'language', DEFAULT_LANGUAGE)
        t = lambda key: get_translation(f'shop.email.{key}', lang)
        
        subject = f"🛒 {t('order_accepted')} #{order.id[:8]} - SDU SuperApp"

        items_html = ""
        for item in order.items:
            item_total = item['price'] * item['quantity']
            items_html += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #eee;">{item['name']}</td>
                <td style="padding: 12px; border-bottom: 1px solid #eee; text-align: center;">{item['quantity']}</td>
                <td style="padding: 12px; border-bottom: 1px solid #eee; text-align: right;">{item_total:.0f} ₸</td>
            </tr>
            """

        try:
            dt = datetime.fromisoformat(order.created_at)
            formatted_date = dt.strftime("%d.%m.%Y %H:%M")
        except:
            formatted_date = order.created_at[:16].replace('T', ' ')

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 30px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">
                ✅ {t('order_accepted')}
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;">
                {t('order_number')} #{order.id[:8]}
            </p>
            <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 12px;">
                📅 {formatted_date}
            </p>
        </div>
        
        <!-- Content -->
        <div style="padding: 30px;">
            <p style="color: #333; font-size: 16px; margin: 0 0 20px 0;">
                {t('hello')}, <strong>{order.customer_name}</strong>! 👋
            </p>
            
            <p style="color: #666; font-size: 15px; margin: 0 0 25px 0;">
                {t('order_success_message')}
            </p>
            
            <!-- Order Details -->
            <div style="background: #f8f9fa; border-radius: 12px; padding: 20px; margin-bottom: 25px;">
                <h3 style="color: #333; font-size: 16px; margin: 0 0 15px 0;">
                    📦 {t('order_details')}
                </h3>
                
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #e9ecef;">
                            <th style="padding: 10px; text-align: left; font-size: 13px;">{t('product')}</th>
                            <th style="padding: 10px; text-align: center; font-size: 13px;">{t('quantity')}</th>
                            <th style="padding: 10px; text-align: right; font-size: 13px;">{t('amount')}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                </table>
                
                <div style="margin-top: 15px; padding-top: 15px; border-top: 2px solid #11998e;">
                    <p style="margin: 0; font-size: 18px; font-weight: bold; color: #333; text-align: right;">
                        {t('total')} {order.total_amount:.0f} ₸
                    </p>
                </div>
            </div>
            
            <!-- Status -->
            <div style="background: #fff3cd; border-radius: 8px; padding: 15px; text-align: center;">
                <p style="margin: 0; color: #856404; font-size: 14px;">
                    ⏳ <strong>{t('status')}</strong> {t('status_pending')}
                </p>
                <p style="margin: 10px 0 0 0; color: #856404; font-size: 13px;">
                    {t('status_message')}
                </p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #888; font-size: 12px; margin: 0 0 10px 0;">
                {t('thanks')} 🎓
            </p>
            <p style="color: #aaa; font-size: 11px; margin: 0;">
                {t('copyright')}
            </p>
        </div>
    </div>
</body>
</html>
"""
        return self.send(order.customer_email, subject, html_body, html=True)

    def send_order_confirmed(self, order) -> bool:
        """Notification about order confirmation."""
        lang = getattr(order, 'language', DEFAULT_LANGUAGE)
        t = lambda key: get_translation(f'shop.email.{key}', lang)
        
        subject = f"✅ {t('order_confirmed')} #{order.id[:8]} - SDU SuperApp"

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 30px; text-align: center;">
            <div style="font-size: 50px; margin-bottom: 10px;">✅</div>
            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">
                {t('order_confirmed')}!
            </h1>
        </div>
        
        <!-- Content -->
        <div style="padding: 30px; text-align: center;">
            <p style="color: #333; font-size: 16px; margin: 0 0 20px 0;">
                {t('hello')}, <strong>{order.customer_name}</strong>! 👋
            </p>
            
            <div style="background: #d4edda; border-radius: 12px; padding: 25px; margin: 20px 0;">
                <p style="color: #155724; font-size: 18px; margin: 0 0 10px 0; font-weight: bold;">
                    {t('order_confirmed_message')} #{order.id[:8]}
                </p>
                <p style="color: #155724; font-size: 24px; margin: 0; font-weight: bold;">
                    💰 {order.total_amount:.0f} ₸
                </p>
            </div>
            
            <p style="color: #666; font-size: 15px; margin: 20px 0;">
                🚚 {t('order_will_be_delivered')}
            </p>
        </div>
        
        <!-- Footer -->
        <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #888; font-size: 12px; margin: 0 0 10px 0;">
                {t('thanks')} 🎓
            </p>
            <p style="color: #aaa; font-size: 11px; margin: 0;">
                {t('copyright')}
            </p>
        </div>
    </div>
</body>
</html>
"""
        return self.send(order.customer_email, subject, html_body, html=True)

    def send_order_cancelled(self, order) -> bool:
        """Notification about order cancellation."""
        lang = getattr(order, 'language', DEFAULT_LANGUAGE)
        t = lambda key: get_translation(f'shop.email.{key}', lang)
        
        subject = f"❌ {t('order_cancelled')} #{order.id[:8]} - SDU SuperApp"

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); padding: 30px; text-align: center;">
            <div style="font-size: 50px; margin-bottom: 10px;">❌</div>
            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">
                {t('order_cancelled')}
            </h1>
        </div>
        
        <!-- Content -->
        <div style="padding: 30px; text-align: center;">
            <p style="color: #333; font-size: 16px; margin: 0 0 20px 0;">
                {t('hello')}, <strong>{order.customer_name}</strong>!
            </p>
            
            <div style="background: #f8d7da; border-radius: 12px; padding: 25px; margin: 20px 0;">
                <p style="color: #721c24; font-size: 16px; margin: 0;">
                    {t('order_cancelled_reason')} <strong>#{order.id[:8]}</strong>
                </p>
            </div>
            
            <p style="color: #666; font-size: 15px; margin: 20px 0;">
                {t('contact_us')}
            </p>
            
            <p style="color: #888; font-size: 14px; margin: 20px 0;">
                📧 sdusuperapp@gmail.com
            </p>
        </div>
        
        <!-- Footer -->
        <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #888; font-size: 12px; margin: 0 0 10px 0;">
                {t('apologies')}
            </p>
            <p style="color: #aaa; font-size: 11px; margin: 0;">
                {t('copyright')}
            </p>
        </div>
    </div>
</body>
</html>
"""
        return self.send(order.customer_email, subject, html_body, html=True)

    def send_news_notification(self, subscriber_email: str, subscriber_name: str, news, base_url: str = "http://127.0.0.1:5001", language: str = DEFAULT_LANGUAGE) -> bool:
        """
        Sends notification about new news.

        Args:
            subscriber_email: Subscriber email
            subscriber_name: Subscriber name
            news: News object
            base_url: Site base URL
            language: Subscriber language (ru, en, kz)
        """
        lang = language
        t = lambda key: get_translation(f'shop.email.{key}', lang)
        
        # Get translated news title
        news_title = news.get_title(lang) if hasattr(news, 'get_title') else news.title
        news_content = news.get_content(lang) if hasattr(news, 'get_content') else news.content
        news_category = news.get_category(lang) if hasattr(news, 'get_category') else news.category
        
        subject = f"📰 {news_title} - SDU SuperApp"

        news_url = f"{base_url}/news/{news.id}"

        # Get publication date
        pub_date = news.created_at[:10] if hasattr(news, 'created_at') else t('today')

        # News image
        image_html = ""
        if hasattr(news, 'image') and news.image:
            image_html = f'''
            <div style="margin-bottom: 20px; border-radius: 12px; overflow: hidden;">
                <img src="{news.image}" alt="{news.title}" style="width: 100%; height: auto; display: block;">
            </div>
            '''

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        
        <!-- Header with Logo -->
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
            <div style="font-size: 40px; margin-bottom: 15px;">🎓</div>
            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: 1px;">
                SDU SuperApp
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 13px; text-transform: uppercase; letter-spacing: 2px;">
                {t('news_title')}
            </p>
        </div>
        
        <!-- Breaking News Banner -->
        <div style="background: linear-gradient(90deg, #e94560, #ff6b6b); padding: 12px; text-align: center;">
            <span style="color: white; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                🔔 {t('new_publication')}
            </span>
        </div>
        
        <!-- Content -->
        <div style="padding: 35px 30px;">
            <p style="color: #333; font-size: 16px; margin: 0 0 25px 0;">
                {t('hello')}, <span style="color: #667eea; font-weight: 600;">{subscriber_name}</span>! 👋
            </p>
            
            <!-- News Card -->
            <div style="background: #f8f9fa; border-radius: 16px; overflow: hidden; margin-bottom: 25px; border: 1px solid #eee; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                
                {image_html}
                
                <div style="padding: 25px;">
                    <!-- Category & Date -->
                    <div style="margin-bottom: 15px;">
                        <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                            {news_category}
                        </span>
                        <span style="color: #888; font-size: 12px; margin-left: 15px;">
                            📅 {t('date')} {pub_date}
                        </span>
                    </div>
                    
                    <!-- Title -->
                    <h2 style="color: #333; font-size: 22px; margin: 0 0 15px 0; line-height: 1.4; font-weight: 700;">
                        {news_title}
                    </h2>
                    
                    <!-- Author -->
                    <p style="color: #667eea; font-size: 13px; margin: 0 0 20px 0;">
                        ✍️ {t('author')} {news.author}
                    </p>
                    
                    <!-- Preview Text -->
                    <p style="color: #555; font-size: 15px; line-height: 1.7; margin: 0; border-left: 3px solid #667eea; padding-left: 15px;">
                        {news_content[:350]}{'...' if len(news_content) > 350 else ''}
                    </p>
                </div>
            </div>
            
            <!-- CTA Button -->
            <div style="text-align: center; margin: 35px 0;">
                <a href="{news_url}" 
                   style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; text-decoration: none; padding: 16px 45px; border-radius: 30px; 
                          font-weight: 700; font-size: 15px; text-transform: uppercase; letter-spacing: 1px;
                          box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);">
                    📖 {t('read_full')}
                </a>
            </div>
            
            <!-- Link -->
            <p style="color: #888; font-size: 12px; text-align: center; margin: 25px 0 0 0; word-break: break-all;">
                {t('link')} <a href="{news_url}" style="color: #667eea; text-decoration: none;">{news_url}</a>
            </p>
        </div>
        
        <!-- Footer -->
        <div style="background: #f8f9fa; padding: 25px 30px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #888; font-size: 11px; margin: 0 0 8px 0;">
                {t('unsubscribe_footer')}
            </p>
            <p style="color: #aaa; font-size: 10px; margin: 0;">
                {t('copyright')}
            </p>
        </div>
    </div>
</body>
</html>
"""
        return self.send(subscriber_email, subject, html_body, html=True)

    def send_news_update_notification(self, subscriber_email: str, subscriber_name: str, news, base_url: str = "http://127.0.0.1:5001", language: str = DEFAULT_LANGUAGE) -> bool:
        lang = language
        t = lambda key: get_translation(f'shop.email.{key}', lang)

        news_title = news.get_title(lang) if hasattr(news, 'get_title') else news.title
        news_content = news.get_content(lang) if hasattr(news, 'get_content') else news.content
        news_category = news.get_category(lang) if hasattr(news, 'get_category') else news.category
        
        subject = f"📝 {t('read_update')}: {news_title} - SDU SuperApp"

        news_url = f"{base_url}/news/{news.id}"

        pub_date = news.created_at[:10] if hasattr(news, 'created_at') else t('today')

        image_html = ""
        if hasattr(news, 'image') and news.image:
            image_html = f'''
            <div style="margin-bottom: 20px; border-radius: 12px; overflow: hidden;">
                <img src="{news.image}" alt="{news.title}" style="width: 100%; height: auto; display: block;">
            </div>
            '''

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        
        <!-- Header with Logo -->
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
            <div style="font-size: 40px; margin-bottom: 15px;">🎓</div>
            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: 1px;">
                SDU SuperApp
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 13px; text-transform: uppercase; letter-spacing: 2px;">
                {t('news_title')}
            </p>
        </div>
        
        <!-- Update Banner -->
        <div style="background: linear-gradient(90deg, #f39c12, #f1c40f); padding: 12px; text-align: center;">
            <span style="color: #333; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                📝 {t('news_updated')}
            </span>
        </div>
        
        <!-- Content -->
        <div style="padding: 35px 30px;">
            <p style="color: #333; font-size: 16px; margin: 0 0 25px 0;">
                {t('hello')}, <span style="color: #667eea; font-weight: 600;">{subscriber_name}</span>! 👋
            </p>
            
            <p style="color: #666; font-size: 15px; margin: 0 0 20px 0;">
                {t('news_updated_message')}
            </p>
            
            <!-- News Card -->
            <div style="background: #f8f9fa; border-radius: 16px; overflow: hidden; margin-bottom: 25px; border: 1px solid #f39c12; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                
                {image_html}
                
                <div style="padding: 25px;">
                    <!-- Category & Date -->
                    <div style="margin-bottom: 15px;">
                        <span style="background: linear-gradient(135deg, #f39c12, #f1c40f); color: #333; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                            {news_category}
                        </span>
                        <span style="color: #888; font-size: 12px; margin-left: 15px;">
                            📅 {t('date')} {pub_date}
                        </span>
                    </div>
                    
                    <!-- Title -->
                    <h2 style="color: #333; font-size: 22px; margin: 0 0 15px 0; line-height: 1.4; font-weight: 700;">
                        {news_title}
                    </h2>
                    
                    <!-- Author -->
                    <p style="color: #f39c12; font-size: 13px; margin: 0 0 20px 0;">
                        ✍️ {t('author')} {news.author}
                    </p>
                    
                    <!-- Preview Text -->
                    <p style="color: #555; font-size: 15px; line-height: 1.7; margin: 0; border-left: 3px solid #f39c12; padding-left: 15px;">
                        {news_content[:350]}{'...' if len(news_content) > 350 else ''}
                    </p>
                </div>
            </div>
            
            <!-- CTA Button -->
            <div style="text-align: center; margin: 35px 0;">
                <a href="{news_url}" 
                   style="display: inline-block; background: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%); 
                          color: #333; text-decoration: none; padding: 16px 45px; border-radius: 30px; 
                          font-weight: 700; font-size: 15px; text-transform: uppercase; letter-spacing: 1px;
                          box-shadow: 0 8px 25px rgba(243, 156, 18, 0.4);">
                    📖 {t('read_update')}
                </a>
            </div>
            
            <!-- Link -->
            <p style="color: #888; font-size: 12px; text-align: center; margin: 25px 0 0 0; word-break: break-all;">
                {t('link')} <a href="{news_url}" style="color: #f39c12; text-decoration: none;">{news_url}</a>
            </p>
        </div>
        
        <!-- Footer -->
        <div style="background: #f8f9fa; padding: 25px 30px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #888; font-size: 11px; margin: 0 0 8px 0;">
                {t('unsubscribe_footer')}
            </p>
            <p style="color: #aaa; font-size: 10px; margin: 0;">
                {t('copyright')}
            </p>
        </div>
    </div>
</body>
</html>
"""
        return self.send(subscriber_email, subject, html_body, html=True)


    def send_subscription_welcome(self, subscriber_email: str, subscriber_name: str, subscriber_id: str, base_url: str = "http://127.0.0.1:5001", language: str = DEFAULT_LANGUAGE) -> bool:
        from datetime import datetime
        
        lang = language
        t = lambda key: get_translation(f'shop.email.{key}', lang)
        
        subject = f"🎉 {t('subscription_welcome_title')} - SDU SuperApp"
        
        unsubscribe_url = f"{base_url}/news/unsubscribe/{subscriber_id}"
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        
        <!-- Header with Logo -->
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 50px 30px; text-align: center;">
            <div style="font-size: 60px; margin-bottom: 15px;">🎓</div>
            <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 700; letter-spacing: 1px;">
                SDU SuperApp
            </h1>
        </div>
        
        <!-- Welcome Banner -->
        <div style="background: linear-gradient(90deg, #667eea, #764ba2); padding: 20px; text-align: center;">
            <span style="color: white; font-size: 18px; font-weight: 600;">
                ✅ {t('subscription_welcome_title')}
            </span>
        </div>
        
        <!-- Content -->
        <div style="padding: 40px 30px;">
            <p style="color: #333; font-size: 18px; margin: 0 0 25px 0;">
                {t('hello')}, <span style="color: #11998e; font-weight: 700;">{subscriber_name}</span>! 👋
            </p>
            
            <p style="color: #555; font-size: 16px; line-height: 1.8; margin: 0 0 30px 0;">
                {t('subscription_welcome_message')}
            </p>
            
            <!-- Info Card -->
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 16px; padding: 25px; margin-bottom: 30px; border-left: 4px solid #11998e;">
                <p style="color: #333; font-size: 14px; margin: 0 0 10px 0;">
                    📧 <strong>Email:</strong> {subscriber_email}
                </p>
                <p style="color: #333; font-size: 14px; margin: 0;">
                    📅 <strong>{t('subscription_date')}</strong> {current_date}
                </p>
            </div>
            
            <!-- Features -->
            <div style="background: #fff; border: 2px solid #e9ecef; border-radius: 16px; padding: 25px; margin-bottom: 30px;">
                <h3 style="color: #333; font-size: 16px; margin: 0 0 20px 0; text-align: center;">
                    🌟 {t('what_you_receive')}
                </h3>
                <table style="width: 100%;">
                    <tr>
                        <td style="text-align: center; padding: 10px; width: 33.33%;">
                            <div style="font-size: 30px; margin-bottom: 10px;">📰</div>
                            <p style="color: #666; font-size: 13px; margin: 0;">{t('feature_news')}</p>
                        </td>
                        <td style="text-align: center; padding: 10px; width: 33.33%;">
                            <div style="font-size: 30px; margin-bottom: 10px;">🎓</div>
                            <p style="color: #666; font-size: 13px; margin: 0;">{t('feature_events')}</p>
                        </td>
                        <td style="text-align: center; padding: 10px; width: 33.33%;">
                            <div style="font-size: 30px; margin-bottom: 10px;">💡</div>
                            <p style="color: #666; font-size: 13px; margin: 0;">{t('feature_updates')}</p>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        
        <!-- Unsubscribe Section -->
        <div style="background: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #888; font-size: 13px; margin: 0 0 15px 0;">
                {t('unsubscribe_message')}
            </p>
            <a href="{unsubscribe_url}" 
               style="display: inline-block; background: #dc3545; color: white; text-decoration: none; 
                      padding: 12px 30px; border-radius: 25px; font-weight: 600; font-size: 14px;">
                ❌ {t('unsubscribe_button')}
            </a>
        </div>
        
        <!-- Footer -->
        <div style="background: #2d3436; padding: 25px 30px; text-align: center;">
            <p style="color: rgba(255,255,255,0.8); font-size: 12px; margin: 0 0 10px 0;">
                {t('copyright')}
            </p>
            <p style="color: rgba(255,255,255,0.5); font-size: 11px; margin: 0;">
                🎓 SDU SuperApp | Suleyman Demirel University
            </p>
        </div>
    </div>
</body>
</html>
"""
        return self.send(subscriber_email, subject, html_body, html=True)

_email_service = None


def get_email_service() -> EmailService:
    global _email_service
    if _email_service is None:
        try:
            from config import SMTP_EMAIL, SMTP_PASSWORD
            _email_service = EmailService(SMTP_EMAIL, SMTP_PASSWORD)
        except ImportError:
            _email_service = EmailService()
    return _email_service

