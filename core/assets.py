"""Gerenciamento de assets."""

import django_assets

css_files = [
    'css/base.css',
]
css = django_assets.Bundle(*css_files, filters='cssmin', output='css/bundle.min.css')

django_assets.register('css_all', css)
