import requests
import json

class Notification:
    """
    Instantiate a Notification object.

    Args:
        proxy (str): Proxy address
    """    
    def __init__(self, proxy=''):
        self.proxies = {}
        if proxy != '':
            proxies = {
                'http': proxy,
                'https': proxy,
            }

    
    # Sending message through webhook (Google Chat, Slack, etc)
    def send_google_chat_message(self, webhook_url, message):
        """
        Send message through webhook (Google Chat, Slack, etc).

        Args:
            webhook_url (str): Webhook URL
            message (str): Message to be sent

        Returns:
            result (str): Value is 'OK' when successful
        """
        headers = {'Content-type': 'application/json'}
        data = {'text': message}
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data), proxies=self.proxies)
        return 'OK'
    
    
    # Creating Google Chat card as described in https://developers.google.com/chat/how-tos/cards-onclick
    def create_google_chat_card(self, title, subtitle, image_url, image_alt_text, text, button_text, button_url):
        """
        Create Google Chat card.

        Args:
            title (str): Card title
            subtitle (str): Card subtitle
            image_url (str): Image URL
            image_alt_text (str): Image alt text
            text (str): Card text
            button_text (str): Button text
            button_url (str): Button URL

        Returns:
            card (dict): Card to be sent
        """
        card = {
            "cards": [
                {
                    "header": {
                        "title": title,
                        "subtitle": subtitle,
                        "imageUrl": image_url,
                        "imageStyle": "IMAGE"
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": text
                                    }
                                },
                                {
                                    "buttons": [
                                        {
                                            "textButton": {
                                                "text": button_text,
                                                "onClick": {
                                                    "openLink": {
                                                        "url": button_url
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        return card

    # Sending card to Google Chat 
    def send_google_chat_card(self, webhook_url, card):
        """
        Send card to Google Chat.

        Args:
            webhook_url (str): Webhook URL
            card (dict): Card to be sent

        Returns:
            result (str): Value is 'OK' when successful
        """
        headers = {'Content-type': 'application/json'}
        data = card
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data), proxies=self.proxies)
        return 'OK'

    # Sending email through SMTP
    def send_smtp_email(self, smtp_server, smtp_port, smtp_username, smtp_password, sender, recipient, subject, message):
        """
        Send email through SMTP.

        Args:
            smtp_server (str): SMTP server address
            smtp_port (str): SMTP port
            smtp_username (str): SMTP username
            smtp_password (str): SMTP password
            sender (str): Sender email address
            recipient (str): Recipient email address
            subject (str): Email subject
            message (str): Email message

        Returns:
            result (str): Value is 'OK' when successful
        """
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        text = msg.as_string()
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipient, text)
        server.quit()
        return 'OK'
    
    # Sending email through SMTP with attachment
    def send_smtp_email_with_attachment(self, smtp_server, smtp_port, smtp_username, smtp_password, sender, recipient, subject, message, attachment_path):
        """
        Send email through SMTP with attachment.

        Args:
            smtp_server (str): SMTP server address
            smtp_port (str): SMTP port
            smtp_username (str): SMTP username
            smtp_password (str): SMTP password
            sender (str): Sender email address
            recipient (str): Recipient email address
            subject (str): Email subject
            message (str): Email message
            attachment_path (str): Attachment file path

        Returns:
            result (str): Value is 'OK' when successful
        """
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        filename = os.path.basename(attachment_path)
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipient, text)
        server.quit()
        return 'OK'
    
    # Sending email through SMTP in HTML format
    def send_smtp_email_html(self, smtp_server, smtp_port, smtp_username, smtp_password, sender, recipient, subject, message):
        """
        Send email through SMTP in HTML format.

        Args:
            smtp_server (str): SMTP server address
            smtp_port (str): SMTP port
            smtp_username (str): SMTP username
            smtp_password (str): SMTP password
            sender (str): Sender email address
            recipient (str): Recipient email address
            subject (str): Email subject
            message (str): Email message

        Returns:
            result (str): Value is 'OK' when successful
        """
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipient, text)
        server.quit()
        return 'OK'
    
    # Sending email through SMTP in HTML format with attachment
    def send_smtp_email_html_with_attachment(self, smtp_server, smtp_port, smtp_username, smtp_password, sender, recipient, subject, message, attachment_path):
        """
        Send email through SMTP in HTML format with attachment.

        Args:
            smtp_server (str): SMTP server address
            smtp_port (str): SMTP port
            smtp_username (str): SMTP username
            smtp_password (str): SMTP password
            sender (str): Sender email address
            recipient (str): Recipient email address
            subject (str): Email subject
            message (str): Email message
            attachment_path (str): Attachment file path

        Returns:
            result (str): Value is 'OK' when successful
        """
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))
        filename = os.path.basename(attachment_path)
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipient, text)
        server.quit()
        return 'OK'
    

