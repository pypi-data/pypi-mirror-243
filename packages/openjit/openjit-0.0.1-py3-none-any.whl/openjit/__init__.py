#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from os import makedirs

from flask import Flask

from openjit.lane import lane
from openjit.card import card
from openjit.kanban import kanban
from openjit.db import init_app

__version__ = "0.0.1"


def create_app(test_config=None):
    """
    Create and configure an instance of the Flask
    application.
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        MAX_CONTENT_LENGTH=16000000,
        DATABASE=path.join(
            app.instance_path,
            "openjit.sqlite",
        ),
    )
    if test_config is None:
        app.config.from_pyfile(
            "config.py",
            silent=True,
        )
    else:
        app.config.update(test_config)
    try:
        makedirs(app.instance_path)
    except OSError:
        pass
    init_app(app)
    app.register_blueprint(lane)
    app.register_blueprint(card)
    app.register_blueprint(kanban)
    return app
