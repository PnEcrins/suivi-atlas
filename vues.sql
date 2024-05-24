create view suivi_photo as (
WITH inter AS (SELECT COUNT(*) as nb_obs, cd_ref FROM atlas.vm_observations o 
    GROUP BY cd_ref 
    ORDER BY nb_obs DESC) 
    SELECT T.cd_ref, T.nom_complet, T.nom_vern, count(DISTINCT M.id_media) as nb_photos, I.nb_obs, T.patrimonial 
    from atlas.vm_taxons T 
    JOIN inter I ON I.cd_ref = T.cd_ref 
    LEFT JOIN atlas.vm_medias M ON M.cd_ref = T.cd_ref AND m.id_type IN (1,2) 
    GROUP BY T.cd_ref, T.nom_complet, T.nom_vern, I.nb_obs, T.patrimonial 
    ORDER by NB_OBS DESC
)



create view atlas.suivi_attributs as (
WITH inter AS (SELECT COUNT(*) as nb_obs, cd_ref FROM atlas.vm_observations o 
    GROUP BY cd_ref 
    ORDER BY nb_obs DESC), 
    tx_desc AS ( 
    SELECT valeur_attribut AS description, cd_ref 
    FROM atlas.vm_cor_taxon_attribut 
    WHERE id_attribut = 100 
    ), 
    tx_commentaire AS ( 
        SELECT valeur_attribut AS commentaire, cd_ref 
    FROM atlas.vm_cor_taxon_attribut 
    WHERE id_attribut = 101 
    ), 
    tx_milieu AS ( 
    SELECT valeur_attribut AS milieu, cd_ref 
    FROM atlas.vm_cor_taxon_attribut 
    WHERE id_attribut = 102 
    ), 
    tx_repartition AS ( 
    SELECT valeur_attribut AS repartition, cd_ref 
    FROM atlas.vm_cor_taxon_attribut 
    WHERE id_attribut = 103 
    ) 
    SELECT T.cd_ref, T.nom_complet, T.nom_vern, T.patrimonial, descri.description, com.commentaire, mil.milieu, rep.repartition, I.nb_obs 
    from atlas.vm_taxons T 
    JOIN inter I ON I.cd_ref = T.cd_ref 
    LEFT JOIN tx_desc descri ON descri.cd_ref = T.cd_ref 
    LEFT JOIN tx_milieu mil ON mil.cd_ref = T.cd_ref 
    LEFT JOIN tx_commentaire com ON com.cd_ref = T.cd_ref 
    LEFT JOIN tx_repartition rep ON rep.cd_ref=T.cd_ref 
    GROUP BY T.cd_ref, T.nom_complet, T.nom_vern, I.nb_obs, T.patrimonial, descri.description, com.commentaire, mil.milieu, rep.repartition 
    ORDER by NB_OBS desc

)

    
    
    