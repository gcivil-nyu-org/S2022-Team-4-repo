from unittest import TestCase

from django.db import connection

from service.models import Order
from user_center.query import provide_list_query
from users.models import CustomUser
from utils import namedtuplefetchall


class TestViews(TestCase):
    def test_database(self):
        with connection.cursor() as cursor:
            cursor.execute(provide_list_query(1))
            result = namedtuplefetchall(cursor)
            print(result[1].service_time.strftime("%d-%b-%Y %H:%M"))
        user = CustomUser.objects.get(id=1)
        order_list = Order.objects.filter(user=user).order_by("-timestamp")
        print(order_list[0].timestamp)
        print(order_list[1].timestamp)
