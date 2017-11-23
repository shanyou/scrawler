from scrapy import cmdline
#cmdline.execute("scrapy crawl quanben -a start_urls=http://quanben.io/n/jipinxiuzhenxieshao/".split())
# cmdline.execute("scrapy crawl quanben -a start_urls=http://quanben.io/n/jipinxiuzhenxieshao/list.html".split())

cmdline.execute("scrapy crawl qidian -a start_urls=https://book.qidian.com/info/1004962432".split())