# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta
from .model import CACHEKEY_CURRENCY


class CurrencyRate(metaclass=PoolMeta):
    __name__ = 'currency.currency.rate'

    @classmethod
    def create(cls, vlist):
        """ update cache-value
        """
        MemCache = Pool().get('cashbook.memcache')

        records = super(CurrencyRate, cls).create(vlist)
        for rate in records:
            MemCache.record_update(CACHEKEY_CURRENCY % rate.currency.id, rate)
        return records

    @classmethod
    def write(cls, *args):
        """ update cache-value
        """
        MemCache = Pool().get('cashbook.memcache')

        super(CurrencyRate, cls).write(*args)

        actions = iter(args)
        for rates, values in zip(actions, actions):
            for rate in rates:
                MemCache.record_update(
                    CACHEKEY_CURRENCY % rate.currency.id, rate)

    @classmethod
    def delete(cls, records):
        """ set cache to None
        """
        MemCache = Pool().get('cashbook.memcache')

        for record in records:
            MemCache.record_update(CACHEKEY_CURRENCY % record.currency.id, None)
        super(CurrencyRate, cls).delete(records)

# end
