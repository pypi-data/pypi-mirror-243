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


class MarkdownConverter(markdownify.MarkdownConverter):
    convert_b = markdownify.abstract_inline_conversion(lambda self: "**")
    convert_i = markdownify.abstract_inline_conversion(lambda self: "__")
    convert_em = markdownify.abstract_inline_conversion(lambda self: "__")
    convert_sup = markdownify.abstract_inline_conversion(lambda self: "^")
    convert_sub = markdownify.abstract_inline_conversion(lambda self: "~")

    def convert_header(self, el, text, convert_as_inline):
        return self.convert_hn(2, el, text, convert_as_inline)

    def convert_title(self, el, text, convert_as_inline):
        return self.convert_hn(2, el, text, convert_as_inline)

    def convert_soup(self, soup):
        r = super().convert_soup(soup)
        return re.sub(r"\n{2,}", "\n\n", r).replace("\r\n", "").strip()


md = MarkdownConverter(heading_style=markdownify.ATX)
