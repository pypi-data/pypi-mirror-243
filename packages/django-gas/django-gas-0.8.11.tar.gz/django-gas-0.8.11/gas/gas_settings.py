from django.conf import settings


TITLE = getattr(settings, 'GAS_TITLE', 'GAS')
LOGO = getattr(settings, 'GAS_LOGO', 'gas/css/img/logo.svg')

MEDIA = getattr(settings, 'GAS_MEDIA', {
    'css': [
        'vendor/font-awesome/css/all.css',
        'vendor/select2/css/select2.css',
        'gas/css/gas.css',
    ],
    'js': [
        'vendor/jquery-3.6.4.min.js',
        'vendor/jquery.formset.js',
        'vendor/select2/js/select2.full.min.js',
        'gas/js/add_popups.js',
        'gas/js/gas.js',
    ],
})

EXTRA_MEDIA = getattr(settings, 'GAS_EXTRA_MEDIA', None)

IMAGE_PREVIEW_WIDTH = getattr(settings, 'IMAGE_PREVIEW_WIDTH', 240)
