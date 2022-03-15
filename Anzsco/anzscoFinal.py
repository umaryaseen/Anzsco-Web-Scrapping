from os import close
import logging
from bs4.element import PageElement
from requests.api import head
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import requests
from sqlalchemy import null
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker



count = 0
exceptionCount = 0
init_url = 'https://www.acacia-au.com/'
url = 'https://www.acacia-au.com/anzsco.php'
url_sec = []
article = requests.get(url).text
soup = BeautifulSoup(article, 'html.parser')

engine = create_engine(
    "sqlite://///home/lenovo/Documents/Anzsco Web Scrapping/Anzsco/anzscoTestDB", echo=True)

connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


logging.basicConfig(filename="anzsco.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class anzsco(Base):
    __tablename__ = 'anzsco'

    id = Column(Integer, primary_key=True, autoincrement=True)
    anzsco_url = Column(Text)
    authority = Column(Text)
    employer_sponsership = Column(Text)
    indep_and_family_sponsered = Column(Text)
    state_nomination = Column(Text)
    mltssl_stsol = Column(Text)
    caveat = Column(Text)


class anzsco_sec(Base):
    __tablename__ = 'anzsco_sec'

    id = Column(Integer, primary_key=True, autoincrement=True)
    head1 = Column(Text)
    description = Column(Text)
    skill_level = Column(Integer)
    alternative_titles = Column(Text)
    specialisations = Column(Text)
    skills_assess_authority = Column(Text)
    caveats = Column(Text)
    asco_occupations = Column(Text)
    head2 = Column(Text)
    more_description = Column(Text)
    tasks = Column(Text)
    skill_level_desc = Column(Text)
    occupations_in_this_group = Column(Text)


# print(anzsco.__table__)

Base.metadata.create_all(engine)


for tr in soup.find_all('tr'):
    tableData = anzsco(anzsco_url=str(tr.contents[1]), authority=str(tr.contents[3].string),
                       employer_sponsership=str(tr.contents[5].string), indep_and_family_sponsered=str(tr.contents[7].string),
                       state_nomination=str(tr.contents[9].string), mltssl_stsol=str(tr.contents[11].string),
                       caveat=str(tr.contents[13])
                       )

    for a in tr.find_all('a'):
        url_sec.append(init_url + a.get('href'))

    session.add(tableData)


session.commit()

while len(url_sec) != 0:
    for link in url_sec:
        try:
           # url_sec = 'https://www.acacia-au.com/'+ link.get('href')
            article_sec = requests.get(link).text
            soup_sec = BeautifulSoup(article_sec,'html.parser')
            header1 = False
            description = False
            skill_level = False
            alternative_titles = False
            specialisations = False
            skill_assessment = False
            caveats = False
            asco_occupations = False
            header2 = False
            secDesc = False
            tasks = False
            secSkill = False
            occupationInGroup = False


            pageData = {
                        "head1":null(),
                        "description" : null(),
                        "skill_level": null(),
                        "alternative_titles" : null(),
                        "specialisations" : null(),
                        "skill_assessment": null(),
                        "caveats":null(),
                        "asco_occupations":null(),
                        "head2": null(),
                        "secDesc":null(),
                        "tasks":null(),
                        "secSkill":null(),
                        "occupation_in_group":null()
                    }


            if soup_sec.find('h1'):
                pageData["head1"] = soup_sec.find('h1').string
            if soup_sec.find('h2'):
                pageData["head2"] = soup_sec.find('h2').string


            print(link)

            for dl in soup_sec.find_all('dl'):
                for dt in dl.find_all('dt'):
                    if dt.contents[0] == "Description" and description == False:
                        description = True
                        pageData["description"] = dt.next_sibling.next_sibling.contents[0].strip()
                    elif dt.contents[0] == "Skill Level" and skill_level == False:
                        skill_level = True
                        pageData["skill_level"] = dt.next_sibling.next_sibling.contents[0].strip()
                    elif dt.contents[0] == "Alternative Titles":
                        alternative_titles = True
                        pageData["alternative_titles"] = dt.next_sibling.next_sibling.contents[1]
                    elif dt.contents[0] == "Specialisations":
                        specialisations = True
                        pageData["specialisations"] = dt.next_sibling.next_sibling.contents[1]
                    elif dt.contents[0] == "Skills Assessment Authority":
                        skill_assessment = True
                        pageData["skill_assessment"] = dt.next_sibling.next_sibling
                    elif dt.contents[0] == "Caveats":
                        caveats = True
                        pageData["caveats"] = dt.next_sibling.next_sibling
                    elif dt.contents[0] == "Endorsed Correlations to ASCO Occupations":
                        asco_occupations = True
                        pageData["asco_occupations"] = dt.next_sibling.next_sibling.contents[1]
                    elif dt.contents[0] == "Description":
                        secDesc = True
                        pageData["secDesc"] = dt.next_sibling.next_sibling.contents[0].strip()
                    elif dt.contents[0] == "Tasks":
                        tasks = True
                        pageData["tasks"] = dt.next_sibling.next_sibling.contents[1]
                    elif dt.contents[0] == "Skill Level":
                        secSkill = True
                        pageData["secSkill"] = dt.next_sibling.next_sibling.contents[0].strip()
                    elif dt.contents[0] == "Occupations in this Group":
                        occupationInGroup = True
                        pageData["occupation_in_group"] = dt.next_sibling.contents
            tableDataSec = anzsco_sec(head1 = str(pageData["head1"]),description = str(pageData["description"]),
                            skill_level = str(pageData["skill_level"]),alternative_titles = str(pageData["alternative_titles"]),
                            specialisations = str(pageData["specialisations"]),
                            skills_assess_authority = str(pageData["skill_assessment"]),caveats = str(pageData["caveats"]),
                            asco_occupations = str(pageData["asco_occupations"]),
                            head2 = str(pageData["head2"]),more_description = str(pageData["secDesc"]),tasks = str(pageData["tasks"]),
                            skill_level_desc = str(pageData["secSkill"]),occupations_in_this_group = str(pageData["occupation_in_group"]))


            session.add(tableDataSec)
            session.commit()

            url_sec.remove(link)
            print(len(url_sec))

        except Exception as e:

            text_file = open("/home/lenovo/Documents/testing.html", "a")

            text_file.write(str(link))
            text_file.write('\n')
            text_file.write('\n')
            text_file.write(str(e))
            text_file.write('\n')
            text_file.write('\n')
            exceptionCount = exceptionCount + 1


print("Exception Count: " , exceptionCount)
