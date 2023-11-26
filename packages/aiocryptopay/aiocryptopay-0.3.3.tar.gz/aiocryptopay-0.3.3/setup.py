# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiocryptopay',
 'aiocryptopay.exceptions',
 'aiocryptopay.models',
 'aiocryptopay.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'certifi>=2023.5.7,<2024.0.0',
 'pydantic==2.3.0',
 'strenum>=0.4.10,<0.5.0']

setup_kwargs = {
    'name': 'aiocryptopay',
    'version': '0.3.3',
    'description': '@cryptobot api asynchronous python wrapper',
    'long_description': "## **[@cryptobot](https://t.me/CryptoBot) asynchronous api wrapper**\n**Docs:** https://help.crypt.bot/crypto-pay-api\n\n - MainNet - [@CryptoBot](http://t.me/CryptoBot)\n - TestNet - [@CryptoTestnetBot](http://t.me/CryptoTestnetBot)\n\n\n**Install**\n``` bash\npip install aiocryptopay\npoetry add aiocryptopay\n```\n\n**Basic methods**\n``` python\nfrom aiocryptopay import AioCryptoPay, Networks\n\ncrypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)\n\nprofile = await crypto.get_me()\ncurrencies = await crypto.get_currencies()\nbalance = await crypto.get_balance()\nrates = await crypto.get_exchange_rates()\n\nprint(profile, currencies, balance, rates, sep='\\n')\n```\n\n**Create, get and delete invoice methods**\n``` python\nfrom aiocryptopay import AioCryptoPay, Networks\n\ncrypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)\n\ninvoice = await crypto.create_invoice(asset='TON', amount=1.5)\nprint(invoice.pay_url)\n\n# Create invoice in fiat\nfiat_invoice = await crypto.create_invoice(amount=5, fiat='USD', currency_type='fiat')\nprint(fiat_invoice)\n\nold_invoice = await crypto.get_invoices(invoice_ids=invoice.invoice_id)\nprint(old_invoice.status)\n\ndeleted_invoice = await crypto.delete_invoice(invoice_id=invoice.invoice_id)\nprint(deleted_invoice)\n\n# Get amount in crypto by fiat summ\namount = await crypto.get_amount_by_fiat(summ=100, asset='TON', target='USD')\ninvoice = await crypto.create_invoice(asset='TON', amount=amount)\nprint(invoice.pay_url)\n```\n\n**Create, get and delete check methods**\n``` python\n# The check creation method works when enabled in the application settings\n\nfrom aiocryptopay import AioCryptoPay, Networks\n\ncrypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)\n\ncheck = await crypto.create_check(asset='USDT', amount=1)\nprint(check)\n\nold_check = await crypto.get_checks(check_ids=check.check_id)\nprint(old_check)\n\ndeleted_check = await crypto.delete_check(check_id=check.check_id)\nprint(deleted_check)\n```\n\n\n**WebHook usage**\n``` python\nfrom aiohttp import web\n\nfrom aiocryptopay import AioCryptoPay, Networks\nfrom aiocryptopay.models.update import Update\n\n\nweb_app = web.Application()\ncrypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)\n\n\n@crypto.pay_handler()\nasync def invoice_paid(update: Update, app) -> None:\n    print(update)\n\nasync def create_invoice(app) -> None:\n    invoice = await crypto.create_invoice(asset='TON', amount=1.5)\n    print(invoice.pay_url)\n\nasync def close_session(app) -> None:\n    await crypto.close()\n\n\nweb_app.add_routes([web.post('/crypto-secret-path', crypto.get_updates)])\nweb_app.on_startup.append(create_invoice)\nweb_app.on_shutdown.append(close_session)\nweb.run_app(app=web_app, host='localhost', port=3001)\n```",
    'author': 'layerqa',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/layerqa/aiocryptopay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
