def calculate_compensation(data):
    age = int(data.get('age',0))
    if(age<18):
        return "Abhi dhoti me rkh use"
    
    occupation_bonus = {
        'engineer': 0,
        'doctor': 800000,
        'mba': 600000,
        'teacher': 30000
    }

    income_bonus = 0
    income = int(data.get('income', 0))

    if income < 50000:
        income_bonus = 0
    elif 50000 <= income <= 100000:
        income_bonus = 100000
    else:
        income_bonus = 200000

    cow_bonus = {
        'yes': 100000,
        'no': 0
    }

    cows= data.get('Cows','').lower()
    cow_base= cow_bonus.get(cows,0)


    

    occupation = data.get('occupation', '').lower()
    base = occupation_bonus.get(occupation, 0)

    total = base + income_bonus + cow_base
    return total
