## -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools
from odoo.tools.xml_utils import _check_with_xsd
from odoo.tools import DEFAULT_SERVER_TIME_FORMAT
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
tipo_destino=['800 INTERNACIONAL','800 NACIONAL','LD INTERNACIONAL','LD INTERNACIONAL CELULAR',
'LD NACIONAL','LD NACIONAL CELULAR','LOCAL','CELULAR']

class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.model
    def _getlinessubscription(self):
        id_subscription = self.env['sale.subscription'].search([('code','=',self.origin)])
        fecha=self.date_invoice
        self._cr.execute(
            "select  tipodestino, sum(min) as min, count(*),sum(montofinal) as imp, numeroa,tipotrafico from sale_cdr where subscriptionid = %s and fechafactura=%s group by tipodestino,numeroa,tipotrafico",(id_subscription.id,self.date_invoice,))
        _res = self._cr.dictfetchall()
        return _res

    @api.model
    def _getlinespoblacion(self):
        id_subscription = self.env['sale.subscription'].search([('code', '=', self.origin)])
        self._cr.execute(
            "select  poblacion, sum(min) as min, count(*),sum(montofinal) as imp, numeroa,tipotrafico from sale_cdr where subscriptionid=%s  and fechafactura=%s group by poblacion,numeroa,tipotrafico",
            (id_subscription.id,self.date_invoice,))
        _res = self._cr.dictfetchall()
        return _res

    @api.model
    def _getlinesnumero(self):
        id_subscription = self.env['sale.subscription'].search([('code', '=', self.origin)])
        self._cr.execute(
            "select  fecha,poblacion, sum(min) as min, sum(tarifabase) as tarifa,sum(montofinal) as imp, numeroa,numerob from sale_cdr where subscriptionid=%s  and fechafactura=%s group by fecha,poblacion,numeroa,numerob",
            (id_subscription.id,self.date_invoice,))
        _res = self._cr.dictfetchall()
        return _res