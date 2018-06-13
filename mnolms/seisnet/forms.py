from django import forms
from django.utils.encoding import force_text
from django.urls import reverse_lazy
from django.contrib.admin import StackedInline

from bootstrap_datepicker.widgets import DatePicker
from dal import autocomplete

from .models import Network, Station
# from equipment.models import DataloggerEntity, SensorEntity, EquimpmentItem
from equipment.models import (
    Equipment,
    PowerSupplyModel,
    NetworkDeviceModel,
    SeismologicalEquipmentEntity,
    # EquimpmentItem,
    PowerSupplyModelItem,
    NetworkDeviceModelItem,
)


class NetworkForm(forms.ModelForm):

    class Meta:
        model = Network
        fields = ('code', 'name', 'start_time', 'end_time', 'status', 'describe')

    start_time = forms.DateField(
        label="开始时间",
        widget=DatePicker(
            attrs={'class': 'test-123', },
            options={
                "format": "yyyy-mm-dd",
                "autoclose": True,
            },
        ),
        required=False
    )

    end_time = forms.DateField(
        label="结束时间",
        required=False,
        widget=DatePicker(
            options={
                "format": "yyyy-mm-dd",
                "autoclose": True
            },
        )
    )


class StationForm(forms.ModelForm):

    class Meta:
        model = Station
        fields = ('network', 'code',
                  'en_name', 'zh_name',
                  'longitude', 'latitude',
                  'altitude', 'status',
                  'seismological_equipments',
                  'describe', 'location',
                  )

    seismological_equipments = forms.ModelMultipleChoiceField(
        label='测震仪器列表',
        queryset=SeismologicalEquipmentEntity.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(
            url=reverse_lazy('seis:seisentity-autocomplete')
        )
    )


# class SeismologicalEquipmentEntityForm(forms.ModelForm):
#     class Meta:
#         model = SeismologicalEquipmentEntity
#         fields = ('id',)
#
#     sseismological_equipments = forms.ModelMultipleChoiceField(
#         label='测震设备列表',
#
#         queryset=SeismologicalEquipmentEntity.objects.all(),
#         required=False,
#         widget=autocomplete.ModelSelect2Multiple(
#             url=reverse_lazy('seis:seisentity-autocomplete')
#         )
#     )


class PowerSupplyItemForm(forms.ModelForm):
    # def __init__(self, station, *args, **kwargs):
    #     self.station = station
    #     super(PowerSupplyItemForm, self).__init__(*args, **kwargs)

    # equipment = forms.ModelChoiceField(
    #     label='供电设备列表',
    #     queryset=Equipment.objects.instance_of(PowerSupplyModel),
    #     required=False,
    # )

    class Meta:
        model = PowerSupplyModelItem
        fields = ('equipment', 'quantity')
        labels = {
            'equipment': '供电设备',
            'quantity': '数量',
        }
        widgets = {
            'equipment': forms.Select(),
        }


class NetworkDeviceItemForm(forms.ModelForm):
    # def __init__(self, station, *args, **kwargs):
    #     self.station = station
    #     super(NetworkDeviceItemForm, self).__init__(*args, **kwargs)

    # equipment = forms.ModelChoiceField(
    #     label='网络设备列表',
    #     queryset=Equipment.objects.instance_of(NetworkDeviceModel),
    #     required=False,
    # )

    class Meta:
        model = NetworkDeviceModelItem
        fields = ('equipment', 'quantity')
        labels = {
            'equipment': '网络设备',
            'quantity': '数量',
        }
        widgets = {
            'equipment': forms.Select(),
        }


class SeismologicalEquipmentEntityForm(forms.Form):
    seismological = forms.ModelChoiceField(
        label='测震仪器列表',
        queryset=SeismologicalEquipmentEntity.objects.all(),
    )

# class NetworkDeviceItemForm(forms.ModelForm):
#     class Meta:
#         model = NetworkDeviceItem
#         fields = ('network_device', 'quantity',)
#
#
#     def cleaned_data(self):
#         return True
