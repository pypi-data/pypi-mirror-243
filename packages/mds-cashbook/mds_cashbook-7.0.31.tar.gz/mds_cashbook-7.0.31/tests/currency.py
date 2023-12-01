# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import with_transaction
from trytond.pool import Pool
from trytond.modules.cashbook.model import CACHEKEY_CURRENCY, ENABLE_CACHE
from datetime import date
from decimal import Decimal
import time


class CurrencyTestCase(object):
    """ test currency
    """
    @with_transaction()
    def test_currency_update_cache(self):
        """ add/update/del rate of currency, check cache
        """
        pool = Pool()
        MemCache = pool.get('cashbook.memcache')
        Currency = pool.get('currency.currency')
        CurrencyRate = pool.get('currency.currency.rate')

        self.prep_config()
        self.prep_company()

        MemCache._cashbook_value_cache.clear_all()
        currency, = Currency.search([('name', '=', 'usd')])

        cache_key = CACHEKEY_CURRENCY % currency.id

        # cache should be empty
        self.assertEqual(MemCache.read_value(cache_key), None)
        CurrencyRate.delete(currency.rates)
        self.assertEqual(len(currency.rates), 0)

        # add rate
        Currency.write(*[
            [currency],
            {
                'rates': [('create', [{
                    'date': date(2022, 5, 1),
                    'rate': Decimal('1.05'),
                    }])],
            }])
        self.assertEqual(len(currency.rates), 1)

        # expected key
        value = '%d-c%s' % (
            currency.rates[0].id,
            str(currency.rates[0].create_date.timestamp()))
        if ENABLE_CACHE is True:
            self.assertEqual(MemCache.read_value(cache_key), value)
        else:
            self.assertEqual(MemCache.read_value(cache_key), None)
        time.sleep(1.0)

        Currency.write(*[
            [currency],
            {
                'rates': [
                    ('write', [currency.rates[0].id], {
                        'rate': Decimal('1.06'),
                    })],
            }])
        self.assertEqual(len(currency.rates), 1)

        value = '%d-w%s' % (
            currency.rates[0].id,
            str(currency.rates[0].write_date.timestamp()))
        if ENABLE_CACHE is True:
            self.assertEqual(MemCache.read_value(cache_key), value)
        else:
            self.assertEqual(MemCache.read_value(cache_key), None)

        Currency.write(*[
            [currency],
            {
                'rates': [('delete', [currency.rates[0].id])],
            }])
        self.assertEqual(MemCache.read_value(cache_key), None)

# end CurrencyTestCase
