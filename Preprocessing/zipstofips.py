zip_list = []
with open("zips.txt", "r") as zip_file:
    zip_list = [x.strip() for x in zip_file.readlines()]

zip_dict = { zc : {"self": zc, "count": zip_list.count(zc)} for zc in zip_list }
for x in zip_dict:
	print x + ":" + str(zip_dict[x]["count"])

from pygeocoder import Geocoder
import dstk
from time import sleep

sleep_count = 0

dstk = dstk.DSTK()
for zc in zip_dict:
    try:
	    results = Geocoder.geocode(zc)
	    lat = results[0].coordinates[0]
	    lon = results[0].coordinates[1]
	    zip_dict[zc]["lat"] = lat
	    zip_dict[zc]["lon"] = lon
	    print "zc: %s %s" % (lat, lon)
	    sleep_count += 1
	    if sleep_count > 9:
	    	# break
	    	sleep(1)
	    	sleep_count = 0
	    results = dstk.coordinates2politics([lat, lon])
	    for pdb in results[0]['politics']:
	        if pdb["friendly_type"] == "county":
	            zip_dict[zc]["fips_county"] = pdb["code"].replace("_", "")
	            zip_dict[zc]["county_name"] = pdb["name"]
	        elif pdb["friendly_type"] == "state":
	        	zip_dict[zc]["state"] = pdb["name"]
    except:
        pass
        print "Exception!"
        raise
	print "zc %s: %s/%s, %s/%s" % (zc, lat, lon, zip_dict[zc]["fips_county"], zip_dict[zc]["county_name"])

from csv import DictWriter
fields = ["self", "count", "lat", "lon", "county_name", "fips_county", "state"]
with open("data.csv", 'w') as csvfile:
	cwriter = DictWriter(csvfile, fieldnames = fields, restval = "NA")
	for zc in zip_dict:
		cwriter.writerow(zip_dict[zc])
