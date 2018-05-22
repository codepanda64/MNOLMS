from django.contrib import admin
from .models import Manufacturer
from .models import SensorModel
from .models import SensorFeatures
from .models import Sensor
from .models import DataloggerModel
from .models import DataloggerFeatures
from .models import Datalogger

admin.site.register(Manufacturer)
admin.site.register(SensorModel)
admin.site.register(SensorFeatures)
admin.site.register(Sensor)
admin.site.register(DataloggerModel)
admin.site.register(DataloggerFeatures)
admin.site.register(Datalogger)
