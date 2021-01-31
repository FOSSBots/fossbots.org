"""Powers Flask API for mirahezebots.org web site."""
from MirahezeBots_jsonparser import jsonparser as jp

from flask import Flask, Response, send_file

app = Flask(__name__)


def display_content(path, config):
    """Generate the content for templated pages."""
    with open(config['templatedpages'][path], 'r') as file:
        contents = file.read()
        with open(config['rendertemplates']['navbar'], 'r') as navbar:
            navbarr = navbar.read()
            index = 'href="/"'
            docs = 'href="documentation"'
            contribs = 'href="contribs"'
            about = 'href="about"'
            sourcecode = 'href="https://bots.miraheze.org/wiki/Source_Code"'
            if path == 'index':
                index = 'class="active" href="/"'
            if path == 'about':
                about = 'class="active" href="about"'
            if path == 'documentation':
                docs = 'class="active" href="documentation"'
            if path == 'contribs':
                contribs = 'class="active" href="contribs"'
            navbarr = navbarr.format(
                indexlink=index,
                documentationlink=docs,
                contribslink=contribs,
                aboutlink=about,
                sourcecodelink=sourcecode,
            )
        with open(config['rendertemplates']['footer']) as footer:
            footerr = footer.read()
        with open(config['rendertemplates']['head']) as head:
            headr = head.read()
            canonical = config['canonical-prefix']+path
            if path == 'index':
                canonical = config['canonical-prefix']  # / is canonical
                title = 'Home - MirahezeBot'
            if path == 'about':
                title = 'About - MirahezeBot'
            if path == 'documentation':
                title = 'Documentation - MirahezeBot'
            if path == 'contribs':
                title = 'Contributors - MirahezeBot'
            if path == 'privacy':
                title = 'Privacy - MirahezeBot'
            if path == 'terms':
                title = 'Terns - MirahezeBot'

            headr = headr.format(canonical=canonical, title=title)
    return contents.format(head=headr, footer=footerr, navbar=navbarr)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Generate appropiate response to a request."""
    if path.endswith('.html'):
        path = path[:-5]  # ignore .html endings
    if path == '':
        path = 'index'  # rewrite empty path to index
    try:
        config = jp.createdict('config.json')
    except FileNotFoundError:
        config = jp.createdict('/var/flask/config.json')
    if path in config['directshow']:
        return send_file(config['directshow'][path])
    if path in config['templatedpages']:
        return display_content(path, config)
    if path.startswith(config['font-awesome-url']):
        return send_file(
            str(
                config['Font-awesome-path'],
            )
            +
            str(
                path[len(config['font-awesome-url']):],
            ),
        )
    return Response(status=404)


if __name__ == '__main__':
    app.run(debug=True)  # nosec
