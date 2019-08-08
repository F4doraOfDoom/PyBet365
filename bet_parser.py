from bs4 import BeautifulSoup
from contextlib import suppress

RUN_EXAMPLE = 2


class Match:
    """
    This class stores information about a class
    """
    def __init__(self, team1: str, team2: str, state, _, score1: int, score2: int):
        self.team1 = self._sanitize(team1)
        self.team2 = self._sanitize(team2)
        self.state = state
        self.score1 = score1
        self.score2 = score2

    @staticmethod
    def _sanitize(team_name: str):
        return team_name[:-4] if team_name.endswith("GOAL") else team_name

    def __str__(self):
        return "{} vs {}, {} ({}, {})".format(self.team1, self.team2, self.state, self.score1, self.score2)

    def __repr__(self):
        return self.__str__()


def open_example_page():
    """
    For testing purposes.
    Reads the local bet365.html file and parses it.
    Activate by using the flag --testing
    :return:
    """
    with open("bet365.html", "r", encoding="utf8") as file:
        contents = file.read()
    return contents


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def parse_bet365(page=RUN_EXAMPLE):
    if page == RUN_EXAMPLE:
        page = open_example_page()
    else:
        pass
        #print("got\n " + page)

    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find_all('div')
    items = []
    for row in rows:
        if row.has_attr('class'):
            with suppress(IndexError):
                if "ipo-TeamStack_Team" in row['class']:
                    items.append(row.text)
                elif any(x.startswith("ipo-TeamPoints_TeamScore") for x in row['class']):
                    items.append(row.text)

    return [Match(*x) for x in chunks(items, 6)]
