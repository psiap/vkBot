from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
from threading import Thread

class vkBot(object):
    def __init__(self,link,loginText,groupsLink,time_count,reposts,timePause):
        self.__driver = webdriver.Chrome()
        self.__link = link
        self.__loginText = loginText
        self.__groupsLink = groupsLink
        self.__time_count = float(time_count)
        self.__reposts = int(reposts)
        self.__timePause = float(timePause)

    def startBot(self):
        while(True):
            #Сыллки записей
            self.entering_clicking_through()
            for i in self.__loginText:
                self.__login = i.split(":")[0]
                self.__password = i.split(":")[1]
                #Показ логина
                self.loginPrint()
                #логин
                self.singUp()
                #Проверка и репост на стену
                self.making_reposts()
                #Выход с акаунта
                self.exitUp()
            os.system("cls")
            print("vkBot -- заснул на:",self.__timePause)
            time.sleep(self.__timePause)
        
    def singUp(self):
        try:
            self.__driver.maximize_window()
            self.__driver.get(self.__link)
            self.__driver.find_element_by_id("index_email").send_keys(self.__login)
            self.__driver.find_element_by_id("index_pass").send_keys(self.__password) 
            self.__driver.find_element_by_id("index_login_button").click()
            self.timeSleep()
            self.boxTitleCheck()
        except Exception:
            self.errorText("singUpBlock")

    def exitUp(self):
        self.__driver.get(self.__link)
        self.boxTitleCheck()
        self.timeSleep()
        self.__driver.find_element_by_id("top_profile_link").click()
        self.timeSleep()
        self.__driver.find_element_by_xpath('//*[text()="Выйти"]').click()
        self.timeSleep()

    def boxTitleCheck(self):
        try:
            titleCheck = self.__driver.find_element_by_xpath('//*[text()="Подумайте о безопасности своей страницы"]')
            if titleCheck:
                self.__driver.find_element_by_class_name("box_x_button").click()
        except Exception:
            print("\n")




    def entering_clicking_through(self):
        try:
            self.elemLinks = []
            for gLinks in self.__groupsLink:
                self.__driver.get(gLinks)
                for i in range(5):
                    self.__driver.find_element_by_tag_name('body').send_keys(Keys.END)
                    time.sleep(0.3)
                wallFind = self.__driver.find_elements_by_class_name("wall_item")
                for iWallFind in wallFind:
                    self.elemLinks.append("https://m.vk.com/wall?act=add&share_box=1&object=" + iWallFind.get_attribute("id"))
        except Exception:
            self.errorText("entering_clicking_throughBlock")
            

    def making_reposts(self):
        i = 0
        for iElemLinks in self.elemLinks:
            self.__driver.get(iElemLinks)
            print("URL - %s -: %s" % (i + 1,iElemLinks))
            self.timeSleep()
            try:
                if self.making_test():
                    self.__driver.find_element_by_class_name("Btn_theme_regular").click()
                    i+= 1
                    if i >= self.__reposts:
                        break
                self.elemLinks.remove(iElemLinks)
            except Exception:
                self.errorText("Btn_theme_regular")
            self.timeSleep()

    def making_test(self):
        count = 0
        try:
            self.__driver.find_element_by_xpath("//*[@class='mem_link']")
            count += 1
            print("link: брак: mem_link")
        except NoSuchElementException:
            print("link: норм")
        try:
            self.__driver.find_element_by_xpath('//*[text()="https"]')
            count += 1
            print("link: брак: https")
        except NoSuchElementException:
            print("link: норм")
        try:
            self.__driver.find_element_by_xpath("//*[@class='mail_link']")
            count += 1
            print("link: брак: mail_link")
        except NoSuchElementException:
            print("link: норм")
        try:
            self.__driver.find_element_by_xpath("//*[@class='medias_link_icon']")
            count += 1
            print("link: брак: medias_link_icon")
        except NoSuchElementException:
            print("link: норм")
        try:
            self.__driver.find_element_by_xpath("//*[@class='medias_link_thumbed']")
            count += 1
            print("link: брак: medias_link_thumbed")
        except NoSuchElementException:
            print("link: норм")
        if count == 0:
            return True
        else:
            return False




    def timeSleep(self):
        time.sleep(self.__time_count)
       
    def loginPrint(self):
        os.system("cls")
        print("vkBot  -- Login: %s | Password: %s | Links: %s\n\n" % (self.__login,self.__password,len(self.elemLinks)))

    def errorText(self,error):
        f2 = open('errorLog.txt', 'a')
        f2.write("ERROR: " + error + " " + time.ctime() + "\n")
        f2.close()

            
           




def loginText():
    f2 = open('login.txt', 'r')
    l = list([line.rstrip() for line in f2.readlines()])
    f2.close()
    return l

def groupsText():
    f2 = open('groups.txt', 'r')
    l = list([line.rstrip().replace("https://vk.com/","https://m.vk.com/") for line in f2.readlines()])
    f2.close()
    return l

def configText():
    f1 = open('config.txt', 'r')
    s = f1.readline()
    f1.close()
    return s.split(" ")

def main():
    sl_count = float(float(configText()[7]) * 60 * 60)
    g = vkBot(configText()[5],loginText(),groupsText(),configText()[1],configText()[3],sl_count)
    g.startBot()

if __name__ == "__main__":
    main()
