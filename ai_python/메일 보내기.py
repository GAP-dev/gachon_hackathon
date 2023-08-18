import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 이메일 설정
sender_email = 'charly20@gachon.ac.kr'  # 발신자 이메일 주소
sender_password = '1234'     # 발신자 이메일 비밀번호

receiver_email = 'recipient@example.com'  # 수신자 이메일 주소

subject = 'Matching!'
message = '매칭되었습니다!'

# 이메일 보내기
try:
    # 이메일 서버 연결
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)

    # 이메일 메시지 작성
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # 이메일 전송
    smtp_server.sendmail(sender_email, receiver_email, msg.as_string())
    print("이메일이 성공적으로 전송되었습니다.")

except Exception as e:
    print("이메일 전송 중 오류가 발생했습니다.")
    print(e)

finally:
    # 이메일 서버 연결 종료
    smtp_server.quit()
