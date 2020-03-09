from pymongo import MongoClient
from keywords import keywords
from mongostring import mongostring
from Year import Year

def doAnalysis():
    client = MongoClient(mongostring, retryWrites=False)

    db = client.moneymanager

    months_to_update = []

    number_of_trans = db.transactions.count()
    cat_counter = 0

    # reset current analysis
    db.months.update_many({}, {'$unset': {'categories':1}})


    for trans in db.transactions.find(modifiers={'$snapshot': True}):
        # categorization
        for category in keywords.keys():
            if any(substring in trans['descr'] for substring in keywords[category]):
                cat_counter += 1
                months_to_update.append({'year': trans['date'].year, 'month': trans['date'].month, 'category': 'categories.' + category, 'amount': 0-trans['amount']})
                print('found one')
                #db.months.update_one({'year': trans['date'].year, 'month': trans['date'].month}, {'$inc': {'categories['+ category +']': trans['amount']}})

    print("now updating")
    for entry in months_to_update:
        #query = {'$inc': {'categories.food': 1}}
        query = {'$inc': {entry['category']: entry['amount']}}
        print(query)
        db.months.update_one({'year': entry['year'], 'month': entry['month']}, query)

    print("could categorize", cat_counter, "out of", number_of_trans, "transactions (", cat_counter / number_of_trans * 100, "%)")

    print("now summing up the years")
    years_to_save = {}
    num_of_months = db.months.count()
    for month in db.months.find():
        if month['year'] in years_to_save:
            years_to_save[month['year']]['savings'] += month['savings']
            if 'categories' in month:
                for category in month['categories'].keys():
                    if category in years_to_save[month['year']]['categories']:
                        years_to_save[month['year']]['categories'][category] += month['categories'][category]
                    else:
                        years_to_save[month['year']]['categories'][category] = month['categories'][category]

        else:
            years_to_save[month['year']] = {}
            years_to_save[month['year']]['categories'] = {}
            years_to_save[month['year']]['savings'] = month['savings']
            if 'categories' in month:
                years_to_save[month['year']]['categories'] = {}
                for category in month['categories'].keys():
                    years_to_save[month['year']]['categories'][category] = month['categories'][category]

    print("saving years")

    for year in years_to_save.keys():
        avg_spendings = {}
        if 'categories' in years_to_save[year]:
            avg_spendings = years_to_save[year]['categories'].copy()
            for category in avg_spendings.keys():
                avg_spendings[category] /= num_of_months
        current_year = Year(year, years_to_save[year]['savings'], avg_spendings, years_to_save[year]['categories'])
        db.years.insert_one(current_year.__dict__)


doAnalysis()
