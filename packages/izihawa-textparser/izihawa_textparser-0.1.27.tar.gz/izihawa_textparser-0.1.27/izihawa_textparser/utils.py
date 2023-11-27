import isbnlib
import markdownify

import re


BANNED_SECTIONS = {
    "author contribution",
    "data availability statement",
    "declaration of competing interest",
    "acknowledgments",
    "acknowledgements",
    "supporting information",
    "conflict of interest disclosures",
    "conflict of interest",
    "conflict of interest statement",
    "ethics statement",
    "references",
    "external links",
    "further reading",
    "works cited",
    "bibliography",
    "notes",
    "sources",
    "footnotes",
    "suggested readings",
}


def despace(text: str):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    return text


def clean_empty_references(text: str):
    text = re.sub(r"\((?:[Ff]ig|[Tt]able|[Ss]ection)\.?\s*[^)]*\)", "", text)
    text = re.sub(r"\[[,\s–\d]*]", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+([.,;])", "\g<1>", text, flags=re.MULTILINE)
    return text


def reduce_br(text: str):
    text = (
        text.replace("<br>", "<br/>")
        .replace("<p><br/>", "<p>")
        .replace("<br/></p>", "</p>")
    )
    text = re.sub(r"([^.>])<br/>([^(<br/>)])", r"\g<1> \g<2>", text)
    text = re.sub(r"(?:<br/>\s*)+([^(<br/>)])", r"<br/><br/>\g<1>", text)
    text = despace(text)
    return text


def canonize_tags(soup):
    for el in soup.find_all():
        if el.name == "span":
            el.unwrap()
        elif el.name == "em":
            el.name = "i"
        elif el.name == "italic":
            el.name = "i"
        elif el.name == "strong":
            el.name = "b"
        elif el.name == "sec":
            el.name = "section"
        elif el.name == "title":
            el.name = "h2"
        elif el.name == "bold":
            el.name = "b"
        elif el.name == "p" and "ref" in el.attrs.get("class", []):
            el.name = "ref"
        elif el.name == "disp-formula":
            el.name = "formula"
    return soup


def process_isbns(isbnlikes):
    isbns = []
    for isbnlike in isbnlikes:
        if not isbnlike:
            continue
        if isbnlike[0].isalpha() and len(isbnlike) == 10 and isbnlike[1:].isalnum():
            isbns.append(isbnlike.upper())
            continue
        isbn = isbnlib.canonical(isbnlike)
        if not isbn:
            continue
        isbns.append(isbn)
        if isbnlib.is_isbn10(isbn):
            if isbn13 := isbnlib.to_isbn13(isbn):
                isbns.append(isbn13)
        elif isbnlib.is_isbn13(isbn):
            if isbn10 := isbnlib.to_isbn10(isbn):
                isbns.append(isbn10)
    return list(sorted(set(isbns)))


class MarkdownConverter(markdownify.MarkdownConverter):
    convert_b = markdownify.abstract_inline_conversion(lambda self: '**')
    convert_i = markdownify.abstract_inline_conversion(lambda self: '__')
    convert_em = markdownify.abstract_inline_conversion(lambda self: '__')
    convert_sup = markdownify.abstract_inline_conversion(lambda self: '^')
    convert_sub = markdownify.abstract_inline_conversion(lambda self: '~')

    def convert_header(self, el, text, convert_as_inline):
        return self.convert_hn(2, el, text, convert_as_inline)

    def convert_title(self, el, text, convert_as_inline):
        return self.convert_hn(2, el, text, convert_as_inline)

    def convert_soup(self, soup):
        r = super().convert_soup(soup)
        return re.sub(r'\n{2,}', '\n\n', r).replace('\r\n', '').strip()


md = MarkdownConverter(heading_style=markdownify.ATX)

