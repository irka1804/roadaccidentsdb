from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Accidents, Date, Location, Casualty, Vehicles


from django.db import connection

def index(r):
    return render(r, 'index.html')

def create(request):
    return render(request, 'create.html')

def create_accidents(request):
    if request.method == "POST":
        a = Accidents()
        a.accident_index = request.POST.get("accident_index")
        a.accident_severity = request.POST.get("accident_severity")
        a.weather_conditions = request.POST.get("weather_conditions")
        a.save()
    return HttpResponseRedirect("/")

def create_date(request):
    if request.method == "POST":
        a = Date()
        a.day_of_week = request.POST.get("day")
        a.time = request.POST.get("time")
        a.date = request.POST.get("date")
        a.save()
    return HttpResponseRedirect("/")


def create_location(request):
    if request.method == "POST":
        a = Location()
        a.latitude = request.POST.get("lat")
        a.longitude = request.POST.get("long")
        a.urban_or_rural_area = request.POST.get("area")
        a.save()
    return HttpResponseRedirect("/")

def create_casualty(request):
    if request.method == "POST":
        a = Casualty()
        a.casualty_severity = request.POST.get("cs")
        a.casualty_type = request.POST.get("ct")
        a.age_of_casualty = request.POST.get("age")
        a.save()
    return HttpResponseRedirect("/")

def create_vehicles(request):
    if request.method == "POST":
        a = Vehicles()
        a.vehicle_type = request.POST.get("type")
        a.was_vehicle_left_hand_driver = request.POST.get("hand")
        a.age_of_vehicle = request.POST.get("age")
        a.vehicle_manoeuvre = request.POST.get("man")
        a.save()
    return HttpResponseRedirect("/")

def delete_by_id(request):
    if request.method != "POST":
        return render(request, 'delete.html')
    t = request.POST.get("table")
    ids = request.POST.get("id")
    if 'cci' in t:
        a = Accidents.objects.get(id=ids)
    if 'ate' in t:
        a = Date.objects.get(id=ids)
    if 'ati' in t:
        a = Location.objects.get(id=ids)
    if 'asu' in t:
        a = Casualty.objects.get(id=ids)
    if 'ehi' in t:
        a = Vehicles.objects.get(id=ids)
    try:
        a.delete()
    except:
        pass
    return render(request, 'delete.html')

def update(request):
    return render(request, 'update.html')

def update_accidents(request):
    if request.method == "POST":
        a = Accidents.objects.filter(id=request.POST.get("id")).first()
        a.accident_index = request.POST.get("accident_index")
        a.accident_severity = request.POST.get("accident_severity")
        a.weather_conditions = request.POST.get("weather_conditions")
        a.save()
    return HttpResponseRedirect("/")

def update_date(request):
    if request.method == "POST":
        a = Date.objects.filter(id=request.POST.get("id")).first()
        a.day_of_week = request.POST.get("day")
        a.time = request.POST.get("time")
        a.date = request.POST.get("date")
        a.save()
    return HttpResponseRedirect("/")


def update_location(request):
    if request.method == "POST":
        a = Location.objects.filter(id=request.POST.get("id")).first()
        a.latitude = request.POST.get("lat")
        a.longitude = request.POST.get("long")
        a.urban_or_rural_area = request.POST.get("area")
        a.save()
    return HttpResponseRedirect("/")

def update_casualty(request):
    if request.method == "POST":
        a = Casualty.objects.filter(id=request.POST.get("id")).first()
        a.casualty_severity = request.POST.get("cs")
        a.casualty_type = request.POST.get("ct")
        a.age_of_casualty = request.POST.get("age")
        a.save()
    return HttpResponseRedirect("/")

def update_vehicles(request):
    if request.method == "POST":
        a = Vehicles.objects.filter(id=request.POST.get("id")).first()
        a.vehicle_type = request.POST.get("type")
        a.was_vehicle_left_hand_driver = request.POST.get("hand")
        a.age_of_vehicle = request.POST.get("age")
        a.vehicle_manoeuvre = request.POST.get("man")
        a.save()
    return HttpResponseRedirect("/")

def select1(r):
    cursor = connection.cursor()
    query = 'Все транспортные средства, попавшие в аварии в этот день'

    if r.method == 'POST':

        cursor.execute(f"Select vehicle_type, d.date from vehicles v inner join date d on v.id = d.id and d.date = '{r.POST.get('date')}'")

        row = cursor.fetchall()

        return render(r, 'view.html', {'row': row, 'columns': ['vehicle', 'date'], 'query': query})

    else:

        return render(r, 'view_form.html', {'title': 'Введите дату', 'query': query})

def select2(r):
    cursor = connection.cursor()

    cursor.execute("select depths.date as data, depths.age_of_Casualty as age, Count(*) as depth "
                   "FROM (select dd.id, dd.date, cc.Age_of_Casualty FROM "
                   "(date dd INNER JOIN Casualty cc on dd.Id = cc.Id and dd.date < '2005-01-11'))"
                   " as depths GROUP BY data, age order BY age DESC;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': ['date', 'age', 'count'], 'query':
        'посчитать кол-во людей в период с 1 - 10 января 2005 года упорядоченных по возрасту, которые попали в дтп'})

def select3(r):
    cursor = connection.cursor()

    cursor.execute("select dw as ddw, SUM('age') / COUNT(*) as mean_age "
                   "from (select dd.Day_of_Week as dw, cc.Age_of_Casualty as age "
                   "FROM (date dd INNER JOIN Casualty cc on dd.Id = cc.Id)) as cas "
                   "group by ddw order by ddw ASC;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Средний возраст жертвы попавшей в ДТП по дням недели'})

def select4(r):
    cursor = connection.cursor()

    cursor.execute("select avg(age_of_casualty) from casualty as cc "
                   "inner join date where cc.id = date.id and date.date = '2005-01-03';")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Средний возраст жертвы попавшей в аварию определенного дня'})

def select5(r):
    cursor = connection.cursor()

    cursor.execute("select vehicles.id, age_of_vehicle, day_of_week "
                   "from vehicles inner join date on date.id = vehicles.id "
                   "and (day_of_week = 'Saturday' or day_of_week = 'Sunday') limit 10;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': ['id', 'age', 'day of weak'], 'query': 'вывести возраст самой старой машины, которая попала в аварию в выходные (суббота или воскресенье)'})

def window1(r):
    cursor = connection.cursor()

    cursor.execute("select vehicle_type, weather_conditions, amount_of_dtp, "
                   "row_number() OVER (PARTITION BY weather_conditions ORDER BY amount_of_dtp DESC) "
                   "AS rating_in_section from (select vehicle_type, weather_conditions, count(ac.id) as amount_of_dtp "
                   "from accidents ac inner join vehicles v where ac.id = v.id "
                   "group by vehicle_type, weather_conditions) tt;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': ['vehicle type', 'weather', 'amount of dtp', 'position in top'], 'query': 'Рейтинг опасности видов транспорта по типу погодных условий'})

def window2(r):
    cursor = connection.cursor()

    cursor.execute("select vehicle_type, age_of_casualty, age_sort "
                   "from (select id as personal_id, age_of_casualty, row_number() "
                   "OVER (ORDER BY age_of_casualty DESC) AS age_sort "
                   "from casualty where age_of_casualty > 5 and age_of_casualty < 18 "
                   "order by personal_id) as kids inner join vehicles where id = personal_id")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': ['vehicle type', 'age', ], 'query': 'Мы выбрали несовершеннолетних ребят, которые попали в дтп. И подписали их по старшинству.'})

def window3(r):
    cursor = connection.cursor()

    cursor.execute("select longitude, latitude, date, "
                   "row_number() over (order by date desc) as sort_by_date "
                   "from location inner join date "
                   "where location.id = date.id and day_of_week = 'Friday' "
                   "order by longitude, latitude;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Посмотрели на местоположение аварий которые произошли в пятницу, и подписали какой день по счету, относительно первой такой аварии'})

def view1(r):
    cursor = connection.cursor()

    cursor.execute("create or replace view serious_troubles "
                   "as select vehicle_type, age_of_vehicle, weather_conditions, casualty_severity, age_of_casualty,"
                   " date FROM vehicles, accidents, casualty, date "
                   "WHERE vehicles.id = accidents.id and accidents.accident_severity = 'fatal' "
                   "and casualty.id = accidents.id and casualty.id = date.id ;")

    cursor.execute("select * from serious_troubles limit 10;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Сохранили представление о всех дтп с фатальным исходами.'})

def view2(r):
    cursor = connection.cursor()

    cursor.execute("create or replace view old_people as "
                   "select longitude, latitude, date, age_of_casualty "
                   "from location, casualty, date "
                   "where date.id = location.id and date.id = casualty.id and  "
                   "(age_of_casualty + 10 >= "
                   "(select max(age_of_casualty) from casualty)) "
                   "and casualty_severity = 'serious';")

    cursor.execute("select * from old_people limit 10;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Места, где самые пожилые (не младше 10 лет от самого взрослого) люди попали в серьезное дтп. (с макс возрастом)'})

def view3(r):
    cursor = connection.cursor()

    cursor.execute("create or replace view 13_friday "
                   "as select age_of_casualty, casualty_severity, year(date) "
                   "from date, casualty where casualty.id = date.id"
                   " and dayofmonth(date) = 13 and day_of_week = 'Friday';")

    cursor.execute("select * from 13_friday limit 10;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Люди попавшие в авария в пятницу 13'})

def view4(r):
    cursor = connection.cursor()

    cursor.execute("create or replace view taxi_7 as "
                   "select weather_conditions, vehicle_type, age_of_vehicle, "
                   "date from vehicles, date, accidents where date.id = vehicles.id "
                   "and date.id = accidents.id and age_of_vehicle >= 7 "
                   "and INSTR(vehicle_type, 'taxi') "
                   "order by date;")

    cursor.execute("select * from taxi_7 limit 10;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Узнать в каких погодных условиях произошло дтп с участием всех такси, машинам которых не менее 7 лет. Отфильтрованы по дате события'})

def view5(r):
    cursor = connection.cursor()

    cursor.execute("create or replace view bad_story as "
                   "select vehicle_type, date, time, longitude, latitude"
                   " from date, location, vehicles group by date, time, longitude, latitude "
                   "order by date, time, longitude, latitude")

    cursor.execute("select accident_index, ac "
                   "from (select accident_index, count(*) as ac "
                   "from accidents group by accident_index) as kk where ac > 1;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': ''})

def procedure1(r):
    cursor = connection.cursor()

    cursor.execute("create procedure get_veh_info(type varchar(45)) "
                   "begin select vehicle_type, age_of_vehicle, casualty_type, "
                   "age_of_casualty, longitude, latitude, date, time, weather_conditions "
                   "from vehicles, casualty, accidents, date, location "
                   "where date.id = vehicles.id and date.id = accidents.id and date.id = casualty.id "
                   "and casualty.id = location.id and  INSTR(vehicle_type, type); "
                   "call get_veh_info('bus');"
                    )

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Поиск важной информации о конкретном виде транспорта.'})

def procedure2(r):
    cursor = connection.cursor()

    cursor.execute("delimiter // "
                   "create procedure gismeteo(year_i INT, weather varchar(45))"
                   " begin select vehicle_type, age_of_vehicle, date, latitude, longitude, weather_conditions "
                   "from vehicles, accidents, location, date"
                   " where accidents.id = vehicles.id and location.id = accidents.id "
                   "and date.id = accidents.id and age_of_vehicle = year_i and "
                   "INSTR(weather_conditions, weather); "
                   "end //"
                   "delimiter //"
                   "call gismeteo(5, 'rain');"
                   "end //")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Найти все места, где произошла авария с машиной конкретного года, и заданной погодой'})

def procedure3(r):
    cursor = connection.cursor()

    cursor.execute("delimiter //"
                   "create procedure max_age(year_i INT) "
                   "begin select max(age_of_casualty) from casualty, date "
                   "where date.id = casualty.id and year(date) = year_i; "
                   "end //"
                   "call max_age(2005)")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'Максимальный возраст жертвы в N году'})

def procedure4(r):
    cursor = connection.cursor()

    cursor.execute("delimeter //"
                   "create procedure am_dtp(x float, y float) "
                   "begin select count(*) from location "
                   "where longitude <= x + 0.02 and longitude >= x - 0.02 and latitude <= y + 0.02 and latitude >= y - 0.02;"
                   " end //"
                   "call am_dtp(-0.19, 51.48);")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': 'кол-во аварий по данным координатам (в том месте)'})

def procedure5(r):
    cursor = connection.cursor()

    cursor.execute("select * from bad_story limit 10;")

    row = cursor.fetchall()

    return render(r, 'view.html', {'row': row, 'columns': [], 'query': ''})
