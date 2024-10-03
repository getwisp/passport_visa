from visa_countries import VISA_COUNTRIES

# Define visa ranks
VISA_RANK = [
    "Citizenship",
    "Visa free access",
    "Electronic travel authorisation",
    "Visa on arrival",
    "Visa online",
    "Visa required"
]

class VisaRule:
    def __init__(self, name, countries):
        self.name = name
        self.countries = countries

    def check_access(self, country_name, nationality):
        return "Visa free access" if country_name in self.countries else "Visa required"

class USAVisaRule(VisaRule):
    def __init__(self):
        super().__init__("USA Visa/Green Card", VISA_COUNTRIES["USA Visa/Green Card"])

class CanadianVisaRule(VisaRule):
    def __init__(self):
        super().__init__("Canadian Visa/PR", VISA_COUNTRIES["Canadian Visa/PR"])

class SchengenVisaRule(VisaRule):
    def __init__(self):
        super().__init__("Schengen Visa", VISA_COUNTRIES["Schengen Visa"])

class UKVisaRule(VisaRule):
    def __init__(self):
        super().__init__("UK Visa", VISA_COUNTRIES["UK Visa"])

class AustralianVisaRule(VisaRule):
    def __init__(self):
        super().__init__("Australian Visa", VISA_COUNTRIES["Australian Visa"])

class NewZealandVisaRule(VisaRule):
    def __init__(self):
        super().__init__("New Zealand Visa", VISA_COUNTRIES["New Zealand Visa"])
        self.voa_countries = ["Egypt", "Qatar"]
        self.visa_free_countries = ["Montenegro", "Georgia", "South Korea"]
        self.armenia_voa_nationalities = [
            "Algeria", "Bahrain", "Belize", "Bhutan", "Bolivia", "Brunei", "Cambodia",
            "Colombia", "Costa Rica", "Cuba", "Egypt", "Fiji", "Grenada", "Guatemala",
            "Guyana", "Haiti", "Honduras", "India", "Indonesia", "Iraq", "Jamaica",
            "Kiribati", "Laos", "Malaysia", "Maldives", "Marshall Islands", "Micronesia",
            "Mongolia", "Morocco", "Myanmar", "Nauru", "Nicaragua", "Palau",
            "Papua New Guinea", "Paraguay", "Philippines", "Saint Kitts and Nevis",
            "Saint Lucia", "Samoa", "Saudi Arabia", "Solomon Islands", "Suriname",
            "East Timor", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkmenistan",
            "Tuvalu", "Vanuatu", "Venezuela", "Vietnam"
        ]
        self.taiwan_evisa_nationalities = [
            "Cambodia", "India", "Indonesia", "Laos", "Myanmar", "Vietnam"
        ]

    def check_access(self, country_name, nationality):
        if country_name in self.countries:
            return "Visa free access"
        elif country_name in self.voa_countries:
            return "Visa on arrival"
        elif country_name in self.visa_free_countries:
            return "Visa free access"
        elif country_name == "Armenia" and nationality in self.armenia_voa_nationalities:
            return "Visa on arrival"
        elif country_name == "Taiwan" and nationality in self.taiwan_evisa_nationalities:
            return "Electronic travel authorisation"
        else:
            return "Visa required"

class IrishVisaRule(VisaRule):
    def __init__(self):
        super().__init__("Irish Visa", VISA_COUNTRIES["Irish Visa"])
        self.additional_countries = [
            "Montenegro", "Georgia", "Sint Maarten", "Curacao", "Aruba",
            "Panama", "Costa Rica", "Mexico"
        ]

    def check_access(self, country_name, nationality):
        if country_name in self.countries or country_name in self.additional_countries:
            return "Visa free access"
        else:
            return "Visa required"

class JapaneseVisaRule(VisaRule):
    def __init__(self):
        super().__init__("Japanese Visa", VISA_COUNTRIES["Japanese Visa"])
        self.special_rules = {
            "Egypt": "Visa on arrival",
            "Montenegro": "Visa free access",
            "Kosovo": "Visa free access",
            "Georgia": "Visa free access",
            "Panama": "Visa free access",
        }
        self.armenia_voa_countries = [
            "Algeria", "Bahrain", "Belize", "Bhutan", "Bolivia", "Brunei", "Cambodia",
            "Colombia", "Costa Rica", "Cuba", "Egypt", "Fiji", "Grenada", "Guatemala",
            "Guyana", "Haiti", "Honduras", "India", "Indonesia", "Iraq", "Jamaica",
            "Kiribati", "Laos", "Malaysia", "Maldives", "Marshall Islands", "Micronesia",
            "Mongolia", "Morocco", "Myanmar", "Nauru", "Nicaragua", "Palau",
            "Papua New Guinea", "Paraguay", "Philippines", "Saint Kitts and Nevis",
            "Saint Lucia", "Samoa", "Saudi Arabia", "Solomon Islands", "Suriname",
            "East Timor", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkmenistan",
            "Tuvalu", "Vanuatu", "Venezuela", "Vietnam"
        ]
        self.taiwan_evisa_countries = [
            "Cambodia", "India", "Indonesia", "Laos", "Myanmar", "Vietnam"
        ]
        self.philippines_visa_free_countries = ["India", "China"]

    def check_access(self, country_name, nationality):
        if country_name in self.special_rules:
            return self.special_rules[country_name]
        elif country_name == "Armenia" and nationality in self.armenia_voa_countries:
            return "Visa on arrival"
        elif country_name == "Oman" and nationality in OMAN_EVISA_COUNTRIES:
            return "Electronic travel authorisation"
        elif country_name == "Taiwan" and nationality in self.taiwan_evisa_countries:
            return "Electronic travel authorisation"
        elif country_name == "Philippines" and nationality in self.philippines_visa_free_countries:
            return "Visa free access"
        else:
            return super().check_access(country_name, nationality)

class GCCResidencePermitRule(VisaRule):
    def __init__(self):
        super().__init__("GCC Residence Permit", VISA_COUNTRIES["GCC Residence Permit"])

    def check_access(self, country_name, nationality):
        if country_name in self.countries:
            return "Visa free access"
        elif country_name in GCC_COUNTRIES:
            return GCC_COUNTRIES[country_name]
        else:
            return "Visa required"

# GCC countries and their general visa policies
GCC_COUNTRIES = {
    "Saudi Arabia": "Visa on arrival",
    "Kuwait": "Electronic travel authorisation",
    "Bahrain": "Visa on arrival",
    "Qatar": "Visa on arrival",
    "United Arab Emirates": "Visa on arrival",
    "Oman": "Electronic travel authorisation"
}

# Countries eligible for Oman eVisa
OMAN_EVISA_COUNTRIES = [
    "Albania", "Armenia", "Azerbaijan", "Belarus", "Bhutan", "Bosnia and Herzegovina",
    "Costa Rica", "Cuba", "El Salvador", "Guatemala", "Honduras", "India", "Kazakhstan",
    "Kyrgyzstan", "Laos", "Maldives", "Mexico", "Morocco", "Nicaragua", "Panama", "Peru",
    "Tajikistan", "Turkmenistan", "Uzbekistan", "Vietnam"
]

VISA_RULES = {
    "USA Visa/Green Card": USAVisaRule(),
    "Canadian Visa/PR": CanadianVisaRule(),
    "Schengen Visa": SchengenVisaRule(),
    "UK Visa": UKVisaRule(),
    "Australian Visa": AustralianVisaRule(),
    "New Zealand Visa": NewZealandVisaRule(),
    "Irish Visa": IrishVisaRule(),
    "Japanese Visa": JapaneseVisaRule(),
    "GCC Residence Permit": GCCResidencePermitRule(),
}

def get_best_option(options, selected_visas, country_name, passports):
    best_option = min(options, key=lambda x: VISA_RANK.index(x) if x in VISA_RANK else len(VISA_RANK))
    applicable_visa = None

    for visa in selected_visas:
        for passport in passports:
            new_option = VISA_RULES[visa].check_access(country_name, passport)
            if VISA_RANK.index(new_option) < VISA_RANK.index(best_option):
                best_option = new_option
                applicable_visa = visa

    return best_option, applicable_visa

# Make sure to export the necessary components
__all__ = ['VISA_RANK', 'get_best_option', 'VISA_RULES']