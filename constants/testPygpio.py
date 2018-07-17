import random


class pygpio(object):

    @staticmethod
    def gpi_get(port):
        values = [0, 1]
        return random.choice(values)

    @staticmethod
    def gpio_init():
        return 0

    @staticmethod
    def gpo_set(portNum, gpoNum):
        return -1