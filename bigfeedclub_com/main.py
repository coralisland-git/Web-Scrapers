import pdb
import pdfplumber
import csv
import requests
from lxml import etree
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import shutil

session = requests.Session()

# create photo directory if not exist
ROOT_PATH = 'photos'
if not os.path.isdir(ROOT_PATH):
   os.makedirs(ROOT_PATH)

# setup selenium driver with headless
options = Options()   
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--start-maximized")
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome('./chromedriver.exe', options=options)

# format the item, trim spaces and convert float into string
def validate(item): 
    if item == None:
        item = ''
    if type(item) == int or type(item) == float:
        item = str(item)
    if type(item) == list:
        item = ' '.join(item)
    return item.strip()

# return image url from costco.com by id
def get_images(id):
	try:
		url = 'https://www.costco.ca/TypeAhead?searchTerm={}&dept=All&storeId=10302&catalogId=11201&langId=-24&isMobile=0'.format(id)
		driver.get(url)
		page_source = driver.page_source
		data = validate(etree.HTML(page_source).xpath('.//text()'))
		json_obj = json.loads(data)
		items = json_obj.get('costcoAutoSuggestionView')
		if len(items) > 0:
			# detail_link = items[0].get('baseUrl')
			return items[0].get('properties').get('FullImage')		
	except:
		pass
	return ''

# download image into photo directory on local by image url 
def download_image(id, link):
	if link == '':
		return
	try:
		file_content = session.get(link, stream=True)
		with open('{}/{}.png'.format(ROOT_PATH, id), mode='wb') as output:
			file_content.raw.decode_content = True
			shutil.copyfileobj(file_content.raw, output)
	except:
		pass

# parse pdf template1 (with coupon)
class Template1:
	def __init__(self):
		pass

	# return product id
	def get_id(self, word):
		if float(word['x0']) > 40 and float(word['x0']) < 110:
			return word['text'] + ' '
		return ''

	# return product name
	def get_item(self, word):
		if float(word['x0']) > 110 and float(word['x0']) < 221:
			return word['text']  + ' '
		return ''

	# return product description
	def get_desc(self, word):
		if float(word['x0']) > 221 and float(word['x0']) < 295:
			return word['text']  + ' '
		return ''

	# return product quantity
	def get_quantity(self, word):
		if float(word['x0']) > 295 and float(word['x0']) < 401:
			return word['text']  + ' '
		return ''

	# return product price
	def get_price(self, word):
		if float(word['x0']) > 401 and float(word['x0']) < 433:
			return word['text']  + ' '
		return ''

	# return product coupon
	def get_coupon(self, word):
		if float(word['x0']) > 433 and float(word['x0']) < 465:
			return word['text']  + ' '
		return ''

	# return product sell price
	def get_sell_price(self, word):
		if float(word['x0']) > 465 and float(word['x0']) < 501:
			return word['text']  + ' '
		return ''

	# return product date
	def get_date(self, word):
		if float(word['x0']) > 501 and float(word['x0']) < 560:
			return word['text']  + ' '
		return ''

	# parse pdf content
	def parse_content(self, filename):
		try:
			# create csv file for the result
			with open('{}.csv'.format(filename), mode='w', encoding="utf-8-sig") as output_file:
				writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
				# add headers
				writer.writerow(['Item #', 'Item', 'Description', 'Quantity', 'Price', 'Coupon', 'Sell Price', 'Date', 'Category', 'Image'])
				category, id, item, desc, quantity, price, coupon, sell_price, date, col_cnt, end_flag, row = '', '', '', '', '', '', '', '', '', 0, False, ''
				# load pdf file and add rows into csv file
				pdf = pdfplumber.open("{}.pdf".format(filename))
				for p_idx, page in enumerate(pdf.pages):
					begin = 0
					if p_idx == 0:
						begin = 19
					words = page.extract_words()[begin:]
					for w_idx, word in enumerate(words):
						col_cnt += 1
						id += self.get_id(word)
						item += self.get_item(word)
						desc += self.get_desc(word)
						quantity += self.get_quantity(word)
						price += self.get_price(word)
						coupon += self.get_coupon(word)
						sell_price += self.get_sell_price(word)
						date += self.get_date(word)
						row += word['text'] + ' '
						if w_idx > len(words)-2:
							end_flag = True
						else:
							n_word = words[w_idx+1]
						if abs(float(n_word['top']) - float(word['top'])) > 2 or end_flag:
							if col_cnt < 4:
								category = row
							else:
								image = get_images(id)
								writer.writerow([
									validate(id),
									validate(item),
									validate(desc),
									validate(quantity),
									validate(price),
									validate(coupon),
									validate(sell_price),
									validate(date),
									validate(category),
									image
								])
								# download_image(id, image)
							id, item, desc, quantity, price, coupon, sell_price, date, col_cnt, end_flag, row = '', '', '', '', '', '', '', '', 0, False, ''

			print('Template1 is parsed successfully !!!')
		except:
			print('Oops, something went wrong in template1.')

# parse pdf template2
class Template2:
	def __init__(self):
		pass

	# return product id
	def get_id(self, word):
		if float(word['x0']) > 40 and float(word['x0']) < 100:
			return word['text'] + ' '
		return ''

	# return product item
	def get_item(self, word):
		if float(word['x0']) > 100 and float(word['x0']) < 250:
			return word['text']  + ' '
		return ''

	# return product quantity
	def get_quantity(self, word):
		if float(word['x0']) > 250 and float(word['x0']) < 387:
			return word['text']  + ' '
		return ''

	# return product description
	def get_desc(self, word):
		if float(word['x0']) > 387	 and float(word['x0']) < 510:
			return word['text']  + ' '
		return ''

	# return product price
	def get_price(self, word):
		if float(word['x0']) > 510 and float(word['x0']) < 560:
			return word['text']  + ' '
		return ''

	# parse pdf content
	def parse_content(self, filename):
		try:
			with open('{}.csv'.format(filename), mode='w', encoding="utf-8-sig") as output_file:
				writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
				# add headers
				writer.writerow(['Item #', 'Item', 'Description', 'Quantity', 'Price', 'Category', 'Image'])
				category, id, item, desc, quantity, price, coupon, sell_price, date, col_cnt, end_flag, row = '', '', '', '', '', '', '', '', '', 0, False, ''
				# load pdf file and add rows into csv file
				pdf = pdfplumber.open("{}.pdf".format(filename))
				for p_idx, page in enumerate(pdf.pages):
					begin = 0
					if p_idx == 0:
						begin = 12
					words = page.extract_words()[begin:]
					for w_idx, word in enumerate(words):
						col_cnt += 1
						item += self.get_item(word)
						id += self.get_id(word)
						quantity += self.get_quantity(word)
						desc += self.get_desc(word)
						price += self.get_price(word)
						row += word['text'] + ' '
						if w_idx > len(words)-2:
							end_flag = True
						else:
							n_word = words[w_idx+1]
						if abs(float(n_word['top']) - float(word['top'])) > 2 or end_flag:
							if col_cnt < 4:
								category = row
							else:
								image = get_images(id)
								writer.writerow([
									validate(id),
									validate(item),
									validate(desc),
									validate(quantity),
									validate(price),
									validate(category),
									image
								])								
								# download_image(id, image)
							id, item, desc, quantity, price, coupon, sell_price, date, col_cnt, end_flag, row = '', '', '', '', '', '', '', '', 0, False, ''
			print('Template2 is parsed successfully!!!')
		except:
			print('Oops, something went wrong in template2.')

if __name__ == '__main__':
	filename = input("PDF File Name:")
	if filename == '':
		filename = 'sample'
	else:
		filename = '.'.join(filename.split('.')[:-1])
	try:
		pdf = pdfplumber.open("{}.pdf".format(filename))	
		headers = ' '.join([word['text'].lower() for word in pdf.pages[0].extract_words()[:20]])
		if 'coupon' in headers:
			Template1().parse_content(filename)
		else:
			Template2().parse_content(filename)
	except:
		print('Oops, PDF file is broken.')
