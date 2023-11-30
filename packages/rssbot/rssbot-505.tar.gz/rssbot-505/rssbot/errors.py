# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E1102


"errors"


import io
import traceback


from .object import Object


def __dir__():
    return (
        'Errors',
        'debug'
    )


__all__ = __dir__()


class Errors(Object):

    errors = []
    filter = []
    output = None
    shown  = []

    @staticmethod
    def add(exc) -> None:
        excp = exc.with_traceback(exc.__traceback__)
        Errors.errors.append(excp)

    @staticmethod
    def format(exc) -> str:
        res = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            res += line + "\n"
        return res

    @staticmethod
    def handle(exc) -> None:
        if Errors.output:
            txt = str(Errors.format(exc))
            Errors.output(txt)

    @staticmethod
    def show() -> None:
        for exc in Errors.errors:
            Errors.handle(exc)

    @staticmethod
    def skip(txt) -> bool:
        for skp in Errors.filter:
            if skp in str(txt):
                return True
        return False


def debug(txt):
    if Errors.output and not Errors.skip(txt):
        Errors.output(txt)
