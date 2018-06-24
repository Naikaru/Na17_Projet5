CREATE TABLE EtapeFabrication(
	idEtape SERIAL PRIMARY KEY
);


CREATE TABLE Incident(
	idIncident VARCHAR PRIMARY KEY,
	description VARCHAR,
	dateIncident DATE,
	etape INTEGER REFERENCES EtapeFabrication(idEtape) NOT NULL
);


CREATE TABLE Parcelle(
	noParcelle INTEGER REFERENCES EtapeFabrication(idEtape) PRIMARY KEY,
	lattitudeEntree NUMERIC(7,2),
	longitudeEntree NUMERIC(7,2),
	superficie NUMERIC(7,2),
	exposition CHAR(1),

	CHECK(exposition IN ('N','S','E','W'))
);


CREATE TABLE Mout(
	noMout INTEGER REFERENCES EtapeFabrication(idEtape) PRIMARY KEY,
	parcelle INTEGER NOT NULL REFERENCES Parcelle(noParcelle),
	dateRecolte DATE NOT NULL,
	meteoRecolte VARCHAR,
	temperatureRecolte NUMERIC(3,1),
	
	UNIQUE (parcelle, dateRecolte)
);


CREATE TABLE Cuve(
	noCuve INTEGER REFERENCES EtapeFabrication(idEtape) PRIMARY KEY,
	capacite NUMERIC(5,2)
);


CREATE TABLE Fermentation(
	noFermentation INTEGER REFERENCES EtapeFabrication(idEtape) PRIMARY KEY,
	cuve INTEGER REFERENCES Cuve(noCuve) NOT NULL,
	debutFermentation TIMESTAMP NOT NULL,
	finFermentation TIMESTAMP NOT NULL,
	chaptalisation NUMERIC (6,3),
	doseLEvure NUMERIC (6,3),
	typeLevure VARCHAR,

	CHECK(typeLevure IN ('cerevisiae', 'bayanus', 'acidifaciens', 'apiculata', 'bacillaris')) 
);


CREATE TABLE AssociationMoutFerm(
	mout INTEGER REFERENCES Mout(noMout),
	fermentation INTEGER REFERENCES Fermentation(noFermentation),

	PRIMARY KEY (mout, fermentation)
); 


CREATE TABLE Fut(
	noFut INTEGER REFERENCES EtapeFabrication(idEtape) PRIMARY KEY,
	contenance NUMERIC(5,2),
	essenceBois VARCHAR
);


CREATE TABLE Vieillissement(
	noVieillissement INTEGER REFERENCES EtapeFabrication(idEtape) PRIMARY KEY,
	fermentation INTEGER REFERENCES fermentation(noFermentation) NOT NULL,
	fut INTEGER NOT NULL REFERENCES Fut(noFut),
	debutV TIMESTAMP NOT NULL,
	finV TIMESTAMP CHECK(finV > debutV),
	qualite CHAR(1),
	robe VARCHAR,
	alcool NUMERIC(3,1),

	UNIQUE (fut, debutV),
	CHECK(qualite IS NULL OR finV IS NOT NULL),
	CHECK((now() >= finV) OR qualite IS NULL),
	CHECK(qualite IN ('A', 'B', 'C', 'D', 'E', 'F')) 
);


CREATE TABLE Bouteille(
	noSerie INTEGER REFERENCES EtapeFabrication(idEtape) PRIMARY KEY,
	vin INTEGER REFERENCES Vieillissement(noVieillissement),
	contenance INTEGER
);


CREATE TABLE Mesure(
	fermentation INTEGER REFERENCES Fermentation(noFermentation),
	dateMesure TIMESTAMP,
	temperature NUMERIC(4,2) NOT NULL,
	masseVol NUMERIC(5,3) NOT NULL,

	PRIMARY KEY (fermentation, dateMesure)
);


CREATE TABLE Remontage(
	fermentation INTEGER REFERENCES Fermentation(noFermentation),
	dateRemontage TIMESTAMP,
	raison VARCHAR REFERENCES Incident(idIncident),

	PRIMARY KEY (fermentation, dateRemontage)
);


CREATE TABLE Diammonium(
	fermentation INTEGER REFERENCES Fermentation(noFermentation),
	dateAjout TIMESTAMP,
	quantite NUMERIC(5,3) ,
	raison VARCHAR REFERENCES Incident(idIncident),

	PRIMARY KEY (fermentation, dateAjout),
	CHECK (quantite > 0)
);


/*
Les trigger suivants ont pour but de permettre l'ajout automatique d'un idEtape dans la table EtapeFabrication lors de l'ajout d'une de ses classes filles.

*/
--Trigger d'ajout des futs
CREATE OR REPLACE FUNCTION funtrig_insfut()
  RETURNS trigger AS
$func$
BEGIN

	INSERT INTO EtapeFabrication (idEtape) VALUES (DEFAULT);
	NEW.noFut := (SELECT idEtape FROM EtapeFabrication ORDER BY idEtape DESC LIMIT 1);

RETURN NEW;
END
$func$  LANGUAGE plpgsql;

CREATE TRIGGER trig_insfut
    BEFORE INSERT
    ON fut
    FOR EACH ROW EXECUTE PROCEDURE funtrig_insfut();

--trigger d'ajout des parcelles
CREATE OR REPLACE FUNCTION funtrig_insparc()
  RETURNS trigger AS
$func$
BEGIN

	INSERT INTO EtapeFabrication (idEtape) VALUES (DEFAULT);
	NEW.noParcelle := (SELECT idEtape FROM EtapeFabrication ORDER BY idEtape DESC LIMIT 1);

RETURN NEW;
END
$func$  LANGUAGE plpgsql;

CREATE TRIGGER trig_insparc BEFORE INSERT ON parcelle FOR EACH ROW EXECUTE PROCEDURE funtrig_insparc();
--trigger d'ajout des moûts
CREATE OR REPLACE FUNCTION funtrig_insmout()
  RETURNS trigger AS
$func$
BEGIN

	INSERT INTO EtapeFabrication (idEtape) VALUES (DEFAULT);
	NEW.noMout := (SELECT idEtape FROM EtapeFabrication ORDER BY idEtape DESC LIMIT 1);

RETURN NEW;
END
$func$  LANGUAGE plpgsql;

CREATE TRIGGER trig_insmout
    BEFORE INSERT
    ON Mout
    FOR EACH ROW EXECUTE PROCEDURE funtrig_insmout();
--trigger d'ajout des cuves
CREATE OR REPLACE FUNCTION funtrig_inscuve()
  RETURNS trigger AS
$func$
BEGIN

	INSERT INTO EtapeFabrication (idEtape) VALUES (DEFAULT);
	NEW.noCuve := (SELECT idEtape FROM EtapeFabrication ORDER BY idEtape DESC LIMIT 1);

RETURN NEW;
END
$func$  LANGUAGE plpgsql;

CREATE TRIGGER trig_inscuve
    BEFORE INSERT
    ON Cuve
    FOR EACH ROW EXECUTE PROCEDURE funtrig_inscuve();
--trigger d'ajout des fermentations
CREATE OR REPLACE FUNCTION funtrig_insferm()
  RETURNS trigger AS
$func$
BEGIN

	INSERT INTO EtapeFabrication (idEtape) VALUES (DEFAULT);
	NEW.noFermentation := (SELECT idEtape FROM EtapeFabrication ORDER BY idEtape DESC LIMIT 1);

RETURN NEW;
END
$func$  LANGUAGE plpgsql;

CREATE  TRIGGER trig_insferm
    BEFORE INSERT
    ON Fermentation
    FOR EACH ROW EXECUTE PROCEDURE funtrig_insferm();
	
--trigger d'ajout des vieillissements
CREATE OR REPLACE FUNCTION funtrig_insvieil()
  RETURNS trigger AS
$func$
BEGIN

	INSERT INTO EtapeFabrication (idEtape) VALUES (DEFAULT);
	NEW.noVieillissement := (SELECT idEtape FROM EtapeFabrication ORDER BY idEtape DESC LIMIT 1);

RETURN NEW;
END
$func$  LANGUAGE plpgsql;

CREATE  TRIGGER trig_insvieil BEFORE INSERT ON Vieillissement
    FOR EACH ROW EXECUTE PROCEDURE funtrig_insvieil();
--trigger d'ajout des bouteilles
CREATE OR REPLACE FUNCTION funtrig_insbout()
  RETURNS trigger AS
$func$
BEGIN

	INSERT INTO EtapeFabrication (idEtape) VALUES (DEFAULT);
	NEW.noSerie := (SELECT idEtape FROM EtapeFabrication ORDER BY idEtape DESC LIMIT 1);

RETURN NEW;
END
$func$  LANGUAGE plpgsql;

CREATE  TRIGGER trig_insbout
    BEFORE INSERT
    ON Bouteille
    FOR EACH ROW EXECUTE PROCEDURE funtrig_insbout();
	
	
	
--trigger vérification date fermentation, pour vérifier la contrainte ensembliste.
CREATE OR REPLACE FUNCTION verif_date_fermentation() 
        RETURNS trigger AS
$func$
BEGIN
        IF EXISTS 
        (
                SELECT F.noFermentation FROM Fermentation as F
                WHERE
                        NEW.cuve = F.cuve 
                        AND(
                                (NEW.debutFermentation < F.debutFermentation AND NEW.finFermentation > F.debutFermentation)
                                OR
                                (NEW.debutFermentation < F.finFermentation AND NEW.finFermentation > F.finFermentation)   
							)
        )
        THEN
                RAISE EXCEPTION 'Erreur, il y a conflit dans la cuve';
        END IF;
        RETURN NEW;
END
$func$ LANGUAGE plpgsql;


CREATE TRIGGER verif_date_fermentation 
        BEFORE INSERT OR UPDATE 
        ON Fermentation
    FOR EACH ROW EXECUTE PROCEDURE verif_date_fermentation();


	
INSERT INTO Parcelle VALUES (DEFAULT,'1234.56','7891.01','40.00','N');
INSERT INTO Parcelle VALUES (DEFAULT,'7891.01','2345.67','30.00','E');

INSERT INTO MOUT VALUES(DEFAULT,'1','2017-09-15','soleil','18');
INSERT INTO MOUT VALUES(DEFAULT,'2','2017-09-18','brume','12');

INSERT INTO CUVE VALUES(DEFAULT,'200');
INSERT INTO CUVE VALUES(DEFAULT,'400');

INSERT INTO Fermentation VALUES (DEFAULT,'5','2017-10-15 15:15:00','2018-01-15 17:17:00','20.30','40.50','cerevisiae');
INSERT INTO Fermentation VALUES (DEFAULT,'6','2017-10-18 18:15:00','2018-01-18 18:17:00','10.20','30.40','bayanus');

INSERT INTO AssociationMoutFerm VALUES ('3','7');
INSERT INTO AssociationMoutFerm VALUES ('4','8');

INSERT INTO Fut VALUES (DEFAULT,'50.00','pin');
INSERT INTO Fut VALUES (DEFAULT,'40.00','cedre');

INSERT INTO Vieillissement VALUES (DEFAULT,'7','9','2017-12-25 14:30:00');
INSERT INTO Vieillissement VALUES (DEFAULT,'8','10','2017-11-15 12:00:00');

INSERT INTO Bouteille VALUES (DEFAULT,'11','75');
INSERT INTO Bouteille VALUES (DEFAULT,'12','150');

INSERT INTO Mesure VALUES ('7','2018-01-15 12:30:00','2.5','1.23');
INSERT INTO Mesure VALUES ('8','2018-01-18 14:30:00','5.2','4.56');

INSERT INTO Incident VALUES('1','fuite','2017-11-12','8');
INSERT INTO Incident VALUES('2','problème avec le fût','2017-12-13','10');

INSERT INTO Remontage VALUES ('7','2017-11-18','1');
INSERT INTO Remontage VALUES ('8','2017-12-23','2');

INSERT INTO Diammonium VALUES ('7','2017-12-15','8.6','1');
INSERT INTO Diammonium VALUES ('8','2018-01-06','4.2','2');


-- Exemple de vue : on peut donner, pour chaque bouteille, des infos sur la traçabilité de la parcelle à la bouteille. En suivant le même principe, on peut afficher toutes les informations nécessaires sur les incidents, les opérations au cours du remontage, ...
CREATE OR REPLACE VIEW trace 
AS
(SELECT parcelle.noParcelle,
	parcelle.exposition,
	mout.meteoRecolte AS meteoRecolte,
	mout.dateRecolte,
	fermentation.finFermentation,
	fermentation.debutFermentation,
	fermentation.noFermentation,
	vieillissement.fut AS Fut,
	bouteille.noSerie
FROM parcelle,
	mout,
	fermentation,
	vieillissement,
	AssociationMoutFerm,
	bouteille
WHERE parcelle.noParcelle = mout.parcelle 
	AND AssociationMoutFerm.mout = mout.noMout
	AND AssociationMoutFerm.fermentation = fermentation.noFermentation
	AND fermentation.noFermentation= vieillissement.fermentation
	AND bouteille.vin = vieillissement.noVieillissement
);



--Insertion qui chevauche une autre fermentation, pour tester l'implémentation de la contrainte ensembliste :
--INSERT INTO Fermentation VALUES (DEFAULT,'6','2017-12-18 15:10:00','2018-05-26 18:30:00','5.20','15.40','bacillaris');
