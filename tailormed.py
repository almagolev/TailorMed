import psycopg2
import requests_html

""" WRITTEN BY ALMA LEVI 10/06/201 """

def doAll(res):
    #GET NAME
    name = (res.html.find("h1")[0]).text

    #GET DETAILS
    details = (res.html.find(".details .clearfix"))
    for i in details:
        if "Status" in i.text:
            nextt = i.text.split()
            status = nextt[nextt.index("Status")+1]
        elif "Maximum Award Level" in i.text:
            nextt = i.text.split()
            amount = nextt[nextt.index("Level")+1]

    #GET TREATMENTS
    treatments_list = (res.html.find(".clearfix")[0].find("li"))
    treatments=""
    for i in treatments_list:
        treatments += i.text + ","
    treatments = treatments[:-1]

    #CONNECT TO DB
    conn = psycopg2.connect(dbname='postgres',host='localhost',port='5432', user='postgres', password='postgres')
    cur = conn.cursor()

    try:
        #INSERT
        cur.execute("insert into public.tailormed values(default,%s,%s,%s,%s);",(name,status.lower(),treatments,amount))
        conn.commit()
    except:
        """print(" BLAH ")"""

    conn = psycopg2.connect(dbname='postgres',host='localhost',port='5432', user='postgres', password='postgres')
    cur = conn.cursor()
    
    try:
        #UPDATE
        cur.execute("update public.tailormed set status = %s, treatments = %s, amount = %s where name = %s;",(status,treatments,amount, name))
        conn.commit()
    except:
        """print(" BLAH 2")"""

    #GET DATA FROM DB AND PRINT
    conn = psycopg2.connect(dbname='postgres',host='localhost',port='5432', user='postgres', password='postgres')
    cur = conn.cursor()
    results = cur.execute("SELECT * FROM public.tailormed")
    row = cur.fetchone()
    while row is not None:
        print(row)
        row = cur.fetchone()
    
    #CLOSE
    cur.close()
    conn.close()

#CREATE CONNECTION
session = requests_html.HTMLSession()
res = session.get("https://www.healthwellfoundation.org/fund/acute-myeloid-leukemia-medicare-access")

funds = ["acute-myeloid-leukemia","adrenal-insufficiency","amyotrophic-lateral-sclerosis","covid-19-front-line-healthcare-worker-behavioral-health"]

res = session.get("https://www.healthwellfoundation.org/disease-funds/")

links = res.html.absolute_links
for i in links:
    if any(fund in i for fund in funds):
        doAll(session.get(i))

