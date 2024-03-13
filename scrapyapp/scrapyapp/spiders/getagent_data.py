from pathlib import Path
import scrapy
import time 
#193.5.93.76:443
class QuotesSpider(scrapy.Spider):
    name = "agent_data"

    def start_requests(self):
        urls = [
            "https://patentscope.wipo.int/search/en/resultWeeklyBrowse.jsf",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #import chompjs
        #import js2xml
        #javascript = response.css("script::text").get()
        #data = js2xml.parse(javascript)
        #print("javascriptjavascriptjavascrip   tjavascriptjavascriptjavascript",javascript,"javascript")
        #data = chompjs.parse_js_object(javascript)
        #print(data,"datadatadatadatadatadatadata")
        #print(js2xml.pretty_print(data))
        #for d in data:
        #    print(d)
        import requests
        url=requests.get('https://patentscope.wipo.int/search/en/resultWeeklyBrowse.jsf')
        data = []
        try:
            import json
            data = url.json() 
        except Exception as e:
            print(e,"error here")
        for i in data:
            print(i) 
        #print(response,"ressssponse response response",response.body)
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html" 
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")