from django.db import models
from django.contrib.contenttypes.fields import ContentType
from django.db import connection

from polymorphic.models import PolymorphicModel, PolymorphicManager


class Manufacturer(models.Model):
    """
    制造商信息
    """
    CATEGORY_LIST = (
        (0, '测震仪器制造商'),
        (1, '供电系统制造商'),
        (2, '网络设备制造商'),
        (3, '配件制造商'),
        (5, '其它')
    )

    name = models.CharField(max_length=64, unique=True, verbose_name="制造商名称")
    alias_name = models.CharField(max_length=64, blank=True, null=True, verbose_name="别名")
    address = models.CharField(max_length=128,
                               null=True,
                               blank=True,
                               verbose_name="地址")
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    is_deleted = models.BooleanField(default=False, verbose_name="已删除")

    category = models.ManyToManyField("ManufacturerCategory", verbose_name="制造商分类")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "制造商信息"
        verbose_name_plural = "制造商信息"


class ManufacturerCategory(models.Model):
    """
    制造商分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="制造商分类名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "制造商分类"
        verbose_name_plural = "制造商分类"


# class EquipmentManager(PolymorphicManager):
#     def seis_instrument(self):
#         return super(EquipmentManager, self).get_queryset().filter(category='SI')
#
#     def powersupply(self):
#         return super(EquipmentManager, self).get_queryset().filter(category='PS')
#
#     def core_accessor(self):
#         return super(EquipmentManager, self).get_queryset().filter(category='CA')
#
#     def network_device(self):
#         return super(EquipmentManager, self).get_queryset().filter(category='ND')
#
#     def other(self):
#         return super(EquipmentManager, self).get_queryset().filter(category='OT')


class Equipment(PolymorphicModel):
# class Equipment(models.Model):
    """
    所有设备的共有字段
    设备信息
    """
    # SEIS_INSTRUMENT = 'SI'
    # POWERSUPPLY = 'PS'
    # CORE_ACCESSOR = 'CA'
    # NETWORK_DEVICE = 'ND'
    # OTHER = 'OT'
    # CATEGORY_LIST = (
    #     (SEIS_INSTRUMENT, '测震仪器'),
    #     (POWERSUPPLY, '供电系统'),
    #     (CORE_ACCESSOR, '核心配件'),
    #     (NETWORK_DEVICE, '网络设备'),
    #     (OTHER, '其它')
    # )

    # category_title = 'OT'

    name = models.CharField(max_length=64, verbose_name="仪器型号")
    features = models.CharField(max_length=64, null=True, blank=True, verbose_name="特征字符")

    # category = models.CharField(max_length=2, choices=CATEGORY_LIST, default=category_title, verbose_name='分类')

    manufacturer = models.ForeignKey("Manufacturer", null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="%(app_label)s_%(class)s_related", verbose_name="制造商")

    totality = models.PositiveIntegerField(default=0, verbose_name="总数")
    stock = models.PositiveIntegerField(default=0, verbose_name="库存")
    fault_number = models.PositiveIntegerField(default=0, verbose_name="故障数")

    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    is_deleted = models.BooleanField(default=False, verbose_name="已删除")

    @property
    def full_name(self):
        return "{manufacturer}/{model}/{features}".format(
            manufacturer=self.manufacturer,
            model=self.name,
            features=self.features
        )

    def __str__(self):
        return self.full_name

    class Meta:
        unique_together=('name', 'features',)

    # objects = EquipmentManager()


    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     self.change_category()
    #     super(Equipment, self).save(force_insert=False, force_update=False, using=None,
    #                                 update_fields=None)

    # class Meta:
    #     abstract = True


class SeismologicalEquipmentModel(Equipment):
    """
    测震系统仪器型号
    """
    SENSOR = 'SS'
    DATALOGGER = 'DL'
    INTEGRATED = 'IG'
    OTHER = 'OT'

    SEISMIC_TYPE=(
        (SENSOR, '地震仪'),
        (DATALOGGER, '数据采集器'),
        (INTEGRATED, '集成一体机'),
        (OTHER, '其它'),
    )

    type = models.CharField(choices=SEISMIC_TYPE, max_length=2, default=DATALOGGER, verbose_name="测震仪器分类")

    class Meta:
        verbose_name = "测震仪器型号"
        verbose_name_plural = "测震仪器型号"

    def __str__(self):
        return "[{type}] {manufacturer}/{name}/{features}".format(
            type=self.get_type_display(),
            manufacturer=self.manufacturer,
            name=self.name,
            features=self.features)


# class SensorModel(Equipment):
#     """
#     地震仪型号
#     """
#     cate_id = 0
#
#     class Meta:
#         verbose_name = "地震仪型号"
#         verbose_name_plural = "地震仪型号"
#         unique_together = ('name', 'features')


# class DataloggerModel(Equipment):
#     """
#     数采型号
#     """
#     cate_id = 1
#
#     class Meta:
#         verbose_name = "数采型号"
#         verbose_name_plural = "数采型号"
#         unique_together = ('name', 'features',)


class GPSAntennaModel(Equipment):
    """
    GPS天线
    """
    class Meta:
        verbose_name = "GPS天线型号"
        verbose_name_plural = "GPS天线型号"


class PowerSupplyModel(Equipment):
    """
    供电系统
    """
    BATTERY = "BT"
    DC_POWER = "DC"
    SMART_POWER = "SP"
    SOLAR_ENERGER = "SE"
    OTHER = "OT"
    POWERSUPPLY_TYPE = (
        (BATTERY, "电瓶"),
        (DC_POWER, "直流电源"),
        (SMART_POWER, "智能电源"),
        (SOLAR_ENERGER, "太阳能"),
        (OTHER, "其它")
    )

    type = models.CharField(choices=POWERSUPPLY_TYPE,
                            max_length=2, default=SMART_POWER,
                            verbose_name="电源类型")

    def __str__(self):
        return "[{type}] {manufacturer}/{name}/{features}".format(
            type=self.get_type_display(),
            manufacturer=self.manufacturer,
            name=self.name,
            features=self.features)

    class Meta:
        verbose_name = "供电设备型号"
        verbose_name_plural = "供电设备型号"


class NetworkDeviceModel(Equipment):
    ROUTER = "RT"
    INTERCHANGER = "IC"
    PHOTOCONVERTER = "PC"
    FIREWALL = "FW"
    OTHER = "OT"

    NETWORK_TYPE = (
        (ROUTER, "路由"),
        (INTERCHANGER, "交换机"),
        (PHOTOCONVERTER, "光电转换器"),
        (FIREWALL, "防火墙"),
        (OTHER, "其它"),
    )

    type = models.CharField(choices=NETWORK_TYPE,
                            max_length=2, default=ROUTER,
                            verbose_name="网络设备类型")

    def __str__(self):
        return "[{type}] {manufacturer}/{name}/{features}".format(
            type=self.get_type_display(),
            manufacturer=self.manufacturer,
            name=self.name,
            features=self.features)

    class Meta:
        verbose_name = "网络设备型号"
        verbose_name_plural = "网络设备型号"


class OtherModel(Equipment):
    class Meta:
        verbose_name = "其它设备型号"
        verbose_name_plural = "其它设备型号"


# class EquimpmentItem(PolymorphicModel):
#     station = models.ForeignKey("seisnet.Station", on_delete=models.CASCADE, verbose_name="所属台站")
#     equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE, verbose_name="设备列表")
#     quantity = models.PositiveSmallIntegerField(default=1, verbose_name="数量")
#
#     class Meta:
#         verbose_name = '设备清单'
#         verbose_name_plural = '设备清单'
#         unique_together = ('station', 'equipment')

        # abstract = True


class PowerSupplyModelItem(models.Model):
    station = models.ForeignKey("seisnet.Station", on_delete=models.CASCADE, verbose_name="所属台站")
    equipment = models.ForeignKey("PowerSupplyModel", on_delete=models.CASCADE, verbose_name="供电设备列表")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="数量")

    class Meta:
        verbose_name = '设备清单'
        verbose_name_plural = '设备清单'
        unique_together = ('station', 'equipment')

    def __str__(self):
        return self.equipment.get_type_display()


class NetworkDeviceModelItem(models.Model):
    station = models.ForeignKey("seisnet.Station", on_delete=models.CASCADE, verbose_name="所属台站")
    equipment = models.ForeignKey("NetworkDeviceModel", on_delete=models.CASCADE, verbose_name="网络设备列表")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="数量")

    class Meta:
        verbose_name = '设备清单'
        verbose_name_plural = '设备清单'
        unique_together = ('station', 'equipment')

    # def __str__(self):
    #     return self.equipment

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #
    #     super(EquimpmentItem, self).save(force_insert, force_update, using,
    #                                         update_fields)
    #     if not self.equipment or self.quantity <= 0:
    #         self.delete()

# class NetworkDeviceItem(models.Model):
#     network_device = models.ForeignKey("NetworkDevice", null=True, blank=True,
#                                        on_delete=models.SET_NULL, verbose_name="网络设备型号")
#     quantity = models.PositiveSmallIntegerField(default=1, verbose_name="数量")
#
#     station = models.ForeignKey("seisnet.Station", on_delete=models.CASCADE, related_name="network_device_item",
#                                    verbose_name="所属台站")
#
#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None):
#
#         super(NetworkDeviceItem, self).save(force_insert, force_update, using,
#                                             update_fields)
#         if not self.network_device or self.quantity <= 0:
#             self.delete()

        # print(connection.queries)


'''
设备实体,用于拥有设备编号的设备实体，
例如：地震仪和数据采集器
'''
class EquipmentEntityManager(models.Manager):
# class EquipmentEntityManager(models.Manager):
    def instock(self):
        '''
        库存
        '''
        return super(EquipmentEntityManager, self).get_queryset().filter(status=0)

    def used(self):
        '''在线'''
        return super(EquipmentEntityManager, self).get_queryset().filter(status=1)

    def malfunction(self):
        '''故障'''
        return super(EquipmentEntityManager, self).get_queryset().filter(status=2)

    def filter_by_instance(self, instance):
        return super(EquipmentEntityManager, self).get_queryset().filter(station=instance)


class SeismologicalEquipmentEntity(models.Model):
    """
    测震仪器设备实体
    """
    ENTITY_STATUS = (
        (0, "库存"),
        (1, "在线"),
        (2, "故障"),
        (3, "维修"),
        (4, "报废"),
        (5, "归还"),
        (6, "其它"),
    )

    GETWAY_TYPE = (
        (0, "自购"),
        (1, "租赁"),
        (2, "借用"),
        (3, "其它"),
    )

    model = models.ForeignKey("SeismologicalEquipmentModel", on_delete=models.DO_NOTHING,
                              related_query_name='sensor_entity', verbose_name="测震仪器型号")

    sn = models.CharField(max_length=32, unique=True, verbose_name="编号")
    station = models.ForeignKey('seisnet.Station', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name="所属台站")
    status = models.PositiveSmallIntegerField(choices=ENTITY_STATUS,
                                              default=0,
                                              verbose_name="状态")

    getway = models.PositiveSmallIntegerField(choices=GETWAY_TYPE,
                                              default=0,
                                              verbose_name="获得方式")

    remark = models.TextField(blank=True, null=True, verbose_name="备注")
    is_deleted = models.BooleanField(default=False, verbose_name="已删除")

    @property
    def full_name(self):
        return "{model}/({sn})".format(
            model=self.model,
            sn=self.sn)

    # class Meta:
    #     abstract = True
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "测震仪器实体"
        verbose_name_plural = "测震仪器实体"

    objects = EquipmentEntityManager()


# class SensorEntity(EquipmentEntity):
#
#     """
#     测震仪实体信息
#     """
#     model = models.ForeignKey("SensorModel", on_delete=models.DO_NOTHING, related_name='sensor_set',
#                               related_query_name='sensor_entity', verbose_name="地震仪型号")
#
#     station = models.ForeignKey('seisnet.Station', default=None, null=True, blank=True, on_delete=models.SET_NULL,
#                                 related_name='sensor_entities',
#                                 related_query_name='sensor_entity',
#                                 verbose_name="所属台站"
#                                 )
#
#     def __str__(self):
#         return "[{model}] {sn}".format(
#             model=self.model,
#             sn=self.sn)
#
#     class Meta:
#         verbose_name = "地震仪实体"
#         verbose_name_plural = "地震仪实体"
#         ordering = ['-id']
#
#     objects = EquipmentEntityManager()


# class DataloggerEntity(EquipmentEntity):
#     """
#     数采实体信息
#     """
#     model = models.ForeignKey("DataloggerModel",
#                               on_delete=models.DO_NOTHING,
#                               related_name="datalogger_set",
#                               related_query_name="datalogger_entity",
#                               verbose_name="数采型号")
#
#     station = models.ForeignKey('seisnet.Station',
#                                 default=None,
#                                 null=True,
#                                 blank=True,
#                                 on_delete=models.SET_NULL,
#                                 related_name='datalogger_entities',
#                                 related_query_name='datalogger_entity',
#                                 verbose_name="所属台站"
#                                 )
#
#     def __str__(self):
#         return "[{model}] {sn}".format(
#             model=self.model,
#             sn=self.sn)
#
#     class Meta:
#         verbose_name = "数采实体"
#         verbose_name_plural = "数采实体"
#         ordering = ['-id']
#
#     objects = EquipmentEntityManager()
