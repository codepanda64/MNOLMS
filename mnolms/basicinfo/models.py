from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, ReverseGenericManyToOneDescriptor

class Net(models.Model):
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
    start_time = models.DateTimeField("开始时间", null=True, blank=True)
    end_time = models.DateTimeField("结束时间", null=True, blank=True)
    min_longitude = models.FloatField(null=True, blank=True, verbose_name="台网最小经度")
    max_longitude = models.FloatField(null=True, blank=True, verbose_name="台网最大经度")
    min_latitude = models.FloatField(null=True, blank=True, verbose_name="台网最小纬度")
    max_latitude = models.FloatField(null=True, blank=True, verbose_name="台网最大纬度")
    status = models.PositiveSmallIntegerField(choices=NET_STATUS, default=0, verbose_name="台网状体")
    describe = models.CharField(max_length=512, blank=True, null=True, verbose_name="台网描述")

    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    m_time = models.DateTimeField(auto_now=True, verbose_name="更新日期")


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
    status = models.PositiveSmallIntegerField(choices=STATION_STATUS, default=0, verbose_name="台站状态")
    describe = models.CharField(max_length=512, null=True, blank=True, verbose_name="台站描述")
    location = models.CharField(max_length=512, verbose_name="位置描述")
    net = models.ForeignKey('Net', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="所属台网")

    caretaker = models.ManyToManyField('Caretaker', verbose_name="看护人")

    care_payments = models.ManyToManyField('CarePayment', verbose_name="看护费")

    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    m_time = models.DateTimeField(auto_now=True, verbose_name="更新日期")

    power_supply = models.ManyToManyField("equipment.PowerSupply")

    # power_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    # power_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="电源系统")
    # power_obj = GenericForeignKey("power_type", "power_id")


class Caretaker(models.Model):
    """
    看护人信息
    """
    CARETAKE_STATUS = (
        (1, '在看护'),
        (2, '曾看护'),
        (3, '中断')
    )

    name = models.CharField(max_length=20, verbose_name="姓名")
    gender = models.PositiveSmallIntegerField(choices=((0, '男'), (1, '女')), default=0, verbose_name="性别")
    id_card = models.CharField(max_length=64, verbose_name="身份证号")
    address = models.CharField(max_length=256, verbose_name="地址")
    phone = models.CharField(max_length=64, verbose_name="电话")

    status = models.PositiveSmallIntegerField(choices=CARETAKE_STATUS, verbose_name="状态")

    start_time = models.DateField(null=True, blank=True, verbose_name="开始时间")
    end_time = models.DateField(null=True, blank=True, verbose_name="结束时间")

    care_payments = models.ManyToManyField('CarePayment', verbose_name="看护费")

    remark = models.CharField(max_length=256, blank=True, null=True, verbose_name="备注")


class CarePayment(models.Model):
    """
    看护费信息
    """
    unit_price = models.FloatField(default=150.00, verbose_name="看护费(元/月)")
    start_pay = models.DateField(verbose_name="支付开始日期(年-月)")
    end_pay = models.DateField(verbose_name="支付截止日期(年-月)")

    pay_date = models.DateField(verbose_name="支付日期")
