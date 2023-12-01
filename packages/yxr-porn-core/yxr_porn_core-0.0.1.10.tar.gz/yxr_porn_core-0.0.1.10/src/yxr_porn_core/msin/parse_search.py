# based on https://github.com/yoshiko2/Movie_Data_Capture/blob/master/scrapinglib/msin.py


from dataclasses import dataclass
from typing import List, cast

from lxml import etree


class ParseSearchError(Exception):
    def __init__(self, error_message: str, error_string: str, *args: object) -> None:
        super().__init__(error_message, *args)
        self.error_string = error_string
        self.error_message = error_message


@dataclass
class SearchResultItem:
    product_id: str
    title: str
    writer: str
    maker: str
    actor: List[str]
    duration: str
    release: str  # YYYY-MM-DD
    cover_url: str


def typed_xpath(htmltree, expr: str) -> List[str]:
    return cast(List[str], htmltree.xpath(expr))


# https://db.msin.jp/search/movie?str=fc2-ppv-3393451
# cookie = {'age':'off'}
def parse_search(html: str) -> SearchResultItem:
    htmltree = etree.HTML(html, etree.HTMLParser())

    expr_err_string = '//div[@class="error_string"]/text()'
    expr_err_message = '//div[@class="error_massage"]/text()'  # 网站拼的就是 massage
    expr_number = '//div[@class="mv_fileName"]/text()'
    expr_title = '//div[contains(@class,"mv_title")]/text()'
    expr_duration = '//div[@class="mv_duration"]/text()'
    expr_writer = '//a[@class="mv_writer"]/text()'
    expr_actor = '//div[contains(text(),"出演者：")]/following-sibling::div[1]/div/div[@class="performer_text"]/a/text()'
    expr_maker = '//a[@class="mv_mfr"]/text()'
    expr_release = '//a[@class="mv_createDate"]/text()'
    expr_cover_url = '//div[@class="movie_top"]/img/@src'

    err_strings = typed_xpath(htmltree, expr_err_string)
    if len(err_strings) > 0:
        raise ParseSearchError(error_string=err_strings[0], error_message=typed_xpath(htmltree, expr_err_message)[0])

    # FC2-PPV-XYZ -> FC2-XYZ
    product_id = typed_xpath(htmltree, expr_number)[0].upper().replace("FC2-PPV", "FC2").strip()
    title: str = typed_xpath(htmltree, expr_title)[0].upper().replace("FC2-PPV", "FC2").replace(product_id, "").strip()
    writer: str = typed_xpath(htmltree, expr_writer)[0]
    maker: str = typed_xpath(htmltree, expr_maker)[0]
    actor: List[str] = [act.replace("（FC2動画）", "") for act in typed_xpath(htmltree, expr_actor)]
    duration: str = typed_xpath(htmltree, expr_duration)[0]
    release: str = typed_xpath(htmltree, expr_release)[0]
    cover_url: str = typed_xpath(htmltree, expr_cover_url)[0]

    return SearchResultItem(
        product_id=product_id,
        title=title,
        writer=writer,
        maker=maker,
        actor=actor,
        duration=duration,
        release=release,
        cover_url=cover_url,
    )
