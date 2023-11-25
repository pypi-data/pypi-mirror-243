import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta


class PsusannxBetfair():
    """
    A class containing functions for connecting to the Betfair Exchange API.
    It's main function is to get Betfair Exchange match odds for upcoming games.
    """
    
    def __init__(self, username, password, app_key, crt_path, pem_path, team_mapping={}):
        """
        Store Betfair credentials & cert paths on creation of class instance.
        
        Parameters
        ----------
        username: str
            The username of the Betfair account.
        
        password: str
            The password for the Betfair account.
        
        app_key: str
            The application key associated with the Betfair account.
            
        crt_path: str
            The path to the .crt file. This is one of the certificates required to make an API call.
            
        pem_path: str
            The path to the .pem file. This is one of the certificates required to make an API call.

        team_mapping: dict
            A mapping dictionary to standardize the team names. eg {"Manchester United": "Man United", "Norwich City": "Norwich"}.
            
        Returns
        -------
        None
        """
        
        # Store the credentials in the class instance
        self.USERNAME = username
        self.PASSWORD = password
        self.APP_KEY = app_key
        self.CRT_PATH = crt_path
        self.PEM_PATH = pem_path
        self.team_mapping = team_mapping
        
        # Create the payload with the username & password for the betfair account
        payload = f"username={self.USERNAME}&password={self.PASSWORD}"

        # Create the required headers to be passed to the request
        headers = {
            "X-Application": self.APP_KEY, 
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Send the post request to login & get the response
        resp = requests.post("https://identitysso-cert.betfair.com/api/certlogin", 
                             data=payload, 
                             cert=(self.CRT_PATH, self.PEM_PATH), 
                             headers=headers)

        if resp.status_code == 200:
            resp_json = resp.json()
            print(f"Betfair Exchange Login Status: {resp_json['loginStatus']}")

            # Store the session token in the class instance
            self.SESSION_TOKEN = resp_json["sessionToken"]
            
        else:
            print("Request failed.")


    def extract_odds_df_from_dict(self, dictionary):
        """Extract the odds as a dataframe from the dictionary containing the odds info."""

        # Set up empty lists to hold the info
        selection_ids = []
        backing_prices = []
        
        # Loop over every element in the dictionary
        for elem in dictionary:
            selection_ids.append(elem["selectionId"])
            backing_prices.append(elem["ex"]["availableToBack"][0]["price"])
            
        return pd.DataFrame({
            "selectionId": selection_ids, 
            "backingPrice":backing_prices
        })


    def make_betfair_api_request(self, request_string):
        """
        Make a request to the Betfair api and return a json.
        
        Parameters
        ----------
        request_string: str
            The request to hit the api with (Sign in to betfair.com then use:
            https://docs.developer.betfair.com/visualisers/api-ng-sports-operations/ 
            to test the generation of request strings).

        Returns
        -------
        dict
            The response from the api.
        """
        
        # Set up the base URL to send requests to
        base_url="https://api.betfair.com/exchange/betting/json-rpc/v1"
        
        # Set up the headers dictionary
        headers = {
            "X-Application": self.APP_KEY, 
            "X-Authentication": self.SESSION_TOKEN, 
            "Content-Type": "application/json"
        }
        
        # Make the request
        request = requests.post(base_url, 
                                data=request_string.encode("utf-8"), 
                                headers=headers)
        
        return request.json()
    
    
    def list_upcoming_pl_matches(self):
        """
        List the upcoming Premier League matches that 
        are available on the Betfair Exchange.
        """
        
        # Set up the request string to list the upcoming premier league events on the betfair exchange
        pl_events_request_string = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": {"filter":{"competitionIds":["10932509"],"marketCountries":["GB"]}}, "id": 1}'
    
        # Make the request to get the upcoming pl events
        pl_events = self.make_betfair_api_request(pl_events_request_string)

        # Put the events into a dataframe sorted from earliest kickoff to latest
        events_df = (
            pd
            .concat([pd.DataFrame(x["event"], index=[0]) for x in pl_events["result"]])
            .sort_values("openDate")
            .reset_index(drop=True)
        )
        
        # Only keep rows where there is a " v " in the name field
        events_df = events_df[[" v " in name for name in events_df.name]].reset_index(drop=True)

        # Set the openDate field to be a datetime object
        events_df["openDate"] = pd.to_datetime(events_df.openDate)

        # Split the event name up into home & away team names
        home_teams = [x.split(" v ")[0] for x in events_df.name]
        away_teams = [x.split(" v ")[1] for x in events_df.name]
        events_df["Home_team"] = home_teams
        events_df["Away_team"] = away_teams

        # Clean the dataframe a bit
        events_df = (
            events_df
            .drop(columns=["name", "countryCode", "timezone"])
            .replace(self.team_mapping)
        )
        
        return events_df
    
    
    def get_betfair_exchange_odds(self, home_team, away_team):
        """
        Get the betfair exchange odds for an upcoming premier league match.
        (the match must be available to bet on online when the function runs)
        
        Parameters
        ----------
        home_team: str
            The name of the home team in the match to bet on.
        
        away_team: str
            The name of the away team in the match to bet on.
            
        Returns
        -------
        pandas.DataFrame with betfair exchange odds info.
        """
        
        # Use a class method to get the upcoming pl matches on the betfair exchange
        events_df = self.list_upcoming_pl_matches()
        
        try:
        
            # Get the betfair event ID of the current match of interest
            current_match_event_id = (
                events_df
                .query(f"""Home_team == '{home_team}' & Away_team == '{away_team}'""")
                .id
                .values[0]
            )
        
        except:
            
            print(f"There is no match between {home_team} & {away_team} in the available matches on the betfair exchange.\nReturning a dataframe with NA's")
            
            # Create a dataframe with missing odds values
            self.odds_df = pd.DataFrame({
                    "Home_team": home_team,
                    "Away_team": away_team,
                    "Home_odds": np.nan,
                    "Draw_odds": np.nan,
                    "Away_odds": np.nan,
                    "Approx_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }, index=[0]
            ).replace(self.team_mapping)
            
            return self.odds_df
        
        # List all the possible betting markets for that event
        list_betting_markets_request = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventIds":["' + current_match_event_id + '"]},"maxResults":"100"}, "id": 1}'
        betting_markets = self.make_betfair_api_request(list_betting_markets_request)

        # Put the event markets into a dataframe
        event_markets_df = (
            pd
            .concat([pd.DataFrame(x, index=[0]) for x in betting_markets["result"]])
            .sort_values("totalMatched", ascending=False)
        )

        # Get the market corresponding to the match odds
        match_odds_market = event_markets_df.query("""marketName == 'Match Odds'""")

        # Get the specific market ID
        match_odds_market_id = match_odds_market.marketId[0]

        # Get the selection IDs for each selection in the market (home team win, away team win or draw)
        selection_id_request_string = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"marketIds":["' + match_odds_market_id + '"]},"maxResults":"1","marketProjection":["RUNNER_METADATA"]}, "id": 1}'
        selection_id_dict = self.make_betfair_api_request(selection_id_request_string)
        betting_options = selection_id_dict["result"][0]["runners"]

        # Create a dataframe with the selection IDs and the selection names(home team, away team, draw)
        selection_id_name_df = (
            pd
            .concat([pd.DataFrame(x, index=[0]) for x in betting_options])[["selectionId", "runnerName"]]
            .reset_index(drop=True)
        )

        # Get the market info for each selection in the market (home odds, away odds, draw odds)
        market_odds_request_str = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": {"marketIds":["' + match_odds_market_id + '"], "priceProjection": {"priceData": ["EX_BEST_OFFERS", "EX_TRADED"],"virtualise": "true"}}, "id": 1}'
        match_odds_market = self.make_betfair_api_request(market_odds_request_str)

        # Extract the selection IDs and the odds from the json info 
        selection_odds = match_odds_market["result"][0]["runners"]
        selection_id_odds_df = self.extract_odds_df_from_dict(selection_odds)

        # Merge the dataframes with the selection IDs, names and odds together
        merged_odds_df = pd.merge(selection_id_name_df, selection_id_odds_df, on="selectionId")

        # Extract the individual info from the dataframe
        home_team = merged_odds_df["runnerName"].values[0]
        away_team = merged_odds_df["runnerName"].values[1]
        home_odds = merged_odds_df["backingPrice"].values[0]
        away_odds = merged_odds_df["backingPrice"].values[1]
        draw_odds = merged_odds_df["backingPrice"].values[2]
        approx_time = (datetime.now() - timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S")

        # Create the odds dataframe with the betfair odds
        self.odds_df = pd.DataFrame({
            "Home_team": home_team,
            "Away_team": away_team,
            "Home_odds": home_odds,
            "Draw_odds": draw_odds,
            "Away_odds": away_odds,
            "Approx_time": approx_time
            }, index=[0]
        ).replace(self.team_mapping)

        return self.odds_df
    

    def create_betfair_ex_odds_data_string(self):
        """Create the Betfair Exchange odds data string"""

        # Extract the data from the current match odds df to create the string
        home_team, away_team, home_odds, draw_odds, away_odds = self.odds_df[["Home_team", "Away_team", "Home_odds", "Draw_odds", "Away_odds"]].values[0]
        
        # Create the odds output string
        odds_data_string = f"\n-> Betfair Exchange Odds Info:\n\n{home_team}: {home_odds}\nDraw: {draw_odds}\n{away_team}: {away_odds}\n"

        return odds_data_string

