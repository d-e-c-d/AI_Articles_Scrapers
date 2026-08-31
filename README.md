<div align="center">

# AI Articles Scrapers

**Cartographier la recherche africaine en IA, une conférence à la fois.**

[![python](https://img.shields.io/badge/python-3.12-3572A5)](https://www.python.org/)
[![scrapy](https://img.shields.io/badge/scrapy-2.13%2B-60A839)](https://scrapy.org/)
[![sources](https://img.shields.io/badge/sources-arXiv%20%2B%20Semantic%20Scholar-14213D)](#les-deux-spiders)
[![licence](https://img.shields.io/badge/licence-MIT-5B6472)](LICENSE)

</div>

---

Deux spiders Scrapy qui interrogent **arXiv** et **Semantic Scholar** pour
une liste de conférences, et produisent un CSV unifié : titre, résumé,
auteurs, année, lien, et **nombre de citations**.

La liste de conférences interrogée n'est pas celle des grandes
conférences généralistes — celles-là sont présentes mais commentées dans
le code. Ce qui est actif, c'est une liste centrée sur l'**écosystème IA
africain** (SACAIR, Deep Learning Indaba, PanAfriCon AI, AfricAIED,
AI Expo Africa…) élargie à une centaine de domaines applicatifs.

## Les deux spiders

| Spider | Source | Ce qu'il fait |
|---|---|---|
| `arxiv` | API arXiv (Atom/XML) | Une requête `search_query=all:<conférence>` par conférence, paginée par 100. Chaque article est ensuite enrichi d'un appel Semantic Scholar pour récupérer son `citationCount`. |
| `semantic_scholar` | API Graph Semantic Scholar | Interroge directement le corpus Semantic Scholar pour les mêmes conférences. |

Les deux écrivent leur propre CSV via le mécanisme `FEEDS` de Scrapy,
déclaré dans les `custom_settings` de chaque spider.

### Champs produits

`Source` · `Conference` · `Title` · `Summary` · `Authors` · `Year` ·
`Published_in` · `Link` · `Citations`

## Politesse réseau

Les deux spiders sont volontairement lents : les API publiques d'arXiv et
de Semantic Scholar renvoient des `429` sans ménagement, et un scraper
trop pressé se fait couper avant d'avoir fini.

| Réglage | `arxiv` | `semantic_scholar` |
|---|---|---|
| `CONCURRENT_REQUESTS` | 3 | 1 |
| `CONCURRENT_REQUESTS_PER_DOMAIN` | 1 | — |
| `DOWNLOAD_DELAY` | 2,0 s | 1,5 s |
| `RANDOMIZE_DOWNLOAD_DELAY` | 0,5 | — |

Compter plusieurs heures pour un passage complet sur toute la liste de
conférences. C'est normal, et c'est voulu.

## Ce que contient le dépôt

```
AI_Articles_Scraper/ai_articles_scraper/
  ai_articles_scraper/
    spiders/
      ArxivSpider.py            requêtes arXiv + enrichissement citations
      SemanticScholarSpider.py  requêtes Semantic Scholar
    items.py                    (gabarit Scrapy, non utilisé : les spiders
                                 yieldent des dicts directement)
    pipelines.py                pipeline d'items
    middlewares.py              middlewares spider et downloader
    settings.py                 réglages du projet
  scrapy.cfg                    point d'entrée Scrapy
```

## Démarrage

```bash
python3 -m venv venv && source venv/bin/activate
pip install scrapy requests xmltodict

cd AI_Articles_Scraper/ai_articles_scraper
scrapy crawl arxiv
scrapy crawl semantic_scholar
```

Les CSV (`arxiv_results2.csv`, `semantic_scholar_results2.csv`)
apparaissent dans le dossier courant.

### Clé API Semantic Scholar

L'API fonctionne sans clé, avec un quota bas. Pour un passage complet,
une clé est recommandée — elle se demande sur
[semanticscholar.org/product/api](https://www.semanticscholar.org/product/api).

Elle se renseigne actuellement dans l'attribut `semantic_scholar_api_key`
de `ArxivSpider`. **C'est un défaut connu** : une clé n'a pas sa place
dans un fichier versionné. Voir [`SECURITY.md`](SECURITY.md).

## Adapter la liste de conférences

Tout est dans l'attribut `conferences` de chaque spider. Les grandes
conférences généralistes (NeurIPS, ICML, ICLR, ACL, CVPR…) sont déjà
écrites, en commentaire, en haut de la liste : les décommenter suffit.

## Limites connues

- La clé API est un attribut de classe, pas une variable d'environnement.
- `items.py` est resté le gabarit vide généré par `scrapy startproject` :
  les spiders produisent des dictionnaires bruts, sans validation de schéma.
- L'arborescence comporte un niveau `ai_articles_scraper/` dupliqué,
  hérité de la génération initiale.
- La déduplication entre les deux sources n'est pas faite : un article
  présent sur arXiv **et** Semantic Scholar apparaît dans les deux CSV.

---

<div align="center">
<sub>Par <a href="https://github.com/d-e-c-d">Charles Darryl Dikoume</a></sub>
</div>
