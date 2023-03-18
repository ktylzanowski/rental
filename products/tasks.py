from __future__ import absolute_import, unicode_literals
from celery import shared_task
from orders.models import Order, OrderItem
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


@shared_task(bind=True)
def send_mail_func(self):
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day
    hour = today.hour
    minute = today.minute
    orders = Order.objects.filter(return_date__year=year, return_date__month=month, return_date__day=day,
                                  return_date__hour=hour, return_date__minute=minute)
    for order in orders:
        order.debt += order.total
        order.save()
        order.return_date = datetime.today()+timedelta(days=7)
        order.save()
        email_template = render_to_string('products/debt_email.html', {})
        email = EmailMessage(
            'DEBIT HAS BUILT UP',
            email_template,
            settings.EMAIL_HOST_USER,
            [order.user.email],
        )
        email.fail_silently = False
        email.send()
    return "Done"
