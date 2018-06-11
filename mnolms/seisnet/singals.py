#!/usr/bin/python3
"""
@Time     : 6/7/18 11:56 AM
@Author   : codepanda
@Email    : 17920082@qq.com
@FIle     : singals.py
@Software : PyCharm
"""
from django.dispatch import receiver
from django.db.models.signals import post_init, pre_save, post_save
from django.core.signals import request_finished

from .models import Station
from equipment.models import DataloggerEntity, SensorEntity


@receiver(request_finished, dispatch_uid="request_finished")
def station_request_finished_callback(sender, **kwargs):
    print('satation request finished', sender, kwargs)

@receiver(post_init, sender=Station)
def station_post_init_callback(sender, **kwargs):
    print('station post init', sender, kwargs)
    print('post init: {}'.format(
        kwargs['instance'].__dict__
    ))

@receiver(pre_save, sender=Station)
def station_pre_save_callback(sender, **kwargs):
    print('satation pre save', sender, kwargs)
    print('pre save: {}'.format(
        kwargs['instance'].__dict__
    ))


@receiver(post_save, sender=Station)
def station_post_save_callback(sender, **kwargs):
    print('satation post save', sender, kwargs)
    print('post save: {}'.format(
        kwargs['instance'].__dict__
    ))
