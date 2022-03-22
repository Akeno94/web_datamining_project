# link to each online file to import data
# dict of columns in the online file associated with our columns name

museum_link = 'https://www.data.gouv.fr/fr/datasets/r/1796dfc3-fa33-4539-a14b-199eaa7a7b4a'
museum_columns = {
    "Identifiant Muséofile": "id",
    "Région administrative": "region",
    "Commune": "city",
    "Nom officiel du musée": "name",
    "Adresse": "address",
    "Code Postal": "postal_code",
    "URL": "url",
    "Latitude": "latitude",
    "Longitude": "longitude"
}
train_station_link = "https://ressources.data.sncf.com/explore/dataset/referentiel-gares-voyageurs/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
train_station_columns = {
    "Code UIC": "id",
    "Intitulé gare": "name",
    "Code postal": "postal_code",
    "Commune": "city",
    "Département": "department",
    "Longitude": "longitude",
    "Latitude": "latitude",
    "Région SNCF": "region"
}
bike_station_link = 'https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B'
bike_station_columns = {
    "Identifiant station": "id",
    "Nom station": "name",
    "Capacité de la station": "station_capacity",
    "Nombre bornettes libres": "free_block",
    "Nombre total vélos disponibles": "available_bike",
    "Vélos mécaniques disponibles": "mechanical_bike",
    "Vélos électriques disponibles": "electric_bike",
    "Retour vélib possible": "return_bike",
    "Coordonnées géographiques": "coordinates",
    "Nom communes équipées": "city"
}
ontology = "http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#"
