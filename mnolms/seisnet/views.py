from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.urls import reverse, reverse_lazy
from django.forms import formset_factory, inlineformset_factory

from dal import autocomplete

from .models import Network, Station
from equipment.models import (
    Equipment,
    PowerSupplyModel,
    NetworkDeviceModel,
    SeismologicalEquipmentEntity,
    # EquimpmentItem,
)

from .forms import (
    NetworkForm,
    StationForm,
    PowerSupplyItemForm,
    NetworkDeviceItemForm,
)


class NetworkListView(ListView):
    model = Network
    context_object_name = 'networks'
    template_name = 'seisnet/network_list.html'

    def get_context_data(self, **kwargs):
        context = super(NetworkListView, self).get_context_data(**kwargs)
        return context


class NetworkDetailView(DetailView):
    model = Network
    context_object_name = 'network'
    template_name = 'seisnet/network_detail.html'


def network_add(request):
    if request.method == "POST":
        form = NetworkForm(request.POST)
        if form.is_valid():
            network = form.save(commit=False)
            network.c_time = timezone.now()
            network.m_time = timezone.now()
            network.save()
            return redirect('seis:network_detail', pk=network.pk)

    else:
        form = NetworkForm()

    return render(request, 'seisnet/network_edit.html', {'form': form})


def network_edit(request, pk):
    network = get_object_or_404(Network, pk=pk)
    if request.method == "POST":
        form = NetworkForm(request.POST, instance=network)
        if form.is_valid():
            network = form.save(commit=False)

            network.m_time = timezone.now()
            network.save()
            url = reverse('seis:network_detail', kwargs={'pk': network.pk})
            return redirect(url)
    else:
        form = NetworkForm(instance=network)

    return render(request, 'seisnet/network_edit.html', {'form': form})


class StationListView(ListView):
    model = Station
    context_object_name = 'stations'
    template_name = 'seisnet/station_list.html'

    def get_context_data(self, **kwargs):
        context = super(StationListView, self).get_context_data(**kwargs)
        return context


def station_detail(request, pk):
    station = get_object_or_404(Station, pk=pk)
    return render(request, 'seisnet/station_detail.html',
                  {'station': station})


def station_add(request):
    station = Station()

    # EquimpentItemFormSet = inlineformset_factory(Station, EquimpmentItem, fields=('equipment', 'quantity'), extra=1)

    PowerSupplyItemFormSet = formset_factory(form=PowerSupplyItemForm)
    NetworkDeviceItemFormSet = formset_factory(form=NetworkDeviceItemForm)
    powersupply_item_form_set = PowerSupplyItemFormSet(form_kwargs={'station': station})
    network_device_item_form_set = NetworkDeviceItemFormSet(form_kwargs={'station': station})

    if request.method == "POST":
        station_form = StationForm(request.POST)
        if station_form.is_valid():
            station = station_form.save(commit=False)
            station.c_time = timezone.now()
            station.m_time = timezone.now()
            seismological_equipments = station_form.cleaned_data.get('seismological_equipments')

            # print(seismological_equipments)
            station.save()

            # datalogger_entities = station_form.cleaned_data.get('datalogger_entities')
            # sensor_entities = station_form.cleaned_data.get('sensor_entities')

            powersupply_item_form_set = PowerSupplyItemFormSet(request.POST, request.FILES,
                                                               form_kwargs={'station': station})
            network_device_item_form_set = NetworkDeviceItemFormSet(request.POST, request.FILES,
                                                                    form_kwargs={'station': station})

            print("before:")
            print(powersupply_item_form_set)

            if powersupply_item_form_set.is_valid() and network_device_item_form_set.is_valid():
                print("true:")
                print(powersupply_item_form_set)
                powersupply_item_form_set.save()
                network_device_item_form_set.save()

                # for form in powersupply_item_form_set:
                #     powersupply_item = form.save(commit=False)
                #     powersupply_item.station = station
                #     print(form)
                #     print(powersupply_item)
                #
                #     powersupply_item.save()
                #
                # for form in network_device_item_form_set:
                #     network_device_item = form.save(commit=False)
                #     network_device_item.station = station
                #     network_device_item.save()

                # powersupply_item_form_set.save()
                # network_device_item_form_set.save()

            # print(station)
            seismological_equipments.update(station=station, status=1)
            url = reverse('seis:station_detail', kwargs={'pk': station.pk})
            # return redirect('station_detail', pk=station.pk)
            return redirect(url)
    else:
        station_form = StationForm(instance=station)

        # station_form = StationForm()

    return render(request, 'seisnet/station_edit.html', {
        'station_form': station_form,
        'powersupply_item_form_set': powersupply_item_form_set,
        'network_device_item_form_set': network_device_item_form_set,
    })


# def station_edit(request, pk):
#     station = get_object_or_404(Station, pk=pk)
#     old_seismological_equipments = station.seismological_equipments
#     old_seismological_equipments_id = old_seismological_equipments.values_list('id', flat=True)
#
#     # EquimpmentItemFormSet = inlineformset_factory(Station, EquimpmentItem, fields=('equipment', 'quantity'), extra=0)
#
#     network_device_itme_form_set = EquimpmentItemFormSet(request.POST, request.FILES, instance=station,
#                                                          form=PowerSupplyItemForm,)
#
#     powersupply_itme_form_set = EquimpmentItemFormSet(request.POST, request.FILES, instance=station,
#                                                       form=PowerSupplyItemForm, )
#
#     if request.method == "POST":
#         station_form = StationForm(request.POST, instance=station)
#
#         if station_form.is_valid():
#             station = station_form.save(commit=False)
#             seismological_equipments = station_form.cleaned_data['seismological_equipments']
#             # dataloggers = station_form.cleaned_data.get('dataloggers')
#             # sensors = station_form.cleaned_data.get('sensors')
#             station.m_time = timezone.now()
#
#             if station_form.has_changed():
#                 if 'seismological_equipments' in station_form.changed_data:
#                     old_seismological_equipments.update(station=None, status=0)
#                     seismological_equipments.update(station=station, status=1)
#
#             if network_device_itme_form_set.is_valid() and powersupply_itme_form_set.is_valid():
#                 powersupply_itme_form_set.save()
#                 network_device_itme_form_set.save()
#
#             station.save()
#
#             return redirect('seis:station_detail', pk=station.pk)
#     else:
#         station_form = StationForm(instance=station)
#         station_form.fields['seismological_equipments'].initial = old_seismological_equipments_id
#         station_form.fields['seismological_equipments'].widget.url = reverse_lazy('seis:seisentity-autocomplete',
#                                                                                   kwargs={'fk': pk})
#         # network_device_itme_form_set = NetworkDeviceItemFormSet(instance=station)
#         # powersupply_itme_form_set = PowerSupplyItemFormSet(instance=station)
#
#     return render(request, 'seisnet/station_edit.html', {
#         'station_form': station_form,
#         'network_device_itme_form_set': network_device_itme_form_set,
#         'powersupply_item_form_set': powersupply_itme_form_set,
#     })


class SeismologicalEquipmentEntityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.kwargs.get('fk'):
            station = Station.objects.get(id=self.kwargs.get('fk'))
            qs = SeismologicalEquipmentEntity.objects.instock() | SeismologicalEquipmentEntity.objects.filter_by_instance(station)
        else:
            qs = SeismologicalEquipmentEntity.objects.instock()

        if self.q:
            qs = qs.filter(
                Q(sn__icontains=self.q) |
                Q(model__name__icontains=self.q)
            )

        return qs


# class DataloggerEntityAutocomplete(autocomplete.Select2QuerySetView):
#
#     def get_queryset(self):
#         if self.kwargs.get('fk'):
#             qs = DataloggerEntity.objects.instock() | DataloggerEntity.objects.filter(station=self.kwargs.get('fk'))
#         else:
#             qs = DataloggerEntity.objects.instock()
#
#         if self.q:
#             qs = qs.filter(
#                 Q(sn__icontains=self.q) |
#                 Q(model__name__icontains=self.q)
#             )
#
#         return qs


# class SensorEntityAutocomplete(autocomplete.Select2QuerySetView):
#
#     def get_queryset(self):
#         if self.kwargs.get('fk'):
#             qs = SensorEntity.objects.instock() | SensorEntity.objects.filter(station=self.kwargs.get('fk'))
#         else:
#             qs = SensorEntity.objects.instock()
#
#         if self.q:
#             qs = qs.filter(
#                 Q(sn__icontains=self.q) |
#                 Q(model__name__icontains=self.q)
#             )
#
#         return qs
#
#
def test(request):
    form = PowerSupplyItemForm()
    return render(request, 'seisnet/test.html', {'form': form})

# def test(request, pk):
#     selected_id_list = SensorEntity.objects.filter(station=pk).values_list('id', flat=True)
#     print(selected_id_list)
#     form = SensorEntityForm()
#     form.fields['sensor_entities'].initial = selected_id_list
#     print(form.as_p())
#     # form.fields['sensor_entities'].initial = selected_id_list
#     form.fields['sensor_entities'].widget.url = reverse_lazy('seis:sensorentity-autocomplete',
#                                                              kwargs={'fk': pk})
#     return render(request, 'seisnet/test.html', {
#         'form': form,
#     })
# # class UpdateView(UpdateView):
#     model = Station
#     form_class = StationForm
#     template_name = 'seisnet/station_edit.html'
#     success_url = reverse_lazy('update_test', kwargs={'pk': 3})
#
#     def get_form_kwargs(self):
#         print(self.kwargs)
#         datalogger_entities = DataloggerEntity.objects.filter(station=self.kwargs.get('pk'))
#         sensor_entities = SensorEntity.objects.filter(station=self.kwargs.get('pk'))
#         kwargs = super(UpdateView, self).get_form_kwargs()
#         kwargs.update({
#             'datalogger_entities': datalogger_entities,
#             'sensor_entities': sensor_entities
#         })
#         return kwargs
#
#     def get_object(self):
#         return Station.objects.get(pk=self.kwargs.get('pk'))
