from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.urls import reverse

from dal import autocomplete

from .models import Network, Station
from equipment.models import DataloggerEntity, SensorEntity
from .forms import NetworkForm, StationForm


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


def station_detail(request, pk):
    station = get_object_or_404(Station, pk=pk)
    return render(request, 'seisnet/station_detail.html',
                  {'station': station})


def station_add(request):
    if request.method == "POST":
        form = StationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.c_time = timezone.now()
            station.m_time = timezone.now()

            station.save()
            url = reverse('seis:station_detail', kwargs={'pk': station.pk})
            # return redirect('station_detail', pk=station.pk)
            return redirect(url)
    else:
        form = StationForm()

    return render(request, 'seisnet/station_edit.html', {'form': form})


def station_edit(request, pk):
    station = get_object_or_404(Station, pk=pk)
    old_datalogger_entities = station.datalogger_entities.all()
    old_sensor_entities = station.sensor_entities.all()

    if request.method == "POST":
        form = StationForm(request.POST, instance=station)

        if form.is_valid():
            station = form.save(commit=False)
            datalogger_entities = form.cleaned_data.get('datalogger_entities')
            sensor_entities = form.cleaned_data.get('sensor_entities')
            station.m_time = timezone.now()
            old_datalogger_entities.update(station=None, status=0)
            old_sensor_entities.update(station=None, status=0)
            datalogger_entities.update(station=station, status=1)
            sensor_entities.update(station=station, status=1)

            station.save()

            return redirect('seis:station_detail', pk=station.pk)
    else:
        form = StationForm(instance=station)
        # form.fields['datalogger_entities'].queryset.append(station.datalogger_entities)
        # form.fields['sensor_entities'].queryset.append(station.sensor_entities)


    return render(request, 'seisnet/station_edit.html', {'form': form})


class DataloggerEntityAutocomplete(autocomplete.Select2QuerySetView):
    # def __init__(self, *args, **kwargs):
    #     super(DataloggerEntityAutocomplete, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.kwargs.get('fk'):
            qs = DataloggerEntity.instock.all() | DataloggerEntity.objects.filter(station=self.kwargs.get('fk'))
        else:
            qs = DataloggerEntity.instock.all()

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
            qs = SensorEntity.instock.all() | SensorEntity.objects.filter(station=self.kwargs.get('fk'))
        else:
            qs = SensorEntity.instock.all()


        if self.q:
            qs = qs.filter(
                Q(sn__icontains=self.q) |
                Q(model__name__icontains=self.q)
            )

        return qs


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
