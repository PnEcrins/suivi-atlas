from app.env import db


from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property


class Taxons(db.Model):
    __tablename__ = "vm_taxons"
    __table_args__ = {"schema": "atlas"}
    cd_ref = db.Column(db.Integer, primary_key=True)
    id_rang = db.Column(db.Unicode)
    regne = db.Column(db.Unicode)
    phylum = db.Column(db.Unicode)
    classe = db.Column(db.Unicode)
    regne = db.Column(db.Unicode)
    ordre = db.Column(db.Unicode)
    famille = db.Column(db.Unicode)
    lb_nom = db.Column(db.Unicode)
    lb_auteur = db.Column(db.Unicode)
    nom_complet = db.Column(db.Unicode)
    nom_complet_html = db.Column(db.Unicode)
    nom_vern = db.Column(db.Unicode)
    nom_valide = db.Column(db.Unicode)
    nom_vern_eng = db.Column(db.Unicode)
    group1_inpn = db.Column(db.Unicode)
    group2_inpn = db.Column(db.Unicode)
    patrimonial = db.Column(db.Unicode)



class SuiviPhoto(db.Model):
    __tablename__ = "suivi_photo"
    __table_args__ = {"schema": "atlas"}
    cd_ref = db.Column(
        db.Integer,  
        ForeignKey("atlas.vm_taxons.cd_ref"), 
        primary_key=True
    )
    nom_complet = db.Column(db.Unicode)
    nom_vern = db.Column(db.Unicode)
    nb_photos = db.Column(db.Integer)
    nb_obs = db.Column(db.Unicode)
    patrimonial = db.Column(db.Unicode)
    taxons = db.relationship("Taxons")


class SuiviAtributs(db.Model):
    __tablename__ = "suivi_attributs"
    __table_args__ = {"schema": "atlas"}
    cd_ref = db.Column(
        db.Integer,
        ForeignKey("atlas.vm_taxons.cd_ref"),
        primary_key=True
    )
    nom_complet = db.Column(db.Unicode)
    nom_vern = db.Column(db.Unicode)
    nb_obs = db.Column(db.Unicode)
    patrimonial = db.Column(db.Unicode)
    description = db.Column(db.Unicode)
    commentaire = db.Column(db.Unicode)
    milieu = db.Column(db.Unicode)
    repartition = db.Column(db.Unicode)

    taxons = db.relationship("Taxons")


class VmMedias(db.Model):
    __tablename__ = "vm_medias"
    __table_args__ = {"schema": "atlas"}
    id_media = db.Column(db.Integer, primary_key=True)
    cd_ref = db.Column(
        db.Integer,
        ForeignKey("atlas.vm_taxons.cd_ref"),
    )