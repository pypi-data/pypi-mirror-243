from bs4 import BeautifulSoup as BS
from ...utils.scraper import WebScraper
from ...utils.props import NoSupportedProvider, SelectedNotAvailable
import re


class Provider(WebScraper):
    def __init__(self, base_url) -> None:
        super().__init__(base_url)
        self.base_url = base_url

    def search(self, q: str = None) -> str:
        q = input(f"[!] {self.translated[self.task]}") if q is None else q
        return q.replace(" ", "+")

    def results(self, data: str) -> list:
        m = self.client.get(
            f"{self.base_url}/ptb-search/?f=search_movies&ptb-search=1&title={data}"
        )
        s = self.client.get(
            f"{self.base_url}/ptb-search/?f=search_series_1&ptb-search=1&title={data}"
        )
        show = BS(s, self.scraper)
        shows = show.findAll("h5", {"class": "ptb_post_title"})
        movie = BS(m, self.scraper)
        movies = movie.findAll("h5", {"class": "ptb_post_title"})
        urls = [movies[i].find("a")["href"] for i in range(len(movies))] + [
            shows[i].find("a")["href"] for i in range(len(shows))
        ]
        title = [movies[i].find("a").text for i in range(len(movies))] + [
            shows[i].find("a").text for i in range(len(shows))
        ]
        ids = [i for i in range(len(movies))] + [i for i in range(len(shows))]
        mov_or_tv = ["MOVIE" for i in range(len(movies))] + [
            "TV" for i in range(len(shows))
        ]
        return [list(sublist) for sublist in zip(title, urls, ids, mov_or_tv)]

    def ask(self, url):
        req = self.client.get(url)
        soup = BS(req, self.scraper)
        t = soup.find("select", {"id": "loadepisode"})
        try:
            episodes = len(t.findAll("option"))
        except:
            raise SelectedNotAvailable
        episode = int(self.askepisode(episodes))
        req = self.client.get(f"{url}?server=cajitatop&episode={episode}").text
        soup = BS(req, self.scraper)
        try:
            t = soup.find("iframe", {"loading": "lazy"})["src"]
            print(t)
        except:
            raise NoSupportedProvider
        return t, episode

    def cdn_url(self, url):
        self.client.set_headers({"origin": "cajita.top", "referer": f"{url}"})
        string = re.findall("""v\/([^"']*)""", url)[0]
        request = self.client.post(
            f"https://cajita.top/api/source/{string}",
            data={"r": f"{self.base_url}", "d": "cajita.top"},
        ).json()
        file = request["data"]
        if file == "Video not found or has been removed":
            raise SelectedNotAvailable
        else:
            file = request["data"][-1]["file"]
        return file

    def download(self, t):
        req = self.client.get(t[self.url])
        soup = BS(req, self.scraper)
        t = soup.find("select", {"id": "loadepisode"})
        try:
            episodes = len(t.findAll("option"))
        except:
            return print("Episode unavailable")
        for e in range(len(episodes)):
            req = self.client.get(f"{[self.url]}?server=cajitatop&episode={e+1}").text
            soup = BS(req, self.scraper)
            try:
                t = soup.find("iframe", {"loading": "lazy"})["src"]
            except:
                raise SelectedNotAvailable
            url = str(self.cdn_url(t))
            self.dl(url, t[self.title], episode=e + 1)

    def TV_PandDP(self, t: list, state: str = "d" or "p" or "sd"):
        name = t[self.title]
        url, episode = self.ask(t[self.url])
        url = str(self.cdn_url(url))
        if state == "d":
            self.dl(url, name, episode=episode)
            return
        self.play(url, name)

    def MOV_PandDP(self, m: list, state: str = "d" or "p" or "sd"):
        name = m[self.title]
        url, episode = self.ask(m[self.url])
        url = self.cdn_url(url)
        if state == "d":
            self.dl(url, name)
            return
        self.play(url, name)
