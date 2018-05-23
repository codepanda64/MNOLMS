# Generated by Django 2.0 on 2018-05-23 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicinfo', '0005_auto_20180523_1451'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='分类名称')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='设备名称')),
                ('equipment_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='电源系统')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='设备', to='equipment.Category')),
                ('equipment_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
        ),
        migrations.RemoveField(
            model_name='battery',
            name='powersupply_ptr',
        ),
        migrations.RemoveField(
            model_name='charger',
            name='powersupply_ptr',
        ),
        migrations.RemoveField(
            model_name='dataloggerfeatures',
            name='datalogger_model',
        ),
        migrations.RemoveField(
            model_name='sensorfeatures',
            name='sensor_model',
        ),
        migrations.RemoveField(
            model_name='solarpanel',
            name='powersupply_ptr',
        ),
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'verbose_name': '制造商信息', 'verbose_name_plural': '制造商信息'},
        ),
        migrations.AlterModelOptions(
            name='sensormodel',
            options={'verbose_name': '地震仪型号', 'verbose_name_plural': '地震仪型号'},
        ),
        migrations.RemoveField(
            model_name='datalogger',
            name='features',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='features',
        ),
        migrations.AddField(
            model_name='datalogger',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='已删除'),
        ),
        migrations.AddField(
            model_name='dataloggermodel',
            name='features',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='特征字符'),
        ),
        migrations.AddField(
            model_name='dataloggermodel',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='已删除'),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='地址'),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='已删除'),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='zip_code',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='邮编'),
        ),
        migrations.AddField(
            model_name='powersupply',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='已删除'),
        ),
        migrations.AddField(
            model_name='powersupply',
            name='type',
            field=models.CharField(choices=[('BT', '电瓶'), ('DC', '直流电源'), ('SP', '智能电源'), ('SE', '太阳能'), ('OT', '其它')], default='SP', max_length=2, verbose_name='电源类型'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='已删除'),
        ),
        migrations.AddField(
            model_name='sensormodel',
            name='features',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='特征字符'),
        ),
        migrations.AddField(
            model_name='sensormodel',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='已删除'),
        ),
        migrations.DeleteModel(
            name='Battery',
        ),
        migrations.DeleteModel(
            name='Charger',
        ),
        migrations.DeleteModel(
            name='DataloggerFeatures',
        ),
        migrations.DeleteModel(
            name='SensorFeatures',
        ),
        migrations.DeleteModel(
            name='SolarPanel',
        ),
    ]