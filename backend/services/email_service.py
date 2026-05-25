import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_otp_email(to_email: str, user_name: str, otp_code: str) -> bool:
    """OTP kodunu email ile gönder. Başarılıysa True döner."""
    mail_username = os.getenv('MAIL_USERNAME', '')
    mail_password = os.getenv('MAIL_PASSWORD', '')
    mail_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    mail_port = int(os.getenv('MAIL_PORT', 587))
    
    if not mail_username or not mail_password:
        # Email servisi yapılandırılmamış - geliştirme modunda console'a yaz
        print(f"\n{'='*50}")
        print(f"📧 OTP Email (DEV MODE - Gerçek email gönderilmedi)")
        print(f"To: {to_email}")
        print(f"OTP Kodu: {otp_code}")
        print(f"{'='*50}\n")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🌸 SkinSense AI — Şifre Sıfırlama Kodunuz'
        msg['From'] = mail_username
        msg['To'] = to_email
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Outfit', Arial, sans-serif; background: #FDF8F5; margin: 0; padding: 0; }}
                .container {{ max-width: 500px; margin: 40px auto; background: white; border-radius: 24px; overflow: hidden; box-shadow: 0 10px 40px rgba(203,153,167,0.2); }}
                .header {{ background: linear-gradient(135deg, #E8B4B8 0%, #C89FC5 100%); padding: 40px 30px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; letter-spacing: -0.5px; }}
                .header p {{ color: rgba(255,255,255,0.85); margin: 8px 0 0; }}
                .body {{ padding: 40px 30px; }}
                .body p {{ color: #5a4a6a; line-height: 1.6; }}
                .otp-box {{ background: linear-gradient(135deg, #FDF0F2, #F5EEFF); border: 2px dashed #C89FC5; border-radius: 16px; padding: 24px; text-align: center; margin: 24px 0; }}
                .otp-code {{ font-size: 42px; font-weight: 800; color: #9B72CF; letter-spacing: 10px; margin: 0; }}
                .otp-note {{ font-size: 13px; color: #9B72CF; margin-top: 8px; }}
                .footer {{ background: #FDF8F5; padding: 20px 30px; text-align: center; font-size: 12px; color: #a08090; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌸 SkinSense AI</h1>
                    <p>Kişisel Cilt Bakım Asistanınız</p>
                </div>
                <div class="body">
                    <p>Merhaba <strong>{user_name}</strong>,</p>
                    <p>Şifrenizi sıfırlamak için aşağıdaki OTP kodunu kullanın:</p>
                    <div class="otp-box">
                        <p class="otp-code">{otp_code}</p>
                        <p class="otp-note">Bu kod 10 dakika geçerlidir</p>
                    </div>
                    <p>Bu işlemi siz yapmadıysanız, bu emaili görmezden gelebilirsiniz.</p>
                    <p>Sağlıklı günler diliyoruz ✨</p>
                    <p><strong>SkinSense AI Ekibi</strong></p>
                </div>
                <div class="footer">
                    <p>© 2024 SkinSense AI • Bu email otomatik olarak gönderilmiştir.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        part = MIMEText(html, 'html', 'utf-8')
        msg.attach(part)
        
        with smtplib.SMTP(mail_server, mail_port) as server:
            server.starttls()
            server.login(mail_username, mail_password)
            server.sendmail(mail_username, to_email, msg.as_string())
        
        return True
    except Exception as e:
        print(f"Email gönderme hatası: {e}")
        print(f"DEV OTP for {to_email}: {otp_code}")
        return False
