import collections
import pprint

import pendulum

# TODO from micropub.readability import Readability
import web
from mf import discover_post_type
from web.framework import templates
from webagt import Document
from webint_live import app as live_app
from webint_posts import app as posts_app
from webint_system import get_key, get_onion

__all__ = [
    "discover_post_type",
    "pformat",
    "pendulum",
    "tx",
    "post_mkdn",
    # TODO "Readability",
    "get_first",
    "get_months",
    "get_posts",
    "get_categories",
    "Document",
    "livestream",
    "get_key",
    "get_onion",
    "render_breadcrumbs",
]

tx = web.tx
livestream = live_app.view.stream
render_breadcrumbs = templates.render_breadcrumbs


def pformat(obj):
    return f"<pre>{pprint.pformat(obj)}</pre>"


def post_mkdn(content):
    return web.mkdn(content)  # XXX , globals=micropub.markdown_globals)


def get_first(obj, p):
    return obj.get(p, [""])[0]


def get_months():
    months = collections.defaultdict(collections.Counter)
    for post in posts_app.model.get_posts():
        published = post["published"][0]
        months[published.year][published.month] += 1
    return months


def get_posts():
    return posts_app.model.get_posts()


def get_categories():
    return posts_app.model.get_categories()
