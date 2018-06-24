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

# Pour chaque bouteille, on montre les incidents qui ont pu se dérouler lors de son élaboration ainsi que les etapes où ils sont survenus 

def incidentsBouteilles():
	cursor.execute('SELECT B.noSerie AS bouteille, E.idEtape AS etape, I.idIncident, I.description, I.dateIncident FROM Bouteille B, Vieillissement V, Fut F, Fermentation Fe, AssociationMoutFerm A, Mout M, Cuve C, Parcelle P, Incident I, EtapeFabrication E WHERE I.etape = E.idEtape AND B.vin = V.noVieillissement AND V.fut = F.noFut AND V.fermentation = Fe.noFermentation AND Fe.cuve = C.noCuve AND A.fermentation = Fe.noFermentation AND A.mout = M.noMout AND M.parcelle = P.noParcelle AND (B.noSerie = E.idEtape OR V.noVieillissement = E.idEtape OR F.noFut = E.idEtape OR Fe.noFermentation = E.idEtape OR C.noCuve = E.idEtape OR M.noMout = E.idEtape OR P.noParcelle = E.idEtape) GROUP BY B.noSerie, E.idEtape, I.idIncident, I.description, I.dateIncident ORDER BY B.noSerie, E.idEtape, I.idIncident, I.description, I.dateIncident;')

	ligne = cursor.fetchone()
	print("Bouteille\tEtape\tIncident\tDescription\tDate")
	while ligne :
        	chaine =""
        	for i in range(9):
                	chaine = chaine+ str(ligne[i])+"\t"
        	print (chaine)
        	ligne = cursor.fetchone()


# Pour chaque Cuve, on montre les fermentation qui s'y sont déroulées et les mesures qui y ont été faites 

def informationsCuve():
	cursos.execute('SELECT C.noCuve, C.capacite, F.noFermentation, F.debutFermentation, F.finFermentation, F.chaptalisation, F.doseLevure, F.typeLevure, M.dateMesure, M.temperature, M.masseVol FROM Cuve C JOIN Fermentation F ON C.noCuve = F.cuve JOIN Mesure M ON M.fermentation = F.noFermentation GROUP BY C.noCuve, C.capacite, F.noFermentation, F.debutFermentation, F.finFermentation, F.chaptalisation, F.doseLevure, F.typeLevure, M.dateMesure, M.temperature, M.masseVol ORDER BY C.noCuve, C.capacite, F.noFermentation, F.debutFermentation, F.finFermentation, F.chaptalisation, F.doseLevure, F.typeLevure, M.dateMesure, M.temperature, M.masseVol;')

        ligne = cursor.fetchone()
        print("Bouteille\tEtape\tIncident\tDescription\tDate")
        while ligne :
                chaine =""
                for i in range(9):
                        chaine = chaine+ str(ligne[i])+"\t"
                print (chaine)
                ligne = cursor.fetchone()

# Pour chaque fermentation on montre les différentes mesures, ajout de Diammonium ou les remontages qui ont pu être effectués 

def informationsFermentation():
	cursos.exectute('SELECT F.noFermentation AS fermentation, F.debutFermentation AS debutF, F.finFermentation AS finF, M.dateMesure, M.temperature, M.masseVol, R.dateRemontage, D.dateAjout AS ajoutDiammonium, D.quantite FROM Fermentation F JOIN Mesure M ON M.fermentation = F.noFermentation JOIN Remontage R ON R.fermentation = F.noFermentation JOIN Diammonium D ON D.fermentation = F.noFermentation GROUP BY F.noFermentation, F.debutFermentation, F.finFermentation, M.dateMesure, M.temperature, M.masseVol, R.dateRemontage, D.dateAjout, D.quantite ORDER BY F.noFermentation, F.debutFermentation, F.finFermentation, M.dateMesure, M.temperature, M.masseVol, R.dateRemontage, D.dateAjout, D.quantite;')

	ligne = cursor.fetchone()
        print("Fermentation\tdebutF\tfinF\tDate Mesure\tTemperature\tMasse Volumique\tDate Remontage\tAjout Diammonium\tQuantite")
        while ligne :
                chaine =""
                for i in range(9):
                        chaine = chaine+ str(ligne[i])+"\t"
                print (chaine)
                ligne = cursor.fetchone()

