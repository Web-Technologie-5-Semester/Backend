from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from db import get_session
from payment.paypal_sdk import paypalrestsdk
from payment.paypal_services import ExtendedPayPal

payment_router = APIRouter()

@payment_router.post("/create-payment")
async def create_a_payment(json_data: dict, session: Session = Depends(get_session)):
    return ExtendedPayPal(session).create_payment(json_data)
    

@payment_router.post("/execute-payment")
async def execute_a_payment(payment_id: str, payer_id: str, unique_order_id: int, session: Session = Depends(get_session)):
    return ExtendedPayPal(session).execute_payment(payment_id,payer_id,unique_order_id)
