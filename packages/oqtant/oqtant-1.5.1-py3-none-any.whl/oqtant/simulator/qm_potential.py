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

import numpy as np

from oqtant.simulator.three_dim import ThreeDim


class QMPotential:
    """
    'QMPotential' translate Oqtant 'quantum_matter' object into simulation units and uses that objects get_potential function to construct a 2D array used for the potential energy in the simulation
    """

    # natural units of Oqtant
    w = 2 * np.pi * 50  # weak axis trap frequency
    m = 87 * 1.66054e-27  # rb87 mass
    h = 6.626e-34  # planck's constant
    msec = 1e-3
    microns = 1e-6
    khz = 1e3
    hbar = h / 2 / np.pi  # hbar
    # natural units of the simulation (in SI) #CHECKED
    sim_time_unit = 1 / w  # 3.18 milliseconds = 1 simulation time
    sim_length_unit = np.sqrt(hbar / m / w)  # 1.52 microns = 1 simulation length
    sim_energy_unit = hbar * w
    # convert simulation units to Oqtant units # Checked
    sim_length_to_oqt = (
        sim_length_unit / microns
    )  # convert a simulation length to microns.  1.524 microns
    sim_time_to_oqt = (
        sim_time_unit / msec
    )  # convert a simulation time to microseconds.  3.183 mseconds
    oqt_time_to_sim = 1 / sim_time_to_oqt
    w0x = 1.0  # 50hz
    w0r = 8.0  # 400hz

    def __init__(self, quantum_matter):
        self.quantum_matter = quantum_matter
        self.tdm = ThreeDim()
        self.V = None

    # convert units of quantum matter object to simulation relevant quantities
    @property
    def lifetime(self):
        return (
            self.quantum_matter.lifetime * QMPotential.msec / QMPotential.sim_time_unit
        )

    @property
    def time_of_flight(self):
        return (
            self.quantum_matter.time_of_flight
            * QMPotential.msec
            / QMPotential.sim_time_unit
        )

    def update_potential(self, time):
        """
        times within barrier/landscape jobs are automatically converted to simulation units in update_potential
        updates self.V
        potential_1D_x needs only be called every 100 microseconds--potential speedup step.

        Args:
            time:  time (in simulation units)

        Returns:
            None
        """
        # time: sim -> msec # Checked
        time *= QMPotential.sim_time_unit / QMPotential.msec
        # potential in x-direction (in kHz)
        potential_1D_x = np.array(
            self.quantum_matter.get_potential(
                time,
                self.tdm.x_1d * QMPotential.sim_length_unit / QMPotential.microns,
            )
        )
        # potential in z-direction (in sim. units) # Checked
        potential_1D_x *= QMPotential.h * QMPotential.khz / QMPotential.sim_energy_unit
        # potential in r-direction (in sim. units) # Checked
        potential_1D_r = 0.5 * QMPotential.w0r**2 * self.tdm.r_1d**2
        # meshgrid in r and x directions (simulation units)
        pot_x, pot_r = np.meshgrid(potential_1D_x, potential_1D_r)
        # total potential: simulation units
        self.V = pot_x + pot_r
