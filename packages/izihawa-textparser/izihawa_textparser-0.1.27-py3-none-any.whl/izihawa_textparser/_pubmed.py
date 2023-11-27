import datetime
import time

import xmltodict
from iso639 import Lang

from .utils import md


def process_single_record(item):
    medline_citation = item["MedlineCitation"]
    article = medline_citation["Article"]
    pubmed_data = item["PubmedData"]
    issued_date = None

    for date in pubmed_data["History"]["PubMedPubDate"]:
        if date["@PubStatus"] == "pubmed":
            issued_date = date

    document = {
        "id": {"pubmed_id": int(medline_citation["PMID"]["#text"])},
        "metadata": {},
        "type": "journal-article",
        "issued_at": int(
            time.mktime(
                datetime.datetime(
                    year=int(issued_date["Year"]),
                    month=int(issued_date["Month"]),
                    day=int(issued_date["Day"]),
                ).utctimetuple()
            )
        ),
    }

    doi = None
    pii = None

    article_id_list = pubmed_data["ArticleIdList"]["ArticleId"]
    if not isinstance(article_id_list, list):
        article_id_list = [article_id_list]

    for article_id in article_id_list:
        if article_id["@IdType"] == "doi" and "#text" in article_id:
            doi = article_id["#text"].lower()
        if article_id["@IdType"] == "pii" and "#text" in article_id:
            pii = article_id["#text"]

    tags = []
    mesh_heading = medline_citation.get("MeshHeadingList", {"MeshHeading": []})[
        "MeshHeading"
    ]
    if not isinstance(mesh_heading, list):
        mesh_heading = [mesh_heading]
    for mesh_term in mesh_heading:
        tags.append(mesh_term["DescriptorName"]["#text"])
    if tags:
        document["tags"] = tags

    if not article.get("ArticleTitle") or isinstance(article["ArticleTitle"], dict):
        return
    document["title"] = article["ArticleTitle"].strip(".")
    if document["title"].startswith("[") and document["title"].endswith("]"):
        document["title"] = document["title"].lstrip("[").rstrip("]")
    if isinstance(article["Language"], list):
        document["languages"] = [Lang(l).pt1 for l in article["Language"]]
    else:
        document["languages"] = [Lang(article["Language"]).pt1]
    if "ISSN" in article["Journal"]:
        document["metadata"]["issns"] = [article["Journal"]["ISSN"]["#text"]]
    if "Volume" in article["Journal"]["JournalIssue"]:
        document["metadata"]["volume"] = article["Journal"]["JournalIssue"]["Volume"]
    if "Issue" in article["Journal"]["JournalIssue"]:
        document["metadata"]["issue"] = article["Journal"]["JournalIssue"]["Issue"]
    document["metadata"]["container_title"] = (
        article["Journal"]["Title"].split("=")[0].strip()
    )
    try:
        if medline_pgn := article["Pagination"].get("MedlinePgn"):
            pages = medline_pgn.split("-")
            if len(pages) == 2:
                first_page, last_page = pages
                first_page = int(first_page.rstrip("P"))
                last_page = int(last_page.rstrip("P"))
                if last_page < first_page:
                    last_page = int(
                        str(first_page)[: len(str(first_page)) - len(str(last_page))]
                        + str(last_page)
                    )
                (
                    document["metadata"]["first_page"],
                    document["metadata"]["last_page"],
                ) = (first_page, last_page)
            elif len(pages) == 1:
                document["metadata"]["first_page"] = int(pages[0].rstrip("P"))
    except (KeyError, ValueError):
        pass
    if "AuthorList" in article:
        author_list = article["AuthorList"]["Author"]
        if not isinstance(author_list, list):
            author_list = [author_list]
        ready_authors = []
        for author in author_list:
            ready_author = {}
            if "LastName" in author:
                ready_author["family"] = author["LastName"]
            if "ForeName" in author:
                ready_author["given"] = author["ForeName"]
            if ready_author:
                ready_authors.append(ready_author)
        document["authors"] = ready_authors
    if "Abstract" in article:
        if isinstance(article["Abstract"]["AbstractText"], list):
            sections = []
            for part in article["Abstract"]["AbstractText"]:
                if part and "#text" in part:
                    if part.get("@Label") == "UNLABELLED":
                        sections.append(part["#text"])
                    else:
                        if "@Label" in part:
                            label = part["@Label"].capitalize() + ":"
                            sections.append(f"## {label}")
                        sections.append(md.convert(part["#text"].capitalize()))
            abstract = "\n\n".join(sections).strip()
        else:
            abstract = article["Abstract"]["AbstractText"]
            if isinstance(abstract, dict):
                abstract = abstract.get("#text")
            if abstract:
                abstract = md.convert(abstract).strip()
        if abstract:
            document["abstract"] = abstract

    publication_type_list = article["PublicationTypeList"]["PublicationType"]
    if not isinstance(publication_type_list, list):
        publication_type_list = [publication_type_list]

    is_article = False
    stored_publication_type = None
    for publication_type in publication_type_list:
        stored_publication_type = publication_type["#text"]
        is_article = is_article or stored_publication_type in (
            "Journal Article",
            "Historical Article",
            "Case Reports",
            "Comment",
            "Comparative Study",
            "Review",
            "Letter",
            "News",
            "Bibliography",
            "Retraction of Publication",
        )

    if not is_article:
        return

    if doi:
        document["id"]["dois"] = [doi.lower().strip()]
    if pii:
        document["id"]["pii"] = pii

    return document, stored_publication_type


def process_pubmed_archive(data):
    data_dict = xmltodict.parse(data)
    for item in data_dict["PubmedArticleSet"]["PubmedArticle"]:
        result = process_single_record(item)
        if result:
            yield result
