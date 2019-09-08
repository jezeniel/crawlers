import pprint

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

pp = pprint.PrettyPrinter(indent=4)


class ClickTheCitySpider:
    def __init__(self, url: str):
        self.url = url

    def run(self) -> list:
        response = requests.get(self.url)
        page = BeautifulSoup(response.content, 'lxml')
        return self.scrape(page)

    def scrape(self, page: BeautifulSoup) -> dict:
        """ I tried using the meta tags initially, but some cinemas have
        multiple movies on a single room. """
        result = []
        cinemas = page.select('ul#cinemas li.cinema')
        for c in cinemas:
            cinema_name = c.find('h2').text
            movie_infos = []

            for movie in c.select('ul li'):
                movie_infos.append(self.get_movie_info(movie))

            result.append({
                'cinema': cinema_name,
                'movies': movie_infos,
                'total_movies': len(movie_infos)
            })
        return result

    def get_movie_info(self, movie: Tag) -> dict:
        result = {
            'name': movie.find('span', itemprop='name').text,
            'price': movie.find('span').text,
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
        'https://www.clickthecity.com/movies/theaters/sm-aura-premier'
    )
    pp.pprint(spider.run())
