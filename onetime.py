from mail import send_email_with_attachment
import datetime
import subprocess

file_path = "/home/reports/report.txt"

def start_monitoring(email):
    # perform monitoring tasks
    print("Monitoring process running.")

    subprocess.call(['sh', './scan.sh'])

    # file_path
    send_mail(email, file_path)

def send_mail(email, file_path):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    subject = (f"Report from a database monitoring: ({today})")
    body = "Please find the attached report."
    to_email = email
    from_email = "dbnagiosmonitoring@gmail.com"
    password = ""
    file_path = "/home/reports/report.txt"
    send_email_with_attachment(subject, body, to_email, from_email, password, file_path)
