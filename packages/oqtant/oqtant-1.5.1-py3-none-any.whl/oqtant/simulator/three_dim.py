# Copyright 2023 Infleqtion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass

import numpy as np


@dataclass
class ThreeDim:
    """
    'ThreeDim' Defines a two dimensional grid space in cylindrical coordinates with axial symmetry.
    Nx and Nr are the number of points in the x and r directions
    Lx and Lr are the lenghts of the x and z dimensions
    """

    # parameters for 3D space
    Nx = 300
    Nr = 100
    Lx = 30
    Lr = 4
    dx = Lx / Nx
    dr = Lr / Nr

    # defining cylindrical grids using np.meshgrid
    x_1d, r_1d = np.linspace(-Lx / 2, Lx / 2, Nx), np.linspace(dr / 2, Lr - dr / 2, Nr)

    x, r = np.meshgrid(x_1d, r_1d)

    # defining the equivalent cartesian grids for constructing the column densities
    z, y = np.meshgrid(
        np.linspace(-Lr + dr / 2, Lr - dr / 2, 2 * Nr),
        np.linspace(-Lr + dr / 2, Lr - dr / 2, 2 * Nr),
    )
    dz, dy = dr, dr
