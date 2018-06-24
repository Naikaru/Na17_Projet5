import psycopg2

conn_string = "host='tuxa.sme.utc' dbname='dbusername' user='username' password='mdp'"

print ("Connecting to database\n	->%s" % (conn_string))
 
# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()
print ("Connected!\n")

cursor.execute('select * from Trace')

ligne = cursor.fetchone()
print("NParc\tExp\tmeteo\tdRecolte\tfinFerm\t\t\tdebFerm\t\t\tNFerm\tFut\tNBout")
while ligne :
	chaine =""
	for i in range(9):
		chaine = chaine+ str(ligne[i])+"\t"
	print (chaine)
	ligne = cursor.fetchone()


# Requête pour récupérer tous les incidents survenues sur l'élaboration d'une bouteille

#def incidentsBouteilles():
	#cursor.execute('SELECT B.noSerie AS bouteille, I.*, E.idEtape AS etape FROM Bouteille B, Fut F,  
