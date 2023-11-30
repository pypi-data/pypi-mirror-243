# -*- coding: utf-8 -*-
# PyBEST: Pythonic Black-box Electronic Structure Tool
# Copyright (C) 2016-- The PyBEST Development Team
#
# This file is part of PyBEST.
#
# PyBEST is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# PyBEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --

# Detailed changelog:
#
# 2023: GPU cupy support written by Maximilian Kriebel

"""Contract arrays via NVIDIA GPU using cupy."""


cupy_optimized = [
    "xac,xbd,ecfd->eafb",  # much faster (~x10)
    "xac,xbd,ecfd->efab",  # much faster (~x10)
    "xac,xbd,edfc->eafb",  # much faster (~x10)
    "xac,xbd,efcd->efab",  # totest speed
    "xac,xbd,efcd->efba",  # totest speed
    "xac,xbd,efcd->eafb",  # totest speed
    "xac,xbd,efcd->abef",  # totest speed
    "xac,xbd,cefd->faeb",  # totest speed
    "xac,xbd,cedf->aebf",  # totest speed
    "xac,xbd,cedf->aefb",  # totest speed
    "xac,xbd,cedf->abfe",  # totest speed
]


def cupy_availability_check():
    """Checks if Cupy CUDA is properly installed.

    Returns True or False.

    """

    from pybest.log import log

    try:
        import cupy as cp
    except ImportError:
        log.warn("Warning")
        log.warn("Cupy CUDA not available.")
        log.warn("Defaulting to numpy.tensordot if select=None.")
        return False
    try:
        test_dummy_cupy = cp.zeros(0)
    except Exception:
        log.warn("Warning")
        log.warn("Can not allocate on VRAM.")
        log.warn("Cupy CUDA not properly installed.")
        log.warn("Defaulting to numpy.tensordot if select=None.")
        return False
    test_dummy_cupy += 1.0  # needed to make ruff happy
    del test_dummy_cupy
    cp.get_default_memory_pool().free_all_blocks()
    return True


# Check if cupy cuda is available.
# If yes, set PYBEST_CUPY_AVAIL to True, if no, set PYBEST_CUPY_AVAIL to False.
PYBEST_CUPY_AVAIL = cupy_availability_check()


def cupy_helper(subs, *args, **kwargs):
    """Contraction using GPU via cupy

    *** Arguments ***

    * subscript : string
          Specifies the subscripts for summation as comma separated-list
          of subscript labels, for example: 'abcd,efcd->abfe'.

    * operands : DenseNIndex
          These are the other arrays for the operation.
          The last operand is treated as output.

    *** Keyword argument ***

    * parts : positive integer > 0
          If given, an array is split "parts" times and looped over.
          Mostly Cholesky array is split at index "x".
          Option for the user for limited GPU memory.

    """

    import os

    import cupy as cp
    import numpy as np

    os.system("export CUPY_GPU_MEMORY_LIMIT='100%'")
    os.environ["CUPY_ACCELERATORS"] = "cutensor"

    if subs in (
        "xac,xbd,ecfd->eafb",  # much faster
        "xac,xbd,ecfd->efab",  # much faster
        "xac,xbd,edfc->eafb",  # much faster
        "xac,xbd,efcd->efab",
        "xac,xbd,efcd->efba",
        "xac,xbd,efcd->eafb",
        "xac,xbd,efcd->abef",
        "xac,xbd,cefd->faeb",
        "xac,xbd,cedf->aebf",
        "xac,xbd,cedf->aefb",
        "xac,xbd,cedf->abfe",
    ):
        dim_x = args[0].shape[0]
        # defaults dim_x is here only used as orientation...
        parts_c = 1
        parts_d = 1
        if dim_x < 2000:
            parts_c = 1
            parts_d = 1
        if dim_x >= 2000:
            parts_c = 1
            parts_d = 1
        if dim_x >= 2500:
            parts_c = 1
            parts_d = 1
        if dim_x >= 3000:
            parts_c = 2
            parts_d = 1
        if dim_x >= 3500:
            parts_c = 2
            parts_d = 1
        if dim_x >= 4000:
            parts_c = 3
            parts_d = 1
        if dim_x >= 4500:
            parts_c = 4
            parts_d = 2
        if dim_x >= 5000:
            parts_c = 4
            parts_d = 3
        if dim_x >= 5500:
            parts_c = 4
            parts_d = 4
        parts_c = kwargs.get("parts", parts_c)
        parts_d = kwargs.get("parts", parts_d)

        if subs in (
            "xac,xbd,ecfd->efab",
            "xac,xbd,ecfd->eafb",
        ):
            axis1 = 1
            axis2 = 3
        elif subs == "xac,xbd,edfc->eafb":  # totest speed
            axis1 = 3
            axis2 = 1
        elif subs in (
            "xac,xbd,efcd->efab",  # totest speed
            "xac,xbd,efcd->efba",  # totest speed
            "xac,xbd,efcd->eafb",  # totest speed
            "xac,xbd,efcd->abef",  # totest speed
        ):
            axis1 = 2
            axis2 = 3
        elif subs == "xac,xbd,cefd->faeb":  # totest speed
            axis1 = 0
            axis2 = 3
        elif subs in (
            "xac,xbd,cedf->aebf",  # totest speed
            "xac,xbd,cedf->aefb",  # totest speed
            "xac,xbd,cedf->abfe",  # totest speed
        ):
            axis1 = 0
            axis2 = 2

        # get lengths of chunks
        chol_chunk_lengths = []
        for x in range(0, parts_c):
            chol_chunk_lengths.append(
                np.array_split(args[0], parts_c, axis=1)[x].shape[1]
            )
        dense_e_chunk_lengths = []
        for x in range(0, parts_d):
            dense_e_chunk_lengths.append(
                np.array_split(args[2], parts_d, axis=0)[x].shape[0]
            )

        if parts_c == 1 and parts_d == 1:
            chol1 = cp.array(args[0])
            chol2 = cp.array(args[1])
            result_temp = cp.tensordot(chol1, chol2, axes=(0, 0))
            del chol1, chol2
            cp.get_default_memory_pool().free_all_blocks()
            operand = cp.array(args[2])
            result_part = cp.tensordot(
                result_temp, operand, axes=([1, 3], [axis1, axis2])
            )
            del result_temp, operand
            cp.get_default_memory_pool().free_all_blocks()
            if subs in (
                "xac,xbd,ecfd->efab",
                "xac,xbd,efcd->efab",  # totest speed
            ):
                result_cp = cp.transpose(result_part, axes=(2, 3, 0, 1))
            elif subs in (
                "xac,xbd,ecfd->eafb",
                "xac,xbd,edfc->eafb",  # totest speed
                "xac,xbd,efcd->eafb",  # totest speed
            ):
                result_cp = cp.transpose(result_part, axes=(2, 0, 3, 1))
            elif subs == "xac,xbd,efcd->efba":  # totest speed
                result_cp = cp.transpose(result_part, axes=(2, 3, 1, 0))
            elif subs == "xac,xbd,efcd->abef":  # totest speed
                result_cp = result_part
            elif subs == "xac,xbd,cefd->faeb":  # totest speed
                result_cp = cp.transpose(result_part, axes=(3, 0, 2, 1))
            elif subs == "xac,xbd,cedf->aebf":  # totest speed
                result_cp = cp.transpose(result_part, axes=(0, 2, 1, 3))
            elif subs == "xac,xbd,cedf->aefb":  # totest speed
                result_cp = cp.transpose(result_part, axes=(0, 2, 3, 1))
            elif subs == "xac,xbd,cedf->abfe":  # totest speed
                result_cp = cp.transpose(result_part, axes=(0, 1, 3, 2))
            result = result_cp.get()
            del result_part, result_cp
            cp.get_default_memory_pool().free_all_blocks()
        else:
            result = np.zeros(args[3].shape)
            if parts_d > 1:
                start_e = 0
                end_e = 0
                for e in range(0, parts_d):
                    end_e += dense_e_chunk_lengths[e]
                    start_a = 0
                    end_a = 0
                    for a in range(0, parts_c):
                        end_a += chol_chunk_lengths[a]
                        start_b = 0
                        end_b = 0
                        for b in range(0, parts_c):
                            end_b += chol_chunk_lengths[b]
                            chol_1 = cp.array(
                                np.array_split(args[0], parts_c, axis=1)[a]
                            )
                            chol_2 = cp.array(
                                np.array_split(args[1], parts_c, axis=1)[b]
                            )
                            result_temp = cp.tensordot(
                                chol_1, chol_2, axes=(0, 0)
                            )
                            del chol_1, chol_2
                            cp.get_default_memory_pool().free_all_blocks()
                            operand = cp.array(
                                np.array_split(args[2], parts_d, axis=0)[e]
                            )
                            result_temp_2 = cp.tensordot(
                                result_temp,
                                operand,
                                axes=([1, 3], [axis1, axis2]),
                            )
                            del operand, result_temp
                            cp.get_default_memory_pool().free_all_blocks()
                            if subs in (
                                "xac,xbd,ecfd->efab",
                                "xac,xbd,efcd->efab",  # totest speed
                            ):
                                result_part = cp.transpose(
                                    result_temp_2, axes=(2, 3, 0, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_e:end_e,
                                    :,
                                    start_a:end_a,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            elif subs in (
                                "xac,xbd,ecfd->eafb",
                                "xac,xbd,edfc->eafb",
                                "xac,xbd,efcd->eafb",  # totest speed
                            ):
                                result_part = cp.transpose(
                                    result_temp_2, axes=(2, 0, 3, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_e:end_e,
                                    start_a:end_a,
                                    :,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,efcd->efba":  # totest speed
                                result_part = cp.transpose(
                                    result_temp_2, axes=(2, 3, 1, 0)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_e:end_e,
                                    :,
                                    start_b:end_b,
                                    start_a:end_a,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,cedf->abfe":  # totest speed
                                result_part = cp.transpose(
                                    result_temp_2, axes=(0, 1, 3, 2)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    start_b:end_b,
                                    :,
                                    start_e:end_e,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,cefd->faeb":  # totest speed
                                result_part = cp.transpose(
                                    result_temp_2, axes=(3, 0, 2, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    :,
                                    start_a:end_a,
                                    start_e:end_e,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,cedf->aebf":  # totest speed
                                result_part = cp.transpose(
                                    result_temp_2, axes=(0, 2, 1, 3)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    start_e:end_e,
                                    start_b:end_b,
                                    :,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,cedf->aefb":  # totest speed
                                result_part = cp.transpose(
                                    result_temp_2, axes=(0, 2, 3, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    start_e:end_e,
                                    :,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,efcd->abef":  # totest speed
                                result_part = result_temp_2
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    start_b:end_b,
                                    start_e:end_e,
                                    :,
                                ] = result_part.get()
                                del result_part
                            cp.get_default_memory_pool().free_all_blocks()
                            start_b = end_b
                        start_a = end_a
                    start_e = end_e
            else:
                start_a = 0
                end_a = 0
                for a in range(0, parts_c):
                    end_a += chol_chunk_lengths[a]
                    start_b = 0
                    end_b = 0
                    for b in range(0, parts_c):
                        end_b += chol_chunk_lengths[b]
                        chol_1 = cp.array(
                            np.array_split(args[0], parts_c, axis=1)[a]
                        )
                        chol_2 = cp.array(
                            np.array_split(args[1], parts_c, axis=1)[b]
                        )
                        result_temp = cp.tensordot(chol_1, chol_2, axes=(0, 0))
                        del chol_1, chol_2
                        cp.get_default_memory_pool().free_all_blocks()
                        operand = cp.array(args[2])
                        result_temp_2 = cp.tensordot(
                            result_temp,
                            operand,
                            axes=([1, 3], [axis1, axis2]),
                        )
                        del operand, result_temp
                        cp.get_default_memory_pool().free_all_blocks()
                        if subs in (
                            "xac,xbd,ecfd->efab",
                            "xac,xbd,efcd->efab",  # totest speed
                        ):
                            result_part = cp.transpose(
                                result_temp_2, axes=(2, 3, 0, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                :, :, start_a:end_a, start_b:end_b
                            ] = result_part.get()
                            del result_part
                        elif subs in (
                            "xac,xbd,ecfd->eafb",
                            "xac,xbd,edfc->eafb",
                            "xac,xbd,efcd->eafb",  # totest speed
                        ):
                            result_part = cp.transpose(
                                result_temp_2, axes=(2, 0, 3, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                :, start_a:end_a, :, start_b:end_b
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,efcd->efba":  # totest speed
                            result_part = cp.transpose(
                                result_temp_2, axes=(2, 3, 1, 0)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                :, :, start_b:end_b, start_a:end_a
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,cedf->abfe":  # totest speed
                            result_part = cp.transpose(
                                result_temp_2, axes=(0, 1, 3, 2)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, start_b:end_b, :, :
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,cefd->faeb":  # totest speed
                            result_part = cp.transpose(
                                result_temp_2, axes=(3, 0, 2, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                :, start_a:end_a, :, start_b:end_b
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,cedf->aebf":  # totest speed
                            result_part = cp.transpose(
                                result_temp_2, axes=(0, 2, 1, 3)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, :, start_b:end_b, :
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,cedf->aefb":  # totest speed
                            result_part = cp.transpose(
                                result_temp_2, axes=(0, 2, 3, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, :, :, start_b:end_b
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,efcd->abef":  # totest speed
                            result_part = result_temp_2
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, start_b:end_b, :, :
                            ] = result_part.get()
                            del result_part
                        cp.get_default_memory_pool().free_all_blocks()
                        start_b = end_b
                    start_a = end_a

    elif subs in (
        "sd,pqrs->pqrd",
        "rc,pqrd->pqcd",
        "qb,pqcd->pbcd",
        "pa,pbcd->abcd",
    ):
        dim_y = args[0].shape[1]

        # defaults (need finetuning)
        parts = 1
        if dim_y >= 200:
            parts = 2
        if dim_y >= 250:
            parts = 3
        if dim_y >= 300:
            parts = 6
        if dim_y >= 350:
            parts = 7
        if dim_y >= 400:
            parts = 8
        if dim_y >= 500:
            parts = 16
        parts = kwargs.get("parts", parts)

        if subs == "sd,pqrs->pqrd":
            ax_spl = 2
            axis = 3
        elif subs == "rc,pqrd->pqcd":
            ax_spl = 1
            axis = 2
        elif subs == "qb,pqcd->pbcd":
            ax_spl = 0
            axis = 1
        elif subs == "pa,pbcd->abcd":
            ax_spl = 3
            axis = 0

        # get lengths of chunks
        chunk_lengths = []
        for y in range(0, parts):
            chunk_lengths.append(
                np.array_split(args[1], parts, axis=ax_spl)[y].shape[ax_spl]
            )

        if parts == 1:
            op0 = cp.array(args[0])
            op1 = cp.array(args[1])
            result_temp = cp.tensordot(op0, op1, axes=(0, axis))
            result_cp = 0.0
            del op0, op1
            cp.get_default_memory_pool().free_all_blocks()
            if subs == "sd,pqrs->pqrd":  # totest speed
                result_cp = cp.transpose(result_temp, axes=(1, 2, 3, 0))
            elif subs == "rc,pqrd->pqcd":  # totest speed
                result_cp = cp.transpose(result_temp, axes=(1, 2, 0, 3))
            elif subs == "qb,pqcd->pbcd":  # totest speed
                result_cp = cp.transpose(result_temp, axes=(1, 0, 2, 3))
            elif subs == "pa,pbcd->abcd":  # totest speed
                result_cp = cp.transpose(result_temp, axes=(0, 1, 2, 3))
            del result_temp
            cp.get_default_memory_pool().free_all_blocks()
            result = result_cp.get()
            del result_cp
            cp.get_default_memory_pool().free_all_blocks()
        else:
            result = np.zeros(args[2].shape)
            start_y = 0
            end_y = 0
            op0 = cp.array(args[0])
            for y in range(0, parts):
                end_y += chunk_lengths[y]

                op1 = cp.array(np.array_split(args[1], parts, axis=ax_spl)[y])
                result_temp = cp.tensordot(op0, op1, axes=(0, axis))
                result_cp = 0.0
                if subs == "sd,pqrs->pqrd":  # totest speed
                    result_cp = cp.transpose(result_temp, axes=(1, 2, 3, 0))
                    del result_temp
                    cp.get_default_memory_pool().free_all_blocks()
                    result[:, :, start_y:end_y, :] = result_cp.get()
                elif subs == "rc,pqrd->pqcd":  # totest speed
                    result_cp = cp.transpose(result_temp, axes=(1, 2, 0, 3))
                    del result_temp
                    cp.get_default_memory_pool().free_all_blocks()
                    result[:, start_y:end_y, :, :] = result_cp.get()
                elif subs == "qb,pqcd->pbcd":  # totest speed
                    result_cp = cp.transpose(result_temp, axes=(1, 0, 2, 3))
                    del result_temp
                    cp.get_default_memory_pool().free_all_blocks()
                    result[start_y:end_y, :, :, :] = result_cp.get()
                elif subs == "pa,pbcd->abcd":  # totest speed
                    result_cp = cp.transpose(result_temp, axes=(0, 1, 2, 3))
                    del result_temp
                    cp.get_default_memory_pool().free_all_blocks()
                    result[:, :, :, start_y:end_y] = result_cp.get()
                del result_cp
                cp.get_default_memory_pool().free_all_blocks()
                start_y = end_y

    elif subs in (
        "bi,kbd->kid",
        "dj,kid->kij",
    ):
        dim_k = args[1].shape[1]

        # here index "k" is split "parts" times
        # defaults (need finetuning)
        parts = 1
        if dim_k >= 200:
            parts = 2
        if dim_k >= 300:
            parts = 4
        if dim_k >= 400:
            parts = 8
        if dim_k >= 500:
            parts = 16
        parts = kwargs.get("parts", parts)

        # size of chunks is determined
        chunks = []
        for x in range(0, parts):
            chunks.append(np.array_split(args[1], parts, axis=0)[x].shape[0])
        if subs == "bi,kbd->kid":
            axis = 1
        elif subs == "dj,kid->kij":
            axis = 2
        # Dense array operand is copied to GPU Memory (VRAM)
        operand = cp.array(args[0])

        if parts == 1:
            # Cholesky array is copied to GPU Memory (VRAM)
            chol_cp = cp.array(args[1])
            # Partial calculation on GPU
            result_temp = cp.tensordot(chol_cp, operand, axes=(axis, 0))
            del chol_cp, operand
            cp.get_default_memory_pool().free_all_blocks()
            if subs == "bi,kbd->kid":
                result = cp.transpose(result_temp, axes=(0, 2, 1)).get()
            elif subs == "dj,kid->kij":
                result = result_temp.get()
            del result_temp
            cp.get_default_memory_pool().free_all_blocks()
        else:
            start_k = 0
            end_k = 0
            result = np.zeros(args[2].shape)
            for k in range(0, parts):
                end_k += chunks[k]
                # Cholesky array is copied to GPU Memory (VRAM)
                chol_cp = cp.array(np.array_split(args[1], parts, axis=0)[k])
                # Partial calculation on GPU
                result_temp = cp.tensordot(chol_cp, operand, axes=(axis, 0))
                del chol_cp
                cp.get_default_memory_pool().free_all_blocks()
                if subs == "bi,kbd->kid":
                    result_part = cp.transpose(result_temp, axes=(0, 2, 1))
                elif subs == "dj,kid->kij":
                    result_part = result_temp
                del result_temp
                cp.get_default_memory_pool().free_all_blocks()
                result[start_k:end_k, :, :] = result_part.get()
                del result_part
                cp.get_default_memory_pool().free_all_blocks()
                start_k = end_k
            del operand
            cp.get_default_memory_pool().free_all_blocks()

    # generic
    else:
        pool = cp.cuda.MemoryPool(cp.cuda.memory.malloc_managed)
        cp.cuda.set_allocator(pool.malloc)
        # Input operands are copied to GPU Memory (VRAM).
        operands_cp = []
        for num in range(0, len(subs.split("->")[0].split(","))):
            operands_cp.append(cp.asarray(args[num]))
        # calculation on GPU
        result_cp = cp.einsum(subs, *operands_cp)
        # Result is copied back to RAM
        result = result_cp.get()
        # VRAM deallocation
        del result_cp, operands_cp
        pool.free_all_blocks()

    cp.get_default_memory_pool().free_all_blocks()
    # Result is returned
    return result
