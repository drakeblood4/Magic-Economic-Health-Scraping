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

active_user_percentage = (active_count/(active_count+inactive_count))
        
active_value_percentage = (active_value_total/(active_value_total + inactive_value_total))

average_active_points = active_value_total/active_count

average_inactive_points = inactive_value_total/inactive_count

average_points = (active_value_total+inactive_value_total)/(active_count+inactive_count)

print(active_value_percentage)

