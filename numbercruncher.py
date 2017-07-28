import json

with open('pu_data.json') as json_data:
    pu_save = json.load(json_data)

with open('cs_data.json') as json_data:
    cs_save = json.load(json_data)

pu_inactive_count = 0.0
pu_active_count = 0.0
pu_inactive_value_total = 0.0
pu_active_value_total = 0.0

pu_country_dict = {}

for i in pu_save:
    if pu_save[i]['country'] in pu_country_dict:
        if pu_save[i]['failed'] == 1:
            pu_country_dict[pu_save[i]['country']]['inactive'] += 1
        else:
            pu_country_dict[pu_save[i]['country']]['active'] += 1
    else:
        if pu_save[i]['failed'] == 1:
            pu_country_dict[pu_save[i]['country']] = {'active': 0,
                                                    'inactive': 1}
        else:
            pu_country_dict[pu_save[i]['country']] = {'active': 1,
                                                    'inactive': 0}



    
    if pu_save[i]['failed'] == 1:
        pu_inactive_count += 1
        pu_inactive_value_total += pu_save[i]['value']
        
    else:
        pu_active_count += 1
        pu_active_value_total += pu_save[i]['value']

pu_user_count_total = len(pu_save)

pu_active_user_percentage = 100*(pu_active_count/(pu_active_count+pu_inactive_count))
        
pu_active_value_percentage = 100*(pu_active_value_total/(pu_active_value_total + pu_inactive_value_total))

pu_average_active_points = pu_active_value_total/pu_active_count

pu_average_inactive_points = pu_inactive_value_total/pu_inactive_count

pu_average_points = (pu_active_value_total+pu_inactive_value_total)/(pu_active_count+pu_inactive_count)

print("Active users represent %s%% of all PucaTrade users" % str(round(pu_active_user_percentage,2)))

print("Active users have %s%% of all PucaPoints not in escrow in their accounts" % str(round(pu_active_value_percentage,2)))

print("The average inactive user has %s PucaPoints in their account" % str(round(pu_average_inactive_points,1)))

print("The average active user has %s PucaPoints in their account" % str(round(pu_average_active_points,1)))

print("\n")

for i in pu_country_dict:
    if  pu_country_dict[i]['active'] > 0:
        print('%s is %i active users and %i inactive users' % (i, pu_country_dict[i]['active'], pu_country_dict[i]['inactive']))
        pu_country_active_user_percentage = 100 *(float(pu_country_dict[i]['active'])/float( pu_country_dict[i]['active'] +  pu_country_dict[i]['inactive']))

        print('%f %% of its users are active.' % pu_country_active_user_percentage )

        pu_country_as_percent_total_userbase = 100*float(pu_country_dict[i]['active'] + pu_country_dict[i]['inactive'])/(pu_active_count+pu_inactive_count)
        print('Its users represent %f %% of the total userbase.' % pu_country_as_percent_total_userbase)

        pu_country_as_percent_active_userbase = 100*float(pu_country_dict[i]['active'])/pu_active_count
        print('Its active users represent %f %% of the active userbase.' % pu_country_as_percent_active_userbase)

        print('')

print('-----------------------------------------------------------------')


cs_inactive_count = 0.0
cs_active_count = 0.0
cs_inactive_value_total = 0.0
cs_active_value_total = 0.0
cs_country_dict = {}

for i in cs_save:
    if cs_save[i]['country'] in cs_country_dict:
        if cs_save[i]['failed'] == 1:
            cs_country_dict[cs_save[i]['country']]['inactive'] += 1
        else:
            cs_country_dict[cs_save[i]['country']]['active'] += 1
    else:
        if cs_save[i]['failed'] == 1:
            cs_country_dict[cs_save[i]['country']] = {'active': 0,
                                                    'inactive': 1}
        else:
            cs_country_dict[cs_save[i]['country']] = {'active': 1,
                                                    'inactive': 0}
            


        
    if cs_save[i]['failed'] == 1:
        cs_inactive_count += 1
        cs_inactive_value_total += cs_save[i]['value']
        
    else:
        cs_active_count += 1
        cs_active_value_total += cs_save[i]['value']

cs_active_user_percentage = 100*(cs_active_count/(cs_active_count+cs_inactive_count))
        
cs_active_value_percentage = 100*(cs_active_value_total/(cs_active_value_total + cs_inactive_value_total))

cs_average_active_points = cs_active_value_total/cs_active_count

cs_average_inactive_points = cs_inactive_value_total/cs_inactive_count

cs_stored_value = cs_active_value_total+cs_inactive_value_total

cs_average_points = (cs_stored_value)/(cs_active_count+cs_inactive_count)

cs_in_transit = 15088.68

cs_total_average_points = (cs_stored_value + cs_in_transit)/(cs_active_count+cs_inactive_count)

cs_average_active_availabe_points = (cs_active_value_total+cs_in_transit)/cs_active_count

print("Active users represent %s%% of all CardSphere users" % str(round(cs_active_user_percentage,2)))

print("Active users have %s%% of all stored value not in escrow in their accounts" % str(round(cs_active_value_percentage,2)))

print("The average inactive user has $%s of stored value in their account" % str(round(cs_average_inactive_points,1)))

print("The average active user has $%s of stored value in their account" % str(round(cs_average_active_points,1)))


for i in cs_country_dict:
    if  cs_country_dict[i]['active'] > 0:
        print('%s is %i active users and %i inactive users' % (i, cs_country_dict[i]['active'], cs_country_dict[i]['inactive']))
        cs_country_active_user_percentage = 100 *(float(cs_country_dict[i]['active'])/float( cs_country_dict[i]['active'] +  cs_country_dict[i]['inactive']))

        print('%f %% of its users are active.' % cs_country_active_user_percentage )

        cs_country_as_percent_total_userbase = 100*float(cs_country_dict[i]['active'] + cs_country_dict[i]['inactive'])/(cs_active_count+cs_inactive_count)
        print('Its users represent %f %% of the total userbase.' % cs_country_as_percent_total_userbase)

        cs_country_as_percent_active_userbase = 100*float(cs_country_dict[i]['active'])/cs_active_count
        print('Its active users represent %f %% of the active userbase.' % cs_country_as_percent_active_userbase)

        print('')
