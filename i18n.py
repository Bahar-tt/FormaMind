import json
import os
from datetime import datetime
import babel
from babel.dates import format_date, format_time, format_datetime
from babel.numbers import format_number, format_decimal, format_percent

class I18nManager:
    def __init__(self):
        self.translations_dir = "translations"
        self.default_locale = "en"
        self.current_locale = self.default_locale
        self.translations = {}
        self.date_formats = {
            "short": "short",
            "medium": "medium",
            "long": "long",
            "full": "full"
        }
        self.time_formats = {
            "short": "short",
            "medium": "medium",
            "long": "long",
            "full": "full"
        }
        self.number_formats = {
            "decimal": "#,##0.###",
            "percent": "#,##0%",
            "currency": "#,##0.00"
        }
        
        # Create translations directory if it doesn't exist
        if not os.path.exists(self.translations_dir):
            os.makedirs(self.translations_dir)
        
        # Load translations
        self._load_translations()

    def _load_translations(self):
        """Load all translation files"""
        for filename in os.listdir(self.translations_dir):
            if filename.endswith(".json"):
                locale = filename[:-5]  # Remove .json extension
                with open(os.path.join(self.translations_dir, filename), 'r', encoding='utf-8') as f:
                    self.translations[locale] = json.load(f)

    def _save_translations(self, locale):
        """Save translations for a specific locale"""
        if locale in self.translations:
            with open(os.path.join(self.translations_dir, f"{locale}.json"), 'w', encoding='utf-8') as f:
                json.dump(self.translations[locale], f, ensure_ascii=False, indent=4)

    def set_locale(self, locale):
        """Set the current locale"""
        if locale in self.translations:
            self.current_locale = locale
            return True
        return False

    def get_locale(self):
        """Get the current locale"""
        return self.current_locale

    def get_available_locales(self):
        """Get list of available locales"""
        return list(self.translations.keys())

    def translate(self, key, **kwargs):
        """Translate a key to the current locale"""
        if self.current_locale not in self.translations:
            return key

        # Get translation
        translation = self.translations[self.current_locale].get(key, key)
        
        # Replace placeholders
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError:
                pass
        
        return translation

    def add_translation(self, locale, key, value):
        """Add a new translation"""
        if locale not in self.translations:
            self.translations[locale] = {}
        
        self.translations[locale][key] = value
        self._save_translations(locale)
        return True

    def remove_translation(self, locale, key):
        """Remove a translation"""
        if locale in self.translations and key in self.translations[locale]:
            del self.translations[locale][key]
            self._save_translations(locale)
            return True
        return False

    def format_date(self, date, format_type="medium"):
        """Format a date according to the current locale"""
        if format_type not in self.date_formats:
            format_type = "medium"
        
        try:
            return format_date(date, format=self.date_formats[format_type], locale=self.current_locale)
        except Exception:
            return str(date)

    def format_time(self, time, format_type="medium"):
        """Format a time according to the current locale"""
        if format_type not in self.time_formats:
            format_type = "medium"
        
        try:
            return format_time(time, format=self.time_formats[format_type], locale=self.current_locale)
        except Exception:
            return str(time)

    def format_datetime(self, datetime_obj, format_type="medium"):
        """Format a datetime according to the current locale"""
        if format_type not in self.date_formats:
            format_type = "medium"
        
        try:
            return format_datetime(datetime_obj, format=self.date_formats[format_type], locale=self.current_locale)
        except Exception:
            return str(datetime_obj)

    def format_number(self, number, format_type="decimal"):
        """Format a number according to the current locale"""
        if format_type not in self.number_formats:
            format_type = "decimal"
        
        try:
            if format_type == "percent":
                return format_percent(number, locale=self.current_locale)
            elif format_type == "currency":
                return format_decimal(number, format=self.number_formats[format_type], locale=self.current_locale)
            else:
                return format_number(number, locale=self.current_locale)
        except Exception:
            return str(number)

    def get_text_direction(self):
        """Get text direction for current locale"""
        try:
            locale = babel.Locale(self.current_locale)
            return locale.text_direction
        except Exception:
            return "ltr"

    def get_language_name(self, locale=None):
        """Get language name in its native form"""
        if locale is None:
            locale = self.current_locale
        
        try:
            return babel.Locale(locale).get_language_name()
        except Exception:
            return locale

    def get_territory_name(self, locale=None):
        """Get territory name in its native form"""
        if locale is None:
            locale = self.current_locale
        
        try:
            return babel.Locale(locale).get_territory_name()
        except Exception:
            return locale

    def get_currency_name(self, currency_code):
        """Get currency name in current locale"""
        try:
            return babel.Locale(self.current_locale).currencies.get(currency_code, currency_code)
        except Exception:
            return currency_code

    def get_currency_symbol(self, currency_code):
        """Get currency symbol for current locale"""
        try:
            return babel.Locale(self.current_locale).currency_symbols.get(currency_code, currency_code)
        except Exception:
            return currency_code

    def get_weekday_names(self, width="wide"):
        """Get weekday names in current locale"""
        try:
            locale = babel.Locale(self.current_locale)
            return locale.days.get(width, locale.days["wide"])
        except Exception:
            return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def get_month_names(self, width="wide"):
        """Get month names in current locale"""
        try:
            locale = babel.Locale(self.current_locale)
            return locale.months.get(width, locale.months["wide"])
        except Exception:
            return ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]

    def get_measurement_system(self):
        """Get measurement system for current locale"""
        try:
            locale = babel.Locale(self.current_locale)
            return locale.measurement_system
        except Exception:
            return "metric"

    def get_first_week_day(self):
        """Get first day of week for current locale"""
        try:
            locale = babel.Locale(self.current_locale)
            return locale.first_week_day
        except Exception:
            return 0  # Monday

    def get_timezone_name(self, timezone):
        """Get timezone name in current locale"""
        try:
            return babel.dates.get_timezone_name(timezone, locale=self.current_locale)
        except Exception:
            return str(timezone)

    def get_plural_form(self, number):
        """Get plural form for number in current locale"""
        try:
            locale = babel.Locale(self.current_locale)
            return locale.plural_form(number)
        except Exception:
            return "other" 