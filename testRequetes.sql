/* Pour chaque bouteille, on montre les incidents qui ont pu se dérouler lors de son élaboration ainsi que les etapes où ils sont survenus */

SELECT B.noSerie AS bouteille, E.idEtape AS etape, I.idIncident, I.description, I.dateIncident 
FROM 	Bouteille B, 
	Vieillissement V, 
	Fut F, 
	Fermentation Fe, 
	AssociationMoutFerm A, 
	Mout M, 
	Cuve C, 
	Parcelle P, 
	Incident I, 
	EtapeFabrication E 
WHERE I.etape = E.idEtape
AND B.vin = V.noVieillissement 
AND V.fut = F.noFut 
AND V.fermentation = Fe.noFermentation 
AND Fe.cuve = C.noCuve 
AND A.fermentation = Fe.noFermentation 
AND A.mout = M.noMout 
AND M.parcelle = P.noParcelle 
AND (	B.noSerie = E.idEtape
	OR V.noVieillissement = E.idEtape
	OR F.noFut = E.idEtape 
	OR Fe.noFermentation = E.idEtape
	OR C.noCuve = E.idEtape
	OR M.noMout = E.idEtape
	OR P.noParcelle = E.idEtape
)
GROUP BY B.noSerie, E.idEtape, I.idIncident, I.description, I.dateIncident
ORDER BY B.noSerie, E.idEtape, I.idIncident, I.description, I.dateIncident;



/* Pour chaque Cuve, on montre les fermentation qui s'y sont déroulées et les mesures qui y ont été faites */

SELECT C.noCuve, C.capacite, F.noFermentation, F.debutFermentation, F.finFermentation, F.chaptalisation, F.doseLevure, F.typeLevure, M.dateMesure, M.temperature, M.masseVol
FROM Cuve C 
JOIN Fermentation F ON C.noCuve = F.cuve
JOIN Mesure M ON M.fermentation = F.noFermentation
GROUP BY C.noCuve, C.capacite, F.noFermentation, F.debutFermentation, F.finFermentation, F.chaptalisation, F.doseLevure, F.typeLevure, M.dateMesure, M.temperature, M.masseVol 
ORDER BY C.noCuve, C.capacite, F.noFermentation, F.debutFermentation, F.finFermentation, F.chaptalisation, F.doseLevure, F.typeLevure, M.dateMesure, M.temperature, M.masseVol;


/* Pour chaque fermentation on montre les différentes mesures, ajout de Diammonium ou les remontages qui ont pu être effectués */

SELECT F.noFermentation AS fermentation, F.debutFermentation AS debutF, F.finFermentation AS finF, M.dateMesure, M.temperature, M.masseVol, R.dateRemontage, D.dateAjout AS ajoutDiammonium, D.quantite
FROM Fermentation F
JOIN Mesure M ON M.fermentation = F.noFermentation
JOIN Remontage R ON R.fermentation = F.noFermentation
JOIN Diammonium D ON D.fermentation = F.noFermentation
GROUP BY F.noFermentation, F.debutFermentation, F.finFermentation, M.dateMesure, M.temperature, M.masseVol, R.dateRemontage, D.dateAjout, D.quantite 
ORDER BY F.noFermentation, F.debutFermentation, F.finFermentation, M.dateMesure, M.temperature, M.masseVol, R.dateRemontage, D.dateAjout, D.quantite; 


/* Requete permettant de connaître le mélange de Moût dans une fermentation et de quel parcelle chaque mout provient */

SELECT A.fermentation, A.mout, P.noParcelle
FROM AssociationMoutFerm A 
JOIN Mout M ON M.noMout = A.mout
JOIN Parcelle P ON P.noParcelle = M.parcelle
GROUP BY A.fermentation, A.mout, P.noParcelle
ORDER BY A.fermentation, A.mout, P.noParcelle;
