import psycopg2

#il faut renseigner l'adresse, le login, le mot de passe et le nom de la base.
conn_string = "host='tuxa.sme.utc' dbname='dbusername' user='username' password='mdp'"

# Connection à la base, on passera l'objet conn aux différentes fonctions.
conn = psycopg2.connect(conn_string)


print ("Connected!\n")

#affiche les incidents touchant la bouteille passée en paramètre.
def incidentsBouteilles(numBouteille,connection):
	cursor = connection.cursor()
	cursor.execute('SELECT B.noSerie AS bouteille, E.idEtape AS etape, I.idIncident, I.description, I.dateIncident FROM Bouteille B, Vieillissement V, Fut F, Fermentation Fe, AssociationMoutFerm A, Mout M, Cuve C, Parcelle P, Incident I, EtapeFabrication E WHERE B.noSerie = %d AND I.etape = E.idEtape AND B.vin = V.noVieillissement AND V.fut = F.noFut AND V.fermentation = Fe.noFermentation AND Fe.cuve = C.noCuve AND A.fermentation = Fe.noFermentation AND A.mout = M.noMout AND M.parcelle = P.noParcelle AND (B.noSerie = E.idEtape OR V.noVieillissement = E.idEtape OR F.noFut = E.idEtape OR Fe.noFermentation = E.idEtape OR C.noCuve = E.idEtape OR M.noMout = E.idEtape OR P.noParcelle = E.idEtape) GROUP BY B.noSerie, E.idEtape, I.idIncident, I.description, I.dateIncident ORDER BY B.noSerie, E.idEtape, I.idIncident, I.description, I.dateIncident;'%(numBouteille))


	ligne = cursor.fetchone()
	titre=["Bouteille numéro : ","Etape de l'incident : ","Incident numéro : ","Description de l'incident: ","Date de l'incident: "]
	while ligne :
		chaine =""
		for i in range(5):
				chaine = chaine+titre[i]+str(ligne[i])+"\n"
		print (chaine)
		ligne = cursor.fetchone()


# Pour chaque Cuve, on montre les fermentation qui s'y sont déroulées et les mesures qui y ont été faites 

def informationsCuve(connection):
	cursor = connection.cursor()
	cursor.execute('SELECT C.noCuve, C.capacite, F.noFermentation, F.debutFermentation, F.finFermentation, F.chaptalisation, F.doseLevure, F.typeLevure, M.dateMesure, M.temperature, M.masseVol FROM Cuve C JOIN Fermentation F ON C.noCuve = F.cuve JOIN Mesure M ON M.fermentation = F.noFermentation GROUP BY C.noCuve, C.capacite, F.noFermentation, F.debutFermentation, F.finFermentation, F.chaptalisation, F.doseLevure, F.typeLevure, M.dateMesure, M.temperature, M.masseVol ORDER BY C.noCuve, C.capacite, F.noFermentation, F.debutFermentation, F.finFermentation, F.chaptalisation, F.doseLevure, F.typeLevure, M.dateMesure, M.temperature, M.masseVol;')

	ligne = cursor.fetchone()
	titre = ["Cuve numéro : ","Capacité (L) : ","noFermentation : ","debutFermentation : ","finFermentation : ","chaptalisation :","Quantité de Levure : ", "Type de levures : ", "Date de la mesure : ", "Temperature : ", "Masse volumique : "]
	while ligne :
		chaine =""
		for i in range(11):
			chaine = chaine+titre[i]+str(ligne[i])+"\n"
		print (chaine)
		ligne = cursor.fetchone()


# Pour chaque fermentation on montre les différentes mesures, ajout de Diammonium ou les remontages qui ont pu être effectués 

def informationsFermentation(connection):
	cursor = connection.cursor()
	cursor.execute('SELECT F.noFermentation AS fermentation, F.debutFermentation AS debutF, F.finFermentation AS finF, M.dateMesure, M.temperature, M.masseVol, R.dateRemontage, D.dateAjout AS ajoutDiammonium, D.quantite FROM Fermentation F JOIN Mesure M ON M.fermentation = F.noFermentation JOIN Remontage R ON R.fermentation = F.noFermentation JOIN Diammonium D ON D.fermentation = F.noFermentation GROUP BY F.noFermentation, F.debutFermentation, F.finFermentation, M.dateMesure, M.temperature, M.masseVol, R.dateRemontage, D.dateAjout, D.quantite ORDER BY F.noFermentation, F.debutFermentation, F.finFermentation, M.dateMesure, M.temperature, M.masseVol, R.dateRemontage, D.dateAjout, D.quantite;')

	ligne = cursor.fetchone()
	titre = ["Fermentation : ","debutF : ","finF : ","Date Mesure : ","Temperature : ","Masse Volumique : ","Date Remontage : ","Ajout Diammonium : ","Quantite : "]
	while ligne :
		chaine =""
		for i in range(9):
			chaine = chaine+titre[i]+str(ligne[i])+"\n"
		print (chaine)
		ligne = cursor.fetchone()


# Permet de connaître pour chaque Fermentation le mélange de Moût présent, ainsi que de quelle parcelle proviennent les mouts.

def informationsMoutFermentation(connection):
	cursor = connection.cursor()
	cursor.execute('SELECT A.fermentation, A.mout, P.noParcelle FROM AssociationMoutFerm A JOIN Mout M ON M.noMout = A.mout JOIN Parcelle P ON P.noParcelle = M.parcelle GROUP BY A.fermentation, A.mout, P.noParcelle ORDER BY A.fermentation, A.mout, P.noParcelle;')
	
	ligne = cursor.fetchone()
	titre = ["Fermentation : ","Mout : ","Parcelle : "]
	while ligne :
		chaine =""
		for i in range(3):
			chaine = chaine+titre[i]+str(ligne[i])+"\n"
		print (chaine)
		ligne = cursor.fetchone()





#Permet de choisir une bouteille parmis celles enregistrées en base.
def choix_Bouteille(connection):
	choix =0
	cursor = connection.cursor()
	cursor.execute('select * from Bouteille')
	ligne = cursor.fetchone()
	listeBouteille=[]
	nbBouteille=0
	while ligne :
		nbBouteille+=1
		listeBouteille.append([ligne[0],str("%d. Numéro de série : %s\nContenance : %scl\n" %(nbBouteille,ligne[0],ligne[2]))])
		ligne = cursor.fetchone()
		affichageListe=""
		for j in range(nbBouteille):
			affichageListe += "\n"+listeBouteille[j][1]
	while (choix < 1 or choix > nbBouteille):
		choix = int(input("Veuillez choisir une bouteille :%s"%(affichageListe)))
	return listeBouteille[choix-1][0]

#Affiche la traçabilité de la bouteille passée en paramètre
def afficheTrace(numBouteille,connection):
	cursor = connection.cursor()
	cursor.execute('select * from Trace where noSerie = %d' %(numBouteille))
	ligne=cursor.fetchone()
	parcelleMout =""
	while ligne :
		parcelleMout+=str("\nParcelle numéro %s, exposée %s.\nVendangée le %s.\nMétéo de la récolte : %s\n"%(ligne[0],ligne[1],ligne[3],ligne[2]))
		infoFermentation=("Il a fermenté du %s au %s\n"%(ligne[5],ligne[4]))
		infoVieillissement=("Le vin a vieillis dans le fut %s\n"%(ligne[7]))
		ligne = cursor.fetchone()
	affichage =str("Le raisin provient de:%s\n%s%s"% (parcelleMout,infoFermentation, infoVieillissement))
	print(affichage)
	
#affiche un menu et retourne l'élément choisi.
def menu():
	choix = 0
	
	while(choix < 1 or choix > 6):
		choix = int(input("Que voulez vous faire ? \n\
		1. Visualiser la traçabilité complète d'une bouteille. \n\
		2. Voir tout les incidents impactant une bouteille \n\
		3. Afficher toutes les informations relatives aux cuves \n\
		4. Afficher toutes les informations relatives aux fermentations\n\
		5. Afficher le melange de mout present dans les fermentations\n\
		6. Quitter \n"))
		
		if(choix < 1 or choix > 6):
			print("Erreur dans le choix réalisé, veuillez ressayer.")
	
	return choix
	

if __name__ == '__main__':
	choix = 0
	while (choix!= 6):
		choix = menu()
		if (choix == 1):
			print("Traçabilité :\n")
			afficheTrace(choix_Bouteille(conn),conn)
		elif (choix == 2):
			print("Suivi des incidents : \n")
			incidentsBouteilles(choix_Bouteille(conn),conn)
		elif (choix == 3):
			print("Information sur les cuves : \n")
			informationsCuve(conn)
		elif (choix == 4):
			print("Information sur les fermentations : \n")
			informationsFermentation(conn)
		elif (choix == 5):
			print("Informations sur le melange des mout : \n")
			informationsMoutFermentation(conn)
