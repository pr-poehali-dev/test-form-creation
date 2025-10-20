import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Send test form results via email
    Args: event with httpMethod, body containing form data
    Returns: HTTP response with success/error status
    '''
    method: str = event.get('httpMethod', 'POST')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    if method != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    body_data = json.loads(event.get('body', '{}'))
    
    first_name = body_data.get('firstName', '')
    last_name = body_data.get('lastName', '')
    question1 = body_data.get('question1', '')
    question2 = body_data.get('question2', '')
    question3 = body_data.get('question3', '')
    
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    recipient_email = 'ptizaforest.89@gmail.com'
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'Новые результаты теста от {first_name} {last_name}'
    msg['From'] = smtp_user
    msg['To'] = recipient_email
    
    html_content = f'''
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
      </head>
      <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 40px 20px;">
          <tr>
            <td align="center">
              <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden;">
                
                <tr>
                  <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                    <div style="background-color: rgba(255, 255, 255, 0.2); width: 80px; height: 80px; border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;">
                      <span style="font-size: 40px;">📋</span>
                    </div>
                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">Новая заявка с формы</h1>
                    <p style="margin: 10px 0 0; color: rgba(255, 255, 255, 0.9); font-size: 16px;">Получен новый ответ от пользователя</p>
                  </td>
                </tr>
                
                <tr>
                  <td style="padding: 40px 30px;">
                    
                    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; padding: 25px; margin-bottom: 30px;">
                      <h2 style="margin: 0 0 20px 0; color: #ffffff; font-size: 20px; font-weight: 600; display: flex; align-items: center;">
                        <span style="margin-right: 10px;">👤</span> Личная информация
                      </h2>
                      <table width="100%" cellpadding="8" cellspacing="0">
                        <tr>
                          <td style="color: rgba(255, 255, 255, 0.9); font-size: 14px; font-weight: 500;">Имя:</td>
                          <td style="color: #ffffff; font-size: 16px; font-weight: 600; text-align: right;">{first_name}</td>
                        </tr>
                        <tr>
                          <td style="color: rgba(255, 255, 255, 0.9); font-size: 14px; font-weight: 500;">Фамилия:</td>
                          <td style="color: #ffffff; font-size: 16px; font-weight: 600; text-align: right;">{last_name}</td>
                        </tr>
                      </table>
                    </div>
                    
                    <h2 style="margin: 0 0 25px 0; color: #333333; font-size: 22px; font-weight: 600; display: flex; align-items: center;">
                      <span style="margin-right: 10px;">❓</span> Ответы на вопросы
                    </h2>
                    
                    <div style="border-left: 4px solid #667eea; background-color: #f8f9ff; padding: 20px; margin-bottom: 20px; border-radius: 8px;">
                      <p style="margin: 0 0 10px 0; color: #666; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Вопрос 1</p>
                      <p style="margin: 0 0 8px 0; color: #333; font-size: 15px; font-weight: 500;">Как вы оцениваете качество сервиса?</p>
                      <p style="margin: 0; color: #667eea; font-size: 18px; font-weight: 700;">✓ {question1}</p>
                    </div>
                    
                    <div style="border-left: 4px solid #f5576c; background-color: #fff5f7; padding: 20px; margin-bottom: 20px; border-radius: 8px;">
                      <p style="margin: 0 0 10px 0; color: #666; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Вопрос 2</p>
                      <p style="margin: 0 0 8px 0; color: #333; font-size: 15px; font-weight: 500;">Что вам понравилось больше всего?</p>
                      <p style="margin: 0; color: #f5576c; font-size: 18px; font-weight: 700;">✓ {question2}</p>
                    </div>
                    
                    <div style="border-left: 4px solid #4ade80; background-color: #f0fdf4; padding: 20px; border-radius: 8px;">
                      <p style="margin: 0 0 10px 0; color: #666; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Вопрос 3</p>
                      <p style="margin: 0 0 12px 0; color: #333; font-size: 15px; font-weight: 500;">Дополнительные комментарии или предложения:</p>
                      <div style="background-color: #ffffff; padding: 15px; border-radius: 6px; border: 1px solid #d1fae5;">
                        <p style="margin: 0; color: #333; font-size: 16px; line-height: 1.6;">{question3}</p>
                      </div>
                    </div>
                    
                  </td>
                </tr>
                
                <tr>
                  <td style="background-color: #f9fafb; padding: 25px 30px; border-top: 1px solid #e5e7eb;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="color: #9ca3af; font-size: 13px; line-height: 1.5;">
                          <p style="margin: 0 0 5px 0;">📧 Это автоматическое уведомление с вашего сайта</p>
                          <p style="margin: 0; color: #d1d5db;">Отправлено из формы тестирования</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
                
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    '''
    
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'isBase64Encoded': False,
            'body': json.dumps({'success': True, 'message': 'Email sent successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'isBase64Encoded': False,
            'body': json.dumps({'success': False, 'error': str(e)})
        }