#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:51:22 2022.

@author: Nishad Mandlik
"""

from enum import IntFlag, auto
import requests
import warnings
import json
import xml.etree.ElementTree as ET
import pandas as pd

_LOGIN_URL = "https://api.komoot.de/v006/account/email/%s/"
_TOURS_URL = "https://api.komoot.de/v007/users/%s/tours/"

_EMAIL_ID = "doron.shafrir@bezeqint.net"
_PASSWORD = "Bengefen74"


class API:
    """
    Class for interfacing with the Komoot API.

    Refer to https://static.komoot.de/doc/external-api/v007/index.html
    """

    def __init__(self):
        """
        Initialize a Komoot API object.

        """
        self.user_details = {}


    def login(self, email_id, password):
        """
        Authenticate user credentials and generate access token for the
        Komoot API.

        Parameters
        ----------
        email_id : str
            Email ID for Komoot account.
        password : str
            Password for Komoot account.

        Returns
        -------
        bool
            True if login is successful, False otherwise.

        """
        self.user_details = {}
        resp = requests.get(_LOGIN_URL % email_id, auth=(email_id, password))
        if (resp.status_code != 200):
            return False
        details = resp.json()
        self.user_details["email"] = email_id
        self.user_details["user_id"] = details["username"]
        self.user_details["disp_name"] = details["user"]["displayname"]
        self.user_details["dp_url"] = (
            details["user"]["imageUrl"]
            if details["user"]["content"]["hasImage"] else None)
        self.user_details["token"] = details["password"]
        # print(self.user_details)
        return True


    def get_user_tours_list(self, tour_type=None, tour_status=None,
                            sport=None, tour_owner=None):
        """
        Get the list of tours for the logged-in user, according to the
        user-defined filters.

        Parameters
        ----------
        tour_type : TourType or None, optional
            Bitwise OR-ed flags for filtering multiple tour types.
            The default is None.
        tour_status : TourStatus or None, optional
            Bitwise OR-ed flags for filtering multiple tour statuses.
            The default is None.
        sport : Sport or None, optional
            Bitwise OR-ed flags for filtering multiple sports.
            The default is None.
        tour_owner: TourOwner or None, optional
            Bitwise OR-ed flags for filtering activities according to creator
            (self or others).
            The default is None.

        Raises
        ------
        RuntimeError
            If no user is logged-in.

        Returns
        -------
        tours : list
            List of dictionaries containing details of tours.
        """

        if (self.user_details == {}):
            raise RuntimeError("User Details Not Available. Please Sign In.")
        params = {}
        params["page"] = 0
        ex_count = 1
               # ----------pandas firle creation ------------------------------#
        init_line = ['Date', 'Name', 'Duration', 'Distance', 'Speed', 'UpHill', 'DownHill']
        komoot_tours = pd.DataFrame(columns=init_line)
        while True:

            resp = requests.get(_TOURS_URL % self.user_details["user_id"],
                                params=params,
                                auth=(self.user_details["user_id"],
                                      self.user_details["token"]))
            if (resp.status_code != 200):
                warnings.warn("Request Failed. Tour List May Be Incomplete")
                break

            content = resp.json()
            if (content["page"]["totalElements"] == 0):
                break

            for data in content["_embedded"]["tours"]:
                date = data['date'][:10]
                name = data['name']
                distance = data['distance']
                try:
                    duration = data['time_in_motion']/3600
                    speed = round((distance / duration)/1000 , 1)
                    duration = round(duration , 2)
                except Exception:
                    duration = 0
                    speed = 0
                distance = round(distance / 1000, 2)
                upHill = int(data['elevation_up'])
                downHill = int(data['elevation_down'])
                # print(f"{ex_count}  {date}  {name}     {duration}  {distance} {speed}  {upHill} {downHill}" )

                ex_count += 1
                #-----------add line to komoot_tours---------------------------#

                line = pd.DataFrame([[date, name, duration, distance, speed, upHill, downHill]], columns=init_line)
                komoot_tours = komoot_tours.append(line, ignore_index=True)

            params["page"] += 1
            if (content["page"]["totalPages"] == params["page"]):
                break

        komoot_tours.to_csv('main.csv')








if __name__ == '__main__':
    get_list = API()
    get_list.login(get_list.email_id, get_list.password)
    get_list.get_user_tours_list()