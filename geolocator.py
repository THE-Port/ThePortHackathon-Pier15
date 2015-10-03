from geopy.geocoders import Nominatim
geolocator = Nominatim()

f = open("cities_data.csv", "r")


f_out = open("final_data.csv", "w")


data = f.readlines()

# Name of Province : 2
# Name of Country : 1
# Name of Medicine : 3
# Result  : 4

count = 0

for _d in data:
   try:
       d = _d.split(",")
       province = d[2]
       country = d[1]
       name = d[3]
       result = d[4]
       
       location = geolocator.geocode(province+" , ",country)
       if type(location) == type([]):
           location = location[0]          
       lat = location.latitude
       lng = location.longitude
       
       count += 1    
       
       s = ""
       s += name 
       s += ","
       s +=str(lat)
       s += ","
       s += str(lng)
       s += ","
       s += result
       s += "\n"
       
       
       f_out.write(s)
       f_out.close()
       if count > 500:
           t.sleep(80)
       print f
   except:
       passP