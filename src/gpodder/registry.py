#
# gpodder.registry - Central hub for exchanging plugin resolvers (2014-03-09)
# Copyright (c) 2014, Thomas Perl <m@thp.io>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

import logging

logger = logging.getLogger(__name__)


class Resolver(object):
    def __init__(self, name, description):
        self._name = name
        self._description = description
        self._resolvers = []

    def resolve(self, item, default, *args):
        for resolver in self._resolvers:
            result = resolver(item, *args)
            if result is not None:
                logger.info('{} resolved by {}: {} -> {}'.format(self._name, self._info(resolver),
                                                                 default, result))
                return result

        return default

    def each(self, *args):
        for resolver in self._resolvers:
            result = resolver(*args)
            if result is not None:
                yield result

    def register(self, func):
        logger.debug('Registering {} resolver: {}'.format(self._name, func))
        self._resolvers.append(func)
        return func

    def _info(self, resolver):
        return '%s from %s' % (resolver.__name__, resolver.__module__)

    def _dump(self, indent=''):
        print('== {} ({}) =='.format(self._name, self._description))
        print('\n'.join('%s- %s' % (indent, self._info(resolver)) for resolver in self._resolvers))
        print()

RESOLVER_NAMES = {'cover_art': 'Resolve the real cover art URL of an episode',
                  'download_url': 'Resolve the real download URL of an episode',
                  'episode_basename': 'Resolve a good, unique download filename for an episode',
                  'podcast_title': 'Resolve a good title for a podcast',
                  'content_type': 'Resolve the content type (audio, video) of an episode',
                  'feed_handler': 'Handle parsing of a feed',
                  'fallback_feed_handler': 'Handle parsing of a feed (catch-all)',
                  'url_shortcut': 'Expand shortcuts when adding a new URL'}

LOCALS = locals()

for name, description in RESOLVER_NAMES.items():
    LOCALS[name] = Resolver(name, description)


def dump(module_dict=LOCALS):
    for name in RESOLVER_NAMES:
        module_dict[name]._dump(' ')
