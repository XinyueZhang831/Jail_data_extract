############################################
# open the web automatically               #
# click the field you need                 #
# iterate all jails in different states    #
# write population with citizenship to csv #
# file name is the State+Jail              #
############################################
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import re
import pandas as pd

def prepare_page():
    driver = webdriver.Chrome('C:\/Users\/xinyu\PycharmProjects\webscrape\driver\chromedriver.exe')

    driver.set_page_load_timeout(10)
    driver.get('https://trac.syr.edu/phptools/immigration/detainhistory/')


    selectFirst =Select(driver.find_element_by_xpath("//div[contains(@id, 'col1head2')]").find_element_by_name('dimension_pick_col1'))
    selectFirst.select_by_value('LEA_state')
    time.sleep(2)

    selectSecond = Select(driver.find_element_by_xpath("//div[contains(@id, 'col2head2')]").find_element_by_name('dimension_pick_col1'))
    selectSecond.select_by_value('trac_fac_name_county')

    time.sleep(2)

    selectThird = Select(driver.find_element_by_xpath("//div[contains(@id, 'col3head2')]").find_element_by_name('dimension_pick_col1'))
    selectThird.select_by_value('citizenship')

    time.sleep(2)
    find_state(driver)


def find_state(driver):
    print('find_state')
    list_state_herf = []
    list_state = []
    links = driver.find_elements_by_partial_link_text('')
    for link in links:
        list_link = link.get_attribute("href")
        if 'LEA_state' in list_link:
            list_state_herf.append(list_link[11:])

    table_trs_state = driver.find_elements_by_xpath("//div[contains(@id, 'col1') and contains(@class, 'scroll')]/table/tbody/tr")
    for tr_state in table_trs_state:
        td = tr_state.find_elements_by_xpath(".//td")
        convert_state = str(td[0].get_attribute("innerHTML").encode("UTF-8"))
        convert_state = convert_state.replace('/', '-')
        convert_state = convert_state.replace('\'', '')
        item_split = re.findall('>([^\']*)<', convert_state)
        if len(item_split) == 0:
            append_item = 'you need to check the name'
        else:
            append_item = item_split[0]
        list_state.append(append_item)
    state_href = list(zip(list_state_herf[2:], list_state))[1:0]# you may want to change this part since i ignore the All i n state
    print(state_href)
    for item in state_href:
        print(item)
        click_state_collect_jail(item, driver)


def click_state_collect_jail(item, driver):
    print('click_state_collect_jail')
    state = item[1]
    print(state)
    driver.execute_script(item[0])
    time.sleep(2)
    list_jail_href = []
    list_jail = []
    links = driver.find_elements_by_partial_link_text('')
    print(links)
    print(state)
    for link in links:
        list_link = link.get_attribute("href")
        if 'trac_fac_name_county' in list_link:
            list_jail_href.append(list_link[11:])
    print(list_jail_href)
    print(state)
    table_trs_jail = driver.find_elements_by_xpath("//div[contains(@id, 'col2') and contains(@class, 'scroll')]/table/tbody/tr")
    for tr_jail in table_trs_jail:
        td = tr_jail.find_elements_by_xpath(".//td")
        convert_jail = str(td[0].get_attribute("innerHTML").encode("UTF-8"))
        convert_jail = convert_jail.replace('/', ' ')
        convert_jail = convert_jail.replace('\'', ' ')
        item_split = re.findall('>([^\']*)<', convert_jail)
        if len(item_split) == 0:
            append_item = 'you need to check the name'
        else:
            append_item = item_split[0]
        list_jail.append(append_item)
    print('list_jail')
    print(state)
    print(list_jail)
    state = [state]*len(list_jail)
    jail_href = list(zip(list_jail_href[2:], list_jail,state))
    print(jail_href)
    for each_item in jail_href:
        processing_scrape(each_item,driver)


def processing_scrape(item,driver):
    print('processing_scrape')
    driver.execute_script(item[0])
    time.sleep(2)
    out_put = pd.DataFrame()
    table_trs = driver.find_elements_by_xpath("//div[contains(@id, 'col3') and contains(@class, 'scroll')]/table/tbody/tr")
    for tr in table_trs:
        td = tr.find_elements_by_xpath(".//td")
        convert_citizenship = str(td[0].get_attribute("innerHTML").encode("UTF-8"))
        item_split = re.findall('>([^\']*)<', convert_citizenship)
        convert_population = str(td[1].get_attribute("innerHTML").encode("UTF-8"))
        item_split_pop = re.findall('\'([^\']*)\'', convert_population)
        data = {'Citizenship': item_split[0], 'Population': item_split_pop[0]}
        out_put = out_put.append(data, ignore_index=True)
    out_put.to_csv(item[2] + '-' +item[1] + '.csv')
    time.sleep(2)


prepare_page()