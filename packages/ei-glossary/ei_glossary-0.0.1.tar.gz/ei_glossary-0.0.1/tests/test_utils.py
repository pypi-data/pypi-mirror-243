from ei_glossary.utils import uuid_regex


def test_uuid_regex():
    re = uuid_regex("https://glossary.ecoinvent.org/")
    given = "https://glossary.ecoinvent.org/ids/2cf92850-0f92-4004-9dba-a6ceb6a414c2/"  # noqa: E501
    assert re.search(given).group("uuid") == "2cf92850-0f92-4004-9dba-a6ceb6a414c2"

    given = "https://glossary.ecoinvent.org/ids/2cf92850-0f92"
    assert re.search(given) is None
