#pip install neo4j-driver

from neo4j.v1 import GraphDatabase, basic_auth 
from config import bolt_url,auth_id,auth_pass 

driver = GraphDatabase.driver(bolt_url, auth=basic_auth(auth_id, auth_pass)) 
session = driver.session() 



#retourner toute la traçabilité d'une bouteille :
def tracabilite_bouteile(bouteille, limit=20):
	query = 'match (n)-[*1..20]-(m) where n.name="'+str(bouteille)+'" return m LIMIT ' + str(limit)
	return session.run(query) 


#retourner toutes les bouteilles produites à partir d'une parcelle :
def from_parcelle_to_bouteille(parcelle, limit=20):
	query = 'match (n)-[*1..20]-(m:Bouteille) where n.name="' + str(parcelle) + '" return m LIMIT ' + str(limit)
	return session.run(query)


def choix_requete():
	choix = int(input("Veuillez choisir "))
	
	while(choix < 1 or choix > 5):
		choix = int(input("Veuillez choisir la requête que vous souhaitez lancer : \n\
					1 : retourner toute la traçabilité de la bouteille 1 \n\
					2 : retourner toute la traçabilité de la  bouteille 2 \n\
					3 : retourner toutes les bouteilles produites à partir de la parcelle 1 \n\
					4 : retourner toutes les bouteilles produites à partir de la parcelle 2 \n\
					5 : Quitter \n\
				"))
		
		if(choix < 1 or choix > 5):
			print("Erreur dans le choix réalisé, veuillez ressayer.")
		
	if choix == 1:
		result_some_data = tracabilite_bouteile('bouteille1')
	elif choix==2: 
		result_some_data = tracabilite_bouteile('bouteille2')
	elif choix==3: 
		result_some_data = from_parcelle_to_bouteille('parcelle1')
	elif choix==4: 
		result_some_data = from_parcelle_to_bouteille('parcelle2')
	elif choix==5:
		return

	"""
	gen = result_some_data.records() 

	for record in gen :  
		n = record['n'] 
		m = record['m'] 
		r = record['r'] 
		print() 
		print(n) 
		print(m) 
		print(r)
	"""
	return


"""
WITH [68757,72389,68757,72390,68757,79758,68758,79759] as nodes 
MATCH (n)-[r]->(m) 
WHERE id(n) in nodes 
AND id(m) in modes 
RETURN n,r,m LIMIT 
"""