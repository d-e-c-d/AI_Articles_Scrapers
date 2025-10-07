import scrapy
import json

class SemanticScholarSpider(scrapy.Spider):
    name = "semantic_scholar"
    custom_settings = {
        # "FEEDS": {"semantic_scholar_results.csv": {"format": "csv", "overwrite": True}},
        "FEEDS": {"semantic_scholar_results2.csv": {"format": "csv", "overwrite": True}},
        "ROBOTSTXT_OBEY": False,
        "CONCURRENT_REQUESTS": 1,  # limiter le nombre de requêtes simultanées pour éviter les erreurs 429
        "DOWNLOAD_DELAY": 1.5,     # délai entre les requêtes (en secondes)
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

    max_results_per_query = 100  # nombre maximum de résultats renvoyés par l'API par requête
    semantic_scholar_api_key = "" #Your API key from Semanticscholar

    def start_requests(self):
        headers = {"x-api-key": self.semantic_scholar_api_key}
        fields = "title,authors,year,venue,abstract,url,citationCount"  # champs à récupérer pour chaque papier

        # Boucle sur chaque conférence pour construire l'URL de recherche
        for conf in self.conferences:
            url = (
                f"https://api.semanticscholar.org/graph/v1/paper/search?"
                f"query={conf}&limit={self.max_results_per_query}&"
                f"fields={fields}"
            )
            # Lancer une requête Scrapy pour chaque conférence avec la fonction de callback parse_search
            yield scrapy.Request(url, callback=self.parse_search, headers=headers, meta={"conference": conf, "offset": 0})

    def parse_search(self, response):
        conference = response.meta.get("conference")  # récupérer le nom de la conférence depuis le meta
        offset = response.meta.get("offset", 0)       # récupérer l'offset pour la pagination

        data = json.loads(response.text)  # convertir la réponse JSON en dictionnaire Python
        papers = data.get("data", [])     # extraire la liste de papiers

        # Boucle sur chaque papier pour construire le dictionnaire de sortie
        for paper in papers:
            yield {
                "Source": "Semantic Scholar",
                "Conference": conference,
                "Title": paper.get("title"),
                "Summary": paper.get("abstract"),
                "Authors": ", ".join([a.get("name") for a in paper.get("authors", [])]),
                "Year": paper.get("year"),
                "Published_in": paper.get("venue"),
                "Link": paper.get("url"),
                "Citations": paper.get("citationCount", 0),
            }

        # Pagination
        if len(papers) == self.max_results_per_query:
            next_offset = offset + self.max_results_per_query  # calculer le prochain offset
            fields = "title,authors,year,venue,abstract,url,citationCount"  # champs à récupérer
            next_url = (
                f"https://api.semanticscholar.org/graph/v1/paper/search?"
                f"query={conference}&limit={self.max_results_per_query}&offset={next_offset}&"
                f"fields={fields}"
            )
            headers = {"x-api-key": self.semantic_scholar_api_key}  # ajouter la clé API pour la prochaine requête
            # Lancer la requête suivante pour récupérer les résultats suivants
            yield scrapy.Request(next_url, callback=self.parse_search, headers=headers, meta={"conference": conference, "offset": next_offset})
