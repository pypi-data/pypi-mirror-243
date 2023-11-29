#      Copyright (C) 2020 <Florian Alu - Prolibre - https://prolibre.com
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _


def year_choices():
    now = timezone.localdate()
    min_date = now.year - 1
    max_date = now.year + 2
    return [(r, r) for r in range(min_date, max_date)], now


class AddOfficialHolidayForm(forms.Form):
    """Formulaire de validation pour l'ajout"""
    year = forms.ChoiceField(label=_("Year"), choices=year_choices()[0], initial=year_choices()[1])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-add-holiday-Form'
        self.helper.form_class = 'form-horizontal blueForms'
        self.helper.form_method = 'post'
        self.helper.label_class = ""
        self.helper.field_class = "col-lg-12"

        self.helper.add_input(Submit('submit', _("Submit")))
