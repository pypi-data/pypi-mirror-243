### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###


from openbb_core.app.static.container import Container


class Extensions(Container):
    # fmt: off
    """
Routers:
    /crypto
    /currency
    /derivatives
    /economy
    /equity
    /etf
    /fixedincome
    /index
    /news
    /regulators

Extensions:
    - crypto@1.0.0b1
    - currency@1.0.0b1
    - derivatives@1.0.0b1
    - economy@1.0.0b1
    - equity@1.0.0b1
    - etf@1.0.0b1
    - fixedincome@1.0.0b1
    - index@1.0.0b1
    - news@1.0.0b1
    - regulators@1.0.0b1

    - benzinga@1.0.0b1
    - fmp@1.0.0b1
    - fred@1.0.0b1
    - government_us@1.0.0b1
    - intrinio@1.0.0b1
    - oecd@1.0.0b1
    - polygon@1.0.0b1
    - sec@1.0.0b1
    - tradingeconomics@1.0.0b1    """
    # fmt: on
    def __repr__(self) -> str:
        return self.__doc__ or ""

    @property
    def crypto(self):  # route = "/crypto"
        from . import crypto

        return crypto.ROUTER_crypto(command_runner=self._command_runner)

    @property
    def currency(self):  # route = "/currency"
        from . import currency

        return currency.ROUTER_currency(command_runner=self._command_runner)

    @property
    def derivatives(self):  # route = "/derivatives"
        from . import derivatives

        return derivatives.ROUTER_derivatives(command_runner=self._command_runner)

    @property
    def economy(self):  # route = "/economy"
        from . import economy

        return economy.ROUTER_economy(command_runner=self._command_runner)

    @property
    def equity(self):  # route = "/equity"
        from . import equity

        return equity.ROUTER_equity(command_runner=self._command_runner)

    @property
    def etf(self):  # route = "/etf"
        from . import etf

        return etf.ROUTER_etf(command_runner=self._command_runner)

    @property
    def fixedincome(self):  # route = "/fixedincome"
        from . import fixedincome

        return fixedincome.ROUTER_fixedincome(command_runner=self._command_runner)

    @property
    def index(self):  # route = "/index"
        from . import index

        return index.ROUTER_index(command_runner=self._command_runner)

    @property
    def news(self):  # route = "/news"
        from . import news

        return news.ROUTER_news(command_runner=self._command_runner)

    @property
    def regulators(self):  # route = "/regulators"
        from . import regulators

        return regulators.ROUTER_regulators(command_runner=self._command_runner)
