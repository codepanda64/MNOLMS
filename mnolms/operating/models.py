from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class StationOperationGroup(models.Model):
    '''
    在同一个台站的一次操作
    '''
    station = models.ForeignKey('seisnet.Station', on_delete=models.CASCADE)
    operation_time = models.DateTimeField()


class StationOperating(models.Model):
    '''
    台站操作类
    '''
    OPERATION_TYPE = (
        (1, '回收数据'),
        (2, '设备维护'),
        (3, '新建'),
        (4, '暂停'),
        (5, '恢复'),
        (6, '迁移'),
        (7, '撤销'),
        (8, '其它')
    )
    operation = models.PositiveSmallIntegerField(choices=OPERATION_TYPE)
    belong_group = models.ForeignKey('StationOperationGroup', on_delete=models.CASCADE)


class StationEquipmentAlterationRecord(models.Model):
    '''
    台站设备变更记录
    '''
    operating = models.ForeignKey('StationOperating', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="content_type_alterations")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    event_type = models.CharField(max_length=250, default="created")
