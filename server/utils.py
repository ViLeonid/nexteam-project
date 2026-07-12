import re
from datetime import datetime
def validate_password(password):

    if len(password) < 10:
        return False

    if not re.search(r'[A-Z]', password) and not re.search(r'[А-Я]', password):
        return False

    if not re.search(r'[a-z]', password) and not re.search(r'[а-я]', password):
        return False

    if not re.search(r'\d', password):
        return False

    return True

def parse_date(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, '%Y-%m-%d')
    except ValueError:
        return None

def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        return None

def parse_datetime_with_seconds(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
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



