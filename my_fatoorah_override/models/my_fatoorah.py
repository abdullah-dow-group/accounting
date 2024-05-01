from odoo import http, models, fields, _
from odoo.exceptions import UserError

@http.route('/payment/myfatoorah/response', type='http', auth='public',
            website=True, methods=['POST'], csrf=False, save_session=False)
def myfatoorah_payment_response(self, **data):
    """Function to get the payment response and process based on CustomerReference"""
    amount_total = 0
    payment_data = ast.literal_eval(data["data"])
    CustomerReference = payment_data.get("CustomerReference")

    if not CustomerReference:
        # Handle missing CustomerReference
        return request.render(template="myfatoorah_payment_gateway.myfatoorah_payment_gateway_form",
                              q={
                                  'error': _('Missing CustomerReference in payment data.')
                              })

    # Search for sale.order based on CustomerReference
    sale_order = self.env['sale.order'].search([('reference', '=', CustomerReference)], limit=1)

    if  sale_order:
        amount_total = sale_order.amount_total

    vals = {
        'customer': payment_data["CustomerName"],
        'currency': payment_data["DisplayCurrencyIso"],
        'mobile': payment_data["CustomerMobile"],
        'invoice_amount': amount_total if sale_order else payment_data["InvoiceValue"] ,  # Use sale.order.amount_total
        'address': payment_data["CustomerAddress"]["Address"],
        'payment_url': payment_data["InvoiceURL"],
    }

    return request.render(
        "myfatoorah_payment_gateway.myfatoorah_payment_gateway_form", vals)