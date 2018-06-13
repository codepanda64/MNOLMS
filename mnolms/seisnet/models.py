from django.db import models
from django.contrib.contenttypes.models import ContentType

from equipment.models import SeismologicalEquipmentEntity


class Network(models.Model):
    """
    台网信息
    """
    NET_STATUS = (
        (0, '运行'),
        (1, '测试'),
        (2, '下线')
    )
    code = models.CharField(max_length=10, unique=True, verbose_name="台网代码")
    name = models.CharField(max_length=64, verbose_name="台网名称")
    start_time = models.DateField("开始时间", null=True, blank=True)
    end_time = models.DateField("结束时间", null=True, blank=True)
    min_longitude = models.FloatField(null=True, blank=True, verbose_name="台网最小经度")
    max_longitude = models.FloatField(null=True, blank=True, verbose_name="台网最大经度")
    min_latitude = models.FloatField(null=True, blank=True, verbose_name="台网最小纬度")
    max_latitude = models.FloatField(null=True, blank=True, verbose_name="台网最大纬度")
    status = models.PositiveSmallIntegerField(choices=NET_STATUS, default=0, verbose_name="台网状体")
    describe = models.TextField(blank=True, null=True, verbose_name="台网描述")

    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    m_time = models.DateTimeField(auto_now=True, verbose_name="更新日期")

    class Meta:
        verbose_name = "台网信息"
        verbose_name_plural = "台网信息"

    def __str__(self):
        return "{code}-{name}".format(code=self.code, name=self.name)


class Station(models.Model):
    """
    台站信息
    """
    STATION_STATUS = (
        (0, '运行'),
        (1, '测试'),
        (2, '故障'),
        (3, '下线')
    )
    code = models.CharField(max_length=10, unique=True, verbose_name="台站代码")
    en_name = models.CharField(max_length=64, verbose_name="台站名称(英文)")
    zh_name = models.CharField(max_length=64, verbose_name="台站名称(中文)")
    longitude = models.FloatField(verbose_name="台站经度")
    latitude = models.FloatField(verbose_name="台站纬度")
    altitude = models.FloatField(verbose_name="台站高程")
    status = models.PositiveSmallIntegerField(
        choices=STATION_STATUS,
        default=0,
        verbose_name="台站状态")
    describe = models.TextField(null=True, blank=True, verbose_name="台站描述")
    location = models.TextField(null=True, blank=True, verbose_name="位置描述")
    network = models.ForeignKey(
        'Network',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="所属台网")

    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    m_time = models.DateTimeField(auto_now=True, verbose_name="更新日期")

    class Meta:
        verbose_name = "台站信息"
        verbose_name_plural = "台站信息"

    def __str__(self):
        return "{code}-{zh_name}({en_name})".format(
            code=self.code,
            zh_name=self.zh_name,
            en_name=self.en_name)

    @property
    def seismological_equipments(self):
        instance = self
        qs = SeismologicalEquipmentEntity.objects.filter_by_instance(instance)
        return qs

    # @property
    # def dataloggers(self):
    #     instance = self
    #     qs = DataloggerEntity.objects.filter(station=instance)
    #     return qs
    #
    # @property
    # def sensors(self):
    #     instance = self
    #     qs = SensorEntity.objects.filter(station=instance)
    #     # qs = SensorEntity.objects.filter_by_instance(instance)
    #     return qs


# class EquipmentItem(models.Model):
#     """
#     每个台站的设备清单
#     """
#     station = models.ForeignKey(
#         Station,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='设备清单')
#     equipment = models.ForeignKey(
#         'equipment.Equipment',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL)
#     quantity = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return '{id}'.format(id=self.id)


class Caretaker(models.Model):
    """
    看护人信息
    """
    CARETAKE_STATUS = (
        (1, '在看护'),
        (2, '曾看护'),
        (3, '中断'),
        (4, '其它')
    )

    name = models.CharField(max_length=20, verbose_name="姓名")
    gender = models.PositiveSmallIntegerField(choices=((0, '男'), (1, '女')), default=0, verbose_name="性别")
    id_card = models.CharField(max_length=64, verbose_name="身份证号")
    address = models.CharField(max_length=256, verbose_name="地址")

    status = models.PositiveSmallIntegerField(choices=CARETAKE_STATUS, verbose_name="状态")

    start_time = models.DateField(null=True, blank=True, verbose_name="开始时间")
    end_time = models.DateField(null=True, blank=True, verbose_name="结束时间")

    remark = models.CharField(max_length=256, blank=True, null=True, verbose_name="备注")

    care_station = models.ForeignKey('Station', on_delete=models.DO_NOTHING,
                                     verbose_name="看护的台站")
    is_main = models.BooleanField(default=True, verbose_name="主要看护人")

    class Meta:
        verbose_name = "看护人信息"
        verbose_name_plural = "看护人信息"

    def __str__(self):
        return "{name}({id_card})".format(name=self.name, id_card=self.id_card)


class Phone(models.Model):
    """
    电话号码
    """
    number = models.CharField(max_length=20, verbose_name="号码")
    owner = models.ForeignKey(
        'Caretaker',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="所有者")

    def __str__(self):
        return self.number


class CarePayment(models.Model):
    """
    看护费信息
    """
    unit_price = models.FloatField(default=150.00, verbose_name="看护费(元/月)")
    start_pay = models.DateField(verbose_name="支付开始日期(年-月)")
    end_pay = models.DateField(verbose_name="支付截止日期(年-月)")

    pay_date = models.DateField(verbose_name="支付日期")

    caretaker = models.ForeignKey("Caretaker", on_delete=models.DO_NOTHING,
                                  verbose_name="看护人")

    def pay_months(self):
        months = int(self.end_pay.month - self.start_pay.month + 1)
        return months if months > 0 else months+12

    class Meta:
        verbose_name = "看护费支付信息"
        verbose_name_plural = "看护费支付信息"

    def __str__(self):
        return "{unit_price} - {pay_months} - {end_pay}".format(
            unit_price=self.unit_price,
            pay_months=self.pay_months,
            end_pay=self.end_pay
        )
