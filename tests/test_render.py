"""Test rendering of HTML by Flask."""
from MirahezeBots_jsonparser import jsonparser as jp

from app import display_content


XSS = {"templatedpages":{"about":"templates/about.html","contribs":"templates/contribs.html","documentation":"templates/documentation.html","index":"templates/index.html","privacy":"templates/privacy.html","terms":"templates/terms.html"},"directshow":{"robots.txt":"templates/robots.txt","sitemap.xml":"templates/sitemap.xml","css/common.css":"assets/common.css","logo.png":"assets/logo.png","favicon.png":"assets/favicon.png","fosshost.png":"assets/fosshost.png"},"title":{"index":"</title><img src=1 href=1 onerror=\"javascript:alert(1)\"></img>","about":"About - MirahezeBot","documentation":"Documentation - MirahezeBot","contribs":"Contributions - MirahezeBot","privacy":"Privacy - MirahezeBot","terms":"Terms - MirahezeBot"},"font-awesome-url":"Font-Awesome","Font-awesome-path":"Font-Awesome","canonical-prefix":"https://mirahezebots.org/","rendertemplates":{"navbar":"templates/navbar.html","footer":"templates/footer.html","head":"templates/head.html"}}  # noqa


def test_about_page():
    """Tests about page."""
    content = display_content('about', jp.createdict('./config.json'))
    assert 'IRC' in content  # nosec


def test_title_xss():
    """Check title construction doesn't make an XSS."""
    content = display_content('index', XSS)
    assert '<title></title><img src=1 href=1 onerror="javascript:alert(1)"></img></title>' not in content  # noqa: E501 nosec
    assert '<title>&lt;/title&gt;&lt;img src=1 href=1 onerror=&#34;javascript:alert(1)&#34;&gt;&lt;/img&gt;</title>' in content  # noqa: E501 nosec


def test_docs():
    """Tests docs page."""
    content = display_content('documentation.html', jp.createdict('./config.json'))
    assert 'Commands' in content  # nosec
