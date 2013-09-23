lat = 43.376782
lon = -86.3275351
import dstk
dstk = dstk.DSTK()
results = dstk.coordinates2politics([lat,lon])
print results
for pdb in results[0]['politics']:
    if pdb["friendly_type"] == "county":
        print pdb["code"]
   