# scrawler
crawler based on scrapy

# 小说结构
小说以文件的形式组织

根目录: novel

每个小说一个目录，以小说为目录名称。

每个小说下有个meta.json 存储小说相关元数据。例如名称、作者、章节目录、类别。

每个章节一个文件。

# run
```shell
pip install scrapy-random-useragent
```
config `settings.py`
```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400
}
```
This disables the default UserAgentMiddleware and enables the RandomUserAgentMiddleware.

Then, create a new variable USER_AGENT_LIST with the path to your text file which has the list of all user-agents (one user-agent per line).
```python
USER_AGENT_LIST = "/path/to/useragents.txt"
```
