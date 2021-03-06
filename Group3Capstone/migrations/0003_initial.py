# Generated by Django 4.0.3 on 2022-03-05 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Group3Capstone', '0002_delete_admin_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('Event_Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('Location_Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Location_Name', models.CharField(max_length=40, null=True)),
                ('Location_Address', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('Sport_Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Sport_Name', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('User_ID', models.BigAutoField(primary_key=True, serialize=False)),
                ('User_Password', models.CharField(blank=True, max_length=20, unique=True)),
                ('User_FName', models.CharField(max_length=40, null=True)),
                ('User_LName', models.CharField(max_length=40, null=True)),
                ('User_DOB', models.DateField(null=True)),
                ('User_Address', models.CharField(max_length=100, null=True)),
                ('User_Phone', models.IntegerField(null=True)),
                ('UserName', models.CharField(max_length=40, null=True)),
                ('User_Email', models.CharField(max_length=40, null=True)),
                ('Account_type', models.CharField(choices=[('A', 'Administrator'), ('U', 'User')], default='A', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('Reservation_Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Group3Capstone.event')),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Group3Capstone.user')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('Group_Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Group3Capstone.user')),
                ('Sport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Group3Capstone.sport')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='Creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Group3Capstone.user'),
        ),
        migrations.AddField(
            model_name='event',
            name='Group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Group3Capstone.group'),
        ),
        migrations.AddField(
            model_name='event',
            name='Location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Group3Capstone.location'),
        ),
    ]
