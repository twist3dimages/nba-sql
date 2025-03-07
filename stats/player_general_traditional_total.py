import requests
import urllib.parse

from utils import get_rowset_mapping, column_names_from_table, season_id_to_int
from models import PlayerGeneralTraditionalTotal
from general_requester import GenericRequester
from constants import headers


class PlayerGeneralTraditionalTotalRequester(GenericRequester):

    player_info_url = 'https://stats.nba.com/stats/leaguedashplayerstats'
    per_mode = 'Totals'

    def __init__(self, settings):
        """
        Constructor. Attach settings internally and bind the model to the
        database.
        """
        super().__init__(settings, self.player_info_url, PlayerGeneralTraditionalTotal)

    def generate_rows(self, season_id):
        """
        Build GET REST request to the NBA for a season.
        Also populate this table.
        We cannot rely on the base table's generic method, due to the `season_id` field.
        """
        params = self.build_params(season_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')

        # json response
        response = requests.get(url=self.url, headers=headers, params=params_str).json()

        result_sets = response['resultSets'][0]
        rowset = result_sets['rowSet']

        column_names = column_names_from_table(self.settings.db, self.table._meta.table_name)

        column_mapping = get_rowset_mapping(result_sets, column_names)

        for row in rowset:
            new_row = {column_name: row[row_index] for column_name, row_index in column_mapping.items()}
            new_row['season_id'] = season_id_to_int(season_id)
            self.rows.append(new_row)

        super().populate()

    def build_params(self, season_id):
        """
        Create required parameters dict for the request.
        """
        return {
            'College': '',
            'Conference': '',
            'Country': '',
            'DateFrom': '',
            'DateTo': '',
            'Division': '',
            'DraftPick': '',
            'DraftYear': '',
            'GameScope': '',
            'GameSegment': '',
            'Height': '',
            'LastNGames': '0',
            'LeagueID': '00',
            'Location': '',
            'MeasureType': 'Base',
            'Month': '0',
            'OpponentTeamID': '0',
            'Outcome': '',
            'PORound': '0',
            'PaceAdjust': 'N',
            'PerMode': self.per_mode,
            'Period': '0',
            'PlayerExperience': '',
            'PlayerPosition': '',
            'PlusMinus': 'N',
            'Rank': 'N',
            'Season': season_id,
            'SeasonSegment': '',
            'SeasonType': 'Regular+Season',
            'ShotClockRange': '',
            'StarterBench': '',
            'TeamID': '0',
            'TwoWay': '0',
            'VsConference': '',
            'VsDivision': '',
            'Weight': ''
        }
