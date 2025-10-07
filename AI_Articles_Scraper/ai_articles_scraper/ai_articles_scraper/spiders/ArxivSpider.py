import scrapy
import requests
import xmltodict
import asyncio


class ArxivSpider(scrapy.Spider):
    name = "arxiv"
    custom_settings = {
        # "FEEDS": {"arxiv_results.csv": {"format": "csv", "overwrite": True}},
        "FEEDS": {"arxiv_results2.csv": {"format": "csv", "overwrite": True}},
        "ROBOTSTXT_OBEY": False,
        "CONCURRENT_REQUESTS": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 2.0,       # pause entre requêtes
        "RANDOMIZE_DOWNLOAD_DELAY": 0.5,  # légère variation aléatoire
    }

    # Liste des conférences
    conferences = [
    #     "AAAI", "IJCAI", "ICML", "ICLR", "NeurIPS",
    #     "ACL", "EMNLP", "NAACL",
    #     "KDD", "SIGIR", "WWW",
    #     "CVPR", "ICCV", "ECCV",
    #     "ICAPS", "AAMAS", "UAI",
    #     "AISTATS", "ECML-PKDD", "ECAI",

    "SACAIR",
    "PanAfriCon AI",
    "Deep Learning Indaba",
    "AICA",
    "AI Expo Africa",
    "AiFest Africa",
    "Africa AI Summit",
    "LAGOS",
    "AI Ignite Africa",
    "Africa AI Conference (AIC)",
    "AIBC Africa",
    "AfricAIED",
    "AI4Good Impact Africa Summit",
    "GRACO",
    "AI in Finance Summit",
    "AI for Health Summit",
    "Robotics: Science and Systems (RSS)",
    "ICRA Workshops",
    "IROS Workshops",
    "AI for Social Good",
    "AI Safety Workshop",
    "Cognitive Systems Workshop",
    "NeuroIPS Workshops",
    "Machine Learning for Healthcare",
    "AI for Earth",
    "AI for Climate",
    "AI in Education",
    "AI in Agriculture",
    "AI in Energy",
    "AI in Manufacturing",
    "AI in Transportation",
    "AI in Cybersecurity",
    "AI in Government",
    "AI in Law",
    "AI for Robotics",
    "AI for NLP Workshops",
    "AI in Vision",
    "AI in Audio",
    "AI in Speech",
    "AI in Games",
    "AI in Music",
    "AI in Art",
    "AI in Creativity",
    "AI for Social Media",
    "AI in Marketing",
    "AI in Retail",
    "AI in Healthcare Systems",
    "AI for Drug Discovery",
    "AI in Medical Imaging",
    "AI in Genomics",
    "AI in Proteomics",
    "AI in Neuroscience",
    "AI in Physics",
    "AI in Chemistry",
    "AI in Astronomy",
    "AI in Earth Sciences",
    "AI in Ecology",
    "AI in Climate Modeling",
    "AI in Disaster Response",
    "AI for Humanitarian Aid",
    "AI in Smart Cities",
    "AI in IoT",
    "AI in Edge Computing",
    "AI in Cloud Systems",
    "AI in Blockchain",
    "AI in Quantum Computing",
    "AI in Autonomous Systems",
    "AI in Drones",
    "AI in Self-Driving Cars",
    "AI in Industrial Automation",
    "AI in Supply Chain",
    "AI in Logistics",
    "AI in Customer Service",
    "AI in Chatbots",
    "AI in Virtual Assistants",
    "AI in Social Robotics",
    "AI in Ethics",
    "AI in Policy",
    "AI in Fairness",
    "AI in Bias Detection",
    "AI in Privacy",
    "AI in Explainability",
    "AI in Trustworthy AI",
    "AI in Safety",
    "AI in Verification",
    "AI in Robustness",
    "AI in Multi-Agent Systems",
    "AI in Swarm Robotics",
    "AI in Reinforcement Learning",
    "AI in Continual Learning",
    "AI in Transfer Learning",
    "AI in Meta-Learning",
    "AI in Federated Learning",
    "AI in Human-Robot Interaction",
    "AI in Cognitive Robotics",
    "AI in Knowledge Graphs",
    "AI in Semantic Web",
    "AI in Ontologies",
    "AI in Reasoning",
    "AI in Planning",
    "AI in Search",
    "AI in Optimization",
    "AI in Probabilistic Models",
    "AI in Bayesian Networks",
    "AI in Causal Inference",
    "AI in Statistical Learning",
    "AI in Graph Neural Networks",
    "AI in Social Network Analysis",
    "AI in Natural Language Understanding",
    "AI in Machine Translation",
    "AI in Question Answering",
    "AI in Dialogue Systems",
    "AI in Summarization",
    "AI in Information Retrieval",
    "AI in Recommender Systems",
    "AI in Computer Vision",
    "AI in Object Detection",
    "AI in Image Segmentation",
    "AI in Facial Recognition",
    "AI in Scene Understanding",
    "AI in Video Analysis",
    "AI in Action Recognition",
    "AI in Robotics Vision",
    "AI in Sensor Fusion",
    "AI in Motion Planning"
    ]

    max_results_per_query = 100          # nombre de résultats max par appel API arXiv
    total_limit_per_conf = None          # limite max globale (None = pas de limite)
    semantic_scholar_api_key = "" #Your API key from Semanticscholar

    def fetch_citations(self, arxiv_id):
        """
        Récupère le nombre de citations depuis Semantic Scholar en utilisant l'ID arXiv.
        Appel synchrone via requests (hors Scrapy).
        """
        if not arxiv_id:
            return 0

        # Supprime la version (ex: "1234.5678v1" -> "1234.5678")
        if "v" in arxiv_id:
            arxiv_id = arxiv_id.split("v")[0]

        url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=citationCount"
        headers = {"x-api-key": self.semantic_scholar_api_key} if self.semantic_scholar_api_key else {}

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("citationCount", 0)
            else:
                self.logger.warning(f"Semantic Scholar {resp.status_code} pour {arxiv_id}: {resp.text[:100]}")
                return 0
        except requests.RequestException as e:
            self.logger.error(f"Erreur requests citations {arxiv_id}: {e}")
            return 0
        except Exception as e:
            self.logger.error(f"Erreur citations {arxiv_id}: {e}")
            return 0

    async def start(self):
        """
        Méthode asynchrone pour Scrapy 2.13+.
        Lance les requêtes de recherche arXiv pour chaque conférence.
        """
        base_url = "https://export.arxiv.org/api/query?search_query=all:{query}&start={start}&max_results={max_results}"
        for conf in self.conferences:
            url = base_url.format(query=conf, start=0, max_results=self.max_results_per_query)
            self.logger.info(f"Requête arXiv pour {conf}: {url}")
            yield scrapy.Request(url, callback=self.parse, meta={"conference": conf, "start": 0})
            await asyncio.sleep(0.5)  # petite pause entre chaque conf

    def parse(self, response):
        """
        Parse la réponse XML d'arXiv, extrait les infos des articles,
        enrichit avec les citations depuis Semantic Scholar.
        """
        conference = response.meta.get("conference")
        start = response.meta.get("start", 0)

        try:
            data = xmltodict.parse(response.text)
        except Exception as e:
            self.logger.error(f"Erreur XML {conference}: {e} - Réponse: {response.text[:200]}")
            return

        entries = data.get("feed", {}).get("entry", [])
        if not entries:
            self.logger.warning(f"Aucun papier pour {conference}")
            return

        # Si un seul papier → convertir en liste
        if isinstance(entries, dict):
            entries = [entries]

        self.logger.info(f"{conference}: {len(entries)} papiers (start: {start})")
        items_count = 0

        for entry in entries:
            title = entry.get("title", "").replace("\n", " ").strip()
            if not title:
                continue

            # Auteurs
            authors_list = entry.get("author", [])
            if isinstance(authors_list, dict):
                authors_list = [authors_list]
            authors = ", ".join([a.get("name", "") for a in authors_list if a.get("name")])

            # Résumé
            summary = entry.get("summary", "").replace("\n", " ").strip()

            # Lien arXiv + PDF
            link = entry.get("id")
            pdf_link = None
            for l in entry.get("link", []):
                if isinstance(l, dict) and l.get("@type") == "application/pdf":
                    pdf_link = l.get("@href")
                    break

            # Année de publication
            published = entry.get("published", {})
            year_text = published.get("#text", "") if isinstance(published, dict) else (published or "")
            year = year_text.split("-")[0] if year_text else None

            # ID arXiv
            arxiv_id = link.split("/")[-1] if link else None

            # Citations via Semantic Scholar
            citations = self.fetch_citations(arxiv_id)

            # Construction de l'item
            item = {
                "Source": "arXiv",
                "Conference": conference,
                "Title": title,
                "Summary": summary,
                "Authors": authors,
                "Year": year,
                "Published_in": "arXiv",
                "Link": link,
                "Citations": citations,
            }
            yield item
            items_count += 1

        self.logger.info(f"{conference}: {items_count} items yieldés (start: {start})")

        # Pagination
        next_start = start + self.max_results_per_query
        if len(entries) == self.max_results_per_query and (
                self.total_limit_per_conf is None or next_start < self.total_limit_per_conf):
            next_url = f"https://export.arxiv.org/api/query?search_query=all:{conference}&start={next_start}&max_results={self.max_results_per_query}"
            yield scrapy.Request(next_url, callback=self.parse, meta={"conference": conference, "start": next_start})
        else:
            self.logger.info(f"{conference}: Fin pagination (start: {start}, limit: {self.total_limit_per_conf})")
