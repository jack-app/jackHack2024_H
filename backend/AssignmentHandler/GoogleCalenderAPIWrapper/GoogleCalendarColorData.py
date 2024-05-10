# Google Calendar API v3 で使用されるカラーセット
# このカラーセットは2012年2月14日を最後に更新されていません。

# さしあたっては、このファイルは使用されません。

from pydantic import BaseModel
from pydantic_extra_types.color import Color

__raw_api_response = {
    "kind": "calendar#colors",
    "updated": "2012-02-14T00:00:00.000Z",
    "calendar": {
        "1": {"background": "#ac725e", "foreground": "#1d1d1d"},
        "2": {"background": "#d06b64", "foreground": "#1d1d1d"},
        "3": {"background": "#f83a22", "foreground": "#1d1d1d"},
        "4": {"background": "#fa573c", "foreground": "#1d1d1d"},
        "5": {"background": "#ff7537", "foreground": "#1d1d1d"},
        "6": {"background": "#ffad46", "foreground": "#1d1d1d"},
        "7": {"background": "#42d692", "foreground": "#1d1d1d"},
        "8": {"background": "#16a765", "foreground": "#1d1d1d"},
        "9": {"background": "#7bd148", "foreground": "#1d1d1d"},
        "10": {"background": "#b3dc6c", "foreground": "#1d1d1d"},
        "11": {"background": "#fbe983", "foreground": "#1d1d1d"},
        "12": {"background": "#fad165", "foreground": "#1d1d1d"},
        "13": {"background": "#92e1c0", "foreground": "#1d1d1d"},
        "14": {"background": "#9fe1e7", "foreground": "#1d1d1d"},
        "15": {"background": "#9fc6e7", "foreground": "#1d1d1d"},
        "16": {"background": "#4986e7", "foreground": "#1d1d1d"},
        "17": {"background": "#9a9cff", "foreground": "#1d1d1d"},
        "18": {"background": "#b99aff", "foreground": "#1d1d1d"},
        "19": {"background": "#c2c2c2", "foreground": "#1d1d1d"},
        "20": {"background": "#cabdbf", "foreground": "#1d1d1d"},
        "21": {"background": "#cca6ac", "foreground": "#1d1d1d"},
        "22": {"background": "#f691b2", "foreground": "#1d1d1d"},
        "23": {"background": "#cd74e6", "foreground": "#1d1d1d"},
        "24": {"background": "#a47ae2", "foreground": "#1d1d1d"},
    },
    "event": {
        "1": {"background": "#a4bdfc", "foreground": "#1d1d1d"},
        "2": {"background": "#7ae7bf", "foreground": "#1d1d1d"},
        "3": {"background": "#dbadff", "foreground": "#1d1d1d"},
        "4": {"background": "#ff887c", "foreground": "#1d1d1d"},
        "5": {"background": "#fbd75b", "foreground": "#1d1d1d"},
        "6": {"background": "#ffb878", "foreground": "#1d1d1d"},
        "7": {"background": "#46d6db", "foreground": "#1d1d1d"},
        "8": {"background": "#e1e1e1", "foreground": "#1d1d1d"},
        "9": {"background": "#5484ed", "foreground": "#1d1d1d"},
        "10": {"background": "#51b749", "foreground": "#1d1d1d"},
        "11": {"background": "#dc2127", "foreground": "#1d1d1d"},
    },
}


class GColor(BaseModel):
    key:int
    background:Color
    foreground:Color

CALENDER_COLORS = [
    GColor(
        key=int(key),
        background=Color(__raw_api_response["calendar"][key]["background"]),
        foreground=Color(__raw_api_response["calendar"][key]["foreground"])
    )
    for key in __raw_api_response["calendar"].keys()
]

CALENDER_COLOR_ANOTATIONS = {
    "dull_orange":1,
    "dull_red":2,
    "red":3,
    "light_red":4,
    "orange":5,
    "yellow":6,
    "mint_green":7,
    "green":8,
    "lime_green":9,
    "pastel_green":10,
    "pastel_yellow":11,
    "pastel_orange":12,
    "pastel_mint_green":13,
    "pastel_sky_blue":14,
    "pastel_blue":15,
    "blue":16,
    "pastel_vivid_blue":17,
    "pastel_purple":18,
    "light_gray":19,
    "subtle_red":20,
    "dull_pink":21,
    "pink":22,
    "vivid_purple":23,
    "purple":24
}

EVENT_COLORS = [
    GColor(
        key=int(key),
        background=Color(__raw_api_response["event"][key]["background"]),
        foreground=Color(__raw_api_response["event"][key]["foreground"])
    )
    for key in __raw_api_response["event"].keys()
]

EVENT_COLOR_ANOTATIONS = {
    "sky_blue":1,
    "mint_green":2,
    "purple":3,
    "light_red":4,
    "yellow":5,
    "orange":6,
    "light_blue":7,
    "gray":8,
    "blue":9,
    "green":10,
    "red":11
}

