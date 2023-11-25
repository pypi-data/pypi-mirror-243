import re

import asyncio

from aiokit import AioThing
from bs4 import (
    BeautifulSoup,
    NavigableString,
)

from .utils import BANNED_SECTIONS, md

SECTIONS_MAPS = {
    "Authors": "Authors",
    "AUTHORS": "Authors",
    "Abstract": "Abstract",
    "ABSTRACT": "Abstract",
    "Date": "Date",
    "DATE": "Date",
    "acknowledgements": "Acknowledgements",
    "INTRODUCTION": "Introduction",
    "MATERIALS AND METHODS": "Methods",
    "Materials and methods": "Methods",
    "METHODS": "Methods",
    "RESULTS": "Results",
    "CONCLUSIONS": "Conclusions",
    "CONCLUSIONS AND FUTURE APPLICATIONS": "Conclusions",
    "DISCUSSION": "Discussion",
    "ACKNOWLEDGMENTS": "Acknowledgements",
    "TABLES": "Tables",
    "Tabnles": "Tables",
    "DISCLOSURE": "Disclosure",
    "CONFLICT OF INTEREST": "Disclosure",
    "Declaration of conflicting interests": "Disclosure",
    "Declaration of competing interest": "Disclosure",
    "Acknowledgement": "Acknowledgements",
    "Acknowledgments": "Acknowledgements",
    "conflictofintereststatement": "Disclosure",
    "FUNDING": "Funding",
    "fundinginformation": "Funding",
    "BIOGRAPHIES": "Biographies",
    "disclaimer": "Disclosure",
    "referencesfigure": "References Figure",
    "declaration of competing interest": "Disclosure",
    "conflict of interest disclosures": "Disclosure",
    "conflict of interest statement": "Disclosure",
}


def fix_header_level(header_n: str, header_text: str) -> tuple[str, str]:
    if m := re.match(r"((?:\d{1,2}\.)+)(.*)", header_text):
        header_n = header_n + m.group(1)
        header_text = m.group(2).strip()
    return header_n, header_text


def get_header_level(header_n: str) -> int:
    return len(list(filter(lambda x: bool(x.strip()), header_n.split(".")))) + 1


class GrobidParser(AioThing):
    def __init__(self, grobid_client, banned_sections: set = BANNED_SECTIONS):
        super().__init__()
        self.grobid_client = grobid_client
        if banned_sections is None:
            self.banned_sections = set()
        else:
            self.banned_sections = banned_sections

    async def process_document_in_grobid(self, data):
        async with self.grobid_client.lease() as client:
            return await client.post(
                "/api/processFulltextDocument",
                data={
                    "input": data,
                },
            )

    def parse_response(self, grobid_response):
        article = BeautifulSoup(grobid_response, features="xml")
        article_dict = {}
        if article is not None:
            if title := article.find("title", attrs={"type": "main"}):
                if title := title.text.strip():
                    article_dict["title"] = title
            if issued_at := self.parse_date(article):
                article_dict["issued_at"] = issued_at

            article_dict["abstract"] = self.parse_abstract(article)

            if content := self.parse_content(article.find("text")):
                article_dict["content"] = content

            if keywords := self.parse_keywords(article):
                article_dict["keywords"] = keywords

            doi = article.find("idno", attrs={"type": "DOI"})
            doi = doi.text.lower() if doi is not None else None
            if doi:
                article_dict["doi"] = doi.lower()
            return article_dict
        else:
            return

    async def parse_paper(self, data):
        grobid_response = await self.process_document_in_grobid(data)
        return await asyncio.get_running_loop().run_in_executor(
            None, lambda: self.parse_response(grobid_response)
        )

    def parse_date(self, article):
        """
        Parse date from a given BeautifulSoup of an article
        """
        pub_date = article.find("publicationStmt")
        year = pub_date.find("date")
        year = year.attrs.get("when") if year is not None else ""
        return year

    def parse_abstract(self, article):
        divs = article.find("abstract").find_all(
            "div", attrs={"xmlns": "http://www.tei-c.org/ns/1.0"}
        )
        return self.parse_body(divs)

    def parse_body(self, divs):
        """
        Parse abstract from a given BeautifulSoup of an article
        """
        parts = []

        for div in divs:
            for el in list(div.select("table, nav, ref, formula, math, figure, img")):
                el.extract()

            div_list = list(div.children)

            header_n = ""

            if not div_list:
                continue
            elif len(div_list) == 1:
                if isinstance(div_list[0], NavigableString):
                    parts.append(md.convert(div_list[0]))
                else:
                    parts.append(md.convert_soup(div_list[0]))
            else:
                if div_list[0].name == "head":
                    header_text = div_list[0].text
                    header_n = div_list[0].attrs.get("n", "")
                    p_all = div_list[1:]
                else:
                    header_text = ""
                    p_all = div_list

                header_n, header_text = fix_header_level(
                    header_n=header_n, header_text=header_text
                )

                if header_text:
                    mapped_heading = SECTIONS_MAPS.get(header_text)
                    if not mapped_heading:
                        mapped_heading = SECTIONS_MAPS.get(
                            "".join(header_text.lower()), header_text
                        )

                    if mapped_heading in self.banned_sections:
                        continue

                    if mapped_heading:
                        if header_n:
                            parts.append(
                                f'{"#" * get_header_level(header_n)} {header_n} {mapped_heading}'
                            )
                        else:
                            parts.append(f"## {mapped_heading}\n")

                for p in p_all:
                    if p is None:
                        continue
                    if isinstance(p, NavigableString):
                        parts.append(md.convert(p))
                    else:
                        parts.append(md.convert_soup(p))

        return "\n\n".join(parts).removeprefix("Abstract\n").strip()

    def parse_keywords(self, article):
        """
        Parse abstract from a given BeautifulSoup of an article
        """
        div = article.find("keywords")
        keywords = []
        if keywords:
            for term in div.find_all("term"):
                keywords.append(term.text.strip().lower())
        return keywords

    def parse_content(self, article):
        """
        Parse list of sections from a given BeautifulSoup of an article
        """
        divs = article.find_all("div", attrs={"xmlns": "http://www.tei-c.org/ns/1.0"})
        return self.parse_body(divs)

    def parse_references(self, article):
        """
        Parse list of references from a given BeautifulSoup of an article
        """
        references = article.find("text").find("div", attrs={"type": "references"})
        references = references.find_all("biblStruct") if references is not None else []
        reference_list = []
        for reference in references:
            title = reference.find("title", attrs={"level": "a"})
            if title is None:
                title = reference.find("title", attrs={"level": "m"})
            title = title.text if title is not None else ""
            journal = reference.find("title", attrs={"level": "j"})
            journal = journal.text if journal is not None else ""
            if journal == "":
                journal = reference.find("publisher")
                journal = journal.text if journal is not None else ""
            year = reference.find("date")
            year = year.attrs.get("when") if year is not None else ""
            authors = []
            for author in reference.find_all("author"):
                firstname = author.find("forename", {"type": "first"})
                firstname = firstname.text.strip() if firstname is not None else ""
                middlename = author.find("forename", {"type": "middle"})
                middlename = middlename.text.strip() if middlename is not None else ""
                lastname = author.find("surname")
                lastname = lastname.text.strip() if lastname is not None else ""
                if middlename != "":
                    authors.append(firstname + " " + middlename + " " + lastname)
                else:
                    authors.append(firstname + " " + lastname)
            authors = "; ".join(authors)
            reference_list.append(
                {"title": title, "journal": journal, "year": year, "authors": authors}
            )
        return reference_list
