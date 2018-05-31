from django.urls import path

from dal import autocomplete

from . import views

from equipment.models import DataloggerEntity

app_name = 'seis'

urlpatterns = [

    # path('station', views.station_list, name='station_list'),
    path('station/add', views.station_add, name='station_add'),
    path('station/detail/<int:pk>', views.station_detail, name='station_detail'),
    path('station/edit/<int:pk>', views.station_edit, name='station_edit'),

    path('station/dataloggerentity-autocomplete',
         views.DataloggerEntityAutocomplete.as_view(),
         name='dataloggerentity-autocomplete'),
    path('station/sensorentity-autocomplete',
         views.SensorEntityAutocomplete.as_view(),
         name='sensorentity-autocomplete'),

    # path('net', views.network_list, name='network_list'),
    path('net', views.NetworkListView.as_view(), name='network_list'),
    path('net/add', views.network_add, name='network_add'),
    # path('net/detail/<int:pk>', views.network_detail, name='network_detail'),
    path('net/detail/<int:pk>', views.NetworkDetailView.as_view(), name='network_detail'),
    path('net/edit/<int:pk>', views.network_edit, name='network_edit'),

]