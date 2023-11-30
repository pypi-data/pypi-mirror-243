# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"broker"


from .object import Object


def __dir__():
    return (
        'Broker',
    )


__all__ = __dir__()


class Broker(Object):

    objs = []

    @staticmethod
    def add(obj) -> None:
        Broker.objs.append(obj)

    @staticmethod
    def byorig(orig) -> Object:
        for obj in Broker.objs:
            if object.__repr__(obj) == orig:
                return obj
        return None

    @staticmethod
    def first():
        if Broker.objs:
            return Broker.objs[0]
