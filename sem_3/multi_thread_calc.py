import os
import shutil
import random as rnd
from multiprocessing import Pool
from multiprocessing.pool import AsyncResult
from typing import TextIO

import numpy as np

from exceptions import *


def wrapper(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("Invalid input matrix")
        except InvalidSizeException:
            print("Can't multiple matrix of this size")
        except OSError:
            print("File system error")
        except TypeError:
            print("Invalid arguments")
    return wrap


def read_file(file_path: str) -> TextIO:
    return open(os.path.abspath(file_path), mode="r", encoding="utf-8")


def write_file(file_path: str) -> TextIO:
    return open(os.path.abspath(file_path), mode="w", encoding="utf-8")


def check_size(mx: np.ndarray) -> bool:
    hor_size = len(mx[0])
    for row in mx:
        if len(row) != hor_size:
            return False
    return True


@wrapper
def parse_mx(mx_path: str) -> np.ndarray:
    res = []
    with read_file(mx_path) as file:
        while True:
            row = file.readline()
            if row:
                res.append(list(map(lambda x: float(x), row.split())))
            else:
                break
    arr = np.array(res)
    if not check_size(arr):
        raise InvalidSizeException
    return np.array(res)


def calc_el(m1: np.ndarray, m2: np.ndarray, row: int, col: int) -> float:
    res = 0.0
    for i in range(len(m2)):
        res += m1[row][i] * m2[i][col]
    return res


def cache_size(dir_path: str, ver_size: int, hor_size: int):
    with write_file(f"{dir_path}/size") as file:
        file.write(f"{ver_size} {hor_size}")


def cache_el(cache_path: str, el: float, row: int, col: int):
    with write_file(f"{cache_path}/{row}_{col}") as file:
        file.write(str(el))


def calc_and_cache_el(cache_path, m1: np.ndarray, m2: np.ndarray, row: int, col: int):
    cache_el(cache_path, calc_el(m1, m2, row, col), row, col)


def write_cache(file_path, cache_path) -> None:
    with write_file(file_path) as res_file:
        with read_file(f"{cache_path}/size") as size_file:
            size = tuple(map(lambda x: int(x), size_file.readline().split()))
        for row in range(size[0]):
            for col in range(size[1]):
                with read_file(f"{cache_path}/{row}_{col}") as el_file:
                    res_file.write(f"{el_file.readline().strip():>10} ")
            res_file.write("\n")


def start_workers(cache_path: str, m1: np.ndarray, m2: np.ndarray, threads: int = None):
    ver_size, hor_size = len(m1), len(m2[0])
    pool = Pool(threads) if threads is not None else Pool()
    proc_list = []
    for row in range(ver_size):
        for col in range(hor_size):
            proc_list.append(
                pool.apply_async(
                    calc_and_cache_el, (cache_path, m1, m2, row, col)))
    return proc_list


def wait_workers(workers: list[AsyncResult]):
    total, cur, last_val = len(workers), 0, -1
    for proc in workers:
        proc.wait()
        cur += 1
        new_val = round((cur * 100) / total)
        if new_val != last_val: print(f"{new_val} %")
        last_val = new_val


@wrapper
def calc_mx(res_path: str, m1: np.ndarray, m2: np.ndarray) -> None:
    CACHE_PATH = "temp"
    POOL_COUNT = 4
    if not os.path.exists(CACHE_PATH): os.mkdir(CACHE_PATH)
    if len(m1[0]) != len(m2): raise InvalidSizeException()
    ver_size, hor_size = len(m1), len(m2[0])
    print(f"Size of the resulting matrix: ({hor_size}; {ver_size})")
    cache_size(CACHE_PATH, ver_size, hor_size)
    print("Starting threads ...")
    workers = start_workers(CACHE_PATH, m1, m2, POOL_COUNT)
    print("Calculating ..")
    wait_workers(workers)
    print("Writing resulting matrix ...")
    write_cache(res_path, CACHE_PATH)
    print("Removing cache ...")
    shutil.rmtree(CACHE_PATH)
    print("Completed")


def test(size: int, dest_path: str):
    LIMIT_MODULE = 1e10
    mx = np.array([
            [rnd.uniform(-LIMIT_MODULE, LIMIT_MODULE)
             for _ in range(size)]
            for _ in range(size)
        ])
    calc_mx(dest_path, mx, mx)


if __name__ == "__main__":
    DEST = "dest/res.txt"

    test(1000, DEST)

    # calc_mx(DEST,
    #         parse_mx("src/one"),
    #         parse_mx("src/two"))
