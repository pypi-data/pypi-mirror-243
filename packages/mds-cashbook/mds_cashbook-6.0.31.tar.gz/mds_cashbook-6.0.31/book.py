# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import Workflow, ModelView, ModelSQL, fields, Check, tree
from trytond.pyson import Eval, Or, Bool, Id, Len
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.report import Report
from trytond.config import config
from decimal import Decimal
from datetime import date
from sql.aggregate import Sum
from sql.conditionals import Case
from .model import order_name_hierarchical, sub_ids_hierarchical, \
    AnyInArray, CACHEKEY_CURRENCY


# enable/disable caching of cachekey for 'currency.rate'
if config.get(
            'cashbook', 'cache_currency', default='yes'
        ).lower() in ['yes', '1', 'true']:
    ENA_CURRKEY = True
else:
    ENA_CURRKEY = False


STATES = {
    'readonly': Eval('state', '') != 'open',
    }
DEPENDS = ['state']

# states in case of 'btype'!=None
STATES2 = {
    'readonly': Or(
            Eval('state', '') != 'open',
            ~Bool(Eval('btype')),
        ),
    'invisible': ~Bool(Eval('btype')),
    }
STATES3 = {}
STATES3.update(STATES2)
STATES3['required'] = ~STATES2['invisible']
DEPENDS2 = ['state', 'btype']

sel_state_book = [
    ('open', 'Open'),
    ('closed', 'Closed'),
    ('archive', 'Archive'),
    ]


class Book(tree(separator='/'), Workflow, ModelSQL, ModelView):
    'Cashbook'
    __name__ = 'cashbook.book'

    company = fields.Many2One(
        string='Company', model_name='company.company',
        required=True, select=True, ondelete="RESTRICT")
    name = fields.Char(
        string='Name', required=True, states=STATES, depends=DEPENDS)
    description = fields.Text(
        string='Description', states=STATES, depends=DEPENDS)
    btype = fields.Many2One(
        string='Type', select=True,
        help='A cash book with type can contain postings. ' +
        'Without type is a view.',
        model_name='cashbook.type', ondelete='RESTRICT',
        states={
            'readonly': Or(
                    STATES['readonly'],
                    Len(Eval('lines')) > 0,
                ),
        }, depends=DEPENDS+['lines'])
    feature = fields.Function(fields.Char(
        string='Feature', readonly=True,
        states={'invisible': True}), 'on_change_with_feature')
    owner = fields.Many2One(
        string='Owner', required=True, select=True,
        model_name='res.user', ondelete='SET NULL',
        states=STATES, depends=DEPENDS)
    reviewer = fields.Many2One(
        string='Reviewer', select=True,
        help='Group of users who have write access to the cashbook.',
        model_name='res.group', ondelete='SET NULL',
        states=STATES, depends=DEPENDS)
    observer = fields.Many2One(
        string='Observer', select=True,
        help='Group of users who have read-only access to the cashbook.',
        model_name='res.group', ondelete='SET NULL',
        states=STATES, depends=DEPENDS)
    lines = fields.One2Many(
        string='Lines', field='cashbook',
        model_name='cashbook.line',
        states=STATES, depends=DEPENDS)
    reconciliations = fields.One2Many(
        string='Reconciliations',
        field='cashbook', model_name='cashbook.recon',
        states=STATES2, depends=DEPENDS2)
    number_sequ = fields.Many2One(
        string='Line numbering',
        help='Number sequence for numbering of the cash book lines.',
        model_name='ir.sequence',
        domain=[
            ('sequence_type', '=',
                Id('cashbook', 'sequence_type_cashbook_line')),
            ['OR',
                ('company', '=', None),
                ('company', '=', Eval('company', -1))],
            ],
        states=STATES3, depends=DEPENDS2+['company'])
    number_atcheck = fields.Boolean(
        string="number when 'Checking'",
        help="The numbering of the lines is done in the step Check. " +
        "If the check mark is inactive, this happens with Done.",
        states=STATES2, depends=DEPENDS2)
    start_date = fields.Date(
        string='Initial Date',
        states={
            'readonly': Or(
                STATES2['readonly'],
                Len(Eval('lines')) > 0,
                ),
            'invisible': STATES2['invisible'],
            'required': ~STATES2['invisible'],
        }, depends=DEPENDS2+['lines'])
    balance = fields.Function(fields.Numeric(
        string='Balance',
        readonly=True, depends=['currency_digits'],
        help='Balance of bookings to date',
        digits=(16, Eval('currency_digits', 2))),
        'get_balance_cashbook', searcher='search_balance')
    balance_all = fields.Function(fields.Numeric(
        string='Total balance',
        readonly=True, depends=['currency_digits'],
        help='Balance of all bookings',
        digits=(16, Eval('currency_digits', 2))),
        'get_balance_cashbook', searcher='search_balance')

    balance_ref = fields.Function(fields.Numeric(
        string='Balance (Ref.)',
        help='Balance in company currency',
        readonly=True, digits=(16, Eval('company_currency_digits', 2)),
        states={
            'invisible': ~Bool(Eval('company_currency')),
        }, depends=['company_currency_digits', 'company_currency']),
        'get_balance_cashbook')
    company_currency = fields.Function(fields.Many2One(
        readonly=True,
        string='Company Currency', states={'invisible': True},
        model_name='currency.currency'),
        'on_change_with_company_currency')
    company_currency_digits = fields.Function(fields.Integer(
        string='Currency Digits (Ref.)', readonly=True),
        'on_change_with_currency_digits')

    currency = fields.Many2One(
        string='Currency', select=True,
        model_name='currency.currency',
        states={
            'readonly': Or(
                STATES2['readonly'],
                Len(Eval('lines', [])) > 0,
                ),
        }, depends=DEPENDS2+['lines'])
    currency_digits = fields.Function(fields.Integer(
        string='Currency Digits',
        readonly=True), 'on_change_with_currency_digits')
    state = fields.Selection(
        string='State', required=True,
        readonly=True, selection=sel_state_book)
    state_string = state.translated('state')

    parent = fields.Many2One(
        string="Parent",
        model_name='cashbook.book', ondelete='RESTRICT')
    childs = fields.One2Many(
        string='Children', field='parent',
        model_name='cashbook.book')

    @classmethod
    def __register__(cls, module_name):
        super(Book, cls).__register__(module_name)

        table = cls.__table_handler__(module_name)
        table.drop_column('start_balance')
        table.drop_column('left')
        table.drop_column('right')

    @classmethod
    def __setup__(cls):
        super(Book, cls).__setup__()
        cls._order.insert(0, ('rec_name', 'ASC'))
        cls._order.insert(0, ('state', 'ASC'))
        t = cls.__table__()
        cls._sql_constraints.extend([
            ('state_val',
                Check(t, t.state.in_(['open', 'closed', 'archive'])),
                'cashbook.msg_book_wrong_state_value'),
            ])
        cls._transitions |= set((
                ('open', 'closed'),
                ('closed', 'open'),
                ('closed', 'archive'),
            ))
        cls._buttons.update({
            'wfopen': {
                'invisible': Eval('state', '') != 'closed',
                'depends': ['state'],
                },
            'wfclosed': {
                'invisible': Eval('state') != 'open',
                'depends': ['state'],
                },
            'wfarchive': {
                'invisible': Eval('state') != 'closed',
                'depends': ['state'],
                },
            })

    @classmethod
    def default_number_atcheck(cls):
        return True

    @classmethod
    def default_currency(cls):
        """ currency of company
        """
        Company = Pool().get('company.company')

        company = cls.default_company()
        if company:
            company = Company(company)
            if company.currency:
                return company.currency.id

    @staticmethod
    def default_company():
        return Transaction().context.get('company') or None

    @classmethod
    def default_start_date(cls):
        """ today
        """
        IrDate = Pool().get('ir.date')
        return IrDate.today()

    @classmethod
    def default_state(cls):
        return 'open'

    @classmethod
    def default_owner(cls):
        """ default: current user
        """
        return Transaction().user

    @staticmethod
    def order_state(tables):
        """ edit = 0, check/done = 1
        """
        Book2 = Pool().get('cashbook.book')
        tab_book = Book2.__table__()
        table, _ = tables[None]

        query = tab_book.select(
                Case(
                    (tab_book.state == 'open', 0),
                    else_=1),
                where=tab_book.id == table.id)
        return [query]

    @staticmethod
    def order_rec_name(tables):
        """ order by pos
            a recursive sorting
        """
        return order_name_hierarchical('cashbook.book', tables)

    def get_rec_name(self, name):
        """ name, balance, state
        """
        recname = super(Book, self).get_rec_name(name)
        if self.btype:
            return '%(name)s | %(balance)s %(symbol)s | %(state)s' % {
                'name': recname or '-',
                'balance': Report.format_number(
                    self.balance or 0.0, None,
                    digits=getattr(self.currency, 'digits', 2)),
                'symbol': getattr(self.currency, 'symbol', '-'),
                'state': self.state_string,
                }
        return recname

    @classmethod
    def get_balance_of_cashbook_sql(cls):
        """ sql for balance of a single cashbook
        """
        pool = Pool()
        Line = pool.get('cashbook.line')
        Book2 = pool.get('cashbook.book')
        IrDate = pool.get('ir.date')
        tab_line = Line.__table__()
        tab_book = Book2.__table__()
        context = Transaction().context

        query_date = context.get('date', IrDate.today())

        # deny invalid date in context
        if isinstance(query_date, str):
            try:
                date.fromisoformat(query_date)
            except Exception:
                query_date = IrDate.today()

        query = tab_book.join(
                tab_line,
                condition=tab_book.id == tab_line.cashbook,
            ).select(
                tab_line.cashbook,
                tab_book.currency,
                Sum(Case(
                    (tab_line.date <= query_date,
                        tab_line.credit - tab_line.debit),
                    else_=Decimal('0.0'),
                )).as_('balance'),
                Sum(tab_line.credit - tab_line.debit).as_('balance_all'),
                group_by=[tab_line.cashbook, tab_book.currency],
            )
        return (query, tab_line)

    @staticmethod
    def order_balance(tables):
        """ order by balance
        """
        Book2 = Pool().get('cashbook.book')
        (tab_book, tab2) = Book2.get_balance_of_cashbook_sql()
        table, _ = tables[None]

        query = tab_book.select(
            tab_book.balance,
            where=tab_book.cashbook == table.id)
        return [query]

    @staticmethod
    def order_balance_all(tables):
        """ order by balance-all
        """
        Book2 = Pool().get('cashbook.book')
        (tab_book, tab2) = Book2.get_balance_of_cashbook_sql()
        table, _ = tables[None]

        query = tab_book.select(
            tab_book.balance_all,
            where=tab_book.cashbook == table.id)
        return [query]

    @classmethod
    def search_balance(cls, name, clause):
        """ search in 'balance'
        """
        (tab_line, tab2) = cls.get_balance_of_cashbook_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        query = tab_line.select(
                tab_line.cashbook,
                where=Operator(
                    getattr(tab_line, name), clause[2]),
            )
        return [('id', 'in', query)]

    @classmethod
    def get_balance_cashbook(cls, cashbooks, names):
        """ get balance of cashbook
        """
        pool = Pool()
        Book2 = pool.get('cashbook.book')
        Currency = pool.get('currency.currency')
        Company = pool.get('company.company')
        IrDate = pool.get('ir.date')
        MemCache = pool.get('cashbook.memcache')
        tab_book = Book2.__table__()
        tab_comp = Company.__table__()
        cursor = Transaction().connection.cursor()
        context = Transaction().context

        result = {
            x: {y.id: Decimal('0.0') for y in cashbooks}
            for x in ['balance', 'balance_all', 'balance_ref']}

        # deny invalid date in context
        query_date = context.get('date', IrDate.today())
        if isinstance(query_date, str):
            try:
                date.fromisoformat(query_date)
            except Exception:
                query_date = IrDate.today()

        cache_keys = {
            x.id: MemCache.get_key_by_record(
                name='get_balance_cashbook',
                record=x,
                query=[{
                    'model': 'cashbook.line',
                    'query': [('cashbook.parent', 'child_of', [x.id])],
                    }, {
                    'model': 'currency.currency.rate',
                        'query': [('currency.id', '=', x.currency.id)],
                        'cachekey' if ENA_CURRKEY
                        else 'disabled': CACHEKEY_CURRENCY % x.currency.id,
                    }, ],
                addkeys=[query_date.isoformat()])
            for x in cashbooks}

        # read from cache
        (todo_cashbook, result) = MemCache.read_from_cache(
            cashbooks, cache_keys, names, result)
        if len(todo_cashbook) == 0:
            return result

        # query balances of cashbooks and sub-cashbooks
        with Transaction().set_context({
                'date': query_date}):
            (tab_line, tab2) = cls.get_balance_of_cashbook_sql()
            tab_subids = sub_ids_hierarchical('cashbook.book')
            query = tab_book.join(
                    tab_subids,
                    condition=tab_book.id == tab_subids.parent,
                ).join(
                    tab_comp,
                    condition=tab_book.company == tab_comp.id,
                ).join(
                    tab_line,
                    condition=tab_line.cashbook == AnyInArray(
                        tab_subids.subids),
                ).select(
                    tab_book.id,
                    tab_book.currency.as_('to_currency'),
                    tab_line.currency.as_('from_currency'),
                    tab_comp.currency.as_('company_currency'),
                    Sum(tab_line.balance).as_('balance'),
                    Sum(tab_line.balance_all).as_('balance_all'),
                    group_by=[
                        tab_book.id, tab_line.currency, tab_comp.currency],
                    where=tab_book.id.in_([x.id for x in todo_cashbook]),
                )
            cursor.execute(*query)
            records = cursor.fetchall()

            for record in records:
                result['balance'][record[0]] += Currency.compute(
                        record[2], record[4], record[1])
                result['balance_all'][record[0]] += Currency.compute(
                        record[2], record[5], record[1])
                result['balance_ref'][record[0]] += Currency.compute(
                        record[2], record[5], record[3])

        MemCache.store_result(cashbooks, cache_keys, result, todo_cashbook)
        return result

    @fields.depends('btype')
    def on_change_with_feature(self, name=None):
        """ get feature-set
        """
        if self.btype:
            return self.btype.feature

    @fields.depends('currency')
    def on_change_with_currency_digits(self, name=None):
        """ currency of cashbook
        """
        if self.currency:
            return self.currency.digits
        else:
            return 2

    @fields.depends('company', 'currency', 'btype')
    def on_change_with_company_currency(self, name=None):
        """ get company-currency if its different from current
            cashbook-currency, disable if book is a view
        """
        if self.company:
            if self.currency:
                if self.btype:
                    if self.company.currency.id != self.currency.id:
                        return self.company.currency.id

    @classmethod
    @ModelView.button
    @Workflow.transition('open')
    def wfopen(cls, books):
        """ open cashbook
        """
        pass

    @classmethod
    @ModelView.button
    @Workflow.transition('closed')
    def wfclosed(cls, books):
        """ cashbook is closed
        """
        pass

    @classmethod
    @ModelView.button
    @Workflow.transition('archive')
    def wfarchive(cls, books):
        """ cashbook is archived
        """
        pass

    @classmethod
    def write(cls, *args):
        """ deny update if book is not 'open'
        """
        ConfigUser = Pool().get('cashbook.configuration_user')

        actions = iter(args)
        to_write_config = []
        for books, values in zip(actions, actions):
            for book in books:
                # deny btype-->None if lines not empty
                if 'btype' in values.keys():
                    if (values['btype'] is None) and (len(book.lines) > 0):
                        raise UserError(gettext(
                            'cashbook.msg_book_btype_with_lines',
                            cbname=book.rec_name,
                            numlines=len(book.lines)))

                if book.state != 'open':
                    # allow state-update, if its the only action
                    if not (('state' in values.keys()) and
                            (len(values.keys()) == 1)):
                        raise UserError(gettext(
                            'cashbook.msg_book_deny_write',
                            bookname=book.rec_name,
                            state_txt=book.state_string))

                # if owner changes, remove book from user-config
                if 'owner' in values.keys():
                    if book.owner.id != values['owner']:
                        for x in [
                                'defbook', 'book1', 'book2', 'book3',
                                'book4', 'book5']:
                            cfg1 = ConfigUser.search([
                                    ('iduser', '=', book.owner.id),
                                    ('%s.id' % x, '=', book.id)])
                            if len(cfg1) > 0:
                                to_write_config.extend([cfg1, {x: None}])
        super(Book, cls).write(*args)

        if len(to_write_config) > 0:
            ConfigUser.write(*to_write_config)

    @classmethod
    def delete(cls, books):
        """ deny delete if book has lines
        """
        for book in books:
            if (len(book.lines) > 0) and (book.state != 'archive'):
                raise UserError(gettext(
                    'cashbook.msg_book_deny_delete',
                    bookname=book.rec_name,
                    booklines=len(book.lines)))
        super(Book, cls).delete(books)

# end Book
