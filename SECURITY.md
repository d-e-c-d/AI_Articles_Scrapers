# Politique de sécurité

## Signaler une vulnérabilité

Écrire à **dikoume.ecd@gmail.com** avec « SECURITY » en objet. Réponse
sous 7 jours. Merci de ne pas ouvrir d'issue publique pour un problème
exploitable.

## Périmètre

Ce dépôt est un client de collecte de données. Il n'expose aucun service,
n'ouvre aucun port et ne stocke aucune donnée personnelle : il lit des
API publiques et écrit des fichiers CSV en local.

## Secrets

La clé API Semantic Scholar est actuellement déclarée comme attribut de
classe dans `ArxivSpider` (`semantic_scholar_api_key`). Elle est **vide
dans le dépôt** et doit le rester.

Si une clé y a été écrite puis commitée, la retirer du fichier ne suffit
pas : elle demeure dans l'historique Git. Il faut la **révoquer** sur
[semanticscholar.org](https://www.semanticscholar.org/product/api) puis
en générer une nouvelle.

Correctif prévu : lire la clé depuis `os.environ["SEMANTIC_SCHOLAR_API_KEY"]`.

## Usage responsable

Les spiders sont configurés avec des délais délibérés
(`DOWNLOAD_DELAY`, `CONCURRENT_REQUESTS` bas). Ne pas les augmenter :
arXiv et Semantic Scholar sont des services publics à budget contraint,
et les conditions d'utilisation de leurs API s'appliquent.

`ROBOTSTXT_OBEY` est à `False` parce que le projet interroge des **API
documentées**, pas des pages web. Si de nouveaux spiders ciblent du HTML,
ce réglage doit repasser à `True`.
