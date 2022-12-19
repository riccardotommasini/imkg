Scrapes memes. Usage outside of container possible, 
some abstraction and configuration options provided.

Crawlers available:
<pre>
KnowYourMeme
</pre>

Optional environment variables:
<pre>
SCRAPER_API_KEY
MONGO_URI
MONGO_DB
</pre>

`SCRAPER_API_KEY` Provides proxy for scraping.  
`MONGO_URI` Should contain the mongo daemon location.  
`MONGO_DB` Should contain the specific mongo database to use.  
Both mongo environment variables need to be set for it to be used.

Setup:  
`pip install -r requirements.txt`

To start crawling:  
`scrapy crawl <crawler>`

To store crawled data in a json file:  
`scrapy crawl <crawler> -o <filename>.json`
