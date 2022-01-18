import datetime

d1 = 1515043701960
d2 = 1515042045937#startTime

print(d1-d2)#duration



converted_d1 = datetime.datetime.fromtimestamp(round(d1 / 1000))
converted_d2 = datetime.datetime.fromtimestamp(round(d2 / 1000))
print(converted_d1)
print(converted_d2)
# current_time_utc = datetime.datetime.utcnow()

print((converted_d1 - converted_d2).total_seconds())
if ((converted_d1 - converted_d2).total_seconds() < 600.0):
    print("hey")
