# coding=utf-8
import datetime

import pytz

from UegProject.Model.Election.ElectionDate import ElectionDate
from UegProject.Model.Types.CommunicationType import CommunicationType as CT


class Elections(object):
    """
    ======
    Elections class
    ======
        Attributes:
            electionsList: array list of ElectionDay entity
            toleranceMinutesStart: tolerance time to do CT.Carregamento before election
            toleranceMinutesEnd: tolerance time to do CT.Recebimento after election
    """
    SP_zone = pytz.timezone('America/Sao_Paulo')

    def __init__(self, electionList=None):
        self.__electionsList = electionList
        self.__toleranceMinutesStart = 10
        self.__toleranceMinutesEnd = 60

    def isValidElectionByCommunicationType(self, communicationType):

        now = datetime.datetime.now()

        for electionDate in self.__electionsList:
            if electionDate.date == now.date():

                start = datetime.datetime(electionDate.date.year, electionDate.date.month, electionDate.date.day,
                                          hour=electionDate.startTime.hour, minute=electionDate.startTime.minute)
                end = datetime.datetime(electionDate.date.year, electionDate.date.month, electionDate.date.day,
                                        hour=electionDate.stopTime.hour, minute=electionDate.stopTime.minute)

                diff_start = now - start
                diff_end = now - end

                if communicationType == CT.CARREGAMENTO and datetime.timedelta(
                        minutes=-10) <= diff_start <= datetime.timedelta(minutes=0):
                    print 'CARREGAMENTO das Uevs até %dmin antes do inicio das eleições -> Válido' \
                          % self.__toleranceMinutesStart
                    return True

                else:
                    if communicationType == CT.RECEBIMENTO and datetime.timedelta(
                            minutes=0) <= diff_end <= datetime.timedelta(minutes=self.__toleranceMinutesEnd):
                        print 'RECEBIMENTO dos Votos até %dmin depois do fim das eleições -> Válido' \
                              % self.__toleranceMinutesEnd
                        return True

        return False


    # Just for testing
    @staticmethod
    def testingElectionsModel():
        d0 = ElectionDate(2016, 10, 29, 19, 10, 20, 0)
        d1 = ElectionDate(2016, 10, 30, 20, 10, 19, 50)
        d2 = ElectionDate(2016, 10, 28, 8, 0, 18, 0)
        d3 = ElectionDate(2016, 10, 29, 8, 0, 18, 0)

        list = [d0, d1, d2, d3]

        elections = Elections(list)
        print elections.isValidElectionByCommunicationType(CT.CARREGAMENTO)
        return elections


# testingElectionsModel()
