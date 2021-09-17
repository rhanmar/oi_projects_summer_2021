import scrapy

SKILLS_XPATH = ("/html/body/div[1]/div/div/div/div/article/"
                "section[1]/div/div/div/div[3]")


def get_absolute_url(path: str) -> str:
    """Return absolute url by path career.habr.com resource.

    Example:
    "/vacancies/1000082519" -> "https://career.habr.com/vacancies/1000082519"
    """
    return "https://career.habr.com" + path


class VacancySpider(scrapy.Spider):
    """Spider for scrapping vacancies."""

    name: str = "vacancies"
    page: int = 1
    last_page: bool = False

    def start_requests(self):
        while not self.last_page:
            url = f"https://career.habr.com/vacancies?page={self.page}"
            yield scrapy.Request(
                url=url,
                callback=self.parse_pages
            )
            self.page += 1

    def parse_pages(self, response, **kwargs):
        """Extract vacancy cards hrefs from catalog page."""
        hrefs = response.css(
            ".vacancy-card__title-link::attr('href')"
        ).extract()

        # If hrefs are not specified, then this is the last page.
        if not hrefs:
            self.last_page = True

        for href in hrefs:
            url = get_absolute_url(href)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """Extract data from vacancy card."""
        title = response.css(".page-title__title::text").get()
        skills_card = response.xpath(SKILLS_XPATH)

        item = dict(
            url=response.request.url,
            title=title,
            startup_name=response.css(".company_name *::text").get(),
            startup_description=response.css(".company_about *::text").get(),
            vacancy_skills=skills_card.css(".preserve-line *::text").extract(),
            description=' '.join(response.css(".style-ugc *::text").extract())
        )
        yield item
