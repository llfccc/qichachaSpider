file_object = open('company_name.txt', 'r')
file_content = file_object.readlines()
print type(file_content), len(file_content)
try:
    url_head = "http://www.qichacha.com/search?key="
    for line in file_content:
        print line.decode('utf-8')
except:
    pass