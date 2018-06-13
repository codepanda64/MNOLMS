from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from .models import (
    ManufacturerCategory,
    Manufacturer,
    SeismologicalEquipmentModel,
    SeismologicalEquipmentEntity,
)

from .models import (
    ManufacturerCategory,
    Manufacturer,

    SeismologicalEquipmentModel,

    GPSAntennaModel,
    PowerSupplyModel,
    NetworkDeviceModel,
    OtherModel,

    SeismologicalEquipmentEntity,
)


from .forms import ManufacturerForm
# from .forms import SensorModelForm


# @admin.register(GPSAntennaModel)
# class GPSAntennaAdmin(admin.ModelAdmin):
#     list_display = ('name', 'manufacturer', 'totality', 'stock', 'fault_number')
#     fields = ('name', 'manufacturer', 'totality', 'stock', 'fault_number', 'remark', 'is_deleted')


# @admin.register(SensorModel)
# class SensorModelAdmin(admin.ModelAdmin):
#     form = SensorModelForm


# @admin.register(DataloggerModel)
# class DataloggerModelAdmin(admin.ModelAdmin):
#     list_display = ('name', 'features', 'manufacturer', 'totality', 'stock', 'fault_number')
#     exclude = ('category',)


# @admin.register(SeismologicalEquipmentModel)
# class SeismologicalEquipmentModelAdmin(admin.ModelAdmin):
#     list_display = ('name', 'features', 'manufacturer', 'totality', 'stock', 'fault_number')
#     exclude = ('category',)



# @admin.register(PowerSupplyModel)
# class PowerSupplyAdmin(admin.ModelAdmin):
#     list_display = ('name', 'manufacturer', 'totality', 'stock', 'fault_number')
#     fields = ('name', 'manufacturer', 'type', 'totality', 'stock', 'fault_number', 'remark', 'is_deleted')


# @admin.register(NetworkDeviceModel)
# class NetworkDeviceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'manufacturer', 'totality', 'stock', 'fault_number')
#     exclude = ('category',)


# @admin.register(Manufacturer)
# class ManufacturerAdmin(admin.ModelAdmin):
    # form = ManufacturerForm

    # actions = ['custom_selected_delete']
    #
    # def custom_selected_delete(self, request, queryset):
    #     queryset.update(is_deleted=True)
    #
    # custom_selected_delete.short_description = "删除选中项"


admin.site.register(SeismologicalEquipmentModel)
admin.site.register(SeismologicalEquipmentEntity)
admin.site.register(Manufacturer)
admin.site.register(ManufacturerCategory)
admin.site.register(PowerSupplyModel)
admin.site.register(NetworkDeviceModel)
admin.site.register(GPSAntennaModel)
admin.site.register(OtherModel)

admin.AdminSite.site_header = '流动台站运维日志管理系统'
admin.AdminSite.site_title = '流动台站运维日志管理系统'
admin.AdminSite.index_title = '后台管理'

# admin.site.disable_action('delete_selected')

