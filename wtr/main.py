"""`wtr` main entry point."""
import argparse
import os
import time

import requests
from rich import print as rprint
from rich.table import Table

OPEN_WEATHER_API_BASE_URL = "https://api.openweathermap.org"
OPEN_WEATHER_API_LOCATION_END_POINT = f"{OPEN_WEATHER_API_BASE_URL}/geo/1.0/direct"
OPEN_WEATHER_API_WEATHER_END_POINT = f"{OPEN_WEATHER_API_BASE_URL}/data/2.5/onecall"


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
                CITY_NAME = city.capitalize()
                table = Table(title=f"\nWeather forecast for {city.capitalize()}\n")
                if weather_report is not None:
                    CITY_NAME = weather_report["CITY_NAME"]
                    table = get_display_table(table, args.week, city, CITY_NAME)
                    if table.columns and args.week:
                        for report in weather_report["daily"]:
                            table.add_row(
                                time.strftime("%B %d %Y", time.localtime(int(report["dt"]))),
                                f"{report['temp']['min']}°C - {report['temp']['max']}°C",
                                report["weather"][0]["description"].capitalize(),
                            )
                    else:
                        table.add_row(
                            f"{weather_report['current']['temp']}°C",
                            weather_report["current"]["weather"][0]["description"].capitalize(),
                        )
                if table.columns and table.rows:
                    rprint(table)
                else:
                    rprint(f"[i]No data available for [b][red]{city}[/red][/b][/i]")
            else:
                rprint(f"[i]Enter a valid city name, {city} is not a valid input[/i]")
                break
    else:
        rprint("[i]No API Key available to get weather report...[/i]")


def get_api_key():
    """Get API Key."""
    api_key = os.environ.get("WTR_OPEN_WEATHER_API_KEY")
    return api_key


def get_weather_report(city, api_key):
    """Get weather report for a specific location."""
    location_details = get_location_details(city, api_key)
    try:
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
                try:
                    response = response.json()
                    response["CITY_NAME"] = location_details["CITY_NAME"]
                except AttributeError:
                    pass
                return response
    except Exception:
        pass
    return None


def get_location_details(city, api_key):
    """Get latitude and longitude for a specific city."""
    try:
        if city and type(city) is str:
            response = requests.get(
                OPEN_WEATHER_API_LOCATION_END_POINT,
                params={"q": city, "appid": api_key},
            )
            if response.ok:
                location_details = {}
                response = response.json()
                try:
                    if response:
                        location_details[
                            "CITY_NAME"
                        ] = f"{response[0]['name']}, {response[0]['state']}, {response[0]['country']}"
                        if response[0]["lat"] is not None:
                            location_details["lat"] = response[0]["lat"]
                        if response[0]["lon"] is not None:
                            location_details["lon"] = response[0]["lon"]
                        return location_details
                except AttributeError:
                    pass
    except Exception:
        pass
    return None


def get_display_table(table, isWeek, city, CITY_NAME):
    """Get Table coloumn details to display."""
    if type(table) is not Table:
        table = Table(title="\nWeather forecast for {}\n".format(CITY_NAME if CITY_NAME else city.capitalize()))
    if isWeek:
        table = Table(title="\nWeather forecast for 7 days @ {}".format(CITY_NAME if CITY_NAME else city.capitalize()))
        table.add_column("Date", style="green")
        table.add_column("Temperature", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")
    else:
        table = Table(title="\nToday @ {} ".format(CITY_NAME if CITY_NAME else city.capitalize()))
        table.add_column("Temperature", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")
    return table


if __name__ == "__main__":
    main()
