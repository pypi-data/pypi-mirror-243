from . import JrdData, JrdLink


def test_jrd_link():
    assert JrdLink().build() == {}
    assert JrdLink(rel="rel", href="href", type="type").build() == {
        x: x for x in ["rel", "href", "type"]
    }


def test_jrd_asdict():
    assert JrdData().build() == {}
    assert JrdData(subject="acct:test").build() == {"subject": "acct:test"}

    link = JrdLink(href="https://some.example/")

    assert JrdData(links=[link]).build() == {
        "links": [{"href": "https://some.example/"}]
    }
