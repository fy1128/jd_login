# -*- coding: utf-8 -*-
'''
Required
- requests
- selenium
Info
- author : "ying"
'''
import os,sys,time,random
import signal
import requests
import urllib, http.cookiejar
from selenium import webdriver
from PIL import Image

try:
    from pytesseract import image_to_string
except Exception as e:
    print('Module \'tesseract\' imported failed! '+str(e))

try:
    input = raw_input
except:
    pass
class TimeoutExpired(Exception):
    pass

try:
    import msvcrt
    
    def readInput(caption, default, timeout=10):
        start_time = time.time()
        sys.stdout.write('%s(%d秒自动跳过):' % (caption,timeout))
        sys.stdout.flush()
        input = ''
        while True:
            ini=msvcrt.kbhit()
            try:
                if ini:
                    chr = msvcrt.getche()
                    if ord(chr) == 13:  # enter_key
                        break
                    elif ord(chr) >= 32:
                        input += chr.decode()
            except Exception as e:
                pass
            if len(input) == 0 and time.time() - start_time > timeout:
                break
        print ('')  # needed to move to next line
        if len(input) > 0:
            return input+''
        else:
            return default
except:
    import signal
    def alarm_handler(signum, frame):
        raise TimeoutExpired

    def readInput(caption, default, timeout=10):
        # set signal handler
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(timeout) # produce SIGALRM in `timeout` seconds

        try:
            return input('%s(%d秒自动跳过):' % (caption,timeout))
        except:
            print(default)
            return default
        finally:
            signal.alarm(0) # cancel alarm

def get_userdata(file_url):
    data=[]
    with open(file_url,'r') as f1:
        flists=f1.readlines()
        for flist in flists:
            if flist[-1]=='\n':
                flist=flist[0:-1]
            if flist.strip() and (flist[0] != '#'):
                data.append(flist)
        data=tuple(data)
        return data

class JDlogin(object):
    def __init__(self,un,pw):
        USER_AGENT_LIST = [
                "Mozilla/5.0(WindowsNT6.3;WOW64;rv:47.0)Gecko/20100101Firefox/47.0",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
                "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", 
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",  
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",  
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",  
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",  
                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", 
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",  
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",  
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"  
               ]        
        self.headers = {'User-Agent':random.choice(USER_AGENT_LIST),
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate, sdch',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Connection':'keep-alive',
                        }
        self.session = requests.session()
        self.login_url = "http://passport.jd.com/uc/login"
        self.post_url = "https://passport.jd.com/uc/loginService"
        self.auth_url = "https://passport.jd.com/uc/showAuthCode"
        self.home_url = "http://home.jd.com/"
        self.un = un
        self.pw = pw

        dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
        dcap["phantomjs.page.settings.clearMemoryCaches"] = True
        dcap["phantomjs.page.customHeaders.accept"] = "*/*"
        dcap["phantomjs.page.customHeaders.Accept-Language"] = "en-US,en;q=0.7,zh;q=0.3"
        dcap["phantomjs.page.customHeaders.connection"] = "keep-alive"
        try:
            self.browser = webdriver.PhantomJS('phantomjs', desired_capabilities=dcap)
            self.browser.set_page_load_timeout(30)
        except Exception as e:
            print(e)

    def load_html(self, url):
        while True:
            if hasattr(self, 'browser'):
                try:
                    self.browser.get(url)
                    time.sleep(3)
                    return {'code': 'ok'}
                except Exception as e:
                    print(str(e))
                    print(time.ctime())
                    print("无法下载网页。1秒后重试...")
                    time.sleep(1)
            else:
                try:
                    self.browser = webdriver.PhantomJS('phantomjs', desired_capabilities=dcap)
                    self.browser.set_page_load_timeout(30)
                except Exception as e: 
                    return {'code': 'error', 'msg': str(e)}

    def to_cookielib_cookie(self, selenium_cookie):
        if 'domain' in selenium_cookie:
            domain = selenium_cookie['domain'].split('.')
            domain = '.' + '.'.join([domain[-2], domain[-1]])

        return http.cookiejar.Cookie(
            version=0,
            name=selenium_cookie['name'],
            value=selenium_cookie['value'],
            port='80',
            port_specified=False,
            domain=domain,
            domain_specified=True,
            domain_initial_dot=False,
            path=selenium_cookie['path'],
            path_specified=True,
            secure=selenium_cookie['secure'],
            expires=int(time.time() + 2592000),
            discard=False,
            comment=None,
            comment_url=None,
            rest=None,
            rfc2109=False
        )


    def put_cookies_in_jar(self, selenium_cookies, cookie_jar):
        for cookie in selenium_cookies:
            cookie_jar.set_cookie(self.to_cookielib_cookie(cookie))

    def cookie_update(self):
        print("\nAuto handle cookie in file, Mozilla Format ...");
        cookieJarFileMozilla = http.cookiejar.MozillaCookieJar('cookies/' + self.un + '.txt')
        print('Setting cookies ...')
        #requests.utils.cookiejar_from_dict({c.name: c.value for c in self.session.cookies}, cookieJarFileMozilla, True)
        self.put_cookies_in_jar(self.browser.get_cookies(), cookieJarFileMozilla)
        cookieJarFileMozilla.save('cookies/' + self.un + '.txt', ignore_expires=True, ignore_discard=True)
        print('\n######## ' + self.un + ' login complete ########\n')

    def login(self):
        '''
            登录
        '''
        print('\n######## ' + self.un + ' pending to login ########\n')
        login_test = None
        while login_test is None:
            try:
                authcode = ''
                resp = self.load_html(self.login_url)
                if resp['code'] == 'error':
                    print(resp['msg'])
                    break
                # set cookies from PhantomJS
                for cookie in self.browser.get_cookies():
                    self.session.cookies.set(cookie['name'], cookie['value'], domain='.jd.com', path='/')
                #self.session.cookies.update( {c['name']:c['value'] for c in self.browser.get_cookies()} )
                self.headers['Host'] = 'passport.jd.com'
                acRequired = self.session.post(self.auth_url, headers=self.headers, data={'loginName':self.un}, allow_redirects=False).text #返回({"verifycode":true})或({"verifycode":false})

                self.load_html(self.login_url)
                if resp['code'] == 'error':
                    print(resp['msg'])
                    break
                elem_login_tab = self.browser.find_element_by_xpath('//div[@class="login-tab login-tab-r"]')
                elem_login_tab.click()
                time.sleep(1)
                elem_user = self.browser.find_element_by_xpath('//*[@id="loginname"]')
                elem_user.clear()
                elem_user.send_keys(self.un)
                elem_pwd = self.browser.find_element_by_xpath('//*[@id="nloginpwd"]')
                elem_pwd.click()
                time.sleep(1)
                elem_pwd.send_keys(self.pw)
                if 'true' in acRequired:
                    # print('need authcode, plz find it and fill in ')
                    print('auth code required ... processing ...')
                    self.browser.save_screenshot('logs/screenshot.png')
                    self.browser.get_screenshot_as_file('logs/screenshot.png')
                    element = self.browser.find_element_by_id('JD_Verification1')
                    left = int(element.location['x'])
                    top = int(element.location['y'])
                    right = int(element.location['x'] + element.size['width'])
                    bottom = int(element.location['y'] + element.size['height'])
                    
                    im = Image.open('logs/screenshot.png')
                    im = im.crop((left, top, right, bottom))
                    im.save('logs/authcode.png')

                    if 'image_to_string' in globals():
                        authcode = image_to_string(Image.open('logs/authcode.png'))
                        print('auth code: '+authcode)
                        if len(authcode) != 4:
                            print('invalid auth code!')
                            continue
                    else:
                        authcode = input("plz enter authcode:")

                    elem_authcode = self.browser.find_element_by_xpath('//*[@id="authcode"]')
                    elem_authcode.send_keys(authcode)
                
                elem_sub = self.browser.find_element_by_xpath('//*[@id="loginsubmit"]')
                elem_sub.click()
                time.sleep(1)
                # set cookies from PhantomJS
                for cookie in self.browser.get_cookies():
                    self.session.cookies.set(cookie['name'], cookie['value'], domain='.jd.com', path='/')
                #self.session.cookies.update( {c['name']:c['value'] for c in self.browser.get_cookies()} )

                self.headers['Host'] = 'home.jd.com'
                home_page = self.session.get(self.home_url, headers=self.headers, timeout=30, allow_redirects=False)
                # 若状态码返回200，说明登录成功，登录失败继续重试到成功为止
                # 查看历史请求：home_page.history
                if home_page.status_code != 200 :
                    print('LOGIN FAILED! '+str(home_page.status_code)+' found, cookies is invalid.')
                    self.browser.save_screenshot('logs/screenshot_failed.png')
                    if 'dangerousVerify' in self.browser.current_url:
                        error_msg = self.browser.find_element_by_xpath('//div[@class="tip-box"]').text
                        print('ERROR: '+error_msg)
                        break
                    else:
                        error_msg = self.browser.find_element_by_xpath('//div[@class="msg-error"]').text
                        print('ERROR: '+error_msg)
                        #if '密码错误' in error_msg or '账户名不存在' in error_msg:
                        break
                    time.sleep(1)
                else:
                    print('LOGIN SUCCESS!')
                    self.cookie_update()
                    login_test = 1
            except Exception as e:
                print(e)
                pass

        try:
            self.browser.service.process.send_signal(signal.SIGTERM)
            self.browser.quit()
        except Exception as e:
            print(e)

if __name__=="__main__":
    x = readInput("Generate users' cookies automatically (Y/N) ? ", 'Y').upper()
    if x.upper() == 'N':
        username = input("plz enter username:")
        password = input("plz enter password:")
        JD = JDlogin(username,password)
        JD.login()
    elif x.upper() == 'Y':
        users = get_userdata('users.txt')
        if len(users) < 1:
            print('Users is empty!!')
            sys.exit()
        for u in users:
            u = u.split(' ')
            username = u[0]
            password = u[1]
            JD = JDlogin(username,password)
            JD.login()
    else:
        print('Invaild input detected!!')
