# SemPryv Quick Guide

Guide d'utilisation rapide de SemPryv.

## Annotation

L'instance hébergée à la HEVs est accessible sur:

- https://sempryv.ehealth.hevs.ch.

On peut s'authentifier de 2 manières:

1. En choisissant le serveur (pryv.me, pryv.li ou entrer un autre manuellement)
   puis clicker sur «SIGN IN @ …». D'une fois authentifié à travers le popup
   Pryv, il suffit simplement de cliquer sur «CONNECT WITH PRYV».

2. En entrant manuellement les 3 données identifiantes: serveur, utilisateur et
   token. Puis cliquer sur «Connecter».

D'une fois connecté, on peut voir les infos d'authentification et se déconnecter
dans le menu de droite, qui peut être affiché et masqué en cliquant sur le nom
d'utilisateur en haut à droite.

Le menu de gauche, accessible en cliquant sur les 3 barres, affiche
l'arborescence des streams liée au token. En cliquant sur un stream on peut voir
et modifier ses annotations ainsi que les évènements qu'il contient.

Pour ajouter une annotation, il faut sélectionner (ou entrer manuellement) dans
le champ «Type» pour quel type d'évènement Pryv on veut ajouter une annotation,
puis cliquer sur le bouton «Ajouter» — il y a un bug pour l'instant, après avoir
entré le type il faut cliquer ailleurs sur la page pour que le bouton «Ajouter»
deviennent cliquable —, ensuite cela ouvre une popup pour chercher et ajouter
des annotation sémantiques.

Pour supprimer un annotation il suffit de cliquer sur la corbeille rouge à côté
de celle-ci. La case à cocher «Apply to children streams» permet d'activer ou
non l'application des annotations récursivement à tous les évènements des
streams enfants.

En cliquant sur un évènement on peut voir les annotations sémantiques qui lui
sont associées, depuis quel stream chaque annotation est héritée, et en cliquant
sur les annotations d'accéder directement au stream concerné.

## Export FHIR

L'API est accessible sur:

    https://backend.sempryv.ehealth.hevs.ch.

L'export sur `/events` offre une API similaire à [celle de Pryv][get-events],
c'est à dire qu'il est possible d'utiliser les mêmes paramètres que l'on ferait
sur une instance de Pryv.

[get-events]: http://api.pryv.com/reference/#get-events

Pour faire un export FHIR, il faut effectuer une requête `GET` de la forme
suivante:

    https://backend.sempryv.ehealth.hevs.ch/<username>.<server>/events?<params>

Par exemple:

    https://backend.sempryv.ehealth.hevs.ch/fabiendubosson.pryv.me/events?auth=TOKEN

De manière générale on peut voir cela comme ajouter
`https://backend.sempryv.ehealth.hevs.ch/` en préfixe d'une requête Pryv
traditionnelle:

    https://fabiendubosson.pryv.me/events?streams=[diary]&limit=1

devient

    https://backend.sempryv.ehealth.hevs.ch/fabiendubosson.pryv.me/events?streams=[diary]&limit=1

Note: il est aussi possible d'utiliser le header HTTP «Authorization» pour le
token.

## Import FHIR

L'importation d'évènements se fait sur avec un `POST` sur une adresse de la
forme:

    https://backend.sempryv.ehealth.hevs.ch/<username>.<server>/events/<stream_id>

Le body de la requête doit être le JSON du contenu FHIR.

Il n'est possible d'importer des évènements que dans un stream à la fois. Pour
importer des évènements dans plusieurs streams il faut séparer cela en plusieurs
requêtes sur chaque stream individuellement. L'importation FHIR n'accepte que le
même format que celui qui est exporté, qui ressemble à ceci:

    {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": [
        {
            "resourceType": "Observation",
            "status": "final",
            "effectiveDateTime": "…",
            "issued": "…",
            "identifier": {
                "system": "https://pryv.com",
                "use": "official",
                "value": "…"
            },
            "code": {
                "coding": [
                    {
                        "code": "…",
                        "display": "…",
                        "system": "…"
                    },
                    …
                ]
            },
            "valueString": "…"  # Or ValueObject, ValueQuantity, …
        },
        …]
    }

Les codes sémantiques sont repris tels quels et sont ajoutés au niveau du
stream, dès lors plusieurs points sont à savoir:

- Dans une requête d'importation FHIR, tous les évènements d'un même type
  doivent avoir les mêmes annotations sémantiques.

- En important dans un stream existant possédant déjà des annotations, les types
  importés doivent avoir des annotations sémantiques correspondantes à celle
  déjà sur le stream.
