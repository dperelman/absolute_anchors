"""
Absolute Anchors
-------------

Fix handling of anchor links when viewing an article not on its page.
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

    orig_update_content = contents.Content._update_content
    contents.Content._update_content =\
        lambda instance, content, site_url: \
        transform(orig_update_content(instance, content, site_url),
                  instance.url,
                  site_url)


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
