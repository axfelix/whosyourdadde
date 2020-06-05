import requests
import sys
from google import google
from wikidata.client import Client
client = Client()

def whosyourdad(person):
    search_results = google.search(person, 1)
    for result in search_results:
        if "wikipedia.org" in result.link:
            wikiname = result.name.split(" - ")[0]
            wikiname = wikiname.replace(" ", "_")

            sparql_query = """
                    prefix schema: <http://schema.org/>
                    SELECT ?item ?father
                    WHERE {
                        <https://en.wikipedia.org/wiki/""" + wikiname + """> schema:about ?item .
                        ?item wdt:P22 ?father .
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
                    }
                """

            r = requests.get('https://query.wikidata.org/sparql', params={'format': 'json', 'query': sparql_query})

            try:
                father = r.json()['results']['bindings'][0]['father']['value'].split('/')[-1]
                entity = client.get(father, load=True)
                dadname = entity.data['labels']['en']['value']
                dadlink = entity.data['sitelinks']['enwiki']['url']
                # Might need to disambiguate here
                s = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=" + dadname)
                firstkey = next(iter(s.json()['query']['pages']))
                sins_of_father = s.json()['query']['pages'][firstkey]['extract']
                return("\nTheir daddy is " + dadname + "\n\n" + dadlink + "\n\n" + sins_of_father + "\n")
            except:
                return("Their dad wasn't famous. Good for them.")

    return("Their dad wasn't famous. Good for them.")

if __name__ == "__main__":
    dad = whosyourdad(sys.argv[1])
    print(dad)