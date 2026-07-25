from app.services.analyzer import parse_html


def test_parse_html_happy_path():
    html = """
    <html>
        <head>
            <title>Page Pulse Test</title>
            <meta name="description" content="A test webpage">
        </head>

        <body>
            <h1>Main Heading</h1>

            <p>Hello world from Page Pulse.</p>

            <img src="logo.png" alt="Page Pulse logo">
            <img src="photo.png">
        </body>
    </html>
    """

    result = parse_html(html)

    assert result["title"] == "Page Pulse Test"
    assert result["meta_description"] == "A test webpage"
    assert result["h1_count"] == 1
    assert result["images_missing_alt"] == 1
    assert result["word_count"] > 0

def test_parse_html_missing_metadata():
    html = """
    <html>
        <body>
            <p>This page has no metadata.</p>
        </body>
    </html>
    """

    result = parse_html(html)

    assert result["title"] is None
    assert result["meta_description"] is None
    assert result["h1_count"] == 0

def test_parse_html_missing_alt_text():
    html = """
    <html>
        <body>
            <img src="one.png">
            <img src="two.png" alt="">
            <img src="three.png" alt="Product image">
        </body>
    </html>
    """

    result = parse_html(html)

    assert result["images_missing_alt"] == 2