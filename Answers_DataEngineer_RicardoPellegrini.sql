-- 1) Total equipment failures that happened (in January 2020)?
select count(distinct(datetime_utc)) from tb_equipment_failure_sensors
where datetime_utc between '2020-01-01' and '2020-01-31';
-- Answer: 1528 failures in January 2020.

-- 2) Which equipment code had most failures?
select e.code, count(distinct(f.datetime_utc)) as total_failures
from tb_equipment_failure_sensors as f
join tb_equipment_sensors as s on f.sensor_id = s.sensor_id
join tb_equipments as e on s.equipment_id = e.equipment_id
where datetime_utc between '2020-01-01' and '2020-01-31'
group by e.code
order by total_failures desc limit 1;
-- Answer: E1AD07D4, with 151 failures in January 2020.

-- 3) Average amount of failures across equipment group,
-- ordered by the number of failures in ascending order?
with t1 (group_name, code, failures) as (
	select e.group_name, e.code, count(distinct(f.datetime_utc)) as total_failures
	from tb_equipment_failure_sensors as f
	join tb_equipment_sensors as s on f.sensor_id = s.sensor_id
	join tb_equipments as e on s.equipment_id = e.equipment_id
	where datetime_utc between '2020-01-01' and '2020-01-31'
	group by e.group_name, e.code
	order by e.group_name, e.code
)
select group_name, round(avg(failures),2) as average_failures from t1
group by group_name
order by average_failures;
-- Correct Answer: the average of failures for each group of equipments are below
-- group_name	average
-- "9N127Z5P"	105.50
-- "NQWPA8D3"	113.00
-- "VAPQY59S"	115.50
-- "PA92NCXZ"	119.00
-- "Z9K1SAP4"	124.00
-- "FGHQWR2Q"	124.75