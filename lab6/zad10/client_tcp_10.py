import smtplib

with smtplib.SMTP('127.0.0.1', 2912) as server:
    server.set_debuglevel(1)
    server.helo()
    server.mail('sender@example.com')
    server.rcpt('recipient@example.com')
    server.data('Subject: Test\n\nThis is a test email.')
    server.quit()