from django.db import models
from django.contrib.contenttypes.fields import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation


class Manufacturer(models.Model):
    """
    制造商信息
    """
    name = models.CharField(max_length=64, verbose_name="制造商名称")
    address = models.CharField(max_length=128,
                               null=True,
                               blank=True,
                               verbose_name="地址")
    zip_code = models.CharField(max_length=12,
                                null=True,
                                blank=True,
                                verbose_name="邮编")
    is_delete = models.BooleanField(default=False, verbose_name="已删除")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "制造商信息"
        verbose_name_plural = "制造商信息"


class Equipment(models.Model):
    """
    设备信息
    """
    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="设备")
    name = models.CharField(max_length=128, verbose_name="设备名称")
    # manufacturer = models.ForeignKey("Manufacturer",
    #                                  null=True,
    #                                  blank=True,
    #                                  on_delete=models.SET_NULL,
    #                                  verbose_name="制造商")
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()


class Category(models.Model):
    """
    设备分类
    """
    name = models.CharField(max_length=128, verbose_name="分类名称")


class SensorModel(models.Model):
    """
    地震仪型号
    """
    name = models.CharField(max_length=64, verbose_name="地震仪型号")
    manufacturer = models.ForeignKey("Manufacturer",
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name="制造商")
    features = models.CharField(max_length=64,
                                null=True,
                                blank=True,
                                verbose_name="特征字符")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")

    equipment = GenericRelation(Equipment)
    is_delete = models.BooleanField(default=False, verbose_name="已删除")

    def __str__(self):
        return "{manufacturer}-{model}-{features}".format(
            manufacturer=self.manufacturer.name,
            model=self.name,
            features=self.features
        )

    class Meta:
        verbose_name = "地震仪型号"
        verbose_name_plural = "地震仪型号"


# class SensorFeatures(models.Model):
#     """
#     地震仪器特征
#     """
#     name = models.CharField(max_length=64, verbose_name="地震仪特征")
#     sensor_model = models.ForeignKey("SensorModel",
#                                      null=True,
#                                      blank=True,
#                                      on_delete=models.SET_NULL,
#                                      verbose_name="地震仪型号")
#     remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")


class DataloggerModel(models.Model):
    """
    数采型号
    """
    name = models.CharField(max_length=64, verbose_name="数采型号")
    manufacturer = models.ForeignKey("Manufacturer",
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name="制造商")
    features = models.CharField(max_length=64,
                                null=True,
                                blank=True,
                                verbose_name="特征字符")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")
    is_delete = models.BooleanField(default=False, verbose_name="已删除")

    equipment = GenericRelation(Equipment)


# class DataloggerFeatures(models.Model):
#     """
#     数采特征
#     """
#     name = models.CharField(max_length=64, verbose_name="数采特征")
#     datalogger_model = models.ForeignKey("DataloggerModel",
#                                          null=True,
#                                          blank=True,
#                                          on_delete=models.SET_NULL,
#                                          verbose_name="数采型号")
#     remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")


# class DataloggerSamplingRate(models.Model):
#     rate = models.IntegerField(verbose_name="采样率")
#     datalogger_features = models.ForeignKey("DataloggerFeatures", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="数采特征")
#     remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")


class Sensor(models.Model):
    """
    测震仪信息
    """
    SENSOR_STATUS = (
        (1, "库存"),
        (2, "在线"),
        (3, "故障"),
        (4, "维修"),
        (5, "报废"),
        (6, "归还")
    )
    code = models.CharField(max_length=32, verbose_name="编号")
    model = models.ForeignKey("SensorModel",
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              verbose_name="地震仪型号")
    # features = models.ForeignKey("SensorFeatures",
    #                              null=True,
    #                              blank=True,
    #                              on_delete=models.SET_NULL,
    #                              verbose_name="地震仪特征")
    status = models.PositiveSmallIntegerField(choices=SENSOR_STATUS,
                                              default=0,
                                              verbose_name="状态")

    is_delete = models.BooleanField(default=False, verbose_name="已删除")
    remark = models.CharField(max_length=256, blank=True, null=True, verbose_name="备注")


class Datalogger(models.Model):
    """
    数采信息
    """
    DATALOGGER_STATUS = (
        (1, "库存"),
        (2, "在线"),
        (3, "故障"),
        (4, "维修"),
        (5, "报废"),
        (6, "归还")
    )
    code = models.CharField(max_length=32, verbose_name="编号")
    model = models.ForeignKey("DataloggerModel",
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              verbose_name="数采型号")
    # features = models.ForeignKey("DataloggerFeatures",
    #                              null=True,
    #                              blank=True,
    #                              on_delete=models.SET_NULL,
    #                              verbose_name="数采特征")
    status = models.PositiveSmallIntegerField(choices=DATALOGGER_STATUS,
                                              default=0,
                                              verbose_name="状态")
    is_delete = models.BooleanField(default=False, verbose_name="已删除")
    remark = models.CharField(max_length=256, blank=True, null=True, verbose_name="备注")


class PowerSupply(models.Model):
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
    model = models.CharField(max_length=64, verbose_name="型号")
    manufacturer = models.ForeignKey("Manufacturer",
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name="制造商")
    number = models.IntegerField(default=0, verbose_name="数量")
    inventory = models.IntegerField(default=0, verbose_name="库存")
    type = models.CharField(choices=POWERSUPPLY_TYPE,
                            max_length=2, default=SMART_POWER,
                            verbose_name="电源类型")
    is_delete = models.BooleanField(default=False, verbose_name="已删除")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")

    equipment = GenericRelation(Equipment)

    def __str__(self):
        return "{power_type}-{manufacturer}/{model}".format(
            power_type=self.type,
            manufacturer=self.manufacturer.name,
            model=self.model)

# class Battery(PowerSupply):
#     """
#     电瓶信息
#     """
#     voltage = models.FloatField(verbose_name="标称电压(V)")
#     capacity = models.FloatField(verbose_name="容量(Ah)")
#
#
# class Charger(PowerSupply):
#     """
#     电源
#     """
#     is_support_solar = models.BooleanField(verbose_name="是否支持太阳能")
#     is_support_electricity = models.BooleanField(verbose_name="是否支持市电")
#     is_support_battery = models.BooleanField(verbose_name="是否支持电瓶充电")
#
#
# class SolarPanel(PowerSupply):
#     """
#     太阳能板
#     """
#     power = models.FloatField(verbose_name="功率")
#     width = models.FloatField(verbose_name="宽(mm)")
#     high = models.FloatField(verbose_name="高(mm)")
