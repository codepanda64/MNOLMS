from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Network
from .forms import NetworkForm


def network_list(request):
    networks = Network.objects.all()
    return render(request, 'seisnet/network_list.html',
                  {'networks': networks})


def network_detail(request, pk):
    network = get_object_or_404(Network, pk=pk)
    return render(request, 'seisnet/network_detail.html',
                  {'network': network})


def network_add(request):
    if request.method == "POST":
        form = NetworkForm(request.POST)
        if form.is_valid():
            network = form.save(commit=False)
            network.c_time = timezone.now()
            network.m_time = timezone.now()
            network.save()
            return redirect('network_detail', pk=network.pk)
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
            return redirect('network_detail', pk=network.pk)
    else:
        form = NetworkForm(instance=network)

    return render(request, 'seisnet/network_edit.html', {'form': form})
