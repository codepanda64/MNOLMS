from django.urls import path

from . import views


urlpatterns = [
    path('', views.network_list, name='network_list'),
    path('add', views.network_add, name='network_add'),
    path('detail/<int:pk>', views.network_detail, name='network_detail'),
    path('edit/<int:pk>', views.network_edit, name='network_edit'),
]