#!/usr/bin/env python
# coding: utf-8

from floo import emacs_handler
from floo.common import migrations
from floo.common import reactor
from floo.common import msg
from floo.common import utils
from floo.common import shared as G


def cb(port):
    print('Now listening on %s' % port)


def main():
    G.__VERSION__ = '0.03'
    G.__PLUGIN_VERSION__ = '1.0'
    utils.reload_settings()

    floo_log_level = 'msg'
    if G.DEBUG:
        floo_log_level = 'debug'
    msg.LOG_LEVEL = msg.LOG_LEVELS.get(floo_log_level.upper(), msg.LOG_LEVELS['MSG'])
    migrations.rename_floobits_dir()
    migrations.migrate_symlinks()

    r = reactor.install(20)
    emacs = emacs_handler.EmacsHandler()
    _, port = r.listen(emacs)
    utils.set_timeout(cb, 100, port)
    r.block()

if __name__ == '__main__':
    main()
