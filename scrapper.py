import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl,re
import dataQueries
def scrap_jobs():
    #IGNORE CERTIFICATION ERRORS
    ctx=ssl.create_default_context()
    ctx.check_hostname=False
    ctx.verify_mode=ssl.CERT_NONE
    #GIVING A URL
    url='https://www.ncs.gov.in/Pages/default.aspx'
    #START PARSING
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    #MAKING A LIST OF ALL JOBS AVAILABLE
    states=soup.find_all("li",class_="jobVacanciesOption")
    state_vacancy=[]
    for state in states:
        link=state.find('a').get('href',None)
        name=state.find('span',class_="stateName").get('title',None)
        vacancy=state.find('span',class_="jobsPost").string
        result=[link,name,vacancy]
        state_vacancy.append(result)
    for i in range(len(state_vacancy)):
        link=state_vacancy[i][0]
        html = urllib.request.urlopen(link, context=ctx).read()
        soup=BeautifulSoup(html,'html.parser')
        vacancies=soup.find_all(id="mytab")
        for vacancy in vacancies:
            try:
                form_page=vacancy.find('div').find('a').get('onclick')[14:-2]
                req = urllib.request.Request(form_page, headers={'User-Agent': 'Mozilla/5.0'})
                html = urllib.request.urlopen(req).read()
                soup=BeautifulSoup(html,'html.parser')
                last_date=re.findall('Last .+?2020',soup.text.replace('\n',"").replace("  ","").replace("\r",""))[0][18:]
                last_date="-".join(last_date.split('/')[::-1])
                Post=vacancy.find('div').find_all('span')[0].string
                Company_Name=vacancy.find('div').find_all('span')[4].string+vacancy.find('div').find_all('span')[5].string
                Location=vacancy.find('div').find_all('span')[8].string
                Expected_Salary=vacancy.find('div').find_all('span')[11].string
                Skill_required=vacancy.find('div').find_all('span')[14].string.replace("\t"," ").replace("  "," ")
                Description=vacancy.find('div').find_all('span')[16].string
                if Description!=None:
                    Description=Description.replace("\xa0","")
                avail=dataQueries.check_job_availability(Post,Company_Name)
                if avail==1:
                    continue
                dataQueries.add_scrap_job(Post,Skill_required,Description,Expected_Salary,state_vacancy[i][1],Location,Company_Name,form_page,last_date)
            except Exception:
                continue