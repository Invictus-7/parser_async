import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_links = response.css(
            'section[id=numerical-index] tbody a::attr(href)'
        )
        for link in pep_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        # получаем заголовок PEP
        header = response.xpath('//*[@class="page-title"]/text()').get()
        # получаем из заголовка номер PEP
        pep_number = header.split('-')[0].replace('PEP', '').strip()
        # извлекаем из заголовка название PEP
        pep_name = header.split('–')[1].strip()
        # извлекаем статус PEP
        pep_status = response.css('dd.field-even').xpath('//abbr/text()').get()

        data = {
            'number': pep_number,
            'name': pep_name,
            'status': pep_status
        }
        yield PepParseItem(data)
