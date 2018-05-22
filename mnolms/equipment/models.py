from django.db import models
from django.contrib.contenttypes.fields import GenericRelation


class Manufacturer(models.Model):
    """
    制造商信息
    """

    name = models.CharField(max_length=64, verbose_name="制造商名称")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="描述")


class SensorModel(models.Model):
    """
    地震仪型号
    """
    name = models.CharField(max_length=64, verbose_name="地震仪型号")
    manufacturer = models.ForeignKey("Manufacturer", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="制造商")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")


class SensorFeatures(models.Model):
    """
    地震仪器特征
    """
    name = models.CharField(max_length=64, verbose_name="地震仪特征")
    sensor_model = models.ForeignKey("SensorModel", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="地震仪型号")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")


class DataloggerModel(models.Model):
    """
    数采型号
    """
    name = models.CharField(max_length=64, verbose_name="数采型号")
    manufacturer = models.ForeignKey("Manufacturer", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="制造商")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")


class DataloggerFeatures(models.Model):
    """
    数采特征
    """
    name = models.CharField(max_length=64, verbose_name="数采特征")
    datalogger_model = models.ForeignKey("DataloggerModel", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="数采型号")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")


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
    model = models.ForeignKey("SensorModel", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="地震仪型号")
    features = models.ForeignKey("SensorFeatures", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="地震仪特征")
    status = models.PositiveSmallIntegerField(choices=SENSOR_STATUS, default=0, verbose_name="状态")
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
    model = models.ForeignKey("DataloggerModel", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="数采型号")
    features = models.ForeignKey("DataloggerFeatures", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="数采特征")
    status = models.PositiveSmallIntegerField(choices=DATALOGGER_STATUS, default=0, verbose_name="状态")
    remark = models.CharField(max_length=256, blank=True, null=True, verbose_name="备注")


class PowerSupply(models.Model):
    """
    供电系统
    """
    model = models.CharField(max_length=64, verbose_name="型号")
    manufacturer = models.ForeignKey("Manufacturer", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="制造商")
    number = models.IntegerField(default=0, verbose_name="数量")
    inventory = models.IntegerField(default=0, verbose_name="库存")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")
    # station = GenericRelation("basicinfo.Station")


class Battery(PowerSupply):
    """
    电瓶信息
    """
    voltage = models.FloatField(verbose_name="标称电压(V)")
    capacity = models.FloatField(verbose_name="容量(Ah)")


class Charger(PowerSupply):
    """
    电源
    """
    is_support_solar = models.BooleanField(verbose_name="是否支持太阳能")
    is_support_electricity = models.BooleanField(verbose_name="是否支持市电")
    is_support_battery = models.BooleanField(verbose_name="是否支持电瓶充电")


class SolarPanel(PowerSupply):
    """
    太阳能板
    """
    power = models.FloatField(verbose_name="功率")
    width = models.FloatField(verbose_name="宽(mm)")
    high = models.FloatField(verbose_name="高(mm)")

