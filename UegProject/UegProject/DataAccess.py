import os
import time
import mysql.connector
# from Model.Voter import Voter
# from Model.Region import Region
# from Model.Uev import Uev
# from Model.Candidate import Candidate
import abc

from UegProject.Model.Election.Candidate import Candidate
from UegProject.Model.Election.Region import Region
from UegProject.Model.Election.Uev import Uev
from UegProject.Model.Election.Voter import Voter


class DataAccess:
    __metaclass__ = abc.ABCMeta

    cursor = None
    db = None

    @classmethod
    def _connect_database(cls):
        try:
            cls.db = mysql.connector.connect(user='root',
                                             password='xxx',
                                             host='127.0.0.1',
                                             database='ueg')
            cls.cursor = cls.db.cursor()

        except:
            print("Unable to connect, verify database status.")
            time.sleep(0.5)
            cls._connect_database()

    @classmethod
    def getUevList(cls):
        cls._connect_database()

        query_voters = "SELECT EL.nome, EL.cpf, EL.URL, C.Cidade, E.Estado, P.Pais " \
                       "FROM tb_eleitor AS EL " \
                       "INNER JOIN tb_cidade AS C ON EL.Cidade_id = C.Cidade_id " \
                       "INNER JOIN tb_estado AS E ON C.Estado_id = E.Estado_id " \
                       "INNER JOIN tb_pais AS P ON E.Pais_id = P.Pais_id;"

        query_uevs = "SELECT U.Usuario, U.Senha, C.Cidade, E.Estado, P.Pais, U.Ativo " \
                     "FROM tb_uev AS U " \
                     "INNER JOIN tb_cidade AS C ON C.Cidade_id = U.Cidade_id " \
                     "INNER JOIN tb_estado AS E ON C.Estado_id = E.Estado_id " \
                     "INNER JOIN tb_pais AS P ON E.Pais_id = P.Pais_id;"

        query_candidates = "SELECT EL.Nome, CA.CPF, EL.Votou, C.Cidade, E.Estado, P.Pais, EL.URL, CA.numero, " \
                           "CAR.Cargo, CA.Apelido " \
                           "FROM tb_candidato AS CA " \
                           "INNER JOIN tb_eleitor AS EL ON CA.CPF = EL.CPF " \
                           "LEFT JOIN tb_cidade AS C ON CA.Cidade_id = C.Cidade_id " \
                           "LEFT JOIN tb_estado AS E ON CA.Estado_id = E.Estado_id " \
                           "LEFT JOIN tb_pais AS P ON CA.Pais_id = P.Pais_id " \
                           "INNER JOIN tb_cargo AS CAR ON CA.Cargo_id = CAR.cargo_id;"

        cls.cursor.execute(query_voters)
        cls.__eleitoresListDB = cls.cursor.fetchall()

        cls.cursor.execute(query_uevs)
        cls.__uevListDB = cls.cursor.fetchall()

        cls.cursor.execute(query_candidates)
        cls.__candidateListDB = cls.cursor.fetchall()

        cls.__uevList = []
        for uev in cls.__uevListDB:
            cls.__voterList = []
            for eleitor in cls.__eleitoresListDB:
                if eleitor[3] == uev[2]:
                    cls.__voterList.append(Voter(eleitor[0], eleitor[1], 0, Region(eleitor[3],
                                                                                   eleitor[4], eleitor[5]), eleitor[2]))
            cls.__uevList.append(Uev(uev[0], uev[1], Region(uev[2], uev[3], uev[4]), cls.__voterList, uev[5]))

        for uev in cls.__uevList:
            for candidate in cls.__candidateListDB:
                if candidate[8] == "Presidente" or candidate[0] == "NULO" or candidate[0] == "BRANCO":
                    uev.addCandidate(Candidate(candidate[0], candidate[1], candidate[2], Region(candidate[3],
                                                                                                candidate[4],
                                                                                                candidate[5]),
                                               candidate[6], candidate[7], candidate[8], candidate[9]))
                elif candidate[8] == "Deputado" or candidate[8] == "Governador":
                    if candidate[4] == uev.region.state:
                        uev.addCandidate(Candidate(candidate[0], candidate[1], candidate[2], Region(candidate[3],
                                                                                                    candidate[4],
                                                                                                    candidate[5]),
                                                   candidate[6], candidate[7], candidate[8], candidate[9]))
                else:
                    if candidate[3] == uev.region.city:
                        uev.addCandidate(Candidate(candidate[0], candidate[1], candidate[2], Region(candidate[3],
                                                                                                    candidate[4],
                                                                                                    candidate[5]),
                                                   candidate[6], candidate[7], candidate[8], candidate[9]))

        cls.db.close()
        return cls.__uevList

    @classmethod
    def setVotesPerCandidate(cls, candidates):
        cls._connect_database()

        for candidate in candidates:
            queryUpdateVotes = "UPDATE tb_candidato " \
                               "SET Votos = " + str(candidate.votes) + " " \
                                                                       "WHERE CPF = " + str(candidate.cpf) + ";"
            cls.cursor.execute(queryUpdateVotes)

        cls.db.commit()
        cls.db.close()

    @classmethod
    def setFlagVotesVoter(cls, voters):
        cls._connect_database()

        for voter in voters:
            if voter.votedFlag:
                queryUpdateVotedFlag = "UPDATE tb_eleitor " \
                                       "SET Votou = " + str(voter.votedFlag) + " " \
                                                                               "WHERE CPF = " + str(voter.cpf) + ";"
                cls.cursor.execute(queryUpdateVotedFlag)

        cls.db.commit()
        cls.db.close()

    @classmethod
    def updateActiveFlagUev(cls, uevs):
        cls._connect_database()

        for uev in uevs:
            queryUpdateActiveFlag = "UPDATE tb_uev " \
                                    "SET Ativo = " + str(uev.isActive()) + " " \
                                                                           "WHERE Usuario = " + str(uev.username) + ";"
            cls.cursor.execute(queryUpdateActiveFlag)

        cls.db.commit()
        cls.db.close()


# DataAccess.getUevList()
