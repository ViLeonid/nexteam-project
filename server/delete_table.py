from datetime import datetime, timedelta

a='16 сен-6 окт'
b='6-28 фев'
c='1-2 мая'
d='21 мая-1 июн'
datetime_local='2018-06-12T19:30'

def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        return None



def map_date(i):
    x=[]
    for j in i.split(' '):
        for k in j.split('-'):
            x.append(k)
    months={
        'янв': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'мая': 5,
        'июн': 6,
        'июл': 7,
        'авг': 8,
        'сен': 9,
        'окт': 10,
        'ноя': 11,
        'дек': 12
    }
    if len(x) == 2:
        current_year = datetime.now().year
        current_month = datetime.now().month
        if current_month <= months[x[1]]:
            return [parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'23:59')]
        else:
            return [parse_datetime(str(current_year+1)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year+1)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'23:59')]
    if len(x) == 3:
        current_year = datetime.now().year
        current_month = datetime.now().month
        if current_month <= months[x[2]]:
            return [parse_datetime(str(current_year)+'-'+str(months[x[2]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year)+'-'+str(months[x[2]])+'-'+x[1]+'T'+'23:59')]
        else:
            return [parse_datetime(str(current_year+1)+'-'+str(months[x[2]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year+1)+'-'+str(months[x[2]])+'-'+x[1]+'T'+'23:59')]
    if len(x) == 4:
        current_year = datetime.now().year
        current_month = datetime.now().month
        if current_month <= months[x[1]]:
            if current_month <= months[x[3]]:
                return [parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year)+'-'+str(months[x[3]])+'-'+x[2]+'T'+'23:59')]
            else:
                return [parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year+1)+'-'+str(months[x[3]])+'-'+x[2]+'T'+'23:59')]
        else:
            if current_month <= months[x[3]]:
                return [parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year)+'-'+str(months[x[3]])+'-'+x[2]+'T'+'23:59')]
            else:
                return [parse_datetime(str(current_year+1)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year+1)+'-'+str(months[x[3]])+'-'+x[2]+'T'+'23:59')]


print(a)
print(map_date(a))
print(map_date(b))
print(map_date(c))
print(map_date(d))
print(datetime_local)
print(parse_datetime(datetime_local))
print(parse_datetime(datetime_local) + timedelta(hours=1))