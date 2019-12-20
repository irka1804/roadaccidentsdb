import pandas as pd
import numpy as np
import MySQLdb
from dateutil.parser import parse
import time
import sys
import random

casualty_type = [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23, 90, 97, 98, ]
casualty_type_map = {}
for i, v in enumerate(casualty_type):
    casualty_type_map[v] = i

vehicle_type = [1, 2, 3, 4, 5, 8, 9, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23, 90, 97, 98, -1, ]
vehicle_type_map = {}
for i, v in enumerate(vehicle_type):
    vehicle_type_map[v] = i

tmp_path = '/Users/iyakuncheva/Road/tmp/'
create_tables = True
rebuild_data = True


def clear_sql(s):
    s = s.replace('\t', ' ').replace('\n', ' ')
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s


if create_tables:
    print(time.strftime('%I%p:%M:%S'), 'Connecting to DB')
    connection = MySQLdb.connect(user="root",
                                 passwd="irina1234",
                                 host="localhost",
                                 db="RoadAccidentsDB", )
    cur = connection.cursor()

    print(time.strftime('%I%p:%M:%S'), 'Creating tables')

    # create accidents
    query = clear_sql('''
        create table if not exists accidents
      (
       Id int auto_increment,
       Accident_Index longtext null,
       Accident_Severity enum('fatal', 'serious', 'slight') null,
       Weather_Conditions enum('Fine no high winds', 'Raining no high winds', 'Snowing no high winds', 'Fine + high winds', 'Raining + high winds', 'Snowing + high winds', 'Fog or mist', 'Other', 'Unknown', 'Data missing or out of range') not null,
       constraint accident_pk
        primary key (Id)
      )
    ''')
    cur.execute(query)

    # create date
    query = clear_sql('''create table  if not exists date
      (
       Id int auto_increment,
       Day_of_Week enum('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') null,
       Time time null,
       Date date null,
       constraint date_pk
        primary key (Id)
      )''')
    cur.execute(query)

    # create location
    query = clear_sql('''create table  if not exists location
      (
       Id int auto_increment,
       Longitude float null,
       Latitude float null,
       Urban_or_Rural_Area enum('urban', 'rural', 'Unallocated') null,
       constraint location_pk
        primary key (Id)
      )''')
    cur.execute(query)

    # create location
    query = clear_sql('''create table  if not exists casualty
      (
       Id int auto_increment,
       Casualty_Severity enum('fatal', 'serious', 'slight') null,
       Casualty_Type enum('Pedestrian', 'Cyclist', 'Motorcycle 50cc and under rider or passenger', 'Motorcycle 125cc and under rider or passenger', 'Motorcycle over 125cc and up to 500cc rider or passenger', 'Motorcycle over 500cc rider or passenger', 'Taxi/Private hire car occupant', 'Car occupant', 'Minibus (8 - 16 passenger seats) occupant', 'Bus or coach occupant (17 or more pass seats)', 'Horse rider', 'Agricultural vehicle occupant', 'Tram occupant', 'Van / Goods vehicle (3.5 tonnes mgw or under) occupant', 'Goods vehicle (over 3.5t. and under 7.5t.) occupant', 'Goods vehicle (7.5 tonnes mgw and over) occupant', 'Mobility scooter rider', 'Electric motorcycle rider or passenger', 'Other vehicle occupant', 'Motorcycle - unknown cc rider or passenger', 'Goods vehicle (unknown weight) occupant') null,
       Age_of_Casualty int null,
       constraint casualty_pk
        primary key (Id)
      )''')
    cur.execute(query)

    # create location
    query = clear_sql('''create table  if not exists vehicles
      (
       Id int auto_increment,
       Vehicle_Type enum('Pedal cycle', 'Motorcycle 50cc and under', 'Motorcycle 125cc and under', 'Motorcycle over 125cc and up to 500cc', 'Motorcycle over 500cc', 'Taxi/Private hire car', 'Car', 'Minibus (8 - 16 passenger seats)', 'Bus or coach (17 or more pass seats)', 'Ridden horse', 'Agricultural vehicle', 'Tram', 'Van / Goods 3.5 tonnes mgw or under', 'Goods over 3.5t. and under 7.5t', 'Goods 7.5 tonnes mgw and over', 'Mobility scooter', 'Electric motorcycle', 'Other vehicle', 'Motorcycle - unknown cc', 'Goods vehicle - unknown weight', 'Data missing or out of range') null,
       Was_Vehicle_Left_Hand_Driver tinyint null,
       Age_of_Vehicle int null,
       Vehicle_Manoeuvre enum('Reversing', 'Parked', 'Waiting to go - held up', 'Slowing or stopping', 'Moving off', 'U-turn', 'Turning left', 'Waiting to turn left', 'Turning right', 'Waiting to turn right', 'Changing lane to left', 'Changing lane to right', 'Overtaking moving vehicle - offside', 'Overtaking static vehicle - offside', 'Overtaking - nearside', 'Going ahead left-hand bend', 'Going ahead right-hand bend', 'Going ahead other', 'Data missing or out of range'),
       constraint vehicles_pk
        primary key (Id)
      )''')
    cur.execute(query)

    # add forein keys
    # create location_date
    query = clear_sql('''create table  if not exists location_date
    (
     Location_Id int not null,
     Date_Id int not null,
     constraint location_date_pk
      primary key (Location_Id, Date_Id),
     constraint location_date_date_Id_fk
      foreign key (Date_Id) references date (Id),
     constraint location_date_location_Id_fk
      foreign key (Location_Id) references location (Id)
    );''')
    cur.execute(query)

    # create accident_date
    query = clear_sql('''create table  if not exists accident_date
(
 Accident_Id int not null,
 Date_Id int not null,
 constraint accident_date_pk
  primary key (Accident_Id, Date_Id),
 constraint accident_date_accident_Id_fk
  foreign key (Accident_Id) references accidents (Id),
 constraint accident_date_date_Id_fk
  foreign key (Date_Id) references date (Id)
);''')
    cur.execute(query)

    # create accident_location
    query = clear_sql('''create table  if not exists accident_location
(
 Accident_Id int not null,
 Location_Id int not null,
 constraint accident_location_pk
  primary key (Accident_Id, Location_Id),
 constraint accident_location_accident_Id_fk
  foreign key (Accident_Id) references accidents (Id),
 constraint accident_location_location_Id_fk
  foreign key (Location_Id) references location (Id)
);''')
    cur.execute(query)

    # create accident_casualty
    query = clear_sql('''create table  if not exists accident_casualty
(
 Accident_Id int not null,
 Casualty_Id int not null,
 constraint accident_casualty_pk
  primary key (Accident_Id, Casualty_Id),
 constraint accident_casualty_accident_Id_fk
  foreign key (Accident_Id) references accidents (Id),
 constraint accident_casualty_casualty_Id_fk
  foreign key (Casualty_Id) references casualty (Id)
);''')
    cur.execute(query)

    # create vehicle_casualty
    query = clear_sql('''create table  if not exists vehicle_casualty
(
 Vehicle_Id int not null,
 Casualty_Id int not null,
 constraint vehicle_casualty_pk
  primary key (Vehicle_Id, Casualty_Id),
 constraint vehicle_casualty_casualty_Id_fk
  foreign key (Casualty_Id) references casualty (Id),
 constraint vehicle_casualty_vehicles_Id_fk
  foreign key (Vehicle_Id) references vehicles (Id)
);''')
    cur.execute(query)

    # create accident_vehicle
    query = clear_sql('''create table  if not exists accident_vehicle
(
 Accident_Id int not null,
 Vehicle_Id int not null,
 constraint accident_vehicle_pk
  primary key (Accident_Id, Vehicle_Id),
 constraint accident_vehicle_accident_Id_fk
  foreign key (Accident_Id) references accidents (Id),
 constraint accident_vehicle_vehicles_Id_fk
  foreign key (Vehicle_Id) references vehicles (Id)
);''')
    cur.execute(query)

    connection.commit()

if rebuild_data:
    nrows = 1000
    print(time.strftime('%I%p:%M:%S'), 'Reading files')
    acc = pd.read_csv('./acc2005_2016.csv', nrows=nrows)
    cas = pd.read_csv('./cas2005_2016.csv', nrows=nrows)
    veh = pd.read_csv('./veh2005_2016.csv', nrows=nrows)

    veh['id'] = pd.Series(np.arange(nrows))
    acc['id'] = pd.Series(np.arange(nrows))
    cas['id'] = pd.Series(np.arange(nrows))

    acc = acc.rename(str.lower, axis='columns')
    veh = veh.rename(str.lower, axis='columns')
    cas = cas.rename(str.lower, axis='columns')

    cas['casualty_type'] = cas['casualty_type'].map(casualty_type_map)
    veh['vehicle_type'] = veh['vehicle_type'].map(vehicle_type_map)

    def convert_time(elem):
        return parse(elem).strftime("%Y/%m/%d")

    acc['date'] = acc['date'].apply(convert_time)
    veh['age_of_vehicle'] = veh['age_of_vehicle'].apply(lambda x: random.randint(0, 30) if x == -1 else x)
    cas['age_of_casualty'] = cas['age_of_casualty'].apply(lambda x: random.randint(0, 80) if x == -1 else x)

    # fill accidents
    acc1 = acc.loc[:, ['accident_index', 'accident_severity', 'weather_conditions']]
    acc1.to_csv('./tmp/accidents', encoding='utf-8', index=False, header=False, line_terminator=',\n')

    # fill casualty
    cas1 = cas.loc[:, ['casualty_severity', 'casualty_type', 'age_of_casualty']]
    cas1.to_csv('./tmp/casualty', encoding='utf-8', index=False, header=False, line_terminator=',\n', na_rep='0')

    # fill date
    acc2 = acc.loc[:, ['day_of_week', 'time', 'date']]
    acc2.to_csv('./tmp/date', encoding='utf-8', index=False, header=False, line_terminator=',\n')

    # fill location
    acc3 = acc.loc[:, ['longitude', 'latitude', 'urban_or_rural_area']]
    acc3.to_csv('./tmp/location', encoding='utf-8', index=False, header=False, line_terminator=',\n')

    # fill vehicle
    acc4 = veh.loc[:, ['vehicle_type', 'was_vehicle_left_hand_driver', 'age_of_vehicle', 'vehicle_manoeuvre']]
    acc4.to_csv('./tmp/vehicle', encoding='utf-8', index=False, header=False, line_terminator=',\n', na_rep='0')

    # fill accidents_casualty
    ac = cas.loc[:, ['accident_index', 'id']]
    acac = ac.merge(acc, left_on='accident_index', right_on='accident_index')[['accident_index', 'id_x']]

    # fill accidents_vehicles
    av = veh.loc[:, ['accident_index', 'id']]
    aveh = av.merge(veh, left_on='accident_index', right_on='accident_index')[['accident_index', 'id_x']]

    # fill accidents_ind
    vc = veh.loc[:, ['accident_index', 'id']]
    veh_cas = vc.merge(cas, left_on='accident_index', right_on='accident_index')[['id_x', 'id_y']]
    print(veh_cas)

if create_tables:
    print(time.strftime('%I%p:%M:%S'), 'Filling accidents db with data')
    query = f"load data infile '{tmp_path}accidents' into table accidents fields terminated by ',' LINES TERMINATED BY '\n' (accident_index, accident_severity, weather_conditions);"
    cur.execute(query)

    print(time.strftime('%I%p:%M:%S'), 'Filling casualty db with data')
    query = f"load data infile '{tmp_path}casualty' into table casualty fields terminated by ',' LINES TERMINATED BY '\n' (casualty_severity, casualty_type, age_of_casualty);"
    cur.execute(query)

    print(time.strftime('%I%p:%M:%S'), 'Filling date db with data')
    query = f"load data infile '{tmp_path}date' into table date fields terminated by ',' LINES TERMINATED BY '\n' (day_of_week, time, date);"
    cur.execute(query)

    print(time.strftime('%I%p:%M:%S'), 'Filling location db with data')
    query = f"load data infile '{tmp_path}location' into table location fields terminated by ',' LINES TERMINATED BY '\n' (longitude, latitude, urban_or_rural_area);"
    cur.execute(query)

    print(time.strftime('%I%p:%M:%S'), 'Filling vehicle db with data')
    query = f"load data infile '{tmp_path}vehicle' into table vehicles fields terminated by ',' LINES TERMINATED BY '\n' (vehicle_type, was_vehicle_left_hand_driver, age_of_vehicle, vehicle_manoeuvre);"
    cur.execute(query)

    connection.commit()

    print(time.strftime('%I%p:%M:%S'), 'Filling acc_cas db with data')
    for index, row in acac.iterrows():
        query = f"insert into accident_casualty(Accident_Id, Casualty_Id) values ((select id from accidents where Accident_Index = '{row['accident_index']}'), (select id from casualty where Id = {row['id_x'] + 1}))"
        try:
            cur.execute(query)
        except:
            pass

    print(time.strftime('%I%p:%M:%S'), 'Filling acc_veh db with data')
    for index, row in aveh.iterrows():
        query = f"insert into accident_vehicle(Accident_Id, Vehicle_Id) values ((select id from accidents where Accident_Index = '{row['accident_index']}'), (select id from vehicles where Id = {row['id_x'] + 1}))"
        try:
            cur.execute(query)
        except:
            pass

    print(time.strftime('%I%p:%M:%S'), 'Filling accident_location db with data')
    for index, row in acc.iterrows():
        query = f"insert into accident_location(Accident_Id, Location_Id) values ((select id from accidents where Accident_Index = {index + 1}), (select id from location where Id = {index + 1}))"
        try:
            cur.execute(query)
        except:
            pass

    print(time.strftime('%I%p:%M:%S'), 'Filling accident_date db with data')
    for index, row in acc.iterrows():
        query = f"insert into accident_date(Accident_Id, Date_Id) values ((select id from accidents where Accident_Index = {index + 1}), (select id from date where Id = {index + 1}))"
        try:
            cur.execute(query)
        except:
            pass

    print(time.strftime('%I%p:%M:%S'), 'Filling location_date db with data')
    for index, row in acc.iterrows():
        query = f"insert into location_date(Location_Id, Date_Id) values ((select id from location where id = {index + 1}), (select id from date where Id = {index + 1}))"
        try:
            cur.execute(query)
        except:
            pass

    print(time.strftime('%I%p:%M:%S'), 'Filling vehicle_casualty db with data')
    for index, row in veh_cas.iterrows():
        query = f"insert into vehicle_casualty(Vehicle_Id, Casualty_Id) values ((select id from vehicles where id = {row['id_x']}), (select id from date where Id = {row['id_y']}))"
        try:
            cur.execute(query)
        except:
            pass

    connection.commit()
    cur.close()
