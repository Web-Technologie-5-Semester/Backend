from .paypal_sdk import paypalrestsdk
from order.orderServices import OrderService
from order.orderCRUD import OrderUpdate, StatusEnum
from sqlmodel import Session
import paypalrestsdk

class ExtendedPayPal(paypalrestsdk.Api):
    session:Session = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # einlesen
    def convert_json_to_paypal_payment(self, json_data: dict) -> paypalrestsdk.Payment:
        """ 
        Minimal erforderlich:
            intent: Zahlungsabsicht ("sale", "authorize", "order")
            payer: Ein Objekt mit der Zahlungsmethode ("paypal", "credit_card")
            transactions: Eine Liste mit mindestens einer Transaktion
        """
        try:
            return paypalrestsdk.Payment(json_data)
        except Exception as e:
            print(f"Fehler bei der Konvertierung: {e}")
            return None



    def create_payment(self, myjson_data: dict):
        payment = self.convert_json_to_paypal_payment(myjson_data)

        if payment and payment.create():
            return {"status": "success", "payment_id": payment.id, "approval_url": payment.links[1].href}
        else:
            return {"status": "error", "error_details": payment.error if payment else "Ungültige Zahlungsdaten"}



    def execute_payment(self, payment_id: str, payer_id: str, unique_order_id: int):
        # Bestellung muss erst erfolgreich erstellt werden
        # Führt eine genehmigte Zahlung aus und setzt den Status in der Datenbank
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            order_response = OrderService.update_an_order(unique_order_id, OrderUpdate(status=StatusEnum.PAYED))
            return {"status": "success", "message": f"Zahlung {payment_id} erfolgreich abgeschlossen!\nBestelldetails:\n{order_response}"}
        else:
            return {"status": "error", "error_details": payment.error}

