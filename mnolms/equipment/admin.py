from django.contrib import admin

from .models import Equipment
from .models import Manufacturer
from .models import SensorModel
from .models import SensorEntity
from .models import DataloggerModel
from .models import DataloggerEntity
from .models import GPSAntenna
from .models import PowerSupply
from .models import NetworkDevice
from .models import Category


# admin.site.register(Manufacturer)
admin.site.register(SensorModel)
admin.site.register(SensorEntity)
admin.site.register(DataloggerModel)
admin.site.register(DataloggerEntity)
admin.site.register(GPSAntenna)
admin.site.register(PowerSupply)
admin.site.register(NetworkDevice)
# admin.site.register(Category)
