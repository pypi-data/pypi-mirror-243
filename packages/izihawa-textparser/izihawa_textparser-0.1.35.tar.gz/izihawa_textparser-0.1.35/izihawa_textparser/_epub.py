from bs4 import BeautifulSoup
from izihawa_textutils.html_processing import canonize_tags

from .utils import BANNED_SECTIONS, md


class EpubParser:
    def __init__(self, banned_sections: set = BANNED_SECTIONS):
        if banned_sections is None:
            self.banned_sections = set()
        else:
            self.banned_sections = banned_sections

    def parse_soup(self, soup: BeautifulSoup):
        for section in list(soup.find_all("section")):
            for child in section.children:
                if (
                    child.name in {"header", "h1", "h2", "h3", "h4", "h5", "h6", "div"}
                    and child.text.lower().strip(" :,.;") in self.banned_sections
                ):
                    section.extract()
                    break

        for summary in list(soup.select("details > summary.section-heading")):
            if summary.text.lower().strip(" :,.;") in self.banned_sections:
                summary.parent.extract()

        for b_tag in list(soup.select("b, i")):
            b_tag.unwrap()

        for p_tag in list(soup.find_all("p")):
            sibling = p_tag.next_sibling
            while sibling == "\n":
                sibling = sibling.next_sibling
            if sibling and sibling.name == "blockquote":
                new_p_tag = soup.new_tag("p")
                new_p_tag.extend([p_tag.text, " ", sibling.text])
                p_tag.replace_with(new_p_tag)
                sibling.extract()

        for el in list(
            soup.select(
                'table, nav, ref, formula, math, figure, img, [role="note"], .Affiliations, '
                ".ArticleOrChapterToc, "
                ".AuthorGroup, .ChapterContextInformation, "
                ".Contacts, .CoverFigure, .Bibliography, "
                ".BookTitlePage, .BookFrontmatter, .CopyrightPage, .Equation, "
                ".FootnoteSection, .Table, .reference, .side-box-text, .thumbcaption"
            )
        ):
            el.extract()

        for el in list(soup.select("a, span")):
            el.unwrap()

        return md.convert_soup(canonize_tags(soup))
