from settrade_v2 import Investor

investor = Investor(
    app_id='jVhsPKLXE6BFyatY',
    app_secret='B5QdmXkaGykCAK4HCy+BOOO7YrhanzQJXokuneBZprU=',
    broker_id='SANDBOX',
    app_code='SANDBOX',
    is_auto_queue=False
)

deri = investor.Derivatives(account_no="warunkra-D")
account_info = deri.get_account_info()
print(account_info)