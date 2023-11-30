from __future__ import annotations

import json

from base64 import b64encode
from collections.abc import Iterable, Sequence
from copy import deepcopy
from datetime import datetime, date, time
from io import BytesIO
from json import loads as json_loads
from typing import Any
from zipfile import ZipFile

from lxml.html import parse

from .core import TraderNetCore


class TraderNetAPI(TraderNetCore):
    """
    Client methods to interact TraderNet API.
    """
    def new_user(
        self,
        login: str,
        reception: str | int,
        phone: str,
        lastname: str,
        firstname: str,
        password: str | None = None,
        utm_campaign: str | None = None,
        tariff: int | None = None
    ) -> dict[str, str | int]:
        """
        Creating a new user.

        Parameters
        ----------
        login : str
            A login.
            A password.
        reception : str | int
            A reception number.
        phone : str | None
            User's phone no.
        lastname : str | None
            User's last name.
        firstname : str | None
            User's first name.
        password : str | None
            User's password. If None, it will be generated automatically.
        utm_campaign : str | None
            Referral link. This field is used if a new user is created after
            receiving a referral link.
        tariff : int | None
            Selected rate ID. Optional parameter. During the registration, you
            may immediately assign the desired rate ID.

        Returns
        -------
        dict[str, str | int]
            A dictionary with the following keys: 'clientId', 'userId'.

        Notes
        -----
        https://tradernet.ru/tradernet-api/primary-registration
        """
        cmd = 'registerNewUser'
        params = {
            'login': login,
            'pwd': password,
            'reception': str(reception),
            'phone': phone,
            'lastname': lastname,
            'firstname': firstname,
            'tariff_id': tariff,
            'utm_campaign': utm_campaign
        }
        return self.plain_request(cmd, params)

    def change_phone(self, phone: str) -> dict[str, Any]:
        """
        Changing a phone number.

        Parameters
        ----------
        phone : str
            A phone number.

        Returns
        -------
        dict[str, Any]
            A dictionary with the following keys: 'phoneId'.

        Notes
        -----
        https://tradernet.ru/tradernet-api/check-phone
        """
        cmd = 'checkPhone'
        params = {'phone': phone}
        if not self._session_id:
            self.get_authorized()

        return self.plain_request(cmd, params)

    def check_sms(self, phone_id: int, code: str) -> dict[str, Any]:
        """
        Method for checking the validity of the code sent in SMS using the
        method checkPhone.

        Parameters
        ----------
        phone_id : int
            A phone ID.
        code : str
            A SMS code.

        Returns
        -------
        dict[str, Any]
            A dictionary with the following keys: 'success'.

        Notes
        -----
        https://tradernet.ru/tradernet-api/check-phone
        """
        cmd = 'checkSms'
        params = {'phoneId': phone_id, 'code': code}
        if not self._session_id:
            self.get_authorized()

        return self.plain_request(cmd, params)

    def get_tariffs_list(self) -> dict[str, Any]:
        """
        Get a list of available tariffs.

        Returns
        -------
        dict[str, Any]
            Tariffs list.

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-list-tariff
        """
        cmd = 'GetListTariffs'
        if not self._session_id:
            self.get_authorized()

        return self.plain_request(cmd)

    def select_tariff(self, tariff_id: int) -> dict[str, Any]:
        """
        Selecting a tariff.

        Parameters
        ----------
        tariff_id : int
            A tariff ID.

        Returns
        -------
        dict[str, Any]
            A dictionary with the following keys: 'added'.

        Notes
        -----
        https://tradernet.ru/tradernet-api/select-tariff
        """
        cmd = 'selectTariff'
        params = {'tariff_id': tariff_id}
        if not self._session_id:
            self.get_authorized()

        return self.plain_request(cmd, params)

    def get_agreement(self) -> bytes:
        """
        Receiving application for joining in PDF format.

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-agreement-pdf
        """
        cmd = 'getAgreementPdf'
        if not self._session_id:
            self.get_authorized()

        message: dict[str, Any] = {'cmd': cmd, 'SID': self._session_id}
        url = f'{self.url}/api'
        query = {'q': json.dumps(message)}

        response = self.request('get', url, params=query)
        return response.content

    def send_agreement(
        self,
        agreement: bytes,
        check: int | None
    ) -> dict[str, Any]:
        """
         Uploading a signed application for joining in PDF format.

        Parameters
        ----------
        agreement : bytes
            An application for joining in PDF format.
        check : int | None
            1 - Mandatory check. More details can be found on the page:
            https://tradernet.ru/tradernet-api/special-files-list

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-agreement-pdf
        """
        cmd = 'uploadFiles'
        agreement = b64encode(agreement)

        params = {
            'name': 'anketa_files_signed_agreement',
            'extension': 'pdf',
            'img': agreement,
            'check': check
        }

        return self.authorized_request(cmd, params, version=None)

    def check_missing_fields(self, step: int, office: str) -> dict[str, Any]:
        """
        Checking missing (blank) fields. If any fields are missing, they will
        be specified in the `not_completed` parameter, along with a
        description.

        Parameters
        ----------
        step : int
            A step number.
        office : str
            An office name.

        Notes
        -----
        https://tradernet.ru/tradernet-api/check-step
        """
        cmd = 'checkStep'
        params = {'step': step, 'office': office}
        if not self._session_id:
            self.get_authorized()

        return self.plain_request(cmd, params)

    def get_profile_fields(self, reception: int) -> dict[str, Any]:
        """
        Obtaining profile fields for different offices.

        Parameters
        ----------
        reception : int
            A reception number.

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-anketa-fields
        """
        cmd = 'getAnketaFields'
        params = {'anketa_for_reception': reception}
        return self.plain_request(cmd, params)

    def user_info(self) -> dict[str, Any]:
        """
        Obtaining user information.

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-user-info
        """
        cmd = 'GetAllUserTexInfo'
        if not self._session_id:
            self.get_authorized()

        return self.plain_request(cmd)

    def sign_application(self) -> dict[str, Any]:
        """
        Signing the application by SMS sent to the phone specified by the new
        user.

        Notes
        -----
        https://tradernet.ru/tradernet-api/sign-anketa-electronically
        """
        cmd = 'signAnketaElectronically'
        if not self._session_id:
            self.get_authorized()

        return self.plain_request(cmd)

    def verify_application_signature(
        self,
        phone_id: str,
        code: str
    ) -> dict[str, Any]:
        """
        Confirming the signature via SMS, received to the client's phone number
        using the method `sign_application`.

        Parameters
        ----------
        phone_id : str
            A phone ID.
        code : str
            A SMS code.

        Notes
        -----
        https://tradernet.ru/tradernet-api/check-anketa-electronically-sign-sms-code
        """
        cmd = 'checkAnketaElectronicallySignSmsCode'
        params = {'phoneId': phone_id, 'code': code}
        if not self._session_id:
            self.get_authorized()

        return self.plain_request(cmd, params)

    def get_user_data(self) -> dict[str, Any]:
        """
        Getting initial user data from the server - orders, portfolio, markets,
        open sessions, etc.

        Notes
        -----
        https://tradernet.ru/tradernet-api/auth-get-opq
        """
        cmd = 'getOPQ'
        return self.authorized_request(cmd)

    def get_market_status(
        self,
        market: str = '*',
        mode: str | None = None
    ) -> dict[str, Any]:
        """
        Obtaining information about market statuses and operation.

        Parameters
        ----------
        market : str
            A market code (briefName).
        mode : str | None
            Request mode: demo. If the parameter is not specified, the market
            statuses for real users will be displayed.

        Notes
        -----
        https://tradernet.ru/tradernet-api/market-status
        """
        cmd = 'getMarketStatus'
        params = {'market': market}
        if mode:
            params['mode'] = mode
        return self.plain_request(cmd)

    def security_info(self, symbol: str, sup: bool = True) -> dict[str, Any]:
        """
        Getting info on a specific symbol.

        Parameters
        ----------
        symbol : str
            A TraderNet symbol.
        sup : bool
            IMS and trading system format.

        Returns
        -------
        result : dict
            A dictionary of symbol info.

        Notes
        -----
        https://tradernet.ru/tradernet-api/quotes-get-info
        """
        cmd = 'getSecurityInfo'
        params = {'ticker': symbol, 'sup': sup}
        return self.authorized_request(cmd, params=params)

    def get_options(
        self,
        underlying: str,
        exchange: str
    ) -> list[dict[str, str]]:
        """
        Downloading a list of active options by the underlying asset and
        exchange.

        Parameters
        ----------
        underlying : str
            The underlying symbol.
        exchange : str
            A venue options traded.

        Returns
        -------
        list[dict[str, str]]
            List of very basic properties of options.

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-options-by-mkt
        """
        cmd = 'getOptionsByMktNameAndBaseAsset'
        params = {'base_contract_code': underlying, 'ltr': exchange}
        return self.plain_request(cmd, params)

    def get_most_traded(
        self,
        instrument_type: str = 'stocks',
        exchange: str = 'usa',
        gainers: bool = True,
        limit: int = 10
    ) -> dict[str, Any]:
        """
        Getting a list of the most traded securities or a list of the fastest
        growing stocks (for a year).

        Parameters
        ----------
        instrument_type : str
            Instrument type.
        exchange : str
            Stock exchanges. Possible values: 'usa', 'europe', 'ukraine',
            'currencies'.
        gainers : bool
            True: top fastest-growing, False: top by trading volume.
        limit : int
            Number of instruments displayed.

        Notes
        -----
        https://tradernet.ru/tradernet-api/quotes-get-top-securities
        """
        cmd = 'getTopSecurities'
        params = {
            'type': instrument_type,
            'exchange': exchange,
            'gainers': int(gainers),
            'limit': limit
        }
        return self.plain_request(cmd, params)

    def export_securities(
        self,
        symbols: str | Sequence[str],
        fields: Sequence[str] | None = None
    ) -> list[dict[str, Any]]:
        """
        Exporting securities data from TraderNet.

        Parameters
        ----------
        symbols : str | Sequence[str]
            A symbol or a list of symbols.
        fields : list[str] | None, optional
            Limiting fields, by default None which means all fields.

        Returns
        -------
        list[dict[str, Any]]
            A list of dictionaries with security data.

        Notes
        -----
        https://tradernet.ru/tradernet-api/quotes-get
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        if fields:
            params = {'params': ' '.join(fields)}
        else:
            params = {}

        url = f'{self.url}/securities/export'

        result: list[dict[str, Any]] = []
        for chunk in range(0, len(symbols), self.MAX_EXPORT_SIZE):
            request_params = deepcopy(params)
            request_params['tickers'] = ' '.join(
                symbols[chunk:chunk + self.MAX_EXPORT_SIZE]
            )

            result += self.request(
                'get',
                url,
                headers=self.HEADERS,
                params=request_params
            ).json()

        return result

    def get_candles(
        self,
        symbol: str,
        start: datetime = datetime(2010, 1, 1),
        end: datetime = datetime.utcnow(),
        timeframe: int = 86400
    ) -> dict[str, Any]:
        """
        Getting historical data of a symbol.

        Parameters
        ----------
        symbol : str
            A symbol name on TraderNet.
        start : datetime
            The first date of the period market data to be acquired within.
        end : datetime
            The last date of the period.
        timeframe : int
            Timeframe of candles in seconds. Default is 86400 corresponding to
            day candles. -1 value of the parameter indicating that traders are
            required.

        Returns
        -------
        result : dict
            A dictionary of historical information of the symbol.

        Notes
        -----
        https://tradernet.ru/tradernet-api/quotes-get-hloc
        https://tradernet.ru/tradernet-api/get-trades
        """
        cmd = 'getHloc'
        params = {
            'id': symbol,
            'count': -1,
            'timeframe': int(timeframe / 60),
            'date_from': start.strftime('%d.%m.%Y %H:%M'),
            'date_to': end.strftime('%d.%m.%Y %H:%M'),
            'intervalMode': 'OpenRay'
        }
        return self.authorized_request(cmd, params=params)

    def get_trades_history(
        self,
        start: date = date(1970, 1, 1),
        end: date = date.today(),
        trade_id: int | None = None,
        limit: int | None = None,
        symbol: str | None = None,
        currency: str | None = None
    ) -> dict[str, Any]:
        """
        Getting a list of trades.

        Parameters
        ----------
        start : date
            Period start date.
        end : date
            Period end date.
        trade_id : int | None
            From which Trade ID to start retrieving report data.
        limit : int | None
            Number of trades. If 0 or no parameter is specified - then all
            trades.
        symbol : str | None
            A symbol.
        currency : str | None
            Base currency or quote currency.

        Returns
        -------
        result : dict
            A dictionary of trades.

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-trades-history
        """
        cmd = 'getTradesHistory'
        params: dict[str, str | int] = {
            'beginDate': str(start),
            'endDate': str(end)
        }

        if trade_id is not None:
            params['tradeId'] = trade_id

        if limit is not None:
            params['max'] = limit

        if symbol is not None:
            params['nt_ticker'] = symbol

        if currency is not None:
            params['curr'] = currency

        return self.authorized_request(cmd, params=params)

    def find_symbol(
        self,
        symbol: str,
        exchange: str | None = None
    ) -> dict[str, Any]:
        """
        Stock symbols search.

        Parameters
        ----------
        symbol : str
            A symbol name.
        exchange : str, optional
            Refbook name.

        Returns
        -------
        result : dict
            A dictionary of symbols, max 30.

        Notes
        -----
        https://tradernet.ru/tradernet-api/quotes-finder
        """
        cmd = 'tickerFinder'
        params = {'text': f'{symbol}@{exchange}' if exchange else symbol}
        return self.plain_request(cmd, params)

    def get_news(
        self,
        query: str,
        symbol: str | None = None,
        story_id: str | None = None,
        limit: int = 30
    ) -> dict[str, Any]:
        """
        Getting news on securities.

        Parameters
        ----------
        query : str
            Can be ticker or any word.
        symbol : str | None
            If parameter symbol is set, `query` will be ignored and newsfeed
            will consist only of stories solely based on mentioned symbol.
        story_id : str | None
            If parameter story_id is set, `query` and `symbol` parameters will
            be ignored and news feed will consist only of the story with
            required storyId.
        limit : int
            Max number of news, 30 by default.

        Notes
        -----
        https://tradernet.ru/tradernet-api/quotes-get-news
        """
        cmd = 'getNews'
        params = {
            'searchFor': query,
            'ticker': symbol,
            'storyId': story_id,
            'limit': limit
        }
        if not self._session_id:
            self.get_authorized()
        return self.plain_request(cmd, params)

    def get_all(
        self,
        filters: dict[str, Any] | None = None,
        show_expired: bool = False
    ) -> list[dict[str, Any]]:
        """
        Getting information on securities.

        Parameters
        ----------
        filters : dict, optional
            Field names and their values.
        show_expired : bool, optional
            Getting expired symbols or not.

        Returns
        -------
        result : dict
            A dictionary of symbols.

        Notes
        -----
        https://tradernet.ru/tradernet-api/securities
        https://tradernet.ru/tradernet-api/instruments - instrument types

        Examples
        --------
        >>> await self.get_all(
                filters={'mkt_short_code': 'FIX', 'instr_type_c': 1}
            )
        [dict(...)]

        This command obtains all stocks of the FIX venue.

        >>> await self.get_all(
                filters={'mkt_short_code': 'ICE', 'instr_type_c': 4}
            )
        [dict(...)]

        And this one obtains all active options from the ICE exchange.
        """
        if not filters:
            filters = {}

        if not show_expired:
            filters['istrade'] = 1

        return [
            symbol for symbol
            in self.__get_refbook(filters.get('mkt_short_code'))
            if all(symbol[field] == filters[field] for field in filters)
        ]

    def account_summary(self) -> dict[str, Any]:
        """
        Getting summary of own account.

        Returns
        -------
        result : dict
            A dictionary of all positions, active orders, etc.

        Notes
        -----
        https://tradernet.ru/tradernet-api/portfolio-get-changes
        """
        cmd = 'getPositionJson'
        return self.authorized_request(cmd)

    def get_price_alerts(self, symbol: str | None = None) -> dict[str, Any]:
        """
        Getting a list of price alerts.

        Parameters
        ----------
        symbol : str | None, optional
            Symbol to get alerts for.

        Returns
        -------
        result : dict
            A dictionary of alerts.

        Notes
        -----
        https://tradernet.ru/tradernet-api/alerts-get-list
        """
        cmd = 'getAlertsList'
        params: dict[str, str] = {}
        if symbol:
            params['ticker'] = symbol

        if not self._session_id:
            self.get_authorized()
        return self.plain_request(cmd, params)

    def add_price_alert(
        self,
        symbol: str,
        price: int | float | str | Iterable[int | float | str],
        trigger_type: str = 'crossing',
        quote_type: str = 'ltp',
        send_to: str = 'email',
        frequency: int = 0,
        expire: int = 0
    ) -> dict[str, Any]:
        """
        Adding a price alert.

        Parameters
        ----------
        symbol : str
            Symbol to add alert for.
        price : float | list[float]
            Price of the alert activation.
        trigger_type : str, optional
            Trigger method.
        quote_type : str, optional
            Type of the price underlying the alert calculation. Possible
            values: 'ltp', 'bap', 'bbp', 'op', 'pp'.
        send_to : str, optional
            Type of notification. Possible values: 'email', 'sms', 'push',
            'all', by default 'email'.
        frequency : int, optional
            Frequency.
        expire : int, optional
            Alert period.

        Returns
        -------
        result : dict
            Addition result.

        Notes
        -----
        https://tradernet.ru/tradernet-api/alerts-add
        """
        cmd = 'addPriceAlert'
        if not isinstance(price, Iterable):
            price = [str(price)]
        else:
            price = [*map(str, price)]
        params = {
            'ticker': symbol,
            'price': price,
            'trigger_type': trigger_type,
            'quote_type': quote_type,
            'notification_type': send_to,
            'alert_period': frequency,
            'expire': expire
        }
        if not self._session_id:
            self.get_authorized()
        return self.plain_request(cmd, params)

    def delete_price_alert(self, alert_id: int) -> dict[str, Any]:
        """
        Deleting a price alert.

        Parameters
        ----------
        alert_id : int
            Alert ID.

        Returns
        -------
        result : dict
            Deletion result.

        Notes
        -----
        https://tradernet.ru/tradernet-api/alerts-delete
        """
        cmd = 'addPriceAlert'
        params = {'id': alert_id, 'del': True}
        if not self._session_id:
            self.get_authorized()
        return self.plain_request(cmd, params)

    def get_requests_history(
        self,
        doc_id: int | None = None,
        exec_id: int | None = None,
        start: date = datetime(1970, 1, 1),
        end: date = datetime.utcnow(),
        limit: int | None = None,
        offset: int | None = None,
        status: int | None = None
    ) -> dict[str, Any]:
        """
        Receiving clients' requests history.

        Parameters
        ----------
        doc_id : int | None, optional
            Request type ID.
        exec_id : int | None, optional
            Order ID.
        start : date, optional
            Period start date.
        end : date, optional
            Period end date.
        limit : int | None, optional
            Number of orders displayed in the list.
        offset : int | None, optional
            Step of the list of displayed requests.
        status : int | None, optional
            Requests statuses: 0 - draft request; 1 - in process of execution;
            2 - request is rejected; 3 - request is executed.

        Returns
        -------
        result : dict
            Clients' requests for the specified period.

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-client-cps-history
        """
        cmd = 'getClientCpsHistory'
        params: dict[str, str | int] = {
            'date_from': start.strftime('%Y-%m-%dT%H:%M:%S'),
            'date_to': end.strftime('%Y-%m-%dT%H:%M:%S')
        }
        if doc_id:
            params['cpsDocId'] = doc_id
        if exec_id:
            params['id'] = exec_id
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        if status:
            params['cps_status'] = status
        return self.authorized_request(cmd, params)

    def get_order_files(
        self,
        order_id: int | None,
        internal_id: int | None
    ) -> dict[str, Any]:
        """
        Receiving order files.

        Parameters
        ----------
        order_id : int | None, optional
            Order ID. May be not used if the draft order ID is known
            (internal_id).
        internal_id : int | None, optional
            Draft order number. Used when known, or if the order has the draft
            status and has not yet been assigned the main ID.

        Returns
        -------
        result : dict
            Order files.

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-cps-files
        """
        cmd = 'getCpsFiles'
        params: dict[str, int] = {}
        if internal_id:
            params['internal_id'] = internal_id
        elif order_id:
            params['id'] = order_id
        else:
            raise ValueError(
                'Either order_id or internal_id must be specified'
            )
        return self.authorized_request(cmd, params)

    def get_broker_report(
        self,
        start: date = date(1970, 1, 1),
        end: date = date.today(),
        period: time = time(23, 59, 59),
        data_block_type: str | None = 'account_at_end'
    ) -> dict[str, Any]:
        """
        Getting the broker's report using software methods.

        Parameters
        ----------
        start : date, optional
            Period start date.
        end : date, optional
            Period end date.
        period : time, optional
            Time cut maybe 23:59:59 or 08:40:00.
        data_block_type : str | None, optional
            Data block from the report.

        Returns
        -------
        dict[str, Any]
            Broker's report.
        """
        cmd = 'getBrokerReport'
        params: dict[str, str | None] = {
            'date_start': str(start),
            'date_end': str(end),
            'time_period': period.strftime('%H:%M:%S'),
            'format': 'json',
            'type': data_block_type
        }
        return self.authorized_request(cmd, params)

    def get_depository_report(
        self,
        start: date = datetime(1970, 1, 1),
        end: date = date.today(),
        period: time = time(23, 59, 59),
        file_format: str = 'pdf',
        data_block_type: str | None = 'account_at_end',
        encoded_result: bool = True
    ) -> dict[str, Any]:
        """
        Getting the depository's report using software methods.

        Parameters
        ----------
        start : date, optional
            Period start date.
        end : date, optional
            Period end date.
        period : time, optional
            Time cut maybe 23:59:59 or 08:40:00.
        file_format : str, optional
            Report in the selected format. Acceptable formats: 'json', 'html',
            'xml', 'xls', 'pdf'.
        data_block_type : str | None, optional
            Data block from the report.
        encoded_result : bool, optional
            Retrieves the report as a JSON array containing the encoded file in
            section file base64.

        Returns
        -------
        dict[str, Any]
            Depository's report.
        """
        cmd = 'getDepositoryReport'
        params: dict[str, int | str | None] = {
            'date_start': str(start),
            'date_end': str(end),
            'time_period': period.strftime('%H:%M:%S'),
            'format': file_format,
            'type': data_block_type,
            'encoded_result': int(encoded_result)
        }
        return self.authorized_request(cmd, params)

    def symbol(self, symbol: str, lang: str = 'en') -> dict[str, Any]:
        """
        A method for obtaining information on a given security.

        Parameters
        ----------
        symbol : str
            A TraderNet symbol.
        lang : str
            Language, two letters.

        Returns
        -------
        result : dict
            A dictionary of symbol info.

        Notes
        -----
        https://tradernet.ru/tradernet-api/shop-get-stock-data
        """
        cmd = 'getStockData'
        params = {'ticker': symbol, 'lang': lang}
        return self.authorized_request(cmd, params=params)

    def symbols(self, exchange: str | None = None) -> dict[str, Any]:
        """
        Receiving completed lists of securities.

        Parameters
        ----------
        exchange : str, optional
            Optional parameter that allows to get data from NYSE and NASDAQ or
            Moscow Exchange. May accept the value usa, russia.

        Returns
        -------
        result : dict
            A dictionary of exchanges and symbols.

        Notes
        -----
        https://tradernet.ru/tradernet-api/get-ready-list
        """
        cmd = 'getReadyList'
        if exchange:
            params: dict[str, str] | None = {'mkt': exchange}
        else:
            params = None
        return self.authorized_request(cmd, params=params)

    def corporate_actions(
        self,
        reception: int = 35
    ) -> list[dict[str, Any]]:
        """
        Getting planned corporate actions for a certain office.

        Parameters
        ----------
        reception : 35
            Office number.

        Returns
        -------
        result : list
            Expected corporate actions.
        """
        cmd = 'getPlannedCorpActions'
        params = {'reception': reception}
        return self.plain_request(cmd, params)

    def get_quotes(self, symbols: Sequence[str]) -> dict[str, Any]:
        """
        Getting quotes for a list of symbols.

        Parameters
        ----------
        symbols : Sequence[str]
            A sequence of symbols.

        Returns
        -------
        result : dict
            A dictionary of quotes.

        Notes
        -----
        https://tradernet.ru/tradernet-api/quotes-get
        """
        cmd = 'getStockQuotesJson'
        params = {'tickers': ' '.join(symbols)}
        return self.authorized_request(cmd, params=params)

    def __refbooks(self) -> list[str]:
        """
        Getting the list of available reference books.

        Returns
        -------
        result : list
            The list of reference books for a specific date found.

        Notes
        -----
        https://tradernet.ru/refbooks
        """
        reference_date = self.__latest_refbook()
        url = f'{self.url}/refbooks/{reference_date}'
        page = self.request('get', url)
        content = page.content
        doc = parse(BytesIO(content)).getroot()
        result = [
            div.text_content().rsplit('.', 2)[0]
            for div in doc.cssselect('a')
        ]
        result.remove('')
        return result

    def __get_refbook(
        self,
        name: str | None = 'all',
        reference_date: date | None = None
    ) -> list[dict[str, Any]]:
        """
        Downloading and processing a particular reference book.

        Parameters
        ----------
        name : str
            The name of the book.

        Returns
        -------
        result : list
            The list of all instruments with their properties found in the
            reference book.
        """
        if not reference_date:
            reference_date = self.__latest_refbook()

        if not name or name == 'all':
            self.logger.warning(
                'Downloading all symbols may take a while '
                'and requires at least 40GB of RAM!'
            )

            result: list[dict[str, Any]] = []
            for refbook_name in self.__refbooks():
                result += self.__get_refbook(refbook_name, reference_date)

            return result

        uri = f'/refbooks/{reference_date}/{name}.json.zip'

        # Download and unzip
        response = self.request('get', url=f'{self.url}{uri}')
        content = response.content
        archive_json = self.__extract_zip(content)
        self.logger.debug(
            'Files in the archive: %s',
            ', '.join(archive_json.keys())
        )
        assert len(archive_json) == 1, 'More than one file in the archive'

        return json_loads(archive_json[f'{name}.json'])

    def __latest_refbook(self) -> date:
        """
        Getting the latest reference book date.

        Returns
        -------
        result : date
            The latest reference book date.
        """
        url = f'{self.url}/refbooks'
        page = self.request('get', url)
        content = page.content
        doc = parse(BytesIO(content)).getroot()
        result = [
            div.text_content().rsplit('.', 2)[0]
            for div in doc.cssselect('a')
        ]

        return max(
            datetime.strptime(date_str, '%Y-%m-%d/').date()
            for date_str in result
            if date_str
        )

    @staticmethod
    def __extract_zip(content: bytes) -> dict[str, str]:
        """
        Extracting a zipped file into a dictionary having the structure
        "name->content".
        Parameters
        ----------
        content : bytes
            Byte-representation of an archive.
        Returns
        -------
        dict[str, str]
            Resulting dictionary.
        """
        with ZipFile(BytesIO(content)) as zip_file:
            return {
                name: zip_file.read(name).decode()
                for name in zip_file.namelist()
            }
