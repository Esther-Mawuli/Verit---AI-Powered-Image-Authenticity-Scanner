import logging
from datetime import datetime
import boto3  # Add boto3 to requirements.txt

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/var/log/verit/app.log'),
            logging.StreamHandler()
        ]
    )

def log_scan_attempt(filename, result, ip_address):
    logging.info(f"Scan attempted: {filename}, Result: {result}, IP: {ip_address}")

def send_alert(message):
    # Integrate with AWS SNS for alerts
    try:
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='YOUR_SNS_TOPIC_ARN',
            Message=message,
            Subject='Verit Security Alert'
        )
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")