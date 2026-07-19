COUNTRY_FLAGS = {
    "Albania": "🇦🇱",
    "Andorra": "🇦🇩",
    "Armenia": "🇦🇲",
    "Austria": "🇦🇹",
    "Azerbaijan": "🇦🇿",
    "Belarus": "🇧🇾",
    "Belgium": "🇧🇪",
    "Bosnia and Herzegovina": "🇧🇦",
    "Bulgaria": "🇧🇬",
    "Croatia": "🇭🇷",
    "Cyprus": "🇨🇾",
    "Czech Republic": "🇨🇿",
    "Denmark": "🇩🇰",
    "Estonia": "🇪🇪",
    "Finland": "🇫🇮",
    "France": "🇫🇷",
    "Georgia": "🇬🇪",
    "Germany": "🇩🇪",
    "Greece": "🇬🇷",
    "Hungary": "🇭🇺",
    "Iceland": "🇮🇸",
    "Ireland": "🇮🇪",
    "Italy": "🇮🇹",
    "Kosovo": "🇽🇰",
    "Latvia": "🇱🇻",
    "Liechtenstein": "🇱🇮",
    "Lithuania": "🇱🇹",
    "Luxembourg": "🇱🇺",
    "Malta": "🇲🇹",
    "Moldova": "🇲🇩",
    "Monaco": "🇲🇨",
    "Montenegro": "🇲🇪",
    "Netherlands": "🇳🇱",
    "North Macedonia": "🇲🇰",
    "Norway": "🇳🇴",
    "Poland": "🇵🇱",
    "Portugal": "🇵🇹",
    "Romania": "🇷🇴",
    "Russia": "🇷🇺",
    "San Marino": "🇸🇲",
    "Serbia": "🇷🇸",
    "Slovakia": "🇸🇰",
    "Slovenia": "🇸🇮",
    "Spain": "🇪🇸",
    "Sweden": "🇸🇪",
    "Switzerland": "🇨🇭",
    "Turkey": "🇹🇷",
    "Ukraine": "🇺🇦",
    "United Kingdom": "🇬🇧",
    "Vatican City": "🇻🇦",
}


def country_code_to_flag(code: str):
    return "".join(chr(127397 + ord(letter)) for letter in code.upper())


def get_country_flag(country: str):
    code = COUNTRY_FLAGS.get(country)

    if code is None:
        return "🌍"

    return country_code_to_flag(code)


def get_country_code(country: str):
    return COUNTRY_FLAGS.get(country)


def get_country_flag_url(country: str):
    code = get_country_code(country)

    if code is None:
        return None

    return f"https://flagcdn.com/w40/{code.lower()}.png"