# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'


import re
import json
import orjson
from time import sleep

from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        站大爷 https://www.zdaye.com/dayProxy.html
        """
        start_url = "https://www.zdaye.com/dayProxy.html"
        html_tree = WebRequest().get(start_url, verify=False).tree
        latest_page_time = html_tree.xpath(
            "//span[@class='thread_time_info']/text()")[0].strip()
        from datetime import datetime
        interval = datetime.now() - datetime.strptime(latest_page_time, "%Y/%m/%d %H:%M:%S")
        if interval.seconds < 300:  # 只采集5分钟内的更新
            target_url = "https://www.zdaye.com/" + \
                html_tree.xpath(
                    "//h3[@class='thread_title']/a/@href")[0].strip()
            while target_url:
                _tree = WebRequest().get(target_url, verify=False).tree
                for tr in _tree.xpath("//table//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    yield "%s:%s" % (ip, port)
                next_page = _tree.xpath(
                    "//div[@class='page']/a[@title='下一页']/@href")
                target_url = "https://www.zdaye.com/" + \
                    next_page[0].strip() if next_page else False
                sleep(5)

    @staticmethod
    def freeProxy02():
        """
        代理66 http://www.66ip.cn/
        """
        url = "http://www.66ip.cn/"
        resp = WebRequest().get(url, timeout=10).tree
        for i, tr in enumerate(resp.xpath("(//table)[3]//tr")):
            if i > 0:
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy03():
        """ 开心代理 """
        target_urls = ["http://www.kxdaili.com/dailiip.html",
                       "http://www.kxdaili.com/dailiip/2/1.html"]
        for url in target_urls:
            tree = WebRequest().get(url).tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy04():
        """ FreeProxyList https://www.freeproxylists.net/zh/ """
        url = "https://www.freeproxylists.net/zh/?c=CN&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=50"
        tree = WebRequest().get(url, verify=False).tree
        from urllib import parse

        def parse_ip(input_str):
            html_str = parse.unquote(input_str)
            ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', html_str)
            return ips[0] if ips else None

        for tr in tree.xpath("//tr[@class='Odd']") + tree.xpath("//tr[@class='Even']"):
            ip = parse_ip("".join(tr.xpath('./td[1]/script/text()')).strip())
            port = "".join(tr.xpath('./td[2]/text()')).strip()
            if ip:
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy05(page_count=1):
        """ 快代理 https://www.kuaidaili.com """
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxy06():
        """ 冰凌代理 https://www.binglx.cn """
        url = "https://www.binglx.cn/?page=1"
        try:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy07():
        """ 云代理 """
        urls = ['http://www.ip3366.net/free/?stype=1',
                "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(
                r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy08():
        """ 小幻代理 """
        urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(
                r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy09(page_count=1):
        """ 免费代理库 """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = WebRequest().get(url, verify=False).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def freeProxy10():
        """ 89免费代理 """
        r = WebRequest().get("https://www.89ip.cn/index_1.html", timeout=10)
        proxies = re.findall(
            r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
            r.text)
        for proxy in proxies:
            yield ':'.join(proxy)

    @staticmethod
    def freeProxy11():
        """ 稻壳代理 https://www.docip.net/ """
        r = WebRequest().get("https://www.docip.net/data/free.json", timeout=10,
                             proxies={"http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
        try:
            for each in r.json['data']:
                yield each['ip']
        except Exception as e:
            print(e)

    @staticmethod
    def wallProxy01():
        """
        PzzQz https://pzzqz.com/
        """
        from requests import Session
        from lxml import etree
        session = Session()
        try:
            index_resp = session.get("https://pzzqz.com/", timeout=20, verify=False, proxies={
                                     "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"}).text
            x_csrf_token = re.findall('X-CSRFToken": "(.*?)"', index_resp)
            if x_csrf_token:
                data = {"http": "on", "ping": "3000",
                        "country": "cn", "ports": ""}
                proxy_resp = session.post("https://pzzqz.com/", verify=False,
                                          headers={"X-CSRFToken": x_csrf_token[0]}, json=data).json()
                tree = etree.HTML(proxy_resp["proxy_html"])
                for tr in tree.xpath("//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()"))
                    port = "".join(tr.xpath("./td[2]/text()"))
                    yield "%s:%s" % (ip, port)
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy12():
        """
        墙外网站 cn-proxy
        :return:
        """
        urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            proxies = re.findall(
                r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy13():
        """
        https://proxy-list.org/english/index.php
        :return:
        """
        urls = ['https://proxy-list.org/english/index.php?p=%s' %
                n for n in range(1, 10)]
        request = WebRequest()
        import base64
        for url in urls:
            r = request.get(url, timeout=10, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
            for proxy in proxies:
                yield base64.b64decode(proxy).decode()

    @staticmethod
    def freeProxy14():
        urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            proxies = re.findall(
                r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy15():
        url = "https://raw.githubusercontent.com/casals-ar/proxy-list/main/https"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy16():
        url = "https://raw.githubusercontent.com/parserpp/ip_ports/main/proxyinfo.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy17():
        url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr.replace("http://")
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy18():

        url = "https://raw.githubusercontent.com/arunsakthivel96/proxyBEE/master/proxy.list"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for line in r.text.split("\n"):
                if len(line):
                    line_json = orjson.loads(line)
                    if line_json.get("host") and line_json.get("port"):
                        yield f"{line_json.get('host')}:{line_json.get('port')}"
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy19():
        url = "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy20():
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"https://checkerproxy.net/api/archive/{today}"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            checkproxy_list = orjson.loads(r.text)
            for proxy_datum in checkproxy_list:
                addr = proxy_datum.get("addr")
                if addr:
                    yield addr

        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy21():
        url = "https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr[:addr.rfind(':')]
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy22():
        url = "https://raw.githubusercontent.com/themiralay/Proxy-List-World/master/data.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy23():
        url = "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy24():
        url = "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt"
        request = WebRequest()
        pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$'
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                matcher = re.match(pattern, addr)
                if matcher:
                    yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy25():
        url = "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/https.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy26():
        url = "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/http.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy27():
        url = "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/unknown.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy28():
        url = "https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/http.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy29():
        url = "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/http/global/http_checked.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy30():
        url = "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy31():
        url = "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy32():
        url = "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy33():
        url = "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy34():
        url = "https://raw.githubusercontent.com/im-razvan/proxy_list/main/http.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy35():
        url = "https://raw.githubusercontent.com/NotUnko/autoproxies/main/proxies/https"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy36():
        url = "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy37():
        url = "https://raw.githubusercontent.com/j0rd1s3rr4n0/api/main/proxy/http.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy38():
        url = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
        request = WebRequest()
        try:
            r = request.get(url, timeout=20, proxies={
                            "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
            for addr in r.text.split("\n"):
                yield addr
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy39():
        yield "127.0.0.1:20172"

    @staticmethod
    def freeProxy40():
        # all

        import asyncio
        import aiohttp

        urls_list = ['https://proxy.ionssource.cn','http://139.162.78.207:5050', 'http://172.104.79.56:5050', 'http://106.75.230.47:5000', 'http://14.103.27.255:5010', 'http://124.71.176.96:5010', 'http://111.229.236.207:5010', 'http://43.143.58.28:5010', 'http://118.31.185.215:9042', 'http://120.132.146.118:25010', 'http://43.134.224.107:5010', 'http://154.23.125.114:5010', 'http://154.39.175.145:5010', 'http://154.39.177.179:5010', 'http://154.39.171.132:5010', 'http://154.39.177.163:5010', 'http://154.23.125.115:5010', 'http://154.39.175.168:5010', 'http://154.39.171.137:5010', 'http://154.39.177.182:5010', 'http://154.39.177.175:5010', 'http://154.39.171.145:5010', 'http://154.39.171.161:5010', 'http://154.39.177.139:5010', 'http://154.39.177.138:5010', 'http://154.39.171.151:5010', 'http://154.39.177.145:5010', 'http://154.39.177.134:5010', 'http://154.39.171.164:5010', 'http://154.39.175.163:5010', 'http://154.39.175.169:5010', 'http://154.39.173.180:5010', 'http://154.39.175.170:5010', 'http://154.39.177.151:5010', 'http://154.39.175.167:5010', 'http://154.39.171.167:5010', 'http://154.39.175.149:5010', 'http://154.39.175.172:5010', 'http://154.39.175.174:5010', 'http://154.39.175.156:5010', 'http://154.39.175.132:5010', 'http://154.39.175.157:5010', 'http://154.39.175.135:5010', 'http://154.39.175.150:5010', 'http://154.39.177.176:5010', 'http://154.39.171.143:5010', 'http://154.39.177.168:5010', 'http://154.39.175.152:5010', 'http://154.39.175.142:5010', 'http://154.39.175.179:5010', 'http://154.39.175.176:5010', 'http://154.39.171.172:5010', 'http://154.39.177.153:5010', 'http://154.39.177.187:5010', 'http://wbsubdomain.a.bb.ccc.dddd.mdapp.store:5010', 'http://bb.ccc.dddd.mdapp.store:5010', 'http://ccc.dddd.mdapp.store:5010', 'http://website.mdapp.store:5010', 'http://43.140.214.29:5010', 'http://42.193.159.44:5010', 'http://154.39.175.171:5010', 'http://154.39.177.136:5010', 'http://154.39.171.156:5010', 'http://154.39.177.159:5010', 'http://154.39.171.134:5010', 'http://proxy.waiting8.com', 'http://154.39.175.147:5010', 'http://154.39.177.149:5010', 'http://154.39.175.130:5010', 'http://154.39.175.154:5010', 'http://154.39.175.159:5010', 'http://154.39.171.152:5010', 'http://154.39.171.159:5010', 'http://154.39.177.148:5010', 'http://154.39.177.155:5010', 'http://154.39.177.146:5010', 'http://154.39.175.133:5010', 'http://154.39.177.170:5010', 'http://154.39.175.187:5010', 'http://154.39.175.140:5010', 'http://154.39.175.188:5010', 'http://154.39.171.178:5010', 'http://szyy78585.mdapp.store:5010', 'http://154.39.175.161:5010', 'http://154.39.175.182:5010', 'http://154.39.177.174:5010', 'http://154.39.171.160:5010', 'http://154.23.125.117:5010', 'http://154.39.177.166:5010', 'http://154.39.171.146:5010', 'http://154.39.177.158:5010', 'http://154.39.171.144:5010', 'http://154.39.175.173:5010', 'http://154.39.177.131:5010', 'http://154.39.177.137:5010', 'http://154.39.175.136:5010', 'http://154.39.177.185:5010', 'http://154.39.177.154:5010', 'http://154.39.173.188:5010', 'http://101.42.232.45:5010', 'http://154.39.171.180:5010', 'http://154.39.177.186:5010',
                     'http://154.39.177.161:5010', 'http://154.39.175.158:5010', 'http://154.39.177.141:5010', 'http://110.42.210.247:5010', 'http://154.39.171.182:5010', 'http://154.39.177.190:5010', 'http://154.39.171.170:5010', 'http://154.39.177.180:5010', 'http://154.39.173.137:5010', 'http://154.39.177.143:5010', 'http://154.39.177.142:5010', 'http://154.39.177.162:5010', 'http://154.39.177.152:5010', 'http://154.39.175.148:5010', 'http://154.39.177.144:5010', 'http://154.39.173.152:5010', 'http://154.39.171.165:5010', 'http://154.39.175.144:5010', 'http://154.39.177.178:5010', 'http://154.39.173.150:5010', 'http://154.39.177.140:5010', 'http://what.website.mdapp.store:5010', 'http://154.39.177.156:5010', 'http://154.39.171.171:5010', 'http://154.39.177.167:5010', 'http://154.39.177.165:5010', 'http://124.70.135.145:5010', 'http://154.39.175.164:5010', 'http://154.39.175.165:5010', 'http://154.39.175.143:5010', 'http://154.39.173.165:5010', 'http://154.39.175.160:5010', 'http://154.39.171.175:5010', 'http://154.39.175.141:5010', 'http://154.39.175.151:5010', 'http://154.39.171.130:5010', 'http://154.39.171.166:5010', 'http://154.39.175.146:5010', 'http://154.39.177.184:5010', 'http://154.39.177.157:5010', 'http://154.39.171.184:5010', 'http://154.39.177.147:5010', 'http://154.39.171.187:5010', 'http://154.39.171.168:5010', 'http://154.39.173.166:5010', 'http://154.39.175.186:5010', 'http://154.39.171.150:5010', 'http://154.39.177.169:5010', 'http://154.39.175.131:5010', 'http://154.39.177.130:5010', 'http://154.39.177.183:5010', 'http://47.106.153.111:5010', 'http://a.bb.ccc.dddd.mdapp.store:5010', 'http://154.39.171.148:5010', 'http://154.39.171.154:5010', 'http://154.39.171.188:5010', 'http://154.39.171.157:5010', 'http://154.39.175.184:5010', 'http://154.39.177.173:5010', 'http://154.39.177.164:5010', 'http://154.39.171.135:5010', 'http://154.39.175.162:5010', 'http://154.39.177.133:5010', 'http://154.39.171.169:5010', 'http://154.39.177.177:5010', 'http://154.39.175.177:5010', 'http://154.39.171.158:5010', 'http://154.39.173.155:5010', 'http://155.94.141.245:5010', 'http://154.39.175.189:5010', 'http://154.39.177.132:5010', 'http://64.176.45.28:5010', 'http://154.39.175.180:5010', 'http://154.39.177.135:5010', 'http://dddd.mdapp.store:5010', 'http://154.39.173.135:5010', 'http://154.39.171.131:5010', 'http://8.131.255.184:9301', 'http://154.39.171.153:5010', 'http://154.39.171.155:5010', 'http://154.39.175.175:5010', 'http://154.39.171.136:5010', 'http://43.142.175.53:5010', 'https://proxy.aivvm.com', 'http://82.156.28.207:3000', 'http://114.55.73.183:5020', 'http://47.109.102.107:5010', 'http://154.39.177.150:5010', 'http://154.39.171.149:5010', 'http://154.39.177.181:5010', 'http://154.39.171.176:5010', 'http://154.39.175.139:5010', 'http://154.39.175.134:5010', 'http://154.39.171.179:5010', 'http://154.39.175.178:5010', 'http://154.39.177.188:5010', 'http://154.39.171.173:5010', 'http://154.39.173.138:5010', 'http://154.39.171.141:5010', 'http://154.39.175.183:5010', 'http://154.39.171.142:5010', 'https://iproxy.omycloud.site']

        results_set = set()

        async def getter(results_queue, worker_size, func, *para, **kwarg):
            try:
                inspect
            except NameError:
                import inspect

            get_off_work_counter = worker_size
            while True:
                result = await results_queue.get()
                if not result:
                    get_off_work_counter -= 1
                    if not get_off_work_counter:
                        break
                    continue
                if inspect.iscoroutinefunction(func):
                    await func(result, *para, **kwarg)
                else:
                    func(result, *para, **kwarg)
            print("getter jobs done")

        async def assigner(tasks_queue, some_list, worker_size):
            for i in some_list:
                await tasks_queue.put(i)
            for i in range(worker_size):
                await tasks_queue.put(None)
            print("assigner jobs done")

        async def worker(tasks_queue, results_queue, func, *para, **kwarg):
            """
            func cannot return None or False. It has to return something
            """
            try:
                inspect
            except NameError:
                import inspect

            while True:

                task = await tasks_queue.get()
                if not task:
                    break
                if inspect.iscoroutinefunction(func):
                    result = await func(task, *para, **kwarg)
                else:
                    result = func(task, *para, **kwarg)

                await results_queue.put(result)

            await results_queue.put(None)
            print("a worker has done his job.")

        async def fetch_addr_from_web(url, session: aiohttp.ClientSession):
            try:
                print(f"fetching {url}")
                page_json = None
                async with session.get(f"{url}/all?type=https", timeout=5) as resp:
                    page_json = orjson.loads(await resp.text())
                    result_list = []
                    for items in page_json:
                        if "2024" not in items.get("last_time"):
                            return []
                        result_list.append(items.get("proxy"))
                    print(f"{url}...ok")
                    return result_list
            except:
                return []

        async def main():
            worker_size = 200
            tasks_queue = asyncio.Queue()
            results_queue = asyncio.Queue()
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                workers = [asyncio.create_task(worker(tasks_queue,
                                                      results_queue,
                                                      fetch_addr_from_web,
                                                      session)) for _ in range(worker_size)]
                await asyncio.gather(assigner(tasks_queue, urls_list, worker_size),
                                     getter(results_queue, worker_size,
                                            lambda x: results_set.update(x)),
                                     *workers)

        asyncio.run(main())

        for url in results_set:
            yield url

    @staticmethod
    def freeProxy41():
        # 40 with proxy
        urls_list = [
            "http://154.39.175.152:5010/all/?type=https",

        ]
        urls = set(urls_list)
        request = WebRequest()
        for url in urls:
            try:
                r = request.get(url, timeout=20, proxies={
                                "http": "http://127.0.0.1:20172", "https": "http://127.0.0.1:20172"})
                for item in orjson.loads(r.text):
                    if item.get("proxy"):
                        yield item.get("proxy")
            except Exception as e:
                print(e)

    @staticmethod
    def freeProxy42():
        # loop version
        urls_list = [
            "http://49.232.89.183:5010",
            "http://119.3.210.77:5008",
            "http://101.37.170.16:5010",
            'http://www.datasharehome.com:8080', 
            'http://154.39.175.163:5010', 
            'http://154.39.177.169:5010', 
            'http://47.110.14.149:5010', 
            'http://172.105.115.117:5050', 
            'http://demo.spiderpy.cn', 
            'http://154.39.171.179:5010', 
            'http://64.176.45.28:5010', 
            'http://150.158.84.84:5010',
            'http://101.43.48.164', 
            'http://101.69.246.174:5010',
            "http://101.34.84.62"

        ]
        urls = set(urls_list)
        request = WebRequest()
        for url in urls:
            try:
                for _ in range(30):
                    r = request.get(f"{url}/get/?type=https", timeout=20)
                    if not r.text.startswith('{'):
                        yield r.text
                    else:
                        item = orjson.loads(r.text)
                        if item.get("proxy"):
                            yield item.get("proxy")

            except Exception as e:
                print(e)

    @staticmethod
    def freeProxy43():
        # get_all
        urls_list = ['http://106.15.198.89:5010', 'http://47.118.50.237:5010', 'http://47.98.59.88', 'http://159.75.3.90:5010', 'http://82.157.26.36:5010', 'http://49.232.165.126:5010', 'http://47.106.94.116:5010',
                     'http://47.93.15.215:5010', 'http://49.232.89.183:5010', 'http://119.3.210.77:5009', 'http://119.3.210.77:5008', 'http://106.55.27.198:5010', 'http://119.254.86.251:5010', 'http://54.169.77.139:5010', 'http://42.192.2.74:5010']
        urls = set(urls_list)
        request = WebRequest()
        for url in urls:
            try:
                r = request.get(f"{url}/get_all/?type=https", timeout=20)
                for item in orjson.loads(r.text):
                    yield item["proxy"]
            except Exception as e:
                print(e)

    @staticmethod
    def freeProxy44():
        # get_all
        urls_list = [
            "http://101.132.182.78:500"
        ]
        urls = set(urls_list)
        request = WebRequest()
        for url in urls:
            try:
                r = request.get(f"{url}/get_all/?type=https", timeout=20)
                for item in orjson.loads(r.text):
                    yield item
            except Exception as e:
                print(e)

if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy06():
        print(_)

# http://nntime.com/proxy-list-01.htm
