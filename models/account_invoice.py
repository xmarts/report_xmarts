## -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools
from odoo.tools.xml_utils import _check_with_xsd
from odoo.tools import DEFAULT_SERVER_TIME_FORMAT
from odoo.exceptions import UserError
from datetime import datetime, date, time,timedelta
import logging
_logger = logging.getLogger(__name__)
tipo_destino=['800 INTERNACIONAL','800 NACIONAL','LD INTERNACIONAL','LD INTERNACIONAL CELULAR',
'LD NACIONAL','LD NACIONAL CELULAR','LOCAL','CELULAR']

class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    invoice_phone = fields.Boolean(string='Factura Telefónica', default=False)

    @api.model
    def _getlinessubscription(self):
        id_subscription = self.env['sale.subscription'].search([('code','=',self.origin)])
        fecha=self.date_invoice
        date= datetime.strptime(fecha, '%Y-%m-%d').date()
        mes= date.month
        self._cr.execute(
            "select  tipodestino, sum(min) as min, count(*),sum(montofinal) as imp, numeroa,tipotrafico from sale_cdr where subscriptionid = %s and extract(MONTH FROM fechafactura)=%s group by tipodestino,numeroa,tipotrafico",(id_subscription.id,mes,))
        _res = self._cr.dictfetchall()
        return _res

    @api.model
    def _getlinespoblacion(self):
        id_subscription = self.env['sale.subscription'].search([('code', '=', self.origin)])
        fecha = self.date_invoice
        date = datetime.strptime(fecha, '%Y-%m-%d').date()
        mes = date.month
        self._cr.execute(
            "select  poblacion, sum(min) as min, count(*),sum(montofinal) as imp, numeroa,tipotrafico from sale_cdr where subscriptionid=%s  AND extract(MONTH FROM fechafactura)=%s group by poblacion,numeroa,tipotrafico",
            (id_subscription.id,mes,))
        _res = self._cr.dictfetchall()
        return _res

    @api.model
    def _getlinesnumero(self):
        id_subscription = self.env['sale.subscription'].search([('code', '=', self.origin)])
        fecha = self.date_invoice
        date = datetime.strptime(fecha, '%Y-%m-%d').date()
        mes = date.month
        self._cr.execute(
            "select  fecha,poblacion, sum(min) as min, sum(tarifabase) as tarifa,sum(montofinal) as imp, numeroa,numerob from sale_cdr where subscriptionid=%s  AND extract(MONTH FROM fechafactura)=%s group by fecha,poblacion,numeroa,numerob",
            (id_subscription.id,mes,))
        _res = self._cr.dictfetchall()
        return _res