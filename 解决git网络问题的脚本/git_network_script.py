# -*- coding: utf-8 -*-

from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import yaml
import os
import subprocess

class GitRewriteHosts(object):
    def __init__(self, yaml_path):
        self.params = self.get_params(yaml_path)

    def get_params(self, yaml_path):
        print('解析yaml文件...')
        try:
            # 从.yaml文件中解析url参数
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                # print(data) 
        except Exception as e:
            print('解析yaml文件失败')
            print(e)
            return
        print('解析完成')
        return data

    def get_ip(self):
        # 拼接url
        url1 = os.path.join(self.params['IP_address_tool_url'], self.params['git_url'][0])
        url2 = os.path.join(self.params['IP_address_tool_url'], self.params['git_url'][1])
        print(url1, url2)
        print('请求网络数据...')

        # Edge driver
        options = EdgeOptions()

        options.add_argument('--headless') # 开启无界面模式
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度

        driver = Edge(options=options)

        driver.get(url1)
        # 通过selector定位
        Ip1 = WebDriverWait(driver, 6).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#tabpanel-dns-a > pre > a'))
    ).text
        
        driver.get(url2)
        # 通过selector定位
        Ip2 = WebDriverWait(driver, 6).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#tabpanel-dns-a > pre > a'))
    ).text
        
        driver.close()
    
        return Ip1, Ip2

    def backup_hosts(self):
        # print(f'copy {self.params["host_file_path"]} {os.path.join(self.params["host_file_root"], "hosts_bak")}')
        # 备份hosts文件
        with open(self.params["host_file_path"], 'r') as f:
            with open(os.path.join(self.params["host_file_root"], "hosts_bak"), 'w') as g:
                g.write(f.read())
                print('备份hosts文件完成')
            g.close()
        f.close()

    def rewrite_hosts(self, Ip1, Ip2):
        # 写入hosts文件
        with open(self.params["host_file_path"], 'w') as f:
            f.write(Ip1 + ' ' + f'{self.params["git_url"][0]}\n')
            f.write(Ip2 + ' ' + f'{self.params["git_url"][1]}\n')
            print('写入hosts文件完成')

    def test_baidu(self):
        # ping baidu.com 测试
        try:
            subprocess.run(['ping', 'baidu.com'], timeout=10, check=True)
            print("Ping successful")
            return True
        except subprocess.TimeoutExpired:
            print("Ping timed out")
            return False
        except subprocess.CalledProcessError:
            print("Ping failed")
            return False

    def test_git(self):
        # ping github.com 测试
        try:
            subprocess.run(['ping', 'github.com'], timeout=10, check=True)
            print("Ping successful")
            return True
        except subprocess.TimeoutExpired:
            print("Ping timed out")
            return False
        except subprocess.CalledProcessError:
            print("Ping failed")
            return False

    def run(self):
        # 首先测试网络条件是否可用
        print('测试网络是否可用...')
        if self.test_baidu():
            print('网络正常')
        else:
            print('网络不可用，请检查网络配置')
            return
        
        # 测试git是否可用
        print('测试git是否可用...')
        if self.test_git():
            print('git 连接正常，暂无需配置')
            c = input('是否仍进行配置（y/n）?按任意键继续...')
            while c != 'y' and c != 'n':
                c = input('是否仍进行配置（y/n）?按任意键继续...')
            if c == 'n':
                return
        else:
            print('git 连接不可用，开始覆写hosts文件')

        # 网络环境正常且git不可用，开始覆写hosts文件
        try:
            Ip1, Ip2 = self.get_ip()
        # 遇到
        except Exception as e:
            print('获取IP失败，请检查梯子')
            print(e)
            return
        
        print('备份hosts文件...')
        self.backup_hosts()
        print('覆写hosts文件...')
        self.rewrite_hosts(Ip1, Ip2)
        print('刷新DNS配置...')
        os.system('ipconfig /flushdns')
        print('测试...')
        if self.test_git():
            print('测试成功')
        else:
            print('测试失败')

        # 等待，按任意键退出
        input('\n按Enter退出...')


yaml_path = 'cfg.yaml'
agent = GitRewriteHosts(yaml_path)
agent.run()
    
    
