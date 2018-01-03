"""Gerenciamento de assets."""

import django_assets

css_files = [
    'css/app/*.css',
]
css = django_assets.Bundle(*css_files, filters='cssmin', output='css/bundle.min.css')

django_assets.register('css_all', css)

js_files = [
    'js/app.js',
    'app/main.js',
]
js = django_assets.Bundle(*js_files, filters='uglifyjs', output='js/bundle.min.js')

django_assets.register('js_all', js)
