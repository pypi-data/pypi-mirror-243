# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,E0402,W0611


"disk"


import datetime
import os
import time


from .object import Object, Default, cdir, dump, fqn, items, load, update
from .object import read, search, write


def __dir__():
    return (
        'Storage',
        'fetch',
        'find',
        'fntime',
        'last',
        'sync',
    )


__all__ = __dir__()


class Storage(Object):

    classes = {}
    wd = ""

    @staticmethod
    def add(clz) -> None:
        if not clz:
            return
        name = str(clz).split()[1][1:-2]
        Storage.classes[name] = clz

    @staticmethod
    def files() -> []:
        return os.listdir(Storage.store())

    @staticmethod
    def fns(mtc) -> []:
        dname = ''
        pth = Storage.store(mtc)
        for rootdir, dirs, _files in os.walk(pth, topdown=False):
            if dirs:
                for dname in sorted(dirs):
                    if dname.count('-') == 2:
                        ddd = os.path.join(rootdir, dname)
                        fls = sorted(os.listdir(ddd))
                        for fll in fls:
                            yield strip(os.path.join(ddd, fll))

    @staticmethod
    def long(name) -> str:
        split = name.split(".")[-1].lower()
        res = name
        for named in Storage.classes:
            if split in named.split(".")[-1].lower():
                res = named
                break
        if "." not in res:
            for fnm in Storage.files():
                claz = fnm.split(".")[-1]
                if fnm == claz.lower():
                    res = fnm
        return res

    @staticmethod
    def mods() -> str:
        pth =  Storage.path("mods")
        cdir(pth)
        return pth

    @staticmethod
    def path(pth) -> str:
        if not pth:
            pth = ""
        pth2 =  os.path.join(Storage.wd, pth)
        cdir(pth2)
        return pth2

    @staticmethod
    def store(pth="") -> str:
        pth = os.path.join(Storage.wd, "store", pth)
        pth2 = os.path.dirname(pth)
        cdir(pth2)
        return pth


def find(mtc, selector=None, index=None) -> []:
    clz = Storage.long(mtc)
    nr = -1
    for fnm in sorted(Storage.fns(clz), key=fntime):
        obj = Default()
        fetch(obj, fnm)
        if '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        nr += 1
        if index is not None and nr != int(index):
            continue
        yield (fnm, obj)


def fntime(daystr) -> float:
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def strip(pth, nmr=3) -> str:
    return os.sep.join(pth.split(os.sep)[-nmr:])


def ident(obj) -> str:
    return os.path.join(
                        fqn(obj),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )



def fetch(obj, pth) -> None:
    pth2 = Storage.store(pth)
    read(obj, pth2)
    return strip(pth)


def last(obj, selector=None) -> None:
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        return inp[0]


def sync(obj, pth=None) -> str:
    if pth is None:
        pth = ident(obj)
    pth2 = Storage.store(pth)
    write(obj, pth2)
    return pth
