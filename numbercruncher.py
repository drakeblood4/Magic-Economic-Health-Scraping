import json

with open('data.json') as json_data:
    save = json.load(json_data)


inactive_count = 0.0
active_count = 0.0
inactive_value_total = 0.0
active_value_total = 0.0

for i in save:
    if save[i]['failed'] == 1:
        inactive_count += 1
        inactive_value_total += save[i]['value']
        
    else:
        active_count += 1
        active_value_total += save[i]['value']

active_user_percentage = 100*(active_count/(active_count+inactive_count))
        
active_value_percentage = 100*(active_value_total/(active_value_total + inactive_value_total))

average_active_points = active_value_total/active_count

average_inactive_points = inactive_value_total/inactive_count

average_points = (active_value_total+inactive_value_total)/(active_count+inactive_count)

print("Active users represent %s%% of all users" % str(round(active_user_percentage,2)))

print("Active users have %s%% of all points not in escrow in their accounts" % str(round(active_value_percentage,2)))

print("The average inactive user has %s PucaPoints in their account" % str(round(average_inactive_points,1)))

print("The average active user has %s PucaPoints in their account" % str(round(average_active_points,1)))



