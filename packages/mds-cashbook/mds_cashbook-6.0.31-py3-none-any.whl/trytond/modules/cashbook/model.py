# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import MultiValueMixin, ValueMixin, fields, Unique, Model
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.cache import MemoryCache
from trytond.config import config
from datetime import timedelta
from decimal import Decimal
from sql import With
from sql.functions import Function
from sql.conditionals import Coalesce
import copy

if config.get('cashbook', 'memcache', default='yes').lower() \
        in ['yes', '1', 'true']:
    ENABLE_CACHE = True
else:
    ENABLE_CACHE = False

if config.get('cashbook', 'sync', default='yes').lower() \
        in ['yes', '1', 'true']:
    ENABLE_CACHESYNC = True
else:
    ENABLE_CACHESYNC = False

CACHEKEY_CURRENCY = 'currency-%s'


class ArrayAgg(Function):
    """input values, including nulls, concatenated into an array.
    """
    __slots__ = ()
    _function = 'ARRAY_AGG'

# end ArrayAgg


class ArrayAppend(Function):
    """ sql: array_append
    """
    __slots__ = ()
    _function = 'ARRAY_APPEND'

# end ArrayApppend


class ArrayToString(Function):
    """ sql: array_to_string
    """
    __slots__ = ()
    _function = 'ARRAY_TO_STRING'

# end ArrayToString


class AnyInArray(Function):
    """ sql: array_to_string
    """
    __slots__ = ()
    _function = 'ANY'

    def __str__(self):
        return self._function + '(' + ', '.join(
            map(self._format, self.args)) + '::int[])'

# end AnyInArray


class Array(Function):
    """ sql: array-type
    """
    __slots__ = ()
    _function = 'ARRAY'

    def __str__(self):
        return self._function + '[' + ', '.join(
            map(self._format, self.args)) + ']'

# end Array


class MemCache(Model):
    """ store values to cache
    """
    __name__ = 'cashbook.memcache'

    _cashbook_value_cache = MemoryCache(
        'cashbook.book.valuecache',
        context=False,
        duration=timedelta(seconds=60*60*4))

    @classmethod
    def read_value(cls, cache_key):
        """ read values from cache
        """
        if ENABLE_CACHE is False:
            return None
        return copy.deepcopy(cls._cashbook_value_cache.get(cache_key))

    @classmethod
    def store_result(cls, records, cache_keys, values, skip_records=[]):
        """ store result to cache
        """
        if ENABLE_CACHE is False:
            return
        for record in records:
            if record not in skip_records:
                continue
            data = {
                x: values[x][record.id]
                for x in values.keys() if record.id in values[x].keys()}
            cls._cashbook_value_cache.set(
                cache_keys[record.id], copy.deepcopy(data))
        if ENABLE_CACHESYNC is True:
            cls._cashbook_value_cache.sync(Transaction())

    @classmethod
    def store_value(cls, cache_key, values):
        """ store values to cache
        """
        if ENABLE_CACHE is False:
            return
        cls._cashbook_value_cache.set(cache_key, copy.deepcopy(values))

    @classmethod
    def read_from_cache(cls, records, cache_keys, names, result):
        """ get stored values from memcache
        """
        if ENABLE_CACHE is False:
            return (records, result)

        todo_records = []
        for record in records:
            values = copy.deepcopy(cls.read_value(cache_keys[record.id]))
            if values:
                for name in names:
                    if name not in values.keys():
                        continue
                    if values[name] is None:
                        continue
                    if result[name][record.id] is None:
                        result[name][record.id] = Decimal('0.0')
                    result[name][record.id] += values[name]
            else:
                todo_records.append(record)
        return (todo_records, result)

    @classmethod
    def get_key_by_record(cls, name, record, query, addkeys=[]):
        """ read records to build a cache-key
        """
        pool = Pool()
        cursor = Transaction().connection.cursor()

        if ENABLE_CACHE is False:
            return '-'

        fname = [name, str(record.id)]
        fname.extend(addkeys)

        # query the last edited record for each item in 'query'
        for line in query:
            if len(line.keys()) == 0:
                continue

            if 'cachekey' in line.keys():
                key = cls.read_value(line['cachekey'])
                if key:
                    fname.append(key)
                    continue

            Model = pool.get(line['model'])
            tab_model = Model.__table__()

            tab_query = Model.search(line['query'], query=True)
            qu1 = tab_model.join(
                    tab_query,
                    condition=tab_query.id == tab_model.id,
                ).select(
                    tab_model.id,
                    tab_model.write_date,
                    tab_model.create_date,
                    limit=1,
                    order_by=[
                        Coalesce(
                            tab_model.write_date, tab_model.create_date).desc,
                        tab_model.id.desc,
                        ],
                )
            cursor.execute(*qu1)
            records = cursor.fetchall()
            if len(records) > 0:
                fname.append(cls.genkey(
                    records[0][0],
                    records[0][1],
                    records[0][2],
                    ))
            else:
                fname.append('0')

            if 'cachekey' in line.keys():
                key = cls.store_value(line['cachekey'], fname[-1])
        return '-'.join(fname)

    @classmethod
    def genkey(cls, id_record, write_date, create_date):
        """ get key as text
        """
        date_val = write_date if write_date is not None else create_date
        return '-'.join([
            str(id_record),
            '%s%s' % (
                'w' if write_date is not None else 'c',
                date_val.timestamp() if date_val is not None else '-'),
            ])

    @classmethod
    def record_update(cls, cache_key, record):
        """ update cache-value
        """
        if ENABLE_CACHE is False:
            return
        cls.store_value(
            cache_key,
            cls.genkey(record.id, record.write_date, record.create_date)
            if record is not None else None)

# end mem_cache


def sub_ids_hierarchical(model_name):
    """ get table with id and sub-ids
    """
    Model2 = Pool().get(model_name)
    tab_mod = Model2.__table__()
    tab_mod2 = Model2.__table__()

    lines = With('parent', 'id', recursive=True)
    lines.query = tab_mod.select(
            tab_mod.id, tab_mod.id,
        ) | tab_mod2.join(
            lines,
            condition=lines.id == tab_mod2.parent,
        ).select(lines.parent, tab_mod2.id)
    lines.query.all_ = True

    query = lines.select(
            lines.parent,
            ArrayAgg(lines.id).as_('subids'),
            group_by=[lines.parent],
            with_=[lines])
    return query


def order_name_hierarchical(model_name, tables):
    """ order by pos
        a recursive sorting
    """
    Model2 = Pool().get(model_name)
    tab_mod = Model2.__table__()
    tab_mod2 = Model2.__table__()
    table, _ = tables[None]

    lines = With('id', 'name', 'name_path', recursive=True)
    lines.query = tab_mod.select(
            tab_mod.id, tab_mod.name, Array(tab_mod.name),
            where=tab_mod.parent == None,
        )
    lines.query |= tab_mod2.join(
            lines,
            condition=lines.id == tab_mod2.parent,
        ).select(
            tab_mod2.id,
            tab_mod2.name,
            ArrayAppend(lines.name_path, tab_mod2.name),
        )
    lines.query.all_ = True

    query = lines.select(
            ArrayToString(lines.name_path, '/').as_('rec_name'),
            where=table.id == lines.id,
            with_=[lines])
    return [query]


class UserValueMixin(ValueMixin):
    iduser = fields.Many2One(
        model_name='res.user', string="User",
        select=True, ondelete='CASCADE', required=True)

    @classmethod
    def __setup__(cls):
        super(UserValueMixin, cls).__setup__()
        tab_val = cls.__table__()
        cls._sql_constraints.extend([
            ('val_uniq',
                Unique(tab_val, tab_val.iduser),
                'cashbook.msg_setting_already_exists'),
            ])

# end UserValueMixin


class UserMultiValueMixin(MultiValueMixin):

    def updt_multivalue_pattern(self, pattern):
        """ add values to pattern
        """
        pattern.setdefault('iduser', Transaction().user)
        return pattern

    def get_multivalue(self, name, **pattern):
        Value = self.multivalue_model(name)
        if issubclass(Value, UserValueMixin):
            pattern = self.updt_multivalue_pattern(pattern)
        return super(UserMultiValueMixin, self).get_multivalue(name, **pattern)

    def set_multivalue(self, name, value, **pattern):
        Value = self.multivalue_model(name)
        if issubclass(Value, UserValueMixin):
            pattern = self.updt_multivalue_pattern(pattern)
        return super(
            UserMultiValueMixin, self).set_multivalue(name, value, **pattern)

# end UserMultiValueMixin
