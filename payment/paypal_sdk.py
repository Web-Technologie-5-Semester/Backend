import paypalrestsdk
import logging

# Logging aktivieren
logging.basicConfig(level=logging.INFO)

paypalrestsdk.configure({
    "mode": "sandbox",  # "sandbox" für Tests, "live" für Produktion
    "client_id": "ATl6E7gWqCprgNQ_xN5SfApRajRKol98kJ4dsSFO2J79JUySoB65Qjcnfl1B0cer57klmqBE0jzHE6Sp", 
    "client_secret": "EEnmqJ0kR80mEd56EiMM8KaGO635w4SA5Gb9MeFdcxLUd7j0P4kYHLY1DPCzxbHPWRnnb5F27BcKw2rk"  
})


# ATl6E7gWqCprgNQ_xN5SfApRajRKol98kJ4dsSFO2J79JUySoB65Qjcnfl1B0cer57klmqBE0jzHE6Sp
# ATl6E7gWqCprgNQ_xN5SfApRajRKol98kJ4dsSFO2J79JUySoB65Qjcnfl1B0cer57klmqBE0jzHE6Sp