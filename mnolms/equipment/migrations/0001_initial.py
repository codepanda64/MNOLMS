# Generated by Django 2.0 on 2018-06-13 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seisnet', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='仪器型号')),
                ('features', models.CharField(blank=True, max_length=64, null=True, verbose_name='特征字符')),
                ('totality', models.PositiveIntegerField(default=0, verbose_name='总数')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='库存')),
                ('fault_number', models.PositiveIntegerField(default=0, verbose_name='故障数')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='制造商名称')),
                ('alias_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='别名')),
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
            options={
                'verbose_name': '制造商分类',
                'verbose_name_plural': '制造商分类',
            },
        ),
        migrations.CreateModel(
            name='NetworkDeviceModelItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='数量')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seisnet.Station', verbose_name='所属台站')),
            ],
            options={
                'verbose_name': '设备清单',
                'verbose_name_plural': '设备清单',
            },
        ),
        migrations.CreateModel(
            name='PowerSupplyModelItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='数量')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seisnet.Station', verbose_name='所属台站')),
            ],
            options={
                'verbose_name': '设备清单',
                'verbose_name_plural': '设备清单',
            },
        ),
        migrations.CreateModel(
            name='SeismologicalEquipmentEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=32, unique=True, verbose_name='编号')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '库存'), (1, '在线'), (2, '故障'), (3, '维修'), (4, '报废'), (5, '归还'), (6, '其它')], default=0, verbose_name='状态')),
                ('getway', models.PositiveSmallIntegerField(choices=[(0, '自购'), (1, '租赁'), (2, '借用'), (3, '其它')], default=0, verbose_name='获得方式')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('station', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='seisnet.Station', verbose_name='所属台站')),
            ],
            options={
                'verbose_name': '测震仪器实体',
                'verbose_name_plural': '测震仪器实体',
            },
        ),
        migrations.CreateModel(
            name='GPSAntennaModel',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Equipment')),
            ],
            options={
                'verbose_name': 'GPS天线型号',
                'verbose_name_plural': 'GPS天线型号',
            },
            bases=('equipment.equipment',),
        ),
        migrations.CreateModel(
            name='NetworkDeviceModel',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Equipment')),
                ('type', models.CharField(choices=[('RT', '路由'), ('IC', '交换机'), ('PC', '光电转换器'), ('FW', '防火墙'), ('OT', '其它')], default='RT', max_length=2, verbose_name='网络设备类型')),
            ],
            options={
                'verbose_name': '网络设备型号',
                'verbose_name_plural': '网络设备型号',
            },
            bases=('equipment.equipment',),
        ),
        migrations.CreateModel(
            name='OtherModel',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Equipment')),
            ],
            options={
                'verbose_name': '其它设备型号',
                'verbose_name_plural': '其它设备型号',
            },
            bases=('equipment.equipment',),
        ),
        migrations.CreateModel(
            name='PowerSupplyModel',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Equipment')),
                ('type', models.CharField(choices=[('BT', '电瓶'), ('DC', '直流电源'), ('SP', '智能电源'), ('SE', '太阳能'), ('OT', '其它')], default='SP', max_length=2, verbose_name='电源类型')),
            ],
            options={
                'verbose_name': '供电设备型号',
                'verbose_name_plural': '供电设备型号',
            },
            bases=('equipment.equipment',),
        ),
        migrations.CreateModel(
            name='SeismologicalEquipmentModel',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Equipment')),
                ('type', models.CharField(choices=[('SS', '地震仪'), ('DL', '数据采集器'), ('IG', '集成一体机'), ('OT', '其它')], default='DL', max_length=2, verbose_name='测震仪器分类')),
            ],
            options={
                'verbose_name': '测震仪器型号',
                'verbose_name_plural': '测震仪器型号',
            },
            bases=('equipment.equipment',),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='category',
            field=models.ManyToManyField(to='equipment.ManufacturerCategory', verbose_name='制造商分类'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipment_equipment_related', to='equipment.Manufacturer', verbose_name='制造商'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_equipment.equipment_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='seismologicalequipmententity',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_query_name='sensor_entity', to='equipment.SeismologicalEquipmentModel', verbose_name='测震仪器型号'),
        ),
        migrations.AddField(
            model_name='powersupplymodelitem',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.PowerSupplyModel', verbose_name='供电设备列表'),
        ),
        migrations.AddField(
            model_name='networkdevicemodelitem',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.NetworkDeviceModel', verbose_name='网络设备列表'),
        ),
        migrations.AlterUniqueTogether(
            name='equipment',
            unique_together={('name', 'features')},
        ),
        migrations.AlterUniqueTogether(
            name='powersupplymodelitem',
            unique_together={('station', 'equipment')},
        ),
        migrations.AlterUniqueTogether(
            name='networkdevicemodelitem',
            unique_together={('station', 'equipment')},
        ),
    ]
