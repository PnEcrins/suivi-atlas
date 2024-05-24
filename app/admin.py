
from flask import redirect, url_for, render_template
from markupsafe import Markup
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.babel import lazy_gettext
from sqlalchemy import distinct
from sqlalchemy import or_, and_



from app.env import db
from app.models import SuiviPhoto, Taxons, SuiviAtributs, VmMedias
from app.filters import PatrionialFilter, GroupINPNFilter, HasPhotoFilter, IsCompleteFilter

class SuiviAtlasView(AdminIndexView):
    def is_visible(self):
        # This view won't appear in the menu structure
        return False

    @expose("/")
    def index(self):
        return redirect(url_for("analytics.index"))


admin = Admin(
    name="Suivi atlas", template_mode="bootstrap4", base_template="layout.html",
    index_view=SuiviAtlasView(url='/'),
)



def nb_photo_formater(view, context, model, name):
    nb_photos = model.nb_photos
    has_photo = "has-photo" if nb_photos > 0 else "no-photo"
    return Markup('<span class={}>{}</span>'.format(has_photo, nb_photos))

def attr_formatter(view, context, model, name):
    attr = getattr(model, name)
    has_attr = "has-attr" if attr else "no-attr"
    if not attr:
        attr = "-"
    else:
        attr = attr[0:50]+"..."
    return Markup('<span class={}>{}</span>'.format(has_attr, attr))


class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        nb_taxons = db.session.query(Taxons).count()
        nb_taxons_patrimonial = db.session.query(Taxons).filter(Taxons.patrimonial == "oui").count()
        nb_taxons_photo = db.session.query(distinct(VmMedias.cd_ref)).count()
        nb_taxons_description = db.session.query(SuiviAtributs).filter(SuiviAtributs.description.is_not(None)).count()
        nb_taxons_complet = db.session.query(SuiviAtributs).join(SuiviPhoto, SuiviPhoto.cd_ref == SuiviAtributs.cd_ref).filter(and_(
            SuiviAtributs.commentaire.is_not(None),
            SuiviAtributs.description.is_not(None),
            SuiviAtributs.milieu.is_not(None),
            SuiviAtributs.repartition.is_not(None),
            SuiviPhoto.nb_photos > 0
        )).count()
        patri_without_photo = db.session.query(SuiviPhoto).filter(SuiviPhoto.patrimonial == "oui").filter(SuiviPhoto.nb_photos == 0).count()
        patri_without_description = db.session.query(SuiviAtributs).filter(SuiviAtributs.patrimonial == "oui").filter(SuiviAtributs.description.is_(None)).count()
        return self.render(
            'analytics_index.html', 
            nb_taxons=nb_taxons, 
            nb_taxons_patrimonial=nb_taxons_patrimonial,
            nb_taxons_photo=nb_taxons_photo,
            nb_taxons_description=nb_taxons_description,
            nb_taxons_complet=nb_taxons_complet,
            patri_without_photo=patri_without_photo,
            patri_without_description=patri_without_description
        )



class MediasAdmin(ModelView):
    can_delete = False
    can_create = False
    can_edit = False
    column_sortable_list = ["nom_complet", "nom_vern", "nb_photos", "nb_obs", "patrimonial"]
    column_exclude_list = ["taxons"]
    column_list = ["nom_complet", "nom_vern", "nb_photos", "nb_obs", "patrimonial"]
    column_formatters = {
        "nb_photos": nb_photo_formater
    }
    column_searchable_list = ["nom_complet", "nom_vern"]

    column_filters = [
        PatrionialFilter(column=SuiviPhoto.patrimonial, name="Patrimonial", options=[(1, "Oui"), (0, "Non")]),
        HasPhotoFilter(column="nb_photos", name="A des photos", options=[(1, "Oui"), (0, "Non")]),
        GroupINPNFilter(column=Taxons.group2_inpn, name="Groupe INPN"),
    ]

class AttrAdmin(ModelView):
    can_delete = False
    can_create = False
    can_edit = False
    column_sortable_list = ["nom_complet", "nom_vern", "nb_obs", "patrimonial"]
    column_exclude_list = ["taxons"]
    column_list = ["nom_complet", "nom_vern", "nb_obs", "patrimonial", "description", "commentaire", "milieu", "repartition"]
    column_formatters = {
        "description": attr_formatter,
        "milieu": attr_formatter,
        "commentaire": attr_formatter,
        "repartition": attr_formatter,
    }
    column_searchable_list = ["nom_complet", "nom_vern"]

    column_filters = [
        PatrionialFilter(column=SuiviAtributs.patrimonial, name="Patrimonial", options=[(1, "Oui"), (0, "Non")]),
        GroupINPNFilter(column=Taxons.group2_inpn, name="Groupe INPN"),
        IsCompleteFilter(name="Est incomplet"),
    ]


admin.add_view(AnalyticsView(name=lazy_gettext('Home'), endpoint='analytics'))

admin.add_view(
    MediasAdmin(SuiviPhoto, db.session, name='Photo', endpoint='photos', url='/photos')
)

admin.add_view(
    AttrAdmin(SuiviAtributs, db.session, name='Atributs', endpoint='attributs', url='/attributs')
)

