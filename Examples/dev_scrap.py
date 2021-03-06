#!/usr/bin/python3
# -*- coding: utf-8 -*-
from GoogleScraper import scrape_with_config, GoogleSearchError
import argparse
import chardet
import traceback
import pprint


class ScrapSerps():

    def scrap_serps(self, serp_query):
        search = self.scrap(serp_query)
        result = []
        for serp in search.serps:
            for link in serp.links:
                    # link, snippet, title, visible_link, domain, rank, serp, link_type, rating
                # if 'results' in link.link_type:
                result.append({
                    'query_num_results total': serp.num_results_for_query,
                    'query_num_results_page': serp.num_results,
                    'query_page_number': serp.page_number,
                    'query': serp.query,
                    'serp_rank': link.rank,
                    'serp_type': link.link_type,
                    'serp_url': link.link,
                    'serp_rating': self.adjust_encoding(link.rating)['data'],
                    'serp_title': self.adjust_encoding(link.title)['data'],
                    'serp_domain': self.adjust_encoding(link.domain)['data'],
                    'serp_visible_link': self.adjust_encoding(link.visible_link)['data'],
                    'serp_snippet': self.adjust_encoding(link.snippet)['data'],
                    'serp_sitelinks': self.adjust_encoding(link.sitelinks)['data']
                })
        return result

    def scrap(self, keyword):
        keywords = [keyword]
        # See in the config.cfg file for possible values
        config = {
            'use_own_ip': 'False',
            'keywords': keywords,
            'search_engines': ['google'],
            'num_pages_for_keyword': 2,
            'scrape_method': 'http',  # selenium
            # 'sel_browser': 'chrome', uncomment if scrape_method is selenium
            # 'executable_path': 'path\to\chromedriver' or 'path\to\phantomjs',
            'do_caching': 'True',
            'cachedir': '/tmp/.scrapecache/',
            'database_name': '/tmp/google_scraper',
            'clean_cache_after': 24,
            'output_filename': None,
            'print_results': 'all',
        }
        try:
            return scrape_with_config(config)
        except GoogleSearchError:
            print(traceback.print_exc())

    def adjust_encoding(self, data):
        """detect and adjust encoding of data return data decoded to utf-8"""
        if data is None:
            return {'encoding': None, 'data': data}

        data = data.encode('utf-8')
        check_encoding = chardet.detect(data)

        if check_encoding['encoding'] is not None and 'utf-8' not in check_encoding['encoding']:
            try:
                data = data.decode(check_encoding['encoding']).encode('utf-8')
            except:
                pass
        try:
            data = data.decode('utf-8')
        except:
            data = data.decode('utf-8', 'ignore')

        return {'encoding': check_encoding['encoding'], 'data': data}

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='dev_scrap')
    parser.add_argument('-k', '--keyword', help='keyword for scraping', nargs='*')
    args = parser.parse_args()
    if len(args.keyword) > 0:
        keyword = ' '.join(args.keyword)

    sc = ScrapSerps()
    res = sc.scrap_serps(keyword)
    for r in res:
        pprint.pprint(r)
