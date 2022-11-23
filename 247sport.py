#!/usr/bin/python3
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import xlsxwriter

dates = ['2016', '2017', '2018', '2019', '2020', '2021']
rating = position = lastname = firstname = class_ = listyear = height = weight = hometown = state = country = nationalrank = hs = offers = []
br = webdriver.Firefox()
for d in dates:
    url = f"https://247sports.com/Season/{d}-Basketball/TransferPortal/"
    br.get(url)
    while True:
        try:
            br.find_element_by_class_name("transfer-group-loadMore").click()
        except:
            break
    players = br.find_elements_by_class_name("transfer-player")
    for p in players:
        br.get(p.find_element_by_tag_name("a").get_attribute("href"))
        ps = bs(br.page_source, 'html.parser')
        try:
            rating.append(len(ps.find_all("span", class_="yellow")))
        except:
            rating.append("N/A")
        try:
            for li in ps.find("ul", class_="metrics-list").find_all("li"):
                if 'Pos' in li.text:
                    position.append(li.find_all("span")[1].text)
                if "Height" in li.text:
                    height.append(li.find_all("span")[1].text)
                if "Weight" in li.text:
                    weight.append(li.find_all("span")[1].text)
        except:
            weight.append("N/A")
            height.append("N/A")
            position.append("N/A")
        try:
            lastname.append(ps.find("h1", class_="name").text.split(" ")[1])
            firstname.append(ps.find("h1", class_="name").text.split(" ")[0])
        except:
            lastname.append("N/A")
            firstname.append("N/A")
        print(ps.find('h1', class_="name").text)
        try:
            class_.append(
                ps.find("ul", class_="commitment").find_all("span")[1].text)
        except:
            class_.append("N/A")
        listyear.append(d)
        try:
            for li in ps.find("ul", class_="details").find_all("li"):
                if "City" in li.text:
                    hometown.append(li.find_all("span")[1].text.split(",")[0])
                    state.append(li.find_all("span")[1].text.split(",")[1])
                if 'High School' in li.text:
                    hs.append(li.find_all("span")[1].text)
        except:
            hometown.append("N/A")
            state.append("N/A")
            hs.append("N/A")
        country.append("USA")
        try:
            for li in ps.find("ul", class_="ranks-list").find_all("li"):
                if 'Natl.' in li.text:
                    nationalrank.append(li.find('a').text)
        except:
            nationalrank.append("N/A")
        br.find_element_by_class_name("view-profile-link").click()
        ps = bs(br.page_source, 'html.parser')
        br.get(ps.find('a', class_="college-comp__view-all").get("href"))
        ps = bs(br.page_source, 'html.parser')
        try:
            ofrlst = ps.find("ul", class_="recruit-interest-index_lst")
            frs = ofrlst.find_all("li")
            finfrs = ""
            for fr in frs:
                finfrs += fr.find_element_by_tag_name("a").text + ","
            offers.append(finfrs)
        except:
            offers.append("N/A")

df = pd.DataFrame({
    'stars': rating,
    'Position': position,
    'Last Name': lastname,
    'First Name': firstname,
    'Class': class_,
    'List year': listyear,
    'Height': height,
    'Weight': weight,
    'Home Town': hometown,
    'State': state,
    'Country': country,
    'National Rank': nationalrank,
    'High School': hs,
    'Offers': offers,
})
print(df)
