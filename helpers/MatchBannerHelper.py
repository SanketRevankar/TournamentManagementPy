import subprocess
from datetime import timezone
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

from TournamentManagementPy import handler
from constants import StringConstants as sC


class MatchBannerHelper:
    def __init__(self, config):
        self.banner_img_path = config[sC.FILE_LOCATIONS][sC.BANNER_IMG]
        self.locations_font_path_ = config[sC.FILE_LOCATIONS][sC.BANNER_FONT]
        self.temp = config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER]

    def create_banner(self, match_id):
        """
        Prints the name on the certificate using position defined in Config file

        :param team: Team of the player
        :param c_name: Name of the player
        """

        image = Image.open(self.banner_img_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.locations_font_path_, size=40)
        size = (339, 339)

        match_data = handler.fireStoreHelper.util.get_match_data_by_id(match_id)
        team_1_data = handler.dataHelper.get_team_data_by_id(match_data['team_1'])
        team_2_data = handler.dataHelper.get_team_data_by_id(match_data['team_2'])

        team_1_logo = Image.open(BytesIO(requests.get(team_1_data['team_logo_url']).content))
        team_1_logo.thumbnail(size)
        team_2_logo = Image.open(BytesIO(requests.get(team_2_data['team_logo_url']).content))
        team_2_logo.thumbnail(size)

        self.add_team_1_name(team_1_data['team_name'], draw, font)
        self.add_team_2_name(team_2_data['team_name'], draw, font)
        self.add_timing(match_data['match_time'].replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%d-%m-%Y %I:%M %p'), draw, font)
        self.add_match_name('Match #' + match_id.zfill(2), draw, font)

        banner = Image.new('RGBA', (1280, 720), (255, 255, 255, 255))
        banner.paste(image)
        banner.paste(team_1_logo, (74, 148))
        banner.paste(team_2_logo, (865, 148))

        path = self.temp + match_id +'.png'
        banner.save(path)

        return open(path, 'rb')

    def add_team_1_name(self, text, draw, font):
        (x, y) = (75, 562)
        color = '#465dab'
        w, _ = draw.textsize(text, font=font)
        draw.text((x + (335 - w)/2, y), text, fill=color, font=font)

    def add_team_2_name(self, text, draw, font):
        (x, y) = (865, 562)
        color = '#465dab'
        w, _ = draw.textsize(text, font=font)
        draw.text((x + (335 - w)/2, y), text, fill=color, font=font)

    def add_timing(self, text, draw, font):
        (x, y) = (495, 500)
        color = '#465dab'
        w, _ = draw.textsize(text, font=font)
        draw.text((x + (290 - w)/2, y), text, fill=color, font=font)

    def add_match_name(self, text, draw, font):
        (x, y) = (485, 5)
        color = '#465dab'
        w, _ = draw.textsize(text, font=font)
        draw.text((x + (315 - w)/2, y), text, fill=color, font=font)
