# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
import requests
import json
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class MeituanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MeituanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleWare(object):
    # ip_path = r'C:\python_work\supcon\Proxy.json'

    # def process_request(self, request, spider):
    #     if spider.name == 'feizhu_crawl' or spider.name == 'ctrip_comments1' or spider.name == 'meituan_comments':
    #         host = settings['MYSQL_HOST']
    #         url = 'http://%s:5555/random' % host
    #         r = requests.get(url)
    #         ip = r.text.strip()
    #         print('当前使用的IP：', ip)
    #         request.meta['proxy'] = 'http://'+str(ip)

    ctime = 0

    def process_request(self, request, spider):
        if spider.name in ('meituanwaimai'):
            # 时间差
            time_subtract = time.time() - self.ctime
            # print('时间差为：：：：：：：：：：', time_subtract)
            if time_subtract > 30:
                host = settings['REMOTE_REDIS_HOST']
                url = 'http://%s:8787/random' % host
                r = requests.get(url)
                value = json.loads(r.text.strip())
                self.ip = value[0].replace('3222', '12123')
                self.ip = self.ip
                self.ctime = value[1]
                print('使用新IP：：：：：：：：：：：：：：', self.ip)
                # request.meta['proxy'] = 'http://' + 'peng:1234@' + self.ip
                request.meta['proxy'] = 'http://' + self.ip

            else:
                print('使用原IP：：：：：：：：：：：：', self.ip)
                request.meta['proxy'] = 'http://' + self.ip
