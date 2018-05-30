from django.db import models
from django.contrib.contenttypes.fields import ContentType


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


class Equipment(models.Model):
    """
    所有设备的共有字段
    设备信息
    """
    CATEGORY_LIST = (
        (0, '地震仪'),
        (1, '数据采集器'),
        (2, '供电系统'),
        (3, '核心配件'),
        (4, '网络设备'),
        (5, '其它')
    )

    cate_id = 5
    category = models.PositiveSmallIntegerField(
        choices=CATEGORY_LIST,
        verbose_name='分类')

    manufacturer = models.ForeignKey("Manufacturer",
                                     null=True,
                                     blank=True,
                                     # related_name="%(app_label)s_%(class)s_related",
                                     # related_query_name="%(app_label)s_%(class)ss",
                                     on_delete=models.DO_NOTHING,
                                     verbose_name="制造商")

    totality = models.PositiveIntegerField(default=0, verbose_name="总数")
    stock = models.PositiveIntegerField(default=0, verbose_name="库存")
    fault_number = models.PositiveIntegerField(default=0, verbose_name="故障数")

    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    is_deleted = models.BooleanField(default=False, verbose_name="已删除")

    def change_category(self):
        self.category = self.cate_id

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.change_category()
        super(Equipment, self).save(force_insert=False, force_update=False, using=None,
                                    update_fields=None)

    # class Meta:
    #     abstract = True


# class Category(models.Model):
#     """
#     设备分类
#     """
#     name = models.CharField(max_length=128, verbose_name="分类名称")
#     remark = models.TextField(null=True, blank=True, verbose_name="备注")
#
#     is_deleted = models.BooleanField(default=False, verbose_name="已删除")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "设备分类"
#         verbose_name_plural = "设备分类"


class SensorModel(Equipment):
    """
    地震仪型号
    """
    cate_id = 0
    name = models.CharField(max_length=64, verbose_name="地震仪型号")
    features = models.CharField(max_length=64,
                                null=True,
                                blank=True,
                                verbose_name="特征字符")

    def __str__(self):
        return "{manufacturer}-{model}-{features}".format(
            manufacturer=self.manufacturer,
            model=self.name,
            features=self.features
        )

    class Meta:
        verbose_name = "地震仪型号"
        verbose_name_plural = "地震仪型号"


class DataloggerModel(Equipment):
    """
    数采型号
    """
    cate_id = 1
    name = models.CharField(max_length=64, verbose_name="数采型号")
    features = models.CharField(max_length=64,
                                null=True,
                                blank=True,
                                verbose_name="特征字符")

    def __str__(self):
        return "{manufacturer}-{name}-{features}".format(
            manufacturer=self.manufacturer,
            name=self.name,
            features=self.features
        )

    class Meta:
        verbose_name = "数采型号"
        verbose_name_plural = "数采型号"


class GPSAntenna(Equipment):
    """
    GPS天线
    """
    cate_id = 3
    name = models.CharField(max_length=64, unique=True, verbose_name="型号")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "GPS天线型号"
        verbose_name_plural = "GPS天线型号"


class PowerSupply(Equipment):
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
    name = models.CharField(max_length=64, unique=True, verbose_name="型号")

    cate_id = 2

    type = models.CharField(choices=POWERSUPPLY_TYPE,
                            max_length=2, default=SMART_POWER,
                            verbose_name="电源类型")

    def __str__(self):
        return "[{type}] {manufacturer}-{name}".format(
            type=self.type,
            manufacturer=self.manufacturer,
            name=self.name)

    class Meta:
        verbose_name = "供电设备型号"
        verbose_name_plural = "供电设备型号"


class NetworkDevice(Equipment):
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
    name = models.CharField(max_length=64, unique=True, verbose_name="型号")

    cate_id = 4

    type = models.CharField(choices=NETWORK_TYPE,
                            max_length=2, default=ROUTER,
                            verbose_name="网络设备类型")

    def change_category(self):
        self.category = self.cate_id

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.change_category()
        super(GPSAntenna, self).save(force_insert=False, force_update=False, using=None,
                                     update_fields=None)

    def __str__(self):
        return "[{type}] {manufacturer}-{name}".format(
            type=self.type,
            manufacturer=self.manufacturer,
            name=self.name)

    class Meta:
        verbose_name = "网络设备型号"
        verbose_name_plural = "网络设备型号"


class EquipmentEntity(models.Model):
    """
    设备实体共有信息
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

    sn = models.CharField(max_length=32, verbose_name="编号")
    status = models.PositiveSmallIntegerField(choices=ENTITY_STATUS,
                                              default=0,
                                              verbose_name="状态")

    getway = models.PositiveSmallIntegerField(choices=GETWAY_TYPE,
                                              default=0,
                                              verbose_name="获得方式")

    remark = models.TextField(blank=True, null=True, verbose_name="备注")
    is_deleted = models.BooleanField(default=False, verbose_name="已删除")


class SensorEntity(EquipmentEntity):
    """
    测震仪实体信息
    """
    model = models.ForeignKey("SensorModel",
                              on_delete=models.DO_NOTHING,
                              verbose_name="地震仪型号")

    def __str__(self):
        return "[{model}] {sn}".format(
            model=self.model,
            sn=self.sn)

    class Meta:
        verbose_name = "地震仪实体"
        verbose_name_plural = "地震仪实体"


class DataloggerEntity(EquipmentEntity):
    """
    数采实体信息
    """
    model = models.ForeignKey("DataloggerModel",
                              on_delete=models.DO_NOTHING,
                              verbose_name="数采型号")

    def __str__(self):
        return "[{model}] {sn}".format(
            model=self.model,
            sn=self.sn)

    class Meta:
        verbose_name = "数采实体"
        verbose_name_plural = "数采实体"
