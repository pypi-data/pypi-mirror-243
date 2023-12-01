# kairospay

payments

## Installation

```bash
$ pip install kairospay
```

## Usage

Monnify is one of the products of TeamApt <https://www.teamapt.com/> . Monnify empowers businesses in the formal & informal sectors with the right tools & solutions to manage their finances and grow their businesses. Businesses in the formal economy benefit from our payment infrastructure that simplifies how they accept, manage and make payments. While smaller-scale businesses and entrepreneurs benefit from our market-community focused products that give them accessible, affordable and convenient short term working capital.

- MONNIFY PYTHON LIBRARY USER GUIDE

Before you can start integrating to Monnify, you will need to sign up on Monnify. Click <https://app.monnify.com/create-account> to sign up. After successful registration, login and for your credentials.

- CREDENTIAL NEEDED

1. API KEY
2. SECRET KEY
3. CONTRACT
4. WALLET ID

All this can be seen on the setting area when you login to you logged in.

- API ENDPOINT IN THE LIBRARY

1. monnifyCredential
2. get_token
3. verify_account
4. reserve_account
5. add_link_account
6. update_bvn_reserve
7. deallocate_account
8. reserve_account_transactions
9. tranfer
10. authorize_tranfer
11. resend_otp
12. get_transfer_details
13. get_all_single_transfer
14. get_wallet_balance
15. create_invoice
16. initiate_refund
17. get_refund_status
18. get_all_refund
19. create_sub_account
20. get_sub_account
21. update_sub_account
22. delete_sub_account
23. one_time_payment

- HOW TO USE THE LIBRARY
After successfull installation, we can now use the package in our development by importing it in our script.

```bash
from kairospay.monnify import monnifyCredential, get_token, Monnify

            monnify = Monnify()

            api_key = "MK_TEST_8UBXGKTYYYWB"
            secret_key = "ENRC4FDYYYETKA53YPXBFLUFXWYHG2"
            contractCode = '2917634883'
            walletId = '654CAB211YY36760A659C787B2AA38E8'

            merchant_credential = monnifyCredential(
              api_key, 
              secret_key, 
              contractCode, 
              walletId, 
              is_live=False
              )

            token = get_token(merchant_credential)
```

NOTE: If you are in sandbox please is_live = False and can only be set to True when you are in production and make sure you change credentials to live credentials

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`kairospay` was created by Solomon Olatunji. It is licensed under the terms of the MIT license.

## Credits

`kairospay` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
