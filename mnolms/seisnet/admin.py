from django.contrib import admin

from .models import Network, Station, Caretaker

from equipment.models import (
    SeismologicalEquipmentEntity,
    PowerSupplyModel,
    PowerSupplyModelItem,
    NetworkDeviceModel,
    NetworkDeviceModelItem,
)

from .forms import (
    StationForm,
    SeismologicalEquipmentEntityForm,
    PowerSupplyItemForm,
    NetworkDeviceItemForm,
)

admin.site.register(Network)
# admin.site.register(Station)
admin.site.register(Caretaker)


# class SeismologicalEquipmentEntityInline(admin.ChoicesFieldListFilter):
#     model = SeismologicalEquipmentEntity
#     form = SeismologicalEquipmentEntityForm
#     extra = 0

class PowerSupplyItemInline(admin.TabularInline):
    model = PowerSupplyModelItem
    form = PowerSupplyItemForm
    extra = 0
    verbose_name = '供电设备'
    verbose_name_plural = '供电设备'


class NetworkDeviceItemInline(admin.TabularInline):
    model = NetworkDeviceModelItem
    form = NetworkDeviceItemForm
    extra = 0
    verbose_name = '网络设备'
    verbose_name_plural = '网络设备'


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    form = StationForm
    inlines = (PowerSupplyItemInline, NetworkDeviceItemInline)


    # fieldsets = (
    #     (
    #         '基础信息',
    #         {
    #             'fields': ('network', 'code', 'zh_name', 'en_name', 'longitude', 'latitude', 'altitude', 'status',)
    #         }
    #     ),
        # (
        #     '设备信息',
        #     {
        #         'fields': (SeismologicalEquipmentEntityInline, )
        #
        #     }
        #
        # ),
    # )



    # inlines = (SeismologicalEquipmentEntityInline, )
