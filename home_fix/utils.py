from collections import namedtuple
from django.urls import reverse


# read data from database and save them in dict format
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# read data from database and save them in obj format
# def namedtuplefetchall(cursor):
#     "Return all rows from a cursor as a namedtuple"
#     desc = cursor.description
#     nt_result = namedtuple("Result", [col[0] for col in desc])
#     return [nt_result(*row) for row in cursor.fetchall()]


# test if the user is authed
def auth_test(source, url):
    response = source.client.get(reverse(url))
    source.assertEquals(response.status_code, 302)

    # login
    source.client.post(
        reverse("users:login"),
        data={"email": source.email_login, "password": source.password},
    )


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
