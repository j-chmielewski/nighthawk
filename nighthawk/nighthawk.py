from dataclasses import dataclass
from benedict import benedict
import requests


PATHS = dict(
    sinr='wwan.signalStrength.sinr',
    rsrp='wwan.signalStrength.rsrp',
    rsrq='wwan.signalStrength.rsrq',
    rssi='wwan.signalStrength.rssi',
    bars='wwan.signalStrength.bars',
    network='wwan.registerNetworkDisplay',
    connection='wwan.connectionText',
)


@dataclass
class NightHawkData:
    network: str
    connection: str
    rssi: int
    rsrp: int
    rsrq: int
    sinr: int
    bars: int


class NightHawk:

    def __init__(self, password: str, user: str = 'admin', address: str = 'http://192.168.1.1'):
        self.user = user
        self.password = password
        self.address = address
        self.session = requests.Session()

    def get_data(self) -> NightHawkData:
        url = f'{self.address}/model.json'
        r = self.session.get(url).json()
        r = benedict(r)
        # force login if neccessary
        if PATHS['network'] not in r:
            self._login(r.session.secToken)
            r = benedict(self.session.get(url).json())

        # TODO: fix typing
        return NightHawkData(**{k: r[v] for k, v in PATHS.items()})

    def _login(self, token: str):
        url = f'{self.address}/Forms/config'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data=f'username={self.user}&token={token}&session.password={self.password}&err_redirect=/index.html?loginfailed&ok_redirect=/index.html'
        self.session.post(
            url,
            headers=headers,
            data=data,
        )

