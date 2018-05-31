# Generated by Django 2.0 on 2018-05-31 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seisnet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataloggerEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=32, verbose_name='编号')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '库存'), (1, '在线'), (2, '故障'), (3, '维修'), (4, '报废'), (5, '归还'), (6, '其它')], default=0, verbose_name='状态')),
                ('getway', models.PositiveSmallIntegerField(choices=[(0, '自购'), (1, '租赁'), (2, '借用'), (3, '其它')], default=0, verbose_name='获得方式')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '数采实体',
                'verbose_name_plural': '数采实体',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DataloggerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(choices=[(0, '地震仪'), (1, '数据采集器'), (2, '供电系统'), (3, '核心配件'), (4, '网络设备'), (5, '其它')], verbose_name='分类')),
                ('totality', models.PositiveIntegerField(default=0, verbose_name='总数')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='库存')),
                ('fault_number', models.PositiveIntegerField(default=0, verbose_name='故障数')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('name', models.CharField(max_length=64, verbose_name='数采型号')),
                ('features', models.CharField(blank=True, max_length=64, null=True, verbose_name='特征字符')),
            ],
            options={
                'verbose_name': '数采型号',
                'verbose_name_plural': '数采型号',
            },
        ),
        migrations.CreateModel(
            name='GPSAntenna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(choices=[(0, '地震仪'), (1, '数据采集器'), (2, '供电系统'), (3, '核心配件'), (4, '网络设备'), (5, '其它')], verbose_name='分类')),
                ('totality', models.PositiveIntegerField(default=0, verbose_name='总数')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='库存')),
                ('fault_number', models.PositiveIntegerField(default=0, verbose_name='故障数')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='型号')),
            ],
            options={
                'verbose_name': 'GPS天线型号',
                'verbose_name_plural': 'GPS天线型号',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='制造商名称')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='地址')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '制造商信息',
                'verbose_name_plural': '制造商信息',
            },
        ),
        migrations.CreateModel(
            name='ManufacturerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='制造商分类名称')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(choices=[(0, '地震仪'), (1, '数据采集器'), (2, '供电系统'), (3, '核心配件'), (4, '网络设备'), (5, '其它')], verbose_name='分类')),
                ('totality', models.PositiveIntegerField(default=0, verbose_name='总数')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='库存')),
                ('fault_number', models.PositiveIntegerField(default=0, verbose_name='故障数')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='型号')),
                ('type', models.CharField(choices=[('RT', '路由'), ('IC', '交换机'), ('PC', '光电转换器'), ('FW', '防火墙'), ('OT', '其它')], default='RT', max_length=2, verbose_name='网络设备类型')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='equipment.Manufacturer', verbose_name='制造商')),
            ],
            options={
                'verbose_name': '网络设备型号',
                'verbose_name_plural': '网络设备型号',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PowerSupply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(choices=[(0, '地震仪'), (1, '数据采集器'), (2, '供电系统'), (3, '核心配件'), (4, '网络设备'), (5, '其它')], verbose_name='分类')),
                ('totality', models.PositiveIntegerField(default=0, verbose_name='总数')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='库存')),
                ('fault_number', models.PositiveIntegerField(default=0, verbose_name='故障数')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='型号')),
                ('type', models.CharField(choices=[('BT', '电瓶'), ('DC', '直流电源'), ('SP', '智能电源'), ('SE', '太阳能'), ('OT', '其它')], default='SP', max_length=2, verbose_name='电源类型')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='equipment.Manufacturer', verbose_name='制造商')),
            ],
            options={
                'verbose_name': '供电设备型号',
                'verbose_name_plural': '供电设备型号',
            },
        ),
        migrations.CreateModel(
            name='SensorEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=32, verbose_name='编号')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '库存'), (1, '在线'), (2, '故障'), (3, '维修'), (4, '报废'), (5, '归还'), (6, '其它')], default=0, verbose_name='状态')),
                ('getway', models.PositiveSmallIntegerField(choices=[(0, '自购'), (1, '租赁'), (2, '借用'), (3, '其它')], default=0, verbose_name='获得方式')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '地震仪实体',
                'verbose_name_plural': '地震仪实体',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SensorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(choices=[(0, '地震仪'), (1, '数据采集器'), (2, '供电系统'), (3, '核心配件'), (4, '网络设备'), (5, '其它')], verbose_name='分类')),
                ('totality', models.PositiveIntegerField(default=0, verbose_name='总数')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='库存')),
                ('fault_number', models.PositiveIntegerField(default=0, verbose_name='故障数')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('name', models.CharField(max_length=64, verbose_name='地震仪型号')),
                ('features', models.CharField(blank=True, max_length=64, null=True, verbose_name='特征字符')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='equipment.Manufacturer', verbose_name='制造商')),
            ],
            options={
                'verbose_name': '地震仪型号',
                'verbose_name_plural': '地震仪型号',
            },
        ),
        migrations.AddField(
            model_name='sensorentity',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sensor_set', related_query_name='sensor_entity', to='equipment.SensorModel', verbose_name='地震仪型号'),
        ),
        migrations.AddField(
            model_name='sensorentity',
            name='station',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensor_entities', related_query_name='sensor_entity', to='seisnet.Station', verbose_name='所属台站'),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='category',
            field=models.ManyToManyField(to='equipment.ManufacturerCategory', verbose_name='制造商分类'),
        ),
        migrations.AddField(
            model_name='gpsantenna',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='equipment.Manufacturer', verbose_name='制造商'),
        ),
        migrations.AddField(
            model_name='dataloggermodel',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='equipment.Manufacturer', verbose_name='制造商'),
        ),
        migrations.AddField(
            model_name='dataloggerentity',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='datalogger_set', related_query_name='datalogger_entity', to='equipment.DataloggerModel', verbose_name='数采型号'),
        ),
        migrations.AddField(
            model_name='dataloggerentity',
            name='station',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='datalogger_entities', related_query_name='datalogger_entity', to='seisnet.Station', verbose_name='所属台站'),
        ),
    ]
