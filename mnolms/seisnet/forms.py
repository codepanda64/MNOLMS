from django import forms
from django.utils.encoding import force_text
from django.urls import reverse_lazy
from django.contrib.admin import StackedInline

from bootstrap_datepicker.widgets import DatePicker
from dal import autocomplete

from .models import Network, Station
from equipment.models import DataloggerEntity, SensorEntity, EquimpmentItem



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


    # def __init__(self, *args, **kwargs):
    #     super(StationForm, self).__init__(*args, **kwargs)
    #
    #     if self.instance.pk:
    #         selected_datalogger = DataloggerEntity.objects.filter(station=self.instance.pk)
    #         selected_sensor = SensorEntity.objects.filter(station=self.instance.pk)
    #         print(selected_datalogger.values_list('id', 'sn'))
    #         print(selected_sensor.values_list('id', 'sn'))
    #         self.fields['datalogger_entities'].initial = selected_datalogger.values_list('id', flat=True)
    #         self.fields['sensor_entities'].initial = selected_sensor.values_list('id', flat=True)
    #         self.fields['datalogger_entities'].widget.url = reverse_lazy('seis:dataloggerentity-autocomplete',
    #                                                                      kwargs={'fk': self.instance.pk})
    #         self.fields['sensor_entities'].widget.url = reverse_lazy('seis:sensorentity-autocomplete',
    #                                                                  kwargs={'fk': self.instance.pk})

    class Meta:
        model = Station
        fields = ('network', 'code',
                  'en_name', 'zh_name',
                  'longitude', 'latitude',
                  'altitude', 'status',
                  # 'datalogger_entities', 'sensor_entities',
                  'dataloggers', 'sensors',
                  'describe', 'location',
                  # 'network_device_item',
                  )

        # widgets = {
        #     'datalogger_entity_set': autocomplete.ModelSelect2Multiple(
        #         url='datalogger_entity-autocomplete',
        #     ),
        #     'sensor_entity_set': autocomplete.ModelSelect2Multiple(
        #         url='sensor_entity-autocomplete',
        #     ),
        # }

    dataloggers = forms.ModelMultipleChoiceField(
        label='数采列表',
        # queryset=DataloggerEntity.instock.all(),
        queryset=DataloggerEntity.objects.all(),
        required=False,
        # initial=2,
        widget=autocomplete.ModelSelect2Multiple(
            url=reverse_lazy('seis:dataloggerentity-autocomplete')
        )
    )

    sensors = forms.ModelMultipleChoiceField(
        label='地震仪列表',
        # queryset=SensorEntity.instock.all() ,
        queryset=SensorEntity.objects.all(),
        required=False,
        # initial=(1,2),
        widget=autocomplete.ModelSelect2Multiple(
            url=reverse_lazy('seis:sensorentity-autocomplete')
            # url='test-autocomplete',
        )
    )


class SensorEntityForm(forms.Form):

    sensor_entities = forms.ModelMultipleChoiceField(
        label='地震仪列表',

        queryset=SensorEntity.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(
            url=reverse_lazy('seis:sensorentity-autocomplete')
        )
    )

# class NetworkDeviceItemForm(forms.ModelForm):
#     class Meta:
#         model = NetworkDeviceItem
#         fields = ('network_device', 'quantity',)
#
#
#     def cleaned_data(self):
#         return True
