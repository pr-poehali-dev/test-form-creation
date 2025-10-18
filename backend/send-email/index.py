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
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
          <h2 style="color: #0EA5E9; border-bottom: 2px solid #0EA5E9; padding-bottom: 10px;">
            Результаты тестовой формы
          </h2>
          
          <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #555;">Личная информация</h3>
            <p><strong>Имя:</strong> {first_name}</p>
            <p><strong>Фамилия:</strong> {last_name}</p>
          </div>
          
          <div style="margin: 20px 0;">
            <h3 style="color: #555;">Ответы на вопросы</h3>
            
            <div style="margin: 15px 0;">
              <p style="margin: 5px 0;"><strong>1. Как вы оцениваете качество сервиса?</strong></p>
              <p style="margin: 5px 0; padding-left: 20px; color: #0EA5E9;">{question1}</p>
            </div>
            
            <div style="margin: 15px 0;">
              <p style="margin: 5px 0;"><strong>2. Что вам понравилось больше всего?</strong></p>
              <p style="margin: 5px 0; padding-left: 20px; color: #0EA5E9;">{question2}</p>
            </div>
            
            <div style="margin: 15px 0;">
              <p style="margin: 5px 0;"><strong>3. Дополнительные комментарии или предложения:</strong></p>
              <p style="margin: 5px 0; padding-left: 20px; background: #f8f9fa; padding: 10px; border-radius: 5px;">
                {question3}
              </p>
            </div>
          </div>
          
          <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #888; font-size: 12px;">
            <p>Это письмо отправлено автоматически с вашего сайта тестирования</p>
          </div>
        </div>
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
