import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_reset_email(to_email: str, token: str):
    reset_link = f"http://localhost:8080/reset-password?token={token}"

    # HTML email body
    body = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333333;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 100%;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .email-content {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    margin: 0 auto;
                }}
                h1 {{
                    color: #333333;
                    font-size: 24px;
                }}
                p {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #555555;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #007bff;
                    color: #ffffff !important;
                    padding: 12px 20px;
                    border-radius: 4px;
                    text-decoration: none;
                    font-size: 16px;
                    margin-top: 20px;
                }}
                .footer {{
                    font-size: 12px;
                    color: #777777;
                    margin-top: 20px;
                }}
                .footer a {{
                    color: #007bff;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="email-content">
                    <h1>Reset Your Password</h1>
                    <p>Hi,</p>
                    <p>We received a request to reset your password for your account on <strong>MumbaiPCMart</strong>.</p>
                    <p>If you made this request, click the button below to reset your password:</p>
                    <a href="{reset_link}" class="btn">Reset Password</a>
                    <p>If you did not request this, please ignore this email.</p>
                    <p>Thank you,</p>
                    <p><strong>The MumbaiPCMart Team</strong></p>
                    <div class="footer">
                        <p>If you have any questions, feel free to <a href="mailto:support@mumbaipcmart.com">contact our support team</a>.</p>
                        <p>© 2025 MumbaiPCMart. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

    # Create the message container
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset Your Password"
    msg["From"] = "no-reply@mumbaipcmart.com"
    msg["To"] = to_email

    # Attach the HTML body to the email
    part = MIMEText(body, "html")
    msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("jaikalki02@gmail.com", "qyxk fyfo xpbm cmvh")
        server.send_message(msg)
