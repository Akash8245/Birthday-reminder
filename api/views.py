from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Person
from datetime import timedelta
import pytz
from twilio.rest import Client
import os
from dotenv import load_dotenv
import logging
 
load_dotenv()

def send_alerts(request):
    IST = pytz.timezone('Asia/Kolkata')
    now = timezone.now().astimezone(IST)

    if now.hour == 20 and now.minute == 0:
        tomorrow = now + timedelta(days=1)
        tomorrow_date = tomorrow.day
        tomorrow_month = tomorrow.month
        matching_records = Person.objects.filter(date__day=tomorrow_date, date__month=tomorrow_month)

        if matching_records:
            names = [person.name for person in matching_records]
            names_str = ', '.join(names)

            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            client = Client(account_sid, auth_token)

            from_whatsapp_number = 'whatsapp:+14155238886'
            to_whatsapp_number = 'whatsapp:+916364059064'
            message_body = f"Birthday Reminder ! {names_str}'s Birthday is Tommorow "

            try:
                # Send WhatsApp message
                message = client.messages.create(
                    body=message_body,
                    from_=from_whatsapp_number,
                    to=to_whatsapp_number
                )
                return HttpResponse(f"WhatsApp message sent! {names_str}")
            except Exception as e:
                logging.error(f"Failed to send WhatsApp message: {e}")
                return HttpResponse("Failed to send WhatsApp message")

        else:
            return HttpResponse("Nothing!")
        
    elif now.hour == 8 and now.minute == 0:
        today = now 
        today_date = today.day
        today_month = today.month
        matching_records = Person.objects.filter(date__day=today_date, date__month=today_month)

        if matching_records:
            names = [person.name for person in matching_records]
            names_str = ', '.join(names)

            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            client = Client(account_sid, auth_token)

            from_whatsapp_number = 'whatsapp:+14155238886'
            to_whatsapp_number = 'whatsapp:+916364059064'
            message_body = f"Birthday Reminder ! {names_str}'s Birthday is Today"

            try:
                # Send WhatsApp message
                message = client.messages.create(
                    body=message_body,
                    from_=from_whatsapp_number,
                    to=to_whatsapp_number
                )
                return HttpResponse(f"WhatsApp message sent! {names_str}")
            except Exception as e:
                logging.error(f"Failed to send WhatsApp message: {e}")
                return HttpResponse("Failed to send WhatsApp message")

        else:
            return HttpResponse("Nothing!")

    return HttpResponse("It's not Time yet!")
