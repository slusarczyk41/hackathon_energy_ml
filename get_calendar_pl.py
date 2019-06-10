
### Daylight Saving Time, Holidays and Non Shopping Sundays in Poland ###

from datetime import datetime, date, timedelta

def calendar_pl(year_start, year_end=None, holidays=True, sundays=True): 
    '''Holidays and Non Shopping Sunday in Poland'''
    dict1 = apply_multi(non_shopping_sunday, year_start, year_end) if sundays == True else {}  
    dict2 = apply_multi(holiday_all, year_start, year_end) if holidays == True else {}
    return {**dict1, **dict2}


def time_change(year_start, year_end=None):
    '''Daylight Saving Time'''
    dict1 = apply_multi(time_change_one, year_start, year_end)
    return dict1

	
def apply_multi(func, date_start, date_end=None):
    '''Executes the given function for the given period of time'''
    if date_end is None:
        date_end = date_start
        
    list1 = list()
    for i in range(date_start, date_end+1, 1):
        list1.append(func(i))
    list1

    dict1 = {}
    for j in list1:
        for day, text in j.items():  
            dict1[day] = text

    return dict1


def holiday_all(year):
    dict1 = holiday_regular_dict(year)
    dict2 = easter_dict(year)
    dict3 = holiday_exception(year)
    return {**dict1, **dict2, **dict3}


def holiday_regular_dict(year):
    '''Returns regular holidays in Poland'''
    dict1 = {
        datetime(year, 1, 1).date():'Nowy Rok',
        datetime(year, 1, 6).date():'Trzech Króli',
        datetime(year, 5, 1).date():'Święto Pracy',
        datetime(year, 5, 3).date():'Święto Konstytucji 3 Maja',
        datetime(year, 8, 15).date():'Święto Wojska Polskiego, Wniebowzięcie Najświętszej Maryi Panny', 
        datetime(year, 11, 1).date():'Wszystkich Świętych',
        datetime(year, 11, 11).date():'Narodowe Święto Niepodległości',
        datetime(year, 12, 25).date():'Boże Narodzenie (pierwszy dzień)',
        datetime(year, 12, 26).date():'Boże Narodzenie (drugi dzień)'
    }
    return dict1

	
def easter_date(year):
    '''Returns Easter as a date object according to Butcher's Algorithm'''
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day = ((h + l - 7*m + 114) % 31) + 1  
    return date(year, month, day)

	
def easter_dict(year):  
    '''Returns Easter, Pentecost and Feast of Corpus Christi'''
    easter_ = easter_date(year)
    dict1 = {}
    dict1[easter_] = 'Wielkanoc'
    dict1[easter_ + timedelta(days=1)] = 'Poniedziałek Wielkanocny'
    dict1[easter_ + timedelta(days=49)] = 'Zesłanie Ducha Świętego (Zielone Świątki)'
    dict1[easter_ + timedelta(days=60)] = 'Boże Ciało'
    return dict1

	
def non_shopping_sunday(year):
    '''Returns non shopping Sundays in Poland'''
    sunday_list = sorted(list(set(sunday_1(year)) - set(sunday_2(year))))
    sunday_dict = dict(zip(sunday_list, ['Niedziela wolna od handlu']*len(sunday_list)))
    return sunday_dict

	
def sunday_1(year):
    '''Returns a list of non shopping Sundays in Poland without exceptions'''
    
    sunday = list()
    if year >= 2018:
        m1 = 3 if year == 2018 else 1

        for month in range(m1,13):
            d1 = datetime(year, month, 1).date()
            if month < 12:
                d2 = datetime(year, month+1, 1).date() 
            elif month == 12:
                d2 = datetime(year+1, 1, 1).date()
            delta = d2 - d1

            dict1 = {}
            for i in range(delta.days):
                dict1[d1 + timedelta(days=i)] = (d1 + timedelta(days=i)).weekday()

            all_sunday_month = list()
            for day, weekday in dict1.items():   
                if weekday == 6:  #0 - Monday, ..., 6 - Sunday
                    all_sunday_month.append(day)

            if year == 2018:
                sunday = sunday + all_sunday_month[1:len(all_sunday_month)-1]
            elif year == 2019:
                sunday = sunday + all_sunday_month[:len(all_sunday_month)-1]
            elif year >= 2020:
                if month in [1,4,6,8]:
                    sunday = sunday + all_sunday_month[:len(all_sunday_month)-1]
                else:
                    sunday = sunday + all_sunday_month
                    
    return sunday

	
def sunday_2(year):
    '''Returns a list of exceptions for trading on Sunday'''
    
    christmas_day = datetime(year, 12, 25).date()
    easter = easter_date(year)

    dict1 = {}; dict2 = {}
    for i in range(1,15):
        dict1[christmas_day - timedelta(days=i)] = (christmas_day - timedelta(days=i)).weekday()
    for i in range(1,8):
        dict2[easter - timedelta(days=i)] = (easter - timedelta(days=i)).weekday()

    sunday_specific = list()
    for day, weekday in dict1.items():   
        if weekday == 6:  #0 - Monday, ..., 6 - Sunday
            sunday_specific.append(day)
    for day, weekday in dict2.items():   
        if weekday == 6:  
            sunday_specific.append(day)
    for day, text in holiday_all(year).items(): 
        if day.weekday() == 6:
            sunday_specific.append(day)
    
    return sunday_specific

	
def holiday_exception(year_1):  
    '''Returns exceptionally introduced holidays'''
    dict1 = {
        datetime(2018, 11, 12).date(): 'Dzień wolny z okazji 100-lecia Niepodległości'
    } 
    dict2 = {}
    for day, text in dict1.items():   
        if day.year == year_1:  #0 - Monday, ..., 6 - Sunday
            dict2[day] = text
    return dict2


def time_change_one(year):
    '''Daylight Saving Time'''
    
    d1 = datetime(year, 3, 31).date()
    d2 = datetime(year, 10, 31).date()

    dict1 = {}; dict2 = {}
    for i in range(7):
        dict1[(d1 - timedelta(days=i)).weekday()] = d1 - timedelta(days=i)
        dict2[(d2 - timedelta(days=i)).weekday()] = d2 - timedelta(days=i)

    dict3 = {}
    for weekday, day in dict1.items():   
        if weekday == 6:  #0 - Monday, ..., 6 - Sunday
            dict3[day] = 'Zmiana czasu z zimowego na letni'

    for weekday, day in dict2.items():   
        if weekday == 6:
            dict3[day] = 'Zmiana czasu z letniego na zimowy'

    return dict3

	

# Examples:
calendar_pl(2018,2019,sundays=False)
calendar_pl(2019)
time_change(2018, 2019)

