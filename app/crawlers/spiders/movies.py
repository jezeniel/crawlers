import pprint

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

pp = pprint.PrettyPrinter(indent=4)


class ClickTheCitySpider:
    def __init__(self, url: str):
        self.url = url

    def crawl(self) -> list:
        response = requests.get(self.url)
        page = BeautifulSoup(response.content, 'lxml')
        return self.scrape(page)

    def scrape(self, page: BeautifulSoup) -> dict:
        """ I tried using the meta tags initially, but some cinemas have
        multiple movies on a single room. """
        result = []
        rooms = page.select('ul#cinemas li.cinema')
        for r in rooms:
            room_name = r.find('h2').find('em').text
            movie_infos = []

            for movie in r.select('ul li'):
                movie_infos.append(self.parse_movie(movie))

            result.append({
                'room': room_name,
                'movies': movie_infos,
                'total_movies': len(movie_infos)
            })
        return result

    def parse_movie(self, movie: Tag) -> dict:
        # TODO: Find better handling.
        price = movie.find('meta', itemprop='priceRange')
        if price:
            price = price['content']
        else:
            price = 'n/a'

        result = {
            'image': movie.find('meta', itemprop='image')['content'],
            'title': movie.find('span', itemprop='name').text,
            'price': price,
            'genre': movie.find('span', class_='genre').text,
            'running_time': movie.find('span', class_='running_time').text,
            'schedule': [
                s['content'] for s in movie.find_all(
                    'meta', itemprop='startDate'
                )
            ]
        }
        return result


if __name__ == '__main__':
    spider = ClickTheCitySpider(
        'https://www.clickthecity.com/movies/theaters/sm-megamall'
    )
    pp.pprint(spider.crawl())
