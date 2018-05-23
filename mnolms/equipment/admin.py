from django.contrib import admin
from .models import Manufacturer
from .models import SensorModel
from .models import Sensor
from .models import DataloggerModel
from .models import Datalogger
from .models import PowerSupply
from .models import Equipment
from .models import Category

admin.site.register(Manufacturer)
admin.site.register(SensorModel)
admin.site.register(Sensor)
admin.site.register(DataloggerModel)
admin.site.register(Datalogger)
admin.site.register(PowerSupply)
admin.site.register(Equipment)
admin.site.register(Category)
