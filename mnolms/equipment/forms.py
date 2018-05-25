from django import forms

from .models import Manufacturer
from .models import ManufacturerCategory
from .models import SensorModel


class ManufacturerForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(ManufacturerForm, self).__init__(*args, **kwargs)
    #
    #     self.fields["category"].widget = CheckboxSelectMultiple
    #     self.fields['category'].queryset = ManufacturerCategory.objects.all()

    category = forms.ModelMultipleChoiceField(
        label='厂商分类',
        widget=forms.CheckboxSelectMultiple,
        queryset=ManufacturerCategory.objects.all(),
        required=True
    )

    class Meta:
        model = Manufacturer
        fields = ['name', 'address', 'category', 'remark']


class SensorModelForm(forms.ModelForm):

    manufacturer = forms.ModelChoiceField(
        label='生产厂商',
        queryset=Manufacturer.objects.filter(category=1),
        required=True
    )

    class Meta:
        model = SensorModel
        fields = ['name', 'features', 'manufacturer', 'totality', 'stock', 'fault_number']