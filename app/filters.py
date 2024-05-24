
from flask import has_app_context
from flask_admin.model.filters import BaseBooleanFilter
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_admin.babel import lazy_gettext
from sqlalchemy import or_, and_


from app.env import db
from app.models import SuiviPhoto, Taxons, SuiviAtributs
from app.utils import DynamicOptionsMixin



class PatrionialFilter(FilterEqual):
    def apply(self, query, value, alias=None):
        if int(value) == 1:
            return query.filter(self.column == "oui")
        else:
            return query.filter(self.column == "non")

    
class HasPhotoFilter(FilterEqual):
    def apply(self, query, value, alias=None):
        if int(value) == 1:
            return query.filter(SuiviPhoto.nb_photos > 0)
        else:
            return query.filter(SuiviPhoto.nb_photos == 0)


class IsCompleteFilter(BaseBooleanFilter):
    def apply(self, query, value, alias=None):
        if int(value) == 0:
            return query.filter(and_(
                SuiviAtributs.description.is_not(None),
                SuiviAtributs.commentaire.is_not(None),
                SuiviAtributs.milieu.is_not(None),
                SuiviAtributs.repartition.is_not(None)
            ))
        else:
            return query.filter(or_(
                SuiviAtributs.description.is_(None),
                SuiviAtributs.commentaire.is_(None),
                SuiviAtributs.milieu.is_(None),
                SuiviAtributs.repartition.is_(None)
            ))
    def operation(self):
        return lazy_gettext("equal")

    
class GroupINPNFilter(DynamicOptionsMixin, FilterEqual):
    def apply(self, query, value, alias=None):
        return query. filter(Taxons.group2_inpn == value)

    def get_dynamic_options(self, view):
        if has_app_context():
            yield from [
                (group[0], group[0])
                for group in db.session.query(Taxons.group2_inpn).order_by(
                    Taxons.group2_inpn
                ).distinct()
            ]