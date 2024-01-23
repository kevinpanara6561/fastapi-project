def forgot_password(name: str, otp: str):
    html = """
<html>
    <body>
        <p>Hi <strong>###NAME###</strong>, your OTP for password reset is <strong>###OTP###</strong> and it's valid for 10 minutes.</p>
    </body>
</html>
    """
    html = html.replace("###NAME###", name)
    html = html.replace("###OTP###", otp)
    return html
