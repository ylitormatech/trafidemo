"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.css',
    'libs/font-awesome4/css/font-awesome.css',
    'libs/tether/css/tether.css',
    'libs/tether-tooltip/dist/css/tooltip-theme-arrows.css',
    'libs/tether-tooltip/dist/css/tooltip-theme-twipsy.css',
    'css/style.css',
    filters='cssmin',
    output='public/css/common.css'
)

js = Bundle(
    'libs/jQuery/dist/jquery.js',

    'libs/tether/js/utils.js',
    'libs/tether/js/tether.js',
    'libs/tether-drop/dist/js/drop.js',
    'libs/tether-tooltip/dist/js/tooltip.js',
    'libs/bootstrap/dist/js/bootstrap.js',
    'libs/angular/angular.js',
    'libs/angular-route/angular-route.js',
    # 'libs/angular-tether/dist/angular-tether.js',
    'js/angular1demo/controllers.js',
    'js/angular1demo/services.js',
    'js/angular1demo/app.js',

    'js/react/react.js',

    'libs/d3/d3.min.js',
    'js/plugins.js',

    filters='jsmin',
    output='public/js/common.js'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
