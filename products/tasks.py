from __future__ import absolute_import, unicode_literals
from celery import shared_task
from products.models import Order, OrderItem
from datetime import datetime, timedelta


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
        items = OrderItem.objects.filter(order=order)
        for item in items:
            item.debt += item.price
            item.save()
        order.return_date = datetime.today()+timedelta(days=7)
        order.save()
    return "Done"
