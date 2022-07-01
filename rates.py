import scrapy
import json
from operator import itemgetter


class RatesSpider(scrapy.Spider):
    name = 'rates'
    allowed_domains = ['loanscan.io']
    HISTORICAL_RATES = 'https://api.loanscan.io/v1/interest-rates'
    start_urls = [HISTORICAL_RATES]

    """
        This function returns Top n Interest Rates of USDT.
        It takes a list of USDT rates and return Top N interest rates
        
        rates: List of USDT interest rates
        number: Top n Value 
    """

    def get_top_rates(self, rates, number=5):
        # To return sorted list against the given key in descending order
        top_5_rates = sorted(rates, key=itemgetter('rate'), reverse=True)
        return top_5_rates[0:number]

    def parse(self, response):
        usdt_rates = []
        records = json.loads(response.text)
        for record in records:
            platform = record['provider'].replace('\n', '')
            supplies = record['supply']
            for supply in supplies:
                if supply['symbol'] == 'USDT':  # Fetch only USDT rates
                    usdt_rates.append({'platform': platform, 'rate': supply['rate']})

        top_rates = self.get_top_rates(usdt_rates)
        for top_rate in top_rates:
            yield {
                "Rate": top_rate['rate'],
                "Platform": top_rate['platform'],
            }
