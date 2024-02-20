"""
Summary Footnotes
-------------

Fix handling of footnote links inside article summaries.
Option to either remove them or make them link to the article page.
Also never show the footnotes themselves in the summary.
"""

from pelican import contents
from pelican import signals
from bs4 import BeautifulSoup
from six import text_type


def initialized(pelican):
    orig_summary = contents.Content.summary
    contents.Content.summary = \
        property(lambda instance: get_transformed(instance, orig_summary),
                 orig_summary.fset, orig_summary.fdel,
                 orig_summary.__doc__)

    orig_content = contents.Content.content
    contents.Content.content = \
        property(lambda instance: get_transformed(instance, orig_content),
                 orig_content.fset, orig_content.fdel,
                 orig_content.__doc__)


def transform(value, article_url, site_url):
    value = BeautifulSoup(value, 'html.parser')
    all_links = value.findAll('a')
    for link in all_links:
        if link['href'][0] == '#':
            link['href'] = "%s/%s%s" % (site_url,
                                        article_url,
                                        link['href'])
    return text_type(value)


def get_transformed(self, orig):
    value = orig.fget(self)
    new_value = transform(value, self.url, self.settings['SITEURL'])
    if new_value is not None:
        return new_value
    else:
        return value


def register():
    signals.initialized.connect(initialized)
