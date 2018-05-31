from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

# from .models import Equipment
from .models import Manufacturer
from .models import ManufacturerCategory
from .models import SensorModel
from .models import SensorEntity
from .models import DataloggerModel
from .models import DataloggerEntity
from .models import GPSAntenna
from .models import PowerSupply
from .models import NetworkDevice

from .forms import ManufacturerForm
from .forms import SensorModelForm


@admin.register(GPSAntenna)
class GPSAntennaAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'totality', 'stock', 'fault_number')
    fields = ('name', 'manufacturer', 'totality', 'stock', 'fault_number', 'remark', 'is_deleted')


@admin.register(SensorModel)
class SensorModelAdmin(admin.ModelAdmin):
    form = SensorModelForm


@admin.register(DataloggerModel)
class DataloggerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'features', 'manufacturer', 'totality', 'stock', 'fault_number')
    exclude = ('category',)


@admin.register(PowerSupply)
class PowerSupplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'totality', 'stock', 'fault_number')
    fields = ('name', 'manufacturer', 'type', 'totality', 'stock', 'fault_number', 'remark', 'is_deleted')


@admin.register(NetworkDevice)
class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'totality', 'stock', 'fault_number')
    exclude = ('category',)


# @admin.register(Manufacturer)
# class ManufacturerAdmin(admin.ModelAdmin):
    # form = ManufacturerForm

    # actions = ['custom_selected_delete']
    #
    # def custom_selected_delete(self, request, queryset):
    #     queryset.update(is_deleted=True)
    #
    # custom_selected_delete.short_description = "删除选中项"


admin.site.register(SensorEntity)
admin.site.register(DataloggerEntity)
admin.site.register(Manufacturer)
admin.site.register(ManufacturerCategory)

admin.AdminSite.site_header = '流动台站运维日志管理系统'
admin.AdminSite.site_title = '流动台站运维日志管理系统'
admin.AdminSite.index_title = '后台管理'

# admin.site.disable_action('delete_selected')

