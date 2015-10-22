from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import subprocess
from BeautifulSoup import BeautifulSoup

# 1) " TARRANT	"	"Dynamic zip code"	"1 Year Old	"	"frame	"	"Claim free 5 years	"	"Good Credit	"	"Homeowners	"	75000

# Notice that all the below variables are specific to the website and anyone can modify based on that. As it is a secured link i am not mentioning the link
credit_ratings = ['good','average','bad'] 
homeowner_policies = ['75','150','200','350']
age_of_residences = ['new','10years','35years']
type_of_constructions = ['frame','stucco','brick']

COUNTYCODE = '220'
NUMBEROFZIPCODES = 73
COUNTYNAME = 'TARRANT'

def getData_1(driver,option,credit_rating,homeowner_policy,age_of_residence,type_of_construction):
	driver.get("Website link")
	driver.find_element_by_xpath("//select[@name='cntyCd']/option[@value= "+COUNTYCODE+"]").click()
	driver.find_element_by_xpath("//select[@name='zipCd']/option["+str(option)+"]").click()

	# Write current zip code
	zipCodeElement = Select(browser.find_element_by_name("zipCd"))
	zipCode = zipCodeElement.first_selected_option.text

	# Select other options
	driver.find_element_by_id("claimFree").click()
	driver.find_element_by_id(credit_rating).click()
	driver.find_element_by_id(homeowner_policy).click()
	driver.find_element_by_id(age_of_residence).click()
	driver.find_element_by_id(type_of_construction).click()
	driver.find_element_by_id("submit_button").click()

	element = driver.find_element_by_id('resRates')

	data = element.get_attribute('innerHTML')
	return data,zipCode



def writeTableData(datalist,targetFile):
	# Iterate with each row
	for row in datalist:
		# TD signifies column in a table
		for column in row.findAll('td'):
			# Check if table cell has data
			if len(column.contents) > 0 :
				# Added double quotes on each side of content to preserve number formatting
				targetFile.write("\""+str(column.contents[0]).replace("&nbsp;","")+"\""+",")
			else:
				targetFile.write(",")
		# write newline at end of each row
		targetFile.write("\n")

def writeTitleAndData(zip_code,credit_rating,homeowner_policy,age_of_residence,type_of_construction):					
	data,zipCodestring = getData_1(browser,zip_code,credit_rating,homeowner_policy,age_of_residence,type_of_construction)
	#targetFile.write("\n County "+"," "\t Zip Code" +"," "\t Age of Residence " +"," "\t Type of Construction "+"," "\t Claim History "+"," "\t Credit Rating "+",""\t Policy "+"," "\t Coverage Amount ")
	#targetFile.write("\n " +COUNTYNAME+" \t "+"," +zipCode+"\t"+"," ""+age_of_residence+"\t"+"," "frame\t"+",""Claim free 5 years\t"+"," "Good Credit\t"+"," "Homeowners\t"+"," " 75000\n")



	targetFile.write("\n")
	targetFile.write("County,Zip Code,Age of Residence,Type of Construction,Claim History,Credit Rating,Policy Coverage Amount")
	targetFile.write("\n")
	targetFile.write(COUNTYNAME+","+zipCodestring+","+age_of_residence+","+type_of_construction+",Claim free 5 years,"+credit_rating+","+homeowner_policy)
	targetFile.write("\n Company Name"+"," "\t"+"," "\tAnnual Sample Rate"+"," "\tPolicy Form"+"," "\tA.M.Best Rating"+"," "\tComplaint Index"+"," "\t Rate Change")




	# Parse html with soup
	soup = BeautifulSoup(data)

	# Find all rows in the table
	soupeddata = soup.findAll('tr')

	# Write data
	writeTableData(soupeddata,targetFile)


# Execution starts from here
browser = webdriver.Firefox()
# Open a file, can be chaged to dat range
filename = "somefile.csv"
infoLog = "log.txt"
targetFile = open (filename, 'a')
infoFile = open(infoLog,'a')
infoFile.write("new run")
# Total of 85 zipcodes available in the dropdown

#Good credit
for zip_code in range(68,NUMBEROFZIPCODES+1):
	# Get raw data from browser
	for credit_rating in credit_ratings:
		for homeowner_policy in homeowner_policies:
			for age_of_residence in age_of_residences:
				for type_of_construction in type_of_constructions:
					infoFile.write(str(zip_code)+","+age_of_residence+","+type_of_construction+","+credit_rating+","+homeowner_policy+"\n")
                                        #print ("values are : %r,%r,%r,%r,%r " % (zip_code,credit_rating,homeowner_policy,age_of_residence,type_of_construction))
					writeTitleAndData(zip_code,credit_rating,homeowner_policy,age_of_residence,type_of_construction)






targetFile.write("****end of run****")
targetFile.close()
browser.close()
