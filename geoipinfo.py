import re, sys, urllib2

def geoinfo(*urls):
        with open('output.txt', 'w') as f:
                for url in urls:
                        req = urllib2.Request('http://freegeoip.net/csv/' + url)
                        aResp = urllib2.urlopen(req)
                        web_pg = aResp.read()
                        breakpage = web_pg.split(',')
                        f.write("\n")
                        f.write("################################\n")
                        f.write("Geographic Details: \n")
                        f.write("IP: %s\n" % breakpage[0])
                        f.write("Country Code: %s\n" % breakpage[1])
                        f.write("Country Name: %s\n" % breakpage[2])
                        f.write("Region Code: %s\n" % breakpage[3])
                        f.write("Region Name: %s\n" % breakpage[4])
                        f.write("City: %s\n" % breakpage[5])
                        f.write("Zip Code: %s\n" % breakpage[6])
                        f.write("Time Zone: %s\n" % breakpage[7])
                        f.write("Latitude: %s\n" % breakpage[8])
                        f.write("Longtitude: %s\n" % breakpage[9])
                        f.write("Metro Code: %s\n" % breakpage[10].rstrip("\n"))
                        f.write("################################\n")

def call_geoinfo():
        while True:
                input = raw_input("Insert a comma-separated list of IP addresses: ")
                if not input:        # If user input is blank, freegeoip will send information about the local WAN IP.
                        print("No IP addresses inserted; resorting to the local WAN IP address...")
                        geoinfo(*[''])  # or geoinfo(''); call geoinfo() either with either a list pointer or a null string as an argument.
                        return
                else:
                        urls = input.split(',')
                        urls = [ url.strip(' ') for url in urls ]
                        if not urls_are_valid(urls):
                                continue
                        geoinfo(*urls)
                        return

def urls_are_valid(urls):
        ip_address_pattern = re.compile('^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-4])$')    # IP address string ip_address_pattern
        invalid_urls = []
        for url in urls:
                if not ip_address_pattern.match(url):       # If at least one of the IP addresses the user has inserted does not match the IP address pattern, force them to re-insert IP addresses.
                        invalid_urls.append(url)
        if len(invalid_urls) == 0:
                return True
        elif len(invalid_urls) == 1:
                print("Invalid IP address \"{}\" inserted. Please, try again...".format(invalid_urls[0]))
                return False
        elif len(invalid_urls) > 1:
                print("Invalid IP addresses \"{}\" inserted. Please, try again...\n".format(", ".join(invalid_urls)))
                return False

if __name__ == '__main__':
        if len(sys.argv) < 2:       # No IP addresses have been passed as command-line arguments
                call_geoinfo()
        else:
                urls = sys.argv[1:]
                if not urls_are_valid(urls):
                        call_geoinfo()
                else:
                        geoinfo(*urls)

def insert_geoinfo(urls):
	geoinfo = get_geoinfo(*urls, format=csv)
	geonifo = geoinfo.split(',')
	# Open database connection
	db = MySQLdb.connect("localhost","testuser","test123","geoinfodb" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Prepare SQL query to INSERT a record into the database.
	sql = """INSERT INTO geoinfo (ip_address, country_code, country_name, region_code, region_name, city, zip_code, time_zone, latitude, longitude, metro_code)
				VALUES (geoinfo[0], geoinfo[1], geoinfo[2], geoinfo[3], geoinfo[4], geoinfo[5], geoinfo[6], geoinfo[7], geoinfo[8], geoinfo[9], geoinfo[10])"""
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   # Commit your changes in the database
	   db.commit()
	except:
	   # Rollback in case there is any error
	   db.rollback()
	finally:
		# disconnect from server
		db.close()
		

		
import re, sys, urllib2, json	

def get_user_input(format=None, ip_addresses=None):
	if not format:
		while True:
			format = raw_input("Insert response format csv or json: ")
			if not format:
				print("No response format inserted. Try again...)
				continue
			if format not in ( 'csv', 'json' ):
				print("Wrong response format inserted. Try again...)
				continue
			break
	if not ip_addresses:
		while True:
			ip_addresses = raw_input("Insert a comma-separated list of IP addresses: ")
			if not ip_addresses:
				print("No IP addresses inserted. Try again...)
				continue
			if not ip_addresses_are_valid(ip_addresses):
				continue
			ip_addresses = ip_addresses.split(',')
			ip_addresses = [ ip_address.strip(' ') for ip_address in ip_addresses ]
			break
	return ip_addresses, format
					
def ip_addresses_are_valid(ip_addresses):
	ip_address_pattern = re.compile('^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-4])$')
	invalid_ip_addresses = []
	for ip_address in ip_addresses:
		if not ip_address_pattern.match(url):
			invalid_urls.append(url)
	if len(invalid_ip_addresses) == 0:
		return True
	elif len(invalid_ip_addresses) == 1:
		print("Invalid IP address \"{}\" inserted.".format(invalid_urls[0]))
		return False
	elif len(invalid_urls) > 1:
		print("Invalid IP addresses \"{}\" inserted.\n".format(", ".join(invalid_urls)))
		return False
		
def get_geoinfo(*ip_addresses, format):	
	geoinfos = []
	for ip_address in ip_addresses:
		req = urllib2.Request('http://freegeoip.net/format/' + ip_address)
		aResp = urllib2.urlopen(req)
		webpage = aResp.read()
		geoinfo = webpage.split(',')
		geoinfos.append(geoinfo)
	return geoinfos		
	
def insert_geoinfo(ipaddresses, format):
	geoinfos = get_geoinfo(*ip_addresses, format)
	if format == 'csv'
		for geoinfo in geoinfos:
			# Open database connection
			db = MySQLdb.connect("localhost","testuser","test123","geoinfodb" )

			# prepare a cursor object using cursor() method
			cursor = db.cursor()

			# Prepare SQL query to INSERT a record into the database.
			sql = """INSERT INTO geoinfo (ip_address, country_code, country_name, region_code, region_name, city, zip_code, time_zone, latitude, longitude, metro_code)
				VALUES (geoinfo[0], geoinfo[1], geoinfo[2], geoinfo[3], geoinfo[4], geoinfo[5], geoinfo[6], geoinfo[7], geoinfo[8], geoinfo[9], geoinfo[10])"""
			try:
				# Execute the SQL command
				cursor.execute(sql)
				# Commit your changes in the database
				db.commit()
			except:
				# Rollback in case there is any error
				db.rollback()
			finally:
				# disconnect from server
				db.close()
	elif format == 'json':
		for geoinfo in geoinfos:
			geoinfo_json = json.loads(geoinfo)

def parse_ip_addresses(input_file):
	ip_addresses = []
	with open('input_file', 'r') as f:
		for line in f.read():
			ip_addresses.append(line.spplit(',')[0])
	return ip_addresses
				
if __name__ == '__main__':
	if len(sys.argv) < 2:
		ipaddress, format = get_user_input()
		insert_geoinfo(*ip_addresses, format)
		sys.exit(0)
	if not sys.argv[1] in ( 'csv', 'json' ):
		sys.exit("Wrong format. Exiting...")
	format = sys.argv[1]
	if len(sys.argv) < 3:
		sys.exit("No IP addresses inserted.")
		ip_addresses = get_user_info(format)
	if len(sys.argv) == 3 and os.exists(sys.argv[2]):
		ip_addresses = parse_ip_addresses(sys.argv[2])
	else:
		ip_addresses = sys.argv[2:]
		if not ip_addresses:
			sys.exit("No IP addresses. Exiting...")
	if not ip_addresses_are_valid():
		sys.exit("Exiting...")
	insert_geoinfo(*ip_addresses, format)
	sys.exit(0)
	
	
cat access_log | awk '{print $1}' | uniq -c | awk {'print $2 "," $1'}