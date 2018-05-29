from django import forms

from bootstrap_datepicker.widgets import DatePicker

from .models import Network


class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ('code', 'name', 'start_time', 'end_time', 'status', 'describe')

    start_time = forms.DateField(
        label="开始时间",
        widget=DatePicker(
            options={
                "format": "yyyy-mm-dd",
                "autoclose": True
            },
        )
    )

    end_time = forms.DateField(
        label="结束时间",
        widget=DatePicker(
            options={
                "format": "yyyy-mm-dd",
                "autoclose": True
            },
        )
    )
