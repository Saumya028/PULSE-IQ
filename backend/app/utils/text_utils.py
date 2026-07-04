from difflib import SequenceMatcher


def similarity(a, b):

    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


def remove_duplicate_articles(articles):

    unique = []

    seen_urls = set()

    for article in articles:

        url = article.get("url")

        if url in seen_urls:
            continue

        duplicate = False

        for existing in unique:

            score = similarity(
                article["title"],
                existing["title"]
            )

            if score > 0.90:
                duplicate = True
                break

        if duplicate:
            continue

        seen_urls.add(url)

        unique.append(article)

    return unique