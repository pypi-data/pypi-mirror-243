# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.nereid_cart_b2c.tests.test_nereid_cart_b2c import (
        create_countries, create_pricelists, create_product_template,
        create_website, suite)
except ImportError:
    from .test_nereid_cart_b2c import (
        create_countries, create_pricelists, create_product_template,
        create_website, suite)

__all__ = ['suite', 'create_website', 'create_countries',
    'create_pricelists', 'create_product_template']
