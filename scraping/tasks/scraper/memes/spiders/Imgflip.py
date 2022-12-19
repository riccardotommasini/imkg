import scrapy
import re

class Imgflip(scrapy.Spider):
    name = "Imgflip"
    allowed_domains = ['imgflip.com']
    base_url = 'https://imgflip.com'
    start_urls = ['https://imgflip.com/memetemplates?sort=top-all-time']

    def parse_template_page(self, response):
        response.meta['instance_page'].meta['template_ID'] = \
            response.xpath('//p[contains(text(), "Template ID:")]/text()').get().removeprefix("Template ID: ")
        yield from self.parse_instances(response.meta['instance_page'])

    def parse_instances(self, response):
        next_page = response.xpath('//a[@class="pager-next l but"]/@href').get()
        for div in response.xpath('//div[@class="base-unit clearfix"]'):
            instance_url = div.xpath('.//h2/a/@href').get()
            instance_title = div.xpath('.//h2/a/text()').get()
            instance_author = div.xpath('.//a[@class="u-username"]/text()').get()
            instance_view_info = div.xpath('.//div[@class="base-view-count"]/text()').get()
            instance_view_count = match.group(1) if (match := re.search(r"(\S+) view", instance_view_info)) else 'NA'
            instance_upvote_count = match.group(1) if (match := re.search(r"(\S+) upvote", instance_view_info)) else 'NA'
            instance_comment_count = match.group(1) if (match := re.search(r"(\S+) comment", instance_view_info)) else 'NA'
            image_url = div.xpath('.//img[@class="base-img"]/@src').get()
            alt_text = div.xpath('.//img[@class="base-img"]/@alt').get()
            yield {
                'template_title': response.meta['title'],
                'template_ID': response.meta['template_ID'],
                'URL': instance_url,
                'title': instance_title,
                'author': instance_author,
                'view_count': instance_view_count,
                'upvote_count': instance_upvote_count,
                'comment_count': instance_comment_count,
                'image_url': image_url,
                'alt_text': alt_text
            }
        if next_page:
            yield response.follow(next_page, callback=self.parse_instances,
                                  meta=response.meta)

    def parse_initial(self, response: scrapy.http.Response):
        response.meta['title'] = response.xpath("//h1[@class='base-title']/text()").get().removeprefix(" › ")
        yield response.follow(
            response.xpath('//a[@class="meme-link"]/@href').get(),
            callback=self.parse_template_page,
            meta={'instance_page': response}
        )

    def parse(self, response: scrapy.http.Response, **_):
        yield from (scrapy.Request(self.base_url + path.get(), callback=self.parse_initial)
                    for path in response.xpath("//div[@class='mt-boxes']/div/h3/a/@href"))
        next_page = response.xpath('//a[@class="pager-next l but"]/@href').get()
        if next_page:
            yield response.follow(next_page)
