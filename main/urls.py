from django.urls import path
from .views import TalabaList, TalabaCreate, TalabaUpdate, TalabaDelete, AloqaView

urlpatterns = [
    path('', TalabaList.as_view(), name='royxat'),
    path('yangi/', TalabaCreate.as_view(), name='create'),
    path('<int:pk>/tahrir/', TalabaUpdate.as_view(), name='update'),
    path('<int:pk>/ochir/', TalabaDelete.as_view(), name='delete'),
    path('aloqa/', AloqaView.as_view(), name='aloqa'),
]
