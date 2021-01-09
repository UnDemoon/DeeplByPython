'''
Author: Demoon
Date: 2021-01-09 14:17:03
LastEditTime: 2021-01-09 14:31:36
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \DeeplByPython\DeeplTrans.py
'''
import numpy as np
#   selenium相关
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class DeeplTrans:
    def __init__(self, show: bool = False):
        self.api_url = "https://www.deepl.com/translator"
        self.browser = self.browserInit(show)
        self.lang_type = [
                    'ZH',    # 中文
                    'EN',	 # 英文 美式
                    'DE',   # 德语
                    'FR',   # 法语
                    'ES',   # 西班牙语
                    'PT',   # 葡萄牙语
                    'IT',   # 意大利语
                    'NL',   # 荷兰语
                    'PL',   # 波兰语
                    'RU',   # 俄语
                    'JA',   # 日语
        ]

    '''
    description: 浏览器初始化
    param {bool} show 是否显示界面
    return {browser object}
    '''
    def browserInit(self, show: bool = False):
        # 实例化一个chrome浏览器
        chrome_options = webdriver.ChromeOptions()
        # options.add_argument(".\ChromePortable\App\Chrome\chrome.exe");
        chrome_options.binary_location = ".\\ChromePortable\\App\\Chrome\\chrome.exe"
        # chrome_options = webdriver.ChromeOptions()
        if not show:
            chrome_options.add_argument('--headless')   #   静默开启
            chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--headless')   #   静默开启
        # chrome_options.add_argument('--disable-gpu')
        # browser = webdriver.Chrome(options=chrome_options)
        browser = webdriver.Chrome(options=chrome_options)
        # 设置等待超时
        return browser

    '''
    description: 翻译
    param {str} 翻译内容
    param {str} 原类型
    param {str} 目标类型
    return {str} 目标内容
    '''
    def deeplTranslate(self, words: str, from_type: str, to_type: str):
        tr_url = self.api_url + "#{0}/{1}/{2}".format(from_type.lower(), to_type.lower(), words)
        wait = WebDriverWait(self.browser, 60)
        self.browser.set_page_load_timeout(100)
        try:
            self.browser.get(tr_url)
        except BaseException:
            # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
            self.browser.execute_script("window.stop()")
        # trans_flag表示翻译结果显示了，虽然和结果没什么关系
        trans_flag = wait.until_not(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.lmt__mobile_share_container.lmt__mobile_share_container--inactive')))
        output_area = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#target-dummydiv')))
        res = output_area.get_attribute('innerHTML')
        return res

    '''
    description:  翻译运行
    param {str} words  带翻译字符串
    return {str}
    '''
    def runTranslate(self, words: str):
        type_1, type_2 = np.random.choice(self.lang_type[1:], size=2, replace=False)  # 随机获取非中文两个类型
        step_1 = self.deeplTranslate(words, self.lang_type[0], type_1)
        step_2 = self.deeplTranslate(step_1, type_1, type_2)
        res = self.deeplTranslate(step_2, type_2, self.lang_type[0])
        return res
