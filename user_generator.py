from lxml import html
import requests
import random
import os

def file_is_empty(path):
	return os.stat(path).st_size==0

def get_last_four():
	last_four = random.randrange(1,9999)
	if last_four < 1000:
		last_four = "0" + str(last_four)
	return last_four

def get_name(identity):
	person = identity[0].split()
	givenName = person[0]
	lastName = person[2]
	initials = person[1]
	return givenName + ", " + lastName + ", " + initials

def get_address(identity):
	streetAddress = identity[1].strip()
	city = identity[2].split(', ')[0]
	postalCode = identity[2].strip()[-5:]
	state = identity[2].strip()[-8:-6]
	country = "United States"
	return streetAddress + ", " + city + ", " + postalCode + ", " + state + ", " + country

def get_contact_info(details):
	email = details[16]
	phone = details[8] + " " + details[6]
	phoneIPPrimary = ""
	phoneIPOther = ""
	return email + ", " + phone + ", " + phoneIPPrimary + ", " + phoneIPOther

def get_business_info(details):
	company = details[32]
	department = details[34]
	officeName = ""
	employeeID = ""
	title = ""
	manager = ""
	buildingName = ""
	return company + ", " + department + ", " + officeName + ", " + employeeID + ", " + title + ", " + manager + ", " + buildingName

def get_account_info(details):
	profilePath = "\\profile\path"
	scriptPath = "\\script\path"
	homeDirectory = "\\home\dir"
	homeDrive = "H:"
	password = details[20]
	passwordNeverExpires = "False"
	badPassTimeout = ""
	badPassCount = str(random.randrange(9))
	maxPassAge = ""
	lastLogon = ""
	targetOU = "OU=Users; OU=Lab"
	proxyAddresses = "SMTP:CHECK; SMTP:CHECK2"
	enabled = "True"
	return profilePath + ", " + scriptPath + ", " + homeDirectory + ", " + homeDrive + ", " + password + ", " + passwordNeverExpires + ", " + badPassTimeout + ", " + badPassCount + ", " + maxPassAge + ", " + lastLogon + ", " + targetOU + ", " + proxyAddresses + ", " + enabled

def get_personal_info(details):
	description = ""
	birthLocation = ""
	drink = ""
	jpegPhoto = ""
	wwwHomePage = details[22]
	objectguid = details[52]
	return description + ", " + birthLocation + ", " + drink + ", " + jpegPhoto + ", " + wwwHomePage + ", " + objectguid

def get_additional_info(details):
	motherMaiden = details[0] + ": " + details[1]
	ssn = details[2] + ": " + details[3][:-5] + str(get_last_four())
	birthday = details[9] + ": " + details[10].replace(',',' ')
	creditCard = "Credit Card: " + details[25] + ' ' + details[26] + " " + ': '.join(details[27:31])
	height = ': '.join(details[35:37])
	weight = ': ' .join(details[37:39])
	bloodType = ': '.join(details[39:41])
	favoriteColor = ': '.join(details[47:49])
	vehicle = ': '.join(details[49:51])
	return motherMaiden + '; ' + ssn + '; ' + birthday + '; ' + creditCard + '; ' + height + '; ' + weight + '; ' + bloodType + '; ' + favoriteColor + '; ' + vehicle + '; '

def generate_ad_account():
	page = requests.get('http://www.fakenamegenerator.com')
	tree = html.fromstring(page.content)
	identity = tree.xpath('//div[@class="address"]/*/text()')
	details = tree.xpath('//div[@class="extra"]/*/*/text()')

	implement = "Yes"
	full_name = get_name(identity)
	address = get_address(identity)
	contact_info = get_contact_info(details)
	business_info = get_business_info(details)
	account_info = get_account_info(details)
	personal_info = get_personal_info(details)
	additional_info = get_additional_info(details)
	return implement + ", " + full_name + ", " + address + ", " + contact_info + ", " + business_info + ", " + account_info + ", " + personal_info + ", " + additional_info


def main(number_of_people):
	random.seed()
	directory = open('ad_accounts.csv', 'a')
	if file_is_empty('ad_accounts.csv'):
		fields = open('active_directory_fields.txt', 'r')
		with open('active_directory_fields.txt', 'r') as fields:
			data=fields.read()
			directory.write(data + '\n')

	for person in range(number_of_people):
		row = generate_ad_account()
		directory.write(row + '\n')

	directory.close()

main(5)
