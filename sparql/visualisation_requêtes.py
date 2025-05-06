from rdflib import Graph, Namespace, URIRef
import pandas as pd
import plotly.express as px

# %% 1. Charger l'ontologie
g = Graph()
g.parse("C:\\Users\\pc\\Downloads\\cloud.ttl", format="turtle")
print(f"✅ Ontologie chargée avec succès : {len(g)} triplets RDF.")

# %% 2. Définir le namespace
ont = Namespace("http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#")

# %% 3. Fonction pour exécuter et visualiser les requêtes avec graphes améliorés
def run_and_visualize_sparql(query, title):
    results = g.query(query)
    df = pd.DataFrame(results, columns=results.vars)

    def shorten_uri(value):
        if isinstance(value, URIRef):
            return value.split('#')[-1].split('/')[-1]
        return str(value)

    df = df.applymap(shorten_uri)

    print(f"\n📌 {title} ({len(df)} résultats)")
    print(df)

    if df.empty:
        print("⚠️ Aucun résultat.")
        return

    axis_labels = {
        "offreGratuite": "Offre Gratuite",
        "zone": "Zone Géographique",
        "service": "Service",
        "offre": "Offre",
        "fournisseur": "Fournisseur",
        "tarification": "Tarification",
    }

    df.columns = [axis_labels.get(str(col), str(col).capitalize()) for col in df.columns]

    if len(df.columns) == 2:
        fig = px.bar(
            df,
            x=df.columns[0],
            y=df.columns[1],
            title=title,
            text_auto=True,
            color=df.columns[0],  # Ajout d'une couleur par catégorie
        )
        fig.update_layout(
            xaxis_title=df.columns[0],
            yaxis_title=df.columns[1],
            title_font_size=20,
            bargap=0.3,
            xaxis_tickangle=-45  # Rotation pour lisibilité
        )
        fig.update_traces(marker_line_width=1.5)
        fig.show()

    elif len(df.columns) == 3:
        fig = px.scatter(
            df,
            x=df.columns[1],
            y=df.columns[2],
            color=df.columns[0],
            title=title,
            labels={col: col for col in df.columns},
            hover_name=df.columns[0],
            size=[10]*len(df),  # Taille fixe des points
        )
        fig.update_layout(
            title_font_size=20,
            xaxis_tickangle=-30
        )
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig.show()


# %% 4. Liste des requêtes SPARQL
queries = [
    {
        "title": "Requête N°1: Offres gratuites avec leurs zones géographiques",
        "query": """
        PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
        SELECT ?offreGratuite ?zone WHERE {
            ?offreGratuite a ont:OffreGratuite .
            ?offreGratuite ont:disponibleDans ?zone .
        }
        """
    },
    {
        "title": "Requête N°2: Services disponibles en Asie avec leurs offres",
        "query": """
        PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
        SELECT ?service ?offre ?fournisseur WHERE {
            ?offre ont:estDeType ?service .
            ?offre ont:disponibleDans ont:Asia .
            ?offre ont:estProposePar ?fournisseur .
        }
        """
    },
    {
        "title": "Requête N°3: Offres de type IaaS avec leurs tarifications",
        "query": """
        PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
        SELECT ?offre ?service ?tarification WHERE {
            ?offre ont:estDeType ?service .
            ?service a ont:ServiceIaas .
            ?offre ont:aTarification ?tarification .
        }
        """
    },
    {
        "title": "Requête N°4: Offres à haute disponibilité avec leurs zones géographiques",
        "query": """
        PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
        SELECT ?offre ?zone WHERE {
            ?offre a ont:OffreHauteDisponibilite .
            ?offre ont:disponibleDans ?zone .
        }
        """
    },
    {
        "title": "Requête N°5: Services IaaS proposés par AWS",
        "query": """
        PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
        SELECT DISTINCT ?service WHERE {
            ?offre ont:estDeType ?service .
            ?offre ont:estProposePar ont:AWS .
            ?service a ont:ServiceIaas .
        }
        """
    },
    {
        "title": "Requête N°6: Toutes les offres gratuites avec leurs fournisseurs",
        "query": """
        PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
        SELECT ?offre ?fournisseur WHERE {
            ?offre a ont:OffreGratuite .
            ?offre ont:estProposePar ?fournisseur .
        }
        """
    }
]

# %% 5. Exécution des requêtes
for q in queries:
    run_and_visualize_sparql(q["query"], q["title"])
