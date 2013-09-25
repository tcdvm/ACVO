import csv
from BeautifulSoup import BeautifulSoup

dipcount = {}

reader = csv.reader(open("data.csv"), delimiter=",")

for row in reader:
	try:
		full_fips = row[5]
		dcount = row[1]
		dipcount[full_fips] = dcount
		# dipcount[unicode(full_fips)] = dcount
	except Exception, e:
		raise

# print dipcount

svg = open('counties.svg', 'r').read()

soup = BeautifulSoup(svg, selfClosingTags=['defs', 'sodipodi:namedview'])
paths = soup.findAll('path')

colors = ["#FFF7FB", "#ECE7F2", "#D0D1E6", "#A6BDDB", "#74A9CF", "#3690C0", "#0570B0", "#045A8D", "#023858"]

path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1; stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt; marker-start:none;stroke-linejoin:bevel;fill:'
encoded = 0

for p in paths:
	if p['id'] not in ["State_Lines", "separator"]:
		try:
			continue
			dcount = int(dipcount[p['id']])
			encoded += 1
			# print dcount
		except:
			# print p['id'] + " not found."
			continue
	if dcount > 7:
		color_class = 8
	elif dcount > 6:
		color_class = 7
	elif dcount > 5:
		color_class = 6
	elif dcount > 4:
		color_class = 5
	elif dcount > 3:
		color_class = 4
	elif dcount > 2:
		color_class = 3
	elif dcount > 1:
		color_class = 2
	elif dcount > 0:
		color_class = 1
	else:
		color_class = 0

	color = colors[0]
	p['style'] = path_style + color

print soup.prettify()
# print "Encoded: " + str(encoded)