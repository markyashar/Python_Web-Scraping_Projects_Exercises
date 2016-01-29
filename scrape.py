# See the web scraper tutorial here: https://first-web-scraper.readthedocs.org/en/latest/
# The first step is to import the requests (and other) library and download the Boone County webpage.
import csv
import requests
from BeautifulSoup import BeautifulSoup

url = 'http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp'
response = requests.get(url)
html = response.content
# print html  # We see the entire HTML of the printed out here.

# Next import the BeautifulSoup HTML parsing library and feed it the page (see top of script)

soup = BeautifulSoup(html)
# print soup.prettify()    # We see the page's HTML again, but in a prettier format this time. That's a hint at 
# the magic happening inside BeautifulSoup once it gets its hands on the page.

# Next we take all the detective work we did with the page's HTML above and convert it into a simple, direct command 
# that will instruct BeautifulSoup on how to extract only the table we're after.
table = soup.find('table', attrs={'class': 'collapse shadow BCSDTable'})
# print table.prettify()

# Now that we have our hands on the table, we need to convert the rows in the table into a list, which we can then 
# loop through and grab all the data out of.
# BeautifulSoup gets us going by allowing us to dig down into our table and return a list of rows, which are 
# created in HTML using <tr> tags inside the table.
# for row in table.findAll('tr'):
#     print row.prettify()    # We now see each row printed out separately as the script loops through the table.

# Next we can loop through each of the cells in each row by selecting them inside the loop. Cells are created in 
# HTML by the <td> tag.

list_of_rows = []
#for row in table.findAll('tr'):
for row in table.findAll('tr')[1:]:  # here, we account for the headers (see comments near end of script)
    # for cell in row.findAll('td'):
        # print cell.text
# When that prints you may notice some annoying &nbsp; on the end of many lines. That is the HTML code for a 
# non-breaking space, which forces the browser to render an empty space on the page. It is junk and we can delete 
# it easily with this handy Python trick.
        # print cell.text.replace('&nbsp;', '')

# Now that we have found the data we want to extract, we need to structure it in a way that can be written out 
# to a comma-delimited text file. That won't be hard since CSVs aren't any more than a grid of columns and rows, 
# much like a table.

# Let's start by adding each cell in a row to a new Python list.
    list_of_cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace('&nbsp;', '')
        list_of_cells.append(text)
    # print list_of_cells    # We now see Python lists streaming by one row at a time.
# Those lists can now be lumped together into one big list of lists, which, when you think about it, isn't all 
# that different from how a spreadsheet is structured.
    list_of_rows.append(list_of_cells)

# print list_of_rows    # We see a big bunch of data dumped out into the terminal. Looking closely, we see the 
                      # list of lists.

# To write that list out to a comma-delimited file, we need to import Python's built-in csv module at the top 
# of the file. Then, at the botton, we will create a new file, hand it off to the csv module, and then lead 
# on a handy tool it has called writerows to dump out our list of lists.
outfile = open("./inmates.csv", "wb")
writer = csv.writer(outfile)
# writer.writerows(list_of_rows)  # Nothing happens - at least to appears to happen.
# Since there are no longer any print statements in the file, the script is no longer dumping data out to the 
# terminal. However, if we open up out code directory we now see a new file named inmates.csv. Can open it 
# in a text editor or Excel and should see structured data all scraped out.
# There is still one obvious problem though. There are no headers! Here's why. If you go back and look closely, 
# our script is only looping through lists of <td> tags found within each row. Fun fact: Header tags in HTML 
# tables are often wrapped in the slightly different <th> tag. Look back at the source of the Boone County 
# page and we'll see that's what exactly they do.

# But rather than bend over backwords to dig them out of the page, let's try something a little different. 
# Let's just skip the first row when we loop though, and then write the headers out ourselves at the end.
writer.writerow(["Last", "First", "Middle", "Gender", "Race", "Age", "City", "State"])
writer.writerows(list_of_rows)
