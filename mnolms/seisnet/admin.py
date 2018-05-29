from django.contrib import admin

from .models import Network, Station, Caretaker


admin.site.register(Network)
admin.site.register(Station)
admin.site.register(Caretaker)
