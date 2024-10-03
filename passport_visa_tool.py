import streamlit as st
import requests
import pandas as pd
from visa_rules import get_best_option, VISA_RANK, VISA_RULES

# Set page layout to 'wide' for a better table display
st.set_page_config(layout="wide")

# Add this function near the top of the file, after the imports
def get_flag_emoji(country_code):
    return ''.join(chr(ord(c) + 127397) for c in country_code.upper())

# API Endpoints
COUNTRIES_URL = "https://api.henleypassportindex.com/api/v3/countries"
VISA_URL_TEMPLATE = "https://api.henleypassportindex.com/api/v3/visa-single/{passport_code}"

# Function to fetch country codes, names, and ISO codes from the API
@st.cache_data
def get_country_data():
    response = requests.get(COUNTRIES_URL, timeout=10)
    if response.status_code == 200:
        countries_data = response.json().get("countries", [])
        country_dict = {country['country']: country['code'] for country in countries_data}
        all_countries = [country['country'] for country in countries_data]
        return country_dict, all_countries
    else:
        st.error(f"Failed to fetch country data. API returned status code: {response.status_code}")
        return {}, []

# Fetch the list of countries and their data
passport_countries, all_countries = get_country_data()

# Streamlit App Interface
st.title("Passport Visa Access Tool")

# Check if passport_countries is not empty before displaying the dropdown
if passport_countries:
    # Multi-select for passports
    selected_passports = st.multiselect("Select your passport countries:", list(passport_countries.keys()))

    # Multi-select for visa/residence permits
    visa_options = [
        "USA Visa/Green Card", "Canadian Visa/PR", "Schengen Visa", "UK Visa", 
        "Australian Visa", "New Zealand Visa", "Irish Visa", "Japanese Visa", 
        "GCC Residence Permit"
    ]
    selected_visas = st.multiselect("Select visa/residence permits you hold:", visa_options)

    # Proceed if at least one passport is selected
    if selected_passports:
        passport_codes = [passport_countries[country] for country in selected_passports]

        # Fetch visa requirements for all selected passports
        visa_data = []
        for passport_code in passport_codes:
            response = requests.get(VISA_URL_TEMPLATE.format(passport_code=passport_code), timeout=10)
            if response.status_code == 200:
                visa_data.append(response.json())
            else:
                st.error(f"Failed to fetch visa data for {passport_code}. Please try again later.")
                break

        if len(visa_data) == len(passport_codes):
            # Initialize the list before the loop
            combined_visa_details = []

            # Map countries to their best access option
            for country_name in all_countries:
                visa_detail = {"Country": country_name}
                options = []
                passports = []

                for i, (passport, data) in enumerate(zip(selected_passports, visa_data)):
                    is_home_country = country_name == passport
                    option = "Citizenship" if is_home_country else None

                    if not option:
                        for category in VISA_RANK:
                            category_key = category.replace(" ", "_").lower()
                            if any(c['name'] == country_name for c in data.get(category_key, [])):
                                option = category
                                break

                    options.append(option if option else "No Access")
                    passports.append(passport)
                    visa_detail[f"Passport {i+1}"] = option if option else "No Access"

                best_option, applicable_visa = get_best_option(options, selected_visas, country_name, selected_passports)
                visa_detail["Access Type"] = best_option
                
                # Determine the best travel document
                if applicable_visa:
                    visa_detail["Travel Document"] = applicable_visa
                else:
                    best_index = next((i for i, opt in enumerate(options) if opt == best_option), 0)
                    visa_detail["Travel Document"] = passports[best_index]
                
                combined_visa_details.append(visa_detail)

            # Convert to a DataFrame
            df = pd.DataFrame(combined_visa_details)

            # Reorder columns to ensure "Access Type" and "Travel Document" are at the far right
            columns = ["Country"] + [f"Passport {i+1}" for i in range(len(selected_passports))] + ["Access Type", "Travel Document"]
            df = df[columns]

            # Get flag emojis for the selected countries
            flags = [get_flag_emoji(passport_countries[country]) for country in selected_passports]

            # Rename columns with country codes and flag emojis
            for i, (flag, country) in enumerate(zip(flags, selected_passports)):
                df = df.rename(columns={f"Passport {i+1}": f"{flag} {country}"})

            # Set the "Country" column as the index
            df = df.set_index("Country")

            # Define a color map for different visa categories with background and text colors
            color_map = {
                "Citizenship": {"background": "#E6B8B7", "text": "#000000"},
                "Visa free access": {"background": "#C6EFCE", "text": "#006100"},
                "Visa on arrival": {"background": "#FFEB9C", "text": "#9C6500"},
                "Visa required": {"background": "#FFC7CE", "text": "#9C0006"},
                "Electronic travel authorisation": {"background": "#DDEBF7", "text": "#2F75B5"},
                "Visa online": {"background": "#FCE4D6", "text": "#974706"}
            }

            # Function to apply color to the "Access Type" column
            def style_access_type(val):
                for key in color_map:
                    if key in val:
                        return f'background-color: {color_map[key]["background"]}; color: {color_map[key]["text"]}; font-weight: bold'
                return ''

            # Apply the styling to the DataFrame
            styled_df = df.style.applymap(style_access_type, subset=['Access Type'])

            # Display the table
            st.subheader(f"Visa Access Comparison for {', '.join(selected_passports)}")

            # Display the styled DataFrame with custom CSS
            st.markdown("""
            <style>
            .dataframe {
                font-size: 12px;
                text-align: left;
            }
            .dataframe td, .dataframe th {
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                max-width: 150px;
                padding: 5px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Display the styled DataFrame
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.error("Failed to fetch visa data for all selected passports. Please try again later.")
    else:
        st.info("Please select at least one passport country.")
else:
    st.error("No countries available for selection.")