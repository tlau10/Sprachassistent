from datetime import date, timedelta

def get_date_of_weekday(name):
    weekdays = {'Montag' : 0, 'Dienstag' : 1, 'Mittwoch' : 2, 'Donnerstag' : 3, 'Freitag' : 4, 'Samstag' : 5, 'Sonntag' : 6}

    index_today = date.today().weekday()
    index_target = weekdays.get(name)
    days_diff = abs(index_today - index_target)

    if index_today == index_target:
        return date.today() + timedelta(weeks = 1)
    # target liegt in Zukunft
    elif index_today < index_target:
        return date.today() + timedelta(days = days_diff)
    # target liegt in Vergangenheit
    elif index_today > index_target:
        return date.today() + timedelta(days = -days_diff, weeks = 1)

def main():
    name = "Montag"
    print(f"date of {name} is {get_date_of_weekday(name)}")

if __name__ == "__main__":
    main()
