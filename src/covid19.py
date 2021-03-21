import requests
import locale
import datetime
from tabulate import tabulate
from pyfiglet import figlet_format

try:
    from termcolor import colored
except ImportError:
    colored = None


def log(message, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            print(colored(message, color))
        else:
            print(colored(figlet_format(message, font=font), color))
    else:
        print(message)


def format_number(number):
    return "{:,}".format(number).replace(",", ".")


def fetch_data():
    try:
        r = requests.get(
            "https://coronavirus-italia.netlify.app/preact_prerender_data.json"
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        log(f"Error: {e}", color="red")
        # raise(e)

def main():
    log("COVID-19", color="red", figlet=True)
    log("Numeri del Covid-19 in Italia\n ", color="white")
    locale.setlocale(locale.LC_ALL, "it_IT")
    try:
        data = fetch_data()

        data_latest = data.get("dataLatest")
        cleaned_data = data.get("cleanedData")

        new_positives = data_latest.get("nuovi_positivi")
        new_positives_diff = cleaned_data.get("newCasesDiff").get("number")

        swabs = cleaned_data.get("swabDiff").get("new")
        swabs_diff = cleaned_data.get("swabDiff").get("number")

        cured = cleaned_data.get("recoveredDiff").get("new")
        cured_diff = cleaned_data.get("recoveredDiff").get("number")

        deaths = cleaned_data.get("deathDiff").get("new")
        deaths_diff = cleaned_data.get("deathDiff").get("number")

        build_date = data.get("buildTime")
        date_time_obj = datetime.datetime.strptime(build_date, "%Y-%m-%dT%H:%M:%S.%fZ")

        log(
            f"Ultimo aggiornamento: {date_time_obj.date()} alle {date_time_obj.strftime('%H:%M:%S')}\n",
            color="green",
        )

        print(
            tabulate(
                [
                    [
                        "Nuovi positivi",
                        format_number(new_positives),
                        format_number(new_positives_diff),
                    ],
                    ["Guariti", format_number(cured), format_number(cured_diff)],
                    ["Decessi", format_number(deaths), format_number(deaths_diff)],
                    ["Tamponi", format_number(swabs), format_number(swabs_diff)],
                ],
                tablefmt="fancy_grid",
                colalign=["left", "right", "right"],
            )
        )

    except:
        log("There have been some problems!", color="red")

if __name__ == "__main__":
    main()
