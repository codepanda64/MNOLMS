from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory

from dal import autocomplete

from .models import Network, Station
from equipment.models import DataloggerEntity, SensorEntity, EquimpmentItem
from .forms import NetworkForm, StationForm, SensorEntityForm


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
    print(station.sensor_entities)
    print(station.datalogger_entities)
    return render(request, 'seisnet/station_detail.html',
                  {'station': station})


def station_add(request):
    station = Station()

    EquimpmentItemFormSet = inlineformset_factory(Station, EquimpmentItem, fields=('network_device', 'quantity'),
                                                     extra=2)

    equimpment_item_form_set = EquimpmentItemFormSet(instance=station)
    # equimpment_item_form_set = NetworkDeviceItemFormSet(instance=station)

    # network_item_form = NetworkDeviceItemForm(instance=station)

    if request.method == "POST":
        station_form = StationForm(request.POST)
        if station_form.is_valid():
            station = station_form.save(commit=False)
            station.c_time = timezone.now()
            station.m_time = timezone.now()

            datalogger_entities = station_form.cleaned_data.get('datalogger_entities')
            sensor_entities = station_form.cleaned_data.get('sensor_entities')

            station.save()
            # station.network_device_item.save()
            # network_item_form = NetworkDeviceItemForm(station=station)
            equimpment_item_form_set = EquimpmentItemFormSet(request.POST, request.FILES, instance=station)
            if equimpment_item_form_set.is_valid():
                equimpment_item_form_set.save()

            datalogger_entities.update(station=station, status=1)
            sensor_entities.update(station=station, status=1)
            url = reverse('seis:station_detail', kwargs={'pk': station.pk})
            # return redirect('station_detail', pk=station.pk)
            return redirect(url)
    else:
        station_form = StationForm(instance=station)

        # station_form = StationForm()

    return render(request, 'seisnet/station_edit.html', {
        'station_form': station_form,
        'equimpment_item_form_set': equimpment_item_form_set,
    })


def station_edit(request, pk):
    station = get_object_or_404(Station, pk=pk)
    old_datalogger_entities = station.dataloggers
    old_sensor_entities = station.sensors

    old_datalogger_entities_id = old_datalogger_entities.values_list('id', flat=True)
    old_sensor_entities_id = old_sensor_entities.values_list('id', flat=True)

    EquimpmentItemFormSet = inlineformset_factory(Station, EquimpmentItem, fields=('network_device', 'quantity'),
                                                     extra=2)
    equimpment_item_form_set = EquimpmentItemFormSet(request.POST, request.FILES, instance=station)

    if request.method == "POST":
        station_form = StationForm(request.POST, instance=station)

        if station_form.is_valid():
            station = station_form.save(commit=False)
            dataloggers = station_form.cleaned_data.get('dataloggers')
            sensors = station_form.cleaned_data.get('sensors')
            station.m_time = timezone.now()

            if station_form.has_changed():
                if 'dataloggers' in station_form.changed_data or 'sensors' in station_form.changed_data:

                    old_datalogger_entities.update(station=None, status=0)
                    old_sensor_entities.update(station=None, status=0)
                    dataloggers.update(station=station, status=1)
                    sensors.update(station=station, status=1)

            if equimpment_item_form_set.is_valid():
                # print(equimpment_item_form_set.forms[0].fields['network_device'])
                equimpment_item_form_set.save()

            station.save()

            return redirect('seis:station_detail', pk=station.pk)
    else:
        station_form = StationForm(instance=station)
        station_form.fields['dataloggers'].initial = old_datalogger_entities_id
        station_form.fields['sensors'].initial = old_sensor_entities_id
        station_form.fields['dataloggers'].widget.url = reverse_lazy('seis:dataloggerentity-autocomplete',
                                                             kwargs={'fk': pk})
        station_form.fields['sensors'].widget.url = reverse_lazy('seis:sensorentity-autocomplete',
                                                                         kwargs={'fk': pk})
        equimpment_item_form_set = EquimpmentItemFormSet(instance=station)
        # form.fields['datalogger_entities'].queryset.append(station.datalogger_entities)
        # form.fields['sensor_entities'].queryset.append(station.sensor_entities)

    # return render(request, 'seisnet/station_edit.html', {'form': form})
    return render(request, 'seisnet/station_edit.html', {
        'station_form': station_form,
        'equimpment_item_form_set': equimpment_item_form_set,
    })


class DataloggerEntityAutocomplete(autocomplete.Select2QuerySetView):
    # def __init__(self, *args, **kwargs):
    #     super(DataloggerEntityAutocomplete, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.kwargs.get('fk'):
            qs = DataloggerEntity.objects.instock() | DataloggerEntity.objects.filter(station=self.kwargs.get('fk'))
        else:
            qs = DataloggerEntity.objects.instock()

        if self.q:
            qs = qs.filter(
                Q(sn__icontains=self.q) |
                Q(model__name__icontains=self.q)
            )

        return qs

    # def get_results(self, context):
    #     super(DataloggerEntityAutocomplete, self).get_results(context)
    #     station_pk = context['station']
    #     return [
    #         {
    #             'station_pk': station_pk
    #         }
    #     ]
    # return [
    #     {
    #         'selected': result
    #     } for result in context['object_list']
    # ]


class SensorEntityAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if self.kwargs.get('fk'):
            qs = SensorEntity.objects.instock() | SensorEntity.objects.filter(station=self.kwargs.get('fk'))
        else:
            qs = SensorEntity.objects.instock()

        if self.q:
            qs = qs.filter(
                Q(sn__icontains=self.q) |
                Q(model__name__icontains=self.q)
            )

        return qs


def test(request, pk):
    selected_id_list = SensorEntity.objects.filter(station=pk).values_list('id', flat=True)
    print(selected_id_list)
    form = SensorEntityForm()
    form.fields['sensor_entities'].initial = selected_id_list
    print(form.as_p())
    # form.fields['sensor_entities'].initial = selected_id_list
    form.fields['sensor_entities'].widget.url = reverse_lazy('seis:sensorentity-autocomplete',
                                                             kwargs={'fk': pk})
    return render(request, 'seisnet/test.html', {
        'form': form,
    })
# class UpdateView(UpdateView):
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
