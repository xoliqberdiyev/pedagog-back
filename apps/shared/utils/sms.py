from apps.users.tasks.sms import SendMessage


def send_message(phone, message):
    SendMessage.delay(phone, message)
