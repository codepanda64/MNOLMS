from django import forms
from django.utils.encoding import force_text
from django.contrib.admin import StackedInline

from bootstrap_datepicker.widgets import DatePicker
from dal import autocomplete

from .models import Network, Station
from equipment.models import DataloggerEntity, SensorEntity


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

    # def __init__(self, datalogger_entities, sensor_entities, *args, **kwargs):
    #     super(StationForm, self).__init__(*args, **kwargs)
    #     self.fields['datalogger_entities'].widget.queryset = datalogger_entities
    #     self.fields['sensor_entities'].widget.queryset = sensor_entities

    class Meta:
        model = Station
        fields = ('network', 'code',
                  'en_name', 'zh_name',
                  'longitude', 'latitude',
                  'altitude', 'status',
                  'datalogger_entities', 'sensor_entities',
                  'describe', 'location')
        # widgets = {
        #     'datalogger_entity_set': autocomplete.ModelSelect2Multiple(
        #         url='datalogger_entity-autocomplete',
        #     ),
        #     'sensor_entity_set': autocomplete.ModelSelect2Multiple(
        #         url='sensor_entity-autocomplete',
        #     ),
        # }

    datalogger_entities = forms.ModelMultipleChoiceField(
        label='数采列表',
        queryset=DataloggerEntity.instock.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(
            url='seis:dataloggerentity-autocomplete',
            # url='test-autocomplete',
        )
    )

    sensor_entities = forms.ModelMultipleChoiceField(
        label='地震仪列表',
        queryset=SensorEntity.instock.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(
            url='seis:sensorentity-autocomplete',
            # url='test-autocomplete',
        )
    )
