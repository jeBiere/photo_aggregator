import pendulum
from collections import defaultdict

def generate_availability(working_hours, blocked, booked, start, end, slot_minutes=60):
    blocked_map = defaultdict(list)
    for b in blocked:
        blocked_map[b.date].append((b.start_time, b.end_time))

    booked_map = booked 

    working_by_day = defaultdict(list)
    for w in working_hours:
        working_by_day[w.day_of_week].append((w.start_time, w.end_time))

    result = {}
    current = pendulum.parse(str(start))
    end = pendulum.parse(str(end))
    while current <= end:
        weekday = current.day_of_week
        slots = []
        for interval in working_by_day.get(weekday, []):
            slot_time = current.at(interval[0].hour, interval[0].minute)
            end_time = current.at(interval[1].hour, interval[1].minute)
            while slot_time < end_time:
                t = slot_time.time()
                is_blocked = any(
                    (b_start is None or t >= b_start) and (b_end is None or t < b_end)
                    for b_start, b_end in blocked_map.get(current.date(), [])
                )
                is_booked = t in booked_map.get(current.date(), [])  
                if not is_blocked and not is_booked:
                    slots.append(slot_time.format("HH:mm"))
                slot_time = slot_time.add(minutes=slot_minutes)
        if slots:
            result[current.to_date_string()] = slots
        current = current.add(days=1)
    return result
