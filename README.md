#  ontologie-cloud Offres Cloud Computing des grand fournisseurs

##  1. Domaine choisi

Cette ontologie modélise l'écosystème des offres de services Cloud des grand fournisseurs proposées par les grands fournisseurs tels que AWS, Azure et Google Cloud Platform (GCP).  
Le modèle capture :
- Les différents types de services cloud (IaaS, PaaS, SaaS)
- Les offres commerciales (gratuites, économiques, entreprise)
- Les modèles de tarification (Pay-as-you-go, abonnement)
- La disponibilité géographique

L’objectif est de modéliser ces services pour aider les entreprises à choisir des offres cloud optimales via une modélisation sémantique riche en inférences. 


## 🧭 2. Justification des namespaces utilisés
**xmlns**:
untitled-ontology3="http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#"
Le namespace principal utilise un URI standard pour les ontologies Semantic Web, avec :
- Un chemin hiérarchique incluant l'auteur (administrator)
- La date de création (2025/2)
- Un identifiant unique (untitled-ontology-3)

**rdf** : "http://www.w3.org/1999/02/22-rdf-syntax-ns#" -> Structure de base RDF
**rdfs**: "http://www.w3.org/2000/01/rdf-schema#" -> Définition des classes et relations
**owl**: "http://www.w3.org/2002/07/owl#" -> Ontologie formelle avec OWL
**xsd**: "http://www.w3.org/2001/XMLSchema#" -> Définition des types de données
**Dublin Core**: "http://purl.org/dc/elements/1.1/" -> Métadonnées (titre, créateur...)

##  3. Description des classes et propriétés

**Classes Principales**

**Fournisseur :** AWS, Azure, GCP

**Offre : Classe de base pour toutes les offres cloud**
Sous-classes :

- OffreGratuite (Free Tier avec limites)
- OffreEconomique (pour startups)
- OffreEntreprise (premium)
- OffreHauteDisponibilite (SLA 99.9%)

**Service : Types de services cloud**
Sous-classes :

- ServiceIaas (EC2, AzureVM)
- ServicePaas (AppEngine, AppService)
- ServiceSaas (Office365, Workspace)

**Tarification : Modèles de facturation**
Sous-classes :

- PayAsYouGo (facturation horaire)
- Abonnement (réservations)
- Gratuit (avec limitations)

**ZoneGeographique:** Afrique, Asia, Europe, AmériqueNord, AmériqueSud


## Propriétés

| Propriété          | Description                                  | Domaine     | Portée             | Inverse         |
|--------------------|----------------------------------------------|-------------|---------------------|------------------|
| `propose`          |                                               | Fournisseur | Offre              | `estProposePar`  |
| `estProposePar`    | Inverse de `propose`                          | Offre       | Fournisseur        | `propose`        |
| `estDeType`        | Associe une offre à un type de service        | Offre       | Service            | -                |
| `aTarification`    | Modèle de paiement d'une offre                | Offre       | Tarification       | -                |
| `disponibleDans`   | Zones géographiques disponibles               | Offre       | ZoneGeographique   | -                |


##  5. Requêtes SPARQL

**Requête N°1: Offres gratuites avec leurs zones géographiques**
PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
SELECT ?offreGratuite ?zone
WHERE {
  ?offreGratuite a ont:OffreGratuite .
  ?offreGratuite ont:disponibleDans ?zone .
}

**Requête N°2: Services disponibles en Asie avec leurs offres**
PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
SELECT ?service ?offre ?fournisseur
WHERE {
  ?offre ont:estDeType ?service .
  ?offre ont:disponibleDans ont:Asia .
  ?offre ont:estProposePar ?fournisseur .
}

**Requête N°3: Offres de type IaaS avec leurs tarifications**
PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
SELECT ?offre ?service ?tarification
WHERE {
  ?offre ont:estDeType ?service .
  ?service a ont:ServiceIaas .
  ?offre ont:aTarification ?tarification .
}

**Requête N°4: Offres à haute disponibilité avec leurs zones géographiques**
PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
SELECT ?offre ?zone
WHERE {
  ?offre a ont:OffreHauteDisponibilite .
  ?offre ont:disponibleDans ?zone .
}

**Requête N°5: Services IaaS proposés par AWS**
PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
SELECT DISTINCT ?service
WHERE {
  ?offre ont:estDeType ?service .
  ?offre ont:estProposePar ont:AWS .
  ?service a ont:ServiceIaas .
}

**Requête N°6: Toutes les offres gratuites avec leurs fournisseurs**
PREFIX ont: <http://www.semanticweb.org/administrator/ontologies/2025/2/untitled-ontology-3#>
SELECT ?offre ?fournisseur
WHERE {
  ?offre a ont:OffreGratuite .
  ?offre ont:estProposePar ?fournisseur .
}









