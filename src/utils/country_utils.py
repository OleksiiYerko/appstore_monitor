#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pycountry

# Словарь с эмодзи флагами стран
COUNTRY_FLAGS = {
    "US": "🇺🇸",
    "GB": "🇬🇧",
    "CA": "🇨🇦",
    "AU": "🇦🇺",
    "DE": "🇩🇪",
    "FR": "🇫🇷",
    "IT": "🇮🇹",
    "ES": "🇪🇸",
    "JP": "🇯🇵",
    "KR": "🇰🇷",
    "CN": "🇨🇳",
    "RU": "🇷🇺",
    "BR": "🇧🇷",
    "MX": "🇲🇽",
    "IN": "🇮🇳",
    "NL": "🇳🇱",
    "SE": "🇸🇪",
    "NO": "🇳🇴",
    "DK": "🇩🇰",
    "FI": "🇫🇮",
    "PL": "🇵🇱",
    "CZ": "🇨🇿",
    "AT": "🇦🇹",
    "CH": "🇨🇭",
    "BE": "🇧🇪",
    "IE": "🇮🇪",
    "PT": "🇵🇹",
    "GR": "🇬🇷",
    "TR": "🇹🇷",
    "IL": "🇮🇱",
    "SA": "🇸🇦",
    "AE": "🇦🇪",
    "SG": "🇸🇬",
    "MY": "🇲🇾",
    "TH": "🇹🇭",
    "VN": "🇻🇳",
    "PH": "🇵🇭",
    "ID": "🇮🇩",
    "NZ": "🇳🇿",
    "ZA": "🇿🇦",
    "EG": "🇪🇬",
    "NG": "🇳🇬",
    "KE": "🇰🇪",
    "MA": "🇲🇦",
    "TN": "🇹🇳",
    "AR": "🇦🇷",
    "CL": "🇨🇱",
    "CO": "🇨🇴",
    "PE": "🇵🇪",
    "VE": "🇻🇪",
    "EC": "🇪🇨",
    "UY": "🇺🇾",
    "PY": "🇵🇾",
    "BO": "🇧🇴",
    "CR": "🇨🇷",
    "PA": "🇵🇦",
    "GT": "🇬🇹",
    "SV": "🇸🇻",
    "HN": "🇭🇳",
    "NI": "🇳🇮",
    "DO": "🇩🇴",
    "CU": "🇨🇺",
    "JM": "🇯🇲",
    "TT": "🇹🇹",
    "BB": "🇧🇧",
    "GY": "🇬🇾",
    "SR": "🇸🇷",
    "GF": "🇬🇫",
    "MQ": "🇲🇶",
    "GP": "🇬🇵",
    "HT": "🇭🇹",
    "LC": "🇱🇨",
    "VC": "🇻🇨",
    "GD": "🇬🇩",
    "AG": "🇦🇬",
    "KN": "🇰🇳",
    "DM": "🇩🇲",
    "BZ": "🇧🇿",
    "BH": "🇧🇭",
    "KW": "🇰🇼",
    "OM": "🇴🇲",
    "QA": "🇶🇦",
    "JO": "🇯🇴",
    "LB": "🇱🇧",
    "SY": "🇸🇾",
    "IQ": "🇮🇶",
    "IR": "🇮🇷",
    "AF": "🇦🇫",
    "PK": "🇵🇰",
    "BD": "🇧🇩",
    "LK": "🇱🇰",
    "NP": "🇳🇵",
    "BT": "🇧🇹",
    "MM": "🇲🇲",
    "LA": "🇱🇦",
    "KH": "🇰🇭",
    "MN": "🇲🇳",
    "KP": "🇰🇵",
    "TW": "🇹🇼",
    "HK": "🇭🇰",
    "MO": "🇲🇴",
    "BN": "🇧🇳",
    "TL": "🇹🇱",
    "FJ": "🇫🇯",
    "PG": "🇵🇬",
    "SB": "🇸🇧",
    "VU": "🇻🇺",
    "NC": "🇳🇨",
    "PF": "🇵🇫",
    "TO": "🇹🇴",
    "WS": "🇼🇸",
    "AS": "🇦🇸",
    "GU": "🇬🇺",
    "MP": "🇲🇵",
    "FM": "🇫🇲",
    "PW": "🇵🇼",
    "MH": "🇲🇭",
    "KI": "🇰🇮",
    "TV": "🇹🇻",
    "NR": "🇳🇷",
    "CK": "🇨🇰",
    "NU": "🇳🇺",
    "TK": "🇹🇰",
    "WF": "🇼🇫"
}

def get_country_name(country_code):
    """Получает локализованное название страны по коду с флагом"""
    try:
        country = pycountry.countries.get(alpha_2=country_code.upper())
        flag = COUNTRY_FLAGS.get(country_code.upper(), "")
        if country:
            return f"{flag} {country.name}"
        else:
            return f"{flag} {country_code.upper()}"
    except Exception:
        flag = COUNTRY_FLAGS.get(country_code.upper(), "")
        return f"{flag} {country_code.upper()}"

def get_country_flag(country_code):
    """Получает только флаг страны"""
    return COUNTRY_FLAGS.get(country_code.upper(), "")

def is_valid_country_code(country_code):
    """Проверяет, является ли код страны валидным"""
    try:
        return pycountry.countries.get(alpha_2=country_code.upper()) is not None
    except Exception:
        return False 