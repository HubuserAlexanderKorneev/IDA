# -*- coding: utf-8 -*-
import scrapy
import re

class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['gismeteo.ru']
    start_urls = ['https://www.gismeteo.ru/weather-moscow-4368/10-days/']

    def parse(self, response):
        days = response.css('.forecast_frame .w_date__day::text').extract()
        dates = response.css('.forecast_frame .w_date__date::text').re('\d\d')
        dd = list(map(lambda x: x[0]+' '+x[1]+'.02',list(zip(days,dates))))
        maxt = response.css('.chart__temperature .maxt::text').extract()
        maxt_pure = list(map(lambda x: int(x.replace('−','-')),maxt))
        mint = response.css('.chart__temperature .mint::text').extract()
        mint_pure = list(map(lambda x: int(x.replace('−','-')),mint))
        hum = response.css('.w_precipitation__value::text').extract()
        hum_pure = list(map(lambda x: float(x.split()[0].replace(',','.')),hum))
        wind = response.css('.widget__row_table:nth-child(5) .w_wind__warning::text').extract()
        wind_pure = list(map(lambda x: int(x.split()[0]),wind))
        yield {'dd':dd,'Максимальная температура':maxt_pure,'Минимальная температура':mint_pure,'Уровень осадков':hum_pure,'Скорость ветра':wind_pure}
