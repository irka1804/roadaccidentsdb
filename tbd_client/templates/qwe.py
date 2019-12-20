DROP PROCEDURE IF EXISTS gismeteo;
create procedure gismeteo(year_i INT, weather varchar(45))
begin select vehicle_type, age_of_vehicle, date, latitude, longitude, weather_conditions
from vehicles, accidents, location, date
where accidents.id = vehicles.id and location.id = accidents.id
and date.id = accidents.id and age_of_vehicle = year_i and
INSTR(weather_conditions, weather);
end
call gismeteo(4, 'rain');
