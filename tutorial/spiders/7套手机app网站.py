import scrapy
import os
from urllib.parse import unquote
import re
class QuotesSpider(scrapy.Spider):
    name = "7套手机app网站"
    prefix="http://view.jqueryfuns.com/%E9%A2%84%E8%A7%88-/2018/9/13/108bfb8847bb89ae55db779a8fc87a1b/"
    # start_urls = ['http://view.jqueryfuns.com/%E9%A2%84%E8%A7%88-/2018/9/13/108bfb8847bb89ae55db779a8fc87a1b/',]
    def start_requests(self):
        yield scrapy.Request(url=QuotesSpider.prefix, callback=self.parse)

    def save(self,response,filename):
        # 保存当前文件
        if len(filename)==0 or filename[-1] == "/":
            filename=filename+"index.html"
        path="爬取的数据/%s/%s" %(self.name,filename)
        try:
            os.makedirs(path)
            os.rmdir(path)
        except:
            pass
        with open(path,"wb") as f:
            f.write(response.body)

    def getFileName(self,url):
        t1 = unquote(self.prefix)
        t2 = unquote(url)
        if t2[:len(t1)] == t1:
            return t2[len(t1):]
        else:
            return None

    def parse(self, response):
        filename=self.getFileName(response.url)
        if filename!=None:
            self.save(response,filename)
            # 枚举background
            bgimgs = re.findall("background-image:url\([\w\/\.]*\)", str(response.body))
            for img in bgimgs:
                img=img.split("(")[1].split(")")[0]
                yield response.follow(img,callback=self.parse)
            # 枚举 link
            for link in response.css("link"):
                yield response.follow(link, callback=self.parse)
            # 枚举script
            for src in response.css("script::attr('src')").extract():
                yield response.follow(src, callback=self.parse)
                yield {"script": src}
            # 枚举 img
            for src in response.css("img::attr('src')").extract():
                yield response.follow(src, callback=self.parse)
            # 枚举 a
            for a in response.css("a"):
                yield response.follow(a, callback=self.parse)
        else:
            yield {"prefix_do_not_match":response.url}
