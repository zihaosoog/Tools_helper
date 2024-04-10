import bibtexparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib import parse
import math
from time import sleep

from bs4 import BeautifulSoup
import re

class GG_Bibtex(object):
    def __init__(self, driver_path, gg_search_url):
        self.driver = None
        self.paper_names = []
        self.gg_search_url = gg_search_url
        self.driver_path = driver_path
        self.reset(driver_path)

    def reset(self, driver_path):
        self.service = Service(driver_path) 
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')  # no show window
        self.driver = webdriver.Chrome(service=self.service, options=option)
        self.driver.set_window_size(800,800)
        
    def get_bibtex_for_title(self, paper_title, elements_xpath):
        # elements_xpath = {
        #     'qoute_btn':'/html/body/div/div[10]/div[2]/div[3]/div[2]/div/div[2]/div[5]/a[2]/span',
        #     # 'qoute_btn':'/html/body/div/div[10]/div[2]/div[3]/div[2]/div[1]/div[2]/div[3]/a[2]/span',
        #     'bibtex_btn':'/html/body/div/div[4]/div/div[2]/div/div[2]/a[1]',
        #     'bib_text':'/html/body/pre'
        # }
        strto_pn=parse.quote(paper_title)
        url = self.gg_search_url + strto_pn
        self.driver.get(url)
        qoute_btn = WebDriverWait(self.driver, 30, 0.1).until(
                            EC.presence_of_element_located((By.XPATH, elements_xpath['qoute_btn']))
                            )
        qoute_btn.click()

        bibtex_btn = WebDriverWait(self.driver, 30, 0.1).until(
                            EC.presence_of_element_located((By.XPATH, elements_xpath['bibtex_btn']))
                            )
        bibtex_btn.click()

        bib_text = WebDriverWait(self.driver, 30, 0.1).until(
                            EC.presence_of_element_located((By.XPATH, elements_xpath['bib_text']))
                            )
        bib_text = bib_text.text
        return bib_text
    
    def _quit_driver(self, ):
        self.driver.quit()
        self.service.stop()

    # def get_search_titles(self, paper_title):
    #     """
    #     获取搜索结果中与输入标题一致的搜索结果的引用按钮的 xpath。

    #     Args:
    #         paper_title: 输入的论文标题。

    #     Returns:
    #         一个列表，其中包含与输入标题一致的搜索结果的引用按钮的 xpath。
    #     """

    #     # 将输入标题转换为小写。
    #     paper_title_lower = paper_title.lower()

    #     # 搜索结果可能有多个，因此使用 `//` 匹配所有结果。
    #     search_results = self.driver.find_elements(By.XPATH, "//div[@class='gs_r gs_or gs_scl']")

    #     # 遍历搜索结果。
    #     for search_result in search_results:

    #         # 获取搜索结果的标题。
    #         result_title = search_result.find_element_by_xpath(".//h3[@class='gs_rt']").text

    #         # 将搜索结果的标题转换为小写。
    #         result_title_lower = result_title.lower()

    #         # 如果搜索结果的标题与输入标题一致，则返回其引用按钮的 xpath。
    #         if result_title_lower == paper_title_lower:
    #             return search_result.find_element_by_xpath(".//a[@class='gs_citi']").get_attribute("href")

    #     # 如果没有找到与输入标题一致的搜索结果，则返回空列表。
    #     return []


    def get_search_titles(self, paper_title):
        # 构建谷歌学术搜索链接
        strto_pn=parse.quote(paper_title)
        url = self.gg_search_url + strto_pn
        self.driver.get(url)
        all_sea_res = '#gs_res_ccl_mid > div:nth-child(1) > div.gs_ri > div.gs_fl.gs_flb > a.gs_or_cit.gs_or_btn.gs_nph > span'
        # 等待页面加载
        WebDriverWait(self.driver, 50, 0.1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, all_sea_res))
        )
        
        # 获取页面内容
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取文献标题
        titles = []
        for item in soup.find_all('div', class_='gs_r'):
            h3 = item.find('h3', class_='gs_rt')
            if h3:
                title = h3.get_text()
                titles.append(title)
        # print(titles)
        # 忽略大小写，只比较字母是否相同
        # print(len(titles))
        if len(titles)>1:
            for idx, title in enumerate(titles):
                # print(paper_title.lower())
                # print(title.lower())
                if re.fullmatch(re.escape(paper_title), title, flags=re.IGNORECASE):
                    return len(titles), idx+1
                elif paper_title.lower() in title.lower():
                    return len(titles), idx+1
                else: 
                    pass
        return len(titles), 0
    

    def get_bib_text(self, paper_title):

        elements_xpath = {
            # 'qoute_btn':'/html/body/div/div[10]/div[2]/div[3]/div[2]/div/div[2]/div[5]/a[2]/span',
            # 'qoute_btn':'/html/body/div/div[10]/div[2]/div[3]/div[2]/div[1]/div[2]/div[3]/a[2]/span',
            'bibtex_btn':'/html/body/div/div[4]/div/div[2]/div/div[2]/a[1]',
            'bib_text':'/html/body/pre'
        }
        # if idx==0:
        #     elements_xpath = {
        #         # 'qoute_btn':'/html/body/div/div[10]/div[2]/div[3]/div[2]/div/div[2]/div[5]/a[2]/span',
        #         'qoute_btn':'/html/body/div/div[10]/div[2]/div[3]/div[2]/div[1]/div[2]/div[3]/a[2]/span',
        #         'bibtex_btn':'/html/body/div/div[4]/div/div[2]/div/div[2]/a[1]',
        #         'bib_text':'/html/body/pre'
        #     }
        # else:
        #     elements_xpath = {
        #         'qoute_btn':'/html/body/div/div[10]/div[2]/div[3]/div[2]/div/div[2]/div[5]/a[2]/span',
        #         # 'qoute_btn':'/html/body/div/div[10]/div[2]/div[3]/div[2]/div[1]/div[2]/div[3]/a[2]/span',
        #         'bibtex_btn':'/html/body/div/div[4]/div/div[2]/div/div[2]/a[1]',
        #         'bib_text':'/html/body/pre'
        #     }/html/body/div/div[10]/div[2]/div[3]/div[2]/div/div[2]/div[5]/a[2]/span
        # 获取搜索结果的标题列表
        len_res, idx_res = self.get_search_titles(paper_title)
        # print(len_res, idx_res)
        if len_res>1:
            elements_xpath['qoute_btn'] = f'/html/body/div/div[10]/div[2]/div[3]/div[2]/div[{idx_res}]/div[2]/div[3]/a[2]/span'
            elements_xpath['qoute_btn'] = f'/html/body/div/div[10]/div[2]/div[3]/div[2]/div[{idx_res}]/div/div[3]/a[2]/span'
        else:
            elements_xpath['qoute_btn'] = '/html/body/div/div[10]/div[2]/div[3]/div[2]/div/div[2]/div[5]/a[2]/span'
            elements_xpath['qoute_btn'] = '/html/body/div/div[10]/div[2]/div[3]/div[2]/div/div/div[5]/a[2]/span'
            # elements_xpath['qoute_btn'] = '/html/body/div/div[10]/div[2]/div[3]/div[2]/div/div[2]/div[3]/a[2]/span'

                                          
            
        bibtex = self.get_bibtex_for_title(paper_title, elements_xpath)
        return bibtex
        print(titles)

        if len(titles)>1:
            for title in titles:
                bibtex = self.get_bibtex_for_title(title, elements_xpath)  # 假设这个函数可以获取BibTeX引用
                if bibtex:
                    return bibtex
                else:
            # 如果未找到匹配的标题，返回None或一个默认值
                    return None
        else:
            bibtex = self.get_bibtex_for_title(title, elements_xpath)  # 假设这个函数可以获取BibTeX引用
            return bibtex
        
        # 遍历标题列表，检查每个标题是否与输入的标题匹配


    # ...


    def results_writter(self, results, output_file_path = 'output.txt'):
        wtf = []
        for re_key in results.keys():
            context = results[re_key]
            # wtf.append(re_key + '\n')
            wtf.append(context + '\n\n')
        with open(output_file_path, 'w') as f:
            f.writelines(wtf)

    def run(self, paper_names, output_file_path, reset_len = 100):
        """
        @params:
            paper_names: [LIST], your paper names.
            reset_len: [INT], for avoid the robot checking, you need to reset the driver for more times, default is 10 papers
        """
        self.paper_names = paper_names
        paper_len = len(paper_names)
        rest = paper_len % reset_len
        task_packs = []
        if paper_len > reset_len:
            groups_len = int(math.floor(paper_len / reset_len)) # 21/20 = 1
            for i in range(groups_len):
                sub_names = paper_names[(i)*reset_len:(i+1)*reset_len]
                task_packs.append(sub_names)
        
        task_packs.append(paper_names[-1*rest:])
        results = {}
        for ti in task_packs:
            for idx, pn in enumerate(ti):
                if len(pn) < 3:
                    continue
                print('\n---> Searching paper: {} ---> \n'.format(pn))                    
                bibtex = self.get_bib_text(pn)
                print(bibtex)
                results[pn] = bibtex

            self._quit_driver()
            sleep(10)
            self.reset(self.driver_path)
            print('-'*10+'\n Reset for avoiding robot check')

        self.results_writter(results, output_file_path)
        return results
                    

if __name__ == "__main__":
    driver_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    input_file_path = r'E:\BaiduSyncdisk\Paper_SCI\BIT-thesis-template-grd\reference\titles2.txt'
    output_file_path = r'E:\BaiduSyncdisk\Paper_SCI\BIT-thesis-template-grd\reference\output2.txt'

    # gg_search_url = r'https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&q='
    gg_search_url = r'https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q='
    ggb = GG_Bibtex(driver_path = driver_path, gg_search_url = gg_search_url)
    paper_names = []
    with open(input_file_path, 'r', encoding='utf-8') as f:
        paper_names = f.readlines()
        paper_names = [pn.replace('\n', '') for pn in paper_names]
    results = ggb.run(paper_names = paper_names, output_file_path = output_file_path)



#gs_res_ccl_mid > div:nth-child(1) > div.gs_ri > div.gs_fl.gs_flb > a.gs_or_cit.gs_or_btn.gs_nph > span
#gs_res_ccl_mid > div:nth-child(1) > div.gs_ri > div.gs_fl.gs_flb > a.gs_or_cit.gs_or_btn.gs_nph > span