# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccidentCasualty(models.Model):
    accident = models.OneToOneField('Accidents', models.DO_NOTHING, db_column='Accident_Id', primary_key=True)  # Field name made lowercase.
    casualty = models.ForeignKey('Casualty', models.DO_NOTHING, db_column='Casualty_Id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accident_casualty'
        unique_together = (('accident', 'casualty'),)


class AccidentDate(models.Model):
    accident = models.OneToOneField('Accidents', models.DO_NOTHING, db_column='Accident_Id', primary_key=True)  # Field name made lowercase.
    date = models.ForeignKey('Date', models.DO_NOTHING, db_column='Date_Id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accident_date'
        unique_together = (('accident', 'date'),)


class AccidentLocation(models.Model):
    accident = models.OneToOneField('Accidents', models.DO_NOTHING, db_column='Accident_Id', primary_key=True)  # Field name made lowercase.
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='Location_Id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accident_location'
        unique_together = (('accident', 'location'),)


class AccidentVehicle(models.Model):
    accident = models.OneToOneField('Accidents', models.DO_NOTHING, db_column='Accident_Id', primary_key=True)  # Field name made lowercase.
    vehicle = models.ForeignKey('Vehicles', models.DO_NOTHING, db_column='Vehicle_Id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accident_vehicle'
        unique_together = (('accident', 'vehicle'),)


class Accidents(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    accident_index = models.TextField(db_column='Accident_Index', blank=True, null=True)  # Field name made lowercase.
    accident_severity = models.CharField(db_column='Accident_Severity', max_length=7, blank=True, null=True)  # Field name made lowercase.
    weather_conditions = models.CharField(db_column='Weather_Conditions', max_length=28)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accidents'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Casualty(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    casualty_severity = models.CharField(db_column='Casualty_Severity', max_length=7, blank=True, null=True)  # Field name made lowercase.
    casualty_type = models.CharField(db_column='Casualty_Type', max_length=56, blank=True, null=True)  # Field name made lowercase.
    age_of_casualty = models.IntegerField(db_column='Age_of_Casualty', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'casualty'


class Date(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    day_of_week = models.CharField(db_column='Day_of_Week', max_length=9, blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'date'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Location(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    urban_or_rural_area = models.CharField(db_column='Urban_or_Rural_Area', max_length=11, blank=True, null=True)  # Field name made lowercase.
    accidents = models.ManyToManyField(Accidents)


    class Meta:
        managed = False
        db_table = 'location'


class LocationDate(models.Model):
    location = models.OneToOneField(Location, models.DO_NOTHING, db_column='Location_Id', primary_key=True)  # Field name made lowercase.
    date = models.ForeignKey(Date, models.DO_NOTHING, db_column='Date_Id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'location_date'
        unique_together = (('location', 'date'),)


class VehicleCasualty(models.Model):
    vehicle = models.OneToOneField('Vehicles', models.DO_NOTHING, db_column='Vehicle_Id', primary_key=True)  # Field name made lowercase.
    casualty = models.ForeignKey(Casualty, models.DO_NOTHING, db_column='Casualty_Id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vehicle_casualty'
        unique_together = (('vehicle', 'casualty'),)


class Vehicles(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    vehicle_type = models.CharField(db_column='Vehicle_Type', max_length=37, blank=True, null=True)  # Field name made lowercase.
    was_vehicle_left_hand_driver = models.IntegerField(db_column='Was_Vehicle_Left_Hand_Driver', blank=True, null=True)  # Field name made lowercase.
    age_of_vehicle = models.IntegerField(db_column='Age_of_Vehicle', blank=True, null=True)  # Field name made lowercase.
    vehicle_manoeuvre = models.CharField(db_column='Vehicle_Manoeuvre', max_length=35, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vehicles'
