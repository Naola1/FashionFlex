from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.conf import settings
from .utils import Util

# Signal handler for the password reset token creation
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # URL for the frontend where the user will reset their password
    reset_url = f"http://127.0.0.1:8000/reset-password?token={reset_password_token.key}"
    
    # HTML email body content
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            .ii a[href] {{
                color: white !important;
            }}
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }}
            .button {{
                display: inline-block;
                margin: 20px 0;
                padding: 10px 15px;
                color: white;
                background-color: #007BFF;
                text-decoration: none;
                border-radius: 5px;
                
            }}
            h1 {{
                color: #333;
            }}
            p {{
                font-size: 16px;
                color: #555;
            }}
            a {{
                color: white;
            }}
            .button:hover {{
                background-color: #0056b3;
            }}
            footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #999;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Password Reset Request</h1>
            <p>Hello,</p>
            <p>Please use the following link to reset your password:</p>
            <div class="button"><a href="{reset_url}">Reset Your Password</a></div>
         
            <footer>
                <p>If you did not request this email, please ignore it.</p>
            </footer>
        </div>
    </body>
    </html>
    """

    # Email data
    email_data = {
        'email_subject': 'Password Reset Request',
        'email_body': email_body,
        'to_email': reset_password_token.user.email,
        
    }
     # Send the email using the utility function
    Util.send_email(email_data)
