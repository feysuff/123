# server/urls.py
from django.urls import path
from .views import CreateOrderView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('api/orders/', CreateOrderView.as_view(), name='create_order'),
]


@csrf_exempt
def test_view(request):
    return HttpResponse("Test OK")

urlpatterns = [
    path('test/', test_view),
]
