"""`wtr` main entry point."""
import argparse
import os
import time

import requests

OPEN_WEATHER_API_BASE_URL = "https://api.openweathermap.org"
OPEN_WEATHER_API_LOCATION_END_POINT = f"{OPEN_WEATHER_API_BASE_URL}/geo/1.0/direct"
OPEN_WEATHER_API_WEATHER_END_POINT = f"{OPEN_WEATHER_API_BASE_URL}/data/2.5/onecall"
CITY_NAME = None


def main():
    """Run the `wtr` app."""
    args = get_args()
    if args is not None:
        display_weather_details(args)


def initialize_parser():
    """Initialize the required arguments for the `wtr` app."""
    parser = argparse.ArgumentParser(
        description="wtr is a command-line weather application. It shows the weather for the given locations."
    )
    parser.add_argument("location", help="Location to get weather for.", nargs="+")
    parser.add_argument(
        "-w", "--week", help="Show the weather for the next week starting from today.", action="store_true"
    )
    return parser


def get_args():
    """Get the command-line arguments."""
    return initialize_parser().parse_args()


def display_weather_details(args):
    """Get and display the weather report based on the arguments passed ."""
    api_key = get_api_key()
    if api_key is not None:
        for city in args.location:
            if city.isalpha():
                weather_report = get_weather_report(city, api_key)
                if weather_report is not None:
                    if args.week:
                        print(
                            "\n -- Weather forecast for 7 days @ {} -- ".format(
                                CITY_NAME if CITY_NAME else city.capitalize()
                            )
                        )
                        for report in weather_report["daily"]:
                            print(
                                "{} :\n {}°C - {}°C\n {}".format(
                                    time.strftime("%B %d %Y", time.localtime(int(report["dt"]))),
                                    report["temp"]["min"],
                                    report["temp"]["max"],
                                    report["weather"][0]["description"].capitalize(),
                                ),
                                end="\n\n",
                            )
                    else:
                        print(
                            "\n -- Today @ {} --\n {}°C\n {}".format(
                                CITY_NAME if CITY_NAME else city.capitalize(),
                                weather_report["current"]["temp"],
                                weather_report["current"]["weather"][0]["description"].capitalize(),
                            ),
                            end="\n\n",
                        )


def get_api_key():
    """Get API Key."""
    api_key = os.environ.get("WTR_OPEN_WEATHER_API_KEY")
    if api_key is None:
        print("Open Weather API Key is not available")
    return api_key


def get_weather_report(city, api_key):
    """Get weather report for a specific location."""
    location_details = get_location_details(city, api_key)
    if location_details is not None:
        response = requests.get(
            OPEN_WEATHER_API_WEATHER_END_POINT,
            params={
                "lat": location_details["lat"],
                "lon": location_details["lon"],
                "exclude": "hourly,minutely",
                "units": "metric",
                "appid": api_key,
            },
        )
        if response.ok:
            return response.json()
    return None


def get_location_details(city, api_key):
    """Get latitude and longitude for a specific city."""
    response = requests.get(
        OPEN_WEATHER_API_LOCATION_END_POINT,
        params={"q": city, "appid": api_key},
    )
    if response.ok:
        global CITY_NAME
        location_details = {}
        response = response.json()
        if response:
            CITY_NAME = f"{response[0]['name']}, {response[0]['state']}, {response[0]['country']}"
            if response[0]["lat"] is not None:
                location_details["lat"] = response[0]["lat"]
            if response[0]["lon"] is not None:
                location_details["lon"] = response[0]["lon"]
            return location_details
    return None


if __name__ == "__main__":
    main()
