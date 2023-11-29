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

import math
from dataclasses import dataclass
from logging import getLogger

import matplotlib.pyplot as plt
import numpy as np
from bert_schemas.job import Image
from scipy import interpolate

from oqtant.simulator.qm_potential import QMPotential
from oqtant.simulator.three_dim import ThreeDim
from oqtant.simulator.wave_function import WaveFunction
from oqtant.util.exceptions import SimValueError

logger = getLogger(__name__)


@dataclass
class TimeSpan:
    start: float
    end: float


class Simulator:
    """
    'Simulator' Defines methods for evolution and plotting of the system
    """

    # 2000 timesteps per simulation unit time.
    # time_step = 1 #0.5e-3
    number_of_atoms = 1e5
    # this is specific to interactions between Rubidium - 87 atoms
    scattering_length = 0.00319
    interaction_strength = 4.0 * np.pi * number_of_atoms * scattering_length

    def __init__(self, wavefunction: WaveFunction, potential: QMPotential):
        self.tdm = ThreeDim()
        self.wavefunction = wavefunction
        self.potential = potential
        self.times: list | None = None
        self.psi_history = []  # None
        self.time_step = 0.5e-3
        self.sampling_rate = 100

    def set_ground_state(self):
        """
        This function evolves the condensate with ground = True.
        It is done at negative times before the barriers are switched on.
        2.5 simulation units of time is sufficient to settle down to the ground state.
        Potentially this could be stored as it's always the same unless the user wants to change number_of_atoms.
        """

        self.wavefunction.psi = self.wavefunction.initial_psi(
            sigma_r=1 / np.sqrt(self.potential.w0r)
        )

        self.run_RK4(TimeSpan(-2.5, -0.01), ground=True)

    def run_evolution(self) -> None:
        """
        This function evolves the condensate with ground = False.
        It is done at positive times while the barriers are switched on.
        It runs for the lifetime of the quantum_matter object
        It starts from the end result of running get_ground_state
        """
        # start from the end result of running get_ground_state
        self.wavefunction.psi = self.psi_history[-1]
        self.run_RK4(TimeSpan(0, self.potential.lifetime), ground=False)

    # Move this to a separate class of utility functions (separate module)

    def get_laplacian(self, y) -> np.ndarray:
        """
        Implementation of the second derivatives in x and r including forward, central, and backward formulas to second order accuracy
        """
        # dr, dx = self.wavefunction.dr, self.wavefunction.dx
        dr, dx = self.tdm.dr, self.tdm.dx

        # First derivative.
        dydr = np.gradient(y, axis=0, edge_order=2) / dr  # First derivative.
        dydr[0, :] = 0  # Enforce Neumann boundary condition

        #         # Central difference
        d2ydr2 = (np.roll(y, -1, axis=0) - 2 * y + np.roll(y, 1, axis=0)) / dr**2
        d2ydx2 = (np.roll(y, -1, axis=1) - 2 * y + np.roll(y, 1, axis=1)) / dx**2

        #         # Forward difference at start of array
        d2ydr2[0, :] = (2 * y[0, :] - 5 * y[1, :] + 4 * y[2, :] - y[3, :]) / dr**2
        d2ydx2[:, 0] = (2 * y[:, 0] - 5 * y[:, 1] + 4 * y[:, 2] - y[:, 3]) / dx**2

        #         # Backward difference at end of array
        d2ydr2[-1, :] = (
            -y[-4, :] + 4 * y[-3, :] - 5 * y[-2, :] + 2 * y[-1, :]
        ) / dr**2
        d2ydx2[:, -1] = (
            -y[:, -4] + 4 * y[:, -3] - 5 * y[:, -2] + 2 * y[:, -1]
        ) / dx**2

        return (
            (1.0 / self.tdm.r) * dydr + d2ydr2 + d2ydx2
        )  # Laplacian in cylindrical coordinates with axial symmetry

    def get_GPE(self, psi: np.ndarray) -> np.ndarray:
        """
        Implementation of the Gross-Pitaevskii Equation w/Neumann boundary conditions at r = 0 and Dirichlet at large x and r.
        """
        # Enforce Neumann boundary condition
        psi[1, :] = psi[0, :]

        laplacian = self.get_laplacian(psi)

        return (0.5 * 1j) * laplacian - 1j * (
            self.potential.V + self.interaction_strength * np.abs(psi) ** 2
        ) * psi

    def run_RK4(self, time_span: TimeSpan, ground=False, TOF=False) -> None:
        """
        Implementation of the Runge-Kutta 4th order method to evolve in time.

        Args:
            time_span:  a list of times (in milliseconds)
            ground: allows simulation of ground state and evolves in imaginary time
            TOF:  whether or not to switches off potentials and rescale the grids
        Returns:
            None
        """
        n = int(
            (time_span.end - time_span.start) / self.time_step
        )  # number of subintervals to evaluate rk4 on.
        t = np.linspace(
            time_span.start, time_span.end, n + 1
        )  # list of all time subintervals
        self.times = []  # stored internally in an array
        self.psi_history = []  # reset history each time rk4 is called

        f = np.zeros(
            (self.tdm.Nr, self.tdm.Nx),
            dtype=complex,
        )  # stored wave function at each time

        # Set the initial wave function
        f = self.wavefunction.psi

        dt = self.time_step

        # if ground = True, we evolve in imaginary time
        if ground:
            dt = -dt * 1j

        oqt_times_us = t * QMPotential.sim_time_to_oqt / QMPotential.msec

        for i in range(n):
            if i == 0:
                oqt_times_us[i]
                self.potential.update_potential(t[i])

            elif oqt_times_us[i] % 100 < oqt_times_us[i - 1] % 100 and ground is False:
                self.potential.update_potential(t[i])

            psi = self.wavefunction.psi

            f1 = self.get_GPE(psi)
            f2 = self.get_GPE(psi + f1 * dt / 2)
            f3 = self.get_GPE(psi + f2 * dt / 2)
            f4 = self.get_GPE(psi + f3 * dt)

            f = f + dt * (f1 + 2.0 * f2 + 2.0 * f3 + f4) / 6.0

            # Dirichlet boundary conditions at asymptotes of simulation
            f[-1, :] = 0
            f[:, 0] = 0
            f[:, -1] = 0

            # Enforce Neumann boundary condition
            f[1, :] = f[0, :]

            self.wavefunction.psi = f

            if TOF:  # interpolate wave function between expanding grids
                self.TOF_mode(i, interp_psi=True)
                f = self.wavefunction.psi

            if ground:  # renormalize wave function due to imaginary time decay
                self.wavefunction.psi = self.wavefunction.normalize(
                    self.wavefunction.psi
                )
                f = self.wavefunction.psi

            if i % self.sampling_rate == 0:
                logger.info("sample", t[i])
                self.psi_history.append(f)
                self.times.append(t[i])

        logger.info("psi_history", np.shape(self.psi_history))

    @property
    def it_plot(self) -> Image:
        """
        Generate an simulation analog to an in-trap image from the Oqtant hardware.

        Args:

        Returns:
        - it_image_pixels (list): pixels of the simulation generated IT image
        - columns (int): number of cols in simulation generated IT images
        - rows (int): number of rows in simulation generated IT images
        - pixcal (float): size of a pixel in simulation generated IT images
        """

        # get the Z-integrated column denisty from wavefunction
        _, density_img, _ = self.wavefunction.column_densities
        density_pixels = density_img.flatten() * self.tdm.dx * self.tdm.dz

        # get conversion from simulation length to um
        pixcal = QMPotential.sim_length_to_oqt

        A_pixel_area = (pixcal) ** 2  # um2

        # absorption cross section
        sigma = 2.907e-1  # um2

        it_exp_pixcal = 0.344  # um

        # convert density (atoms/length^2) to OD using the sim grid size and cross section
        OD_pixels = density_pixels * sigma * self.number_of_atoms / A_pixel_area

        # half the length of the simulation grid axes, in um
        Lx_half = (self.tdm.Lx / 2) * pixcal
        Ly_half = self.tdm.Lr * pixcal

        # grids for building simulation interpolation function (um)
        sim_grid_col = np.linspace(-Lx_half, Lx_half, self.tdm.Nx)
        sim_grid_row = np.linspace(-Ly_half, Ly_half, self.tdm.Nr * 2)

        # build interpolation function for sim data
        f = interpolate.RegularGridInterpolator(
            (sim_grid_row, sim_grid_col),
            OD_pixels.reshape((self.tdm.Nr * 2, self.tdm.Nx)),
        )

        # grids for sampling simulation in experiment resolution (um)
        exp_grid_col = np.arange(-Lx_half, Lx_half, it_exp_pixcal)
        exp_grid_row = np.arange(-Ly_half, Ly_half, it_exp_pixcal)

        exp_meshgrid_row, exp_meshgrid_col = np.meshgrid(exp_grid_row, exp_grid_col)

        points = np.array([exp_meshgrid_row.flatten(), exp_meshgrid_col.flatten()]).T

        # sample the interpolation function and reshape the output
        interpolated_sim = f(points).reshape(len(exp_grid_col), len(exp_grid_row))

        # how many pixels to pad the image?
        add_zeros_rows = math.ceil((148 - len(exp_grid_row)) / 2)
        add_zeros_cols = math.ceil((512 - len(exp_grid_col)) / 2)

        # pad the image to match IT_PLOT size
        padded_interp_sim = np.pad(
            interpolated_sim,
            [
                [add_zeros_cols, 512 - len(exp_grid_col) - add_zeros_cols],
                [add_zeros_rows, 148 - len(exp_grid_row) - add_zeros_rows],
            ],
        ).T

        # prepare values to be returned
        columns = len(padded_interp_sim[0])
        rows = len(padded_interp_sim)
        pixels_pad_interp_sim = list(padded_interp_sim.flatten())

        return Image(
            pixels=pixels_pad_interp_sim,
            rows=rows,
            columns=columns,
            pixcal=it_exp_pixcal,
        )

    def show_final_result(self) -> None:
        """
        Plot the density at the end of the simulation in cylindrical coordinates.
        Useful coordinates for diagonising issues but not to be returned to the user.
        """
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        density = self.wavefunction.density
        ax.plot_surface(
            self.potential.sim_length_to_oqt * self.tdm.r,
            self.potential.sim_length_to_oqt * self.tdm.x,
            density,
            cmap="viridis",
        )
        ax.set_xlabel("$R$-Position (microns)")
        ax.set_ylabel("$X$-Position (microns)")

    # @staticmethod
    def convert_timesteps(self, timesteps: list) -> np.ndarray:
        if self.times is None:
            raise SimValueError("times not set")

        np_timesteps = np.array(timesteps, dtype=float)
        # convert input time in msec to simulation units
        np_timesteps *= QMPotential.oqt_time_to_sim

        if (
            np.max(np_timesteps) >= self.times[-1]
            or np.min(np_timesteps) <= self.times[0]
        ):
            raise SimValueError("timesteps outside of job window")

        if np.min(np_timesteps) < 0:
            raise SimValueError("timesteps must be positive")

        return np_timesteps

    def show_density_cylindrical(self, timesteps: list, TOF=False) -> None:
        """
        Plots the density profile of the condensate in cylindrical coordinates
        for an input array of times.
        Useful coordinates for diagonising issues but not to be returned to the user.

        Args:
            timesteps:  a list of times (in milliseconds)
            TOF:  whether or not to switch off potentials and rescale the grids
        Returns:
            None
        """

        converted_timesteps = self.convert_timesteps(timesteps)

        # convert to simulation indices for the nearest timestep, loop over timesteps
        for time in converted_timesteps:
            i = int(time / (self.time_step * self.sampling_rate))

            # if TOF:  # rescale grids in TOF mode.
            #     self.TOF_mode(i)

            self.potential.update_potential(self.times[i])

            fig = plt.figure(figsize=(15, 7))

            ax1 = fig.add_subplot(
                111
            )  # Add first subplot in a plot with two rows and 2 columns.
            self.wavefunction.psi = self.psi_history[i]
            density = self.wavefunction.density
            img1 = ax1.imshow(
                np.concatenate(
                    (np.flip(density, axis=0), density)
                ),  # mirror the condensate over the z-axis
                extent=[
                    self.tdm.x[0, 0] * self.potential.sim_length_to_oqt,
                    self.tdm.x[0, -1] * self.potential.sim_length_to_oqt,
                    -self.tdm.r[-1, 0] * self.potential.sim_length_to_oqt,
                    self.tdm.r[-1, 0] * self.potential.sim_length_to_oqt,
                ],
                aspect="auto",
                cmap="viridis",
            )
            plt.title(f"Density at time {time / self.potential.oqt_time_to_sim} msec")
            ax1.set_xlabel("$X$-Position (microns)")
            ax1.set_ylabel("$R$-Position (microns)")
            ax1.contour(
                self.tdm.x,
                self.tdm.r,
                self.potential.V,
                colors="white",
            )
            ax1.contour(
                self.tdm.x,
                -self.tdm.r,
                self.potential.V,
                colors="white",
            )
            fig.colorbar(img1, ax=ax1, orientation="vertical")

    def show_column_densities(self, timesteps, TOF=False):
        """
        Plots the column densities and slices of the condensate in cartesian coordinates
        for an input array of times.
        In correct coordinates to be returned to the user.

        Args:
            timesteps:  a list of times (in milliseconds)
            TOF:  whether or not to rescale the grids in TOF mode

        Returns:
            None
        """
        converted_timesteps = self.convert_timesteps(timesteps)

        for time in converted_timesteps:
            i = int(time / (self.time_step * self.sampling_rate))

            # if TOF:  # rescale grids in TOF mode.
            #     self.TOF_mode(i)

            self.potential.update_potential(
                self.times[i]
            )  # update potential to plotted time

            self.wavefunction.psi = self.psi_history[i]  # load a snapshot of psi
            # load the column densities
            (
                column_zy,
                column_zx,
                profiles,
            ) = self.wavefunction.column_densities
            slice_x_2 = column_zx[int(self.tdm.Nr - 1), :]
            slice_z = column_zy[int(self.tdm.Nr - 1), :]
            slice_z_zy, slice_z_zx, slice_x = profiles

            fig = plt.figure(figsize=(15, 7))

            # column densities
            ax1 = fig.add_subplot(
                221
            )  # Add first subplot in a plot with two rows and 2 columns.
            im1 = ax1.imshow(
                column_zy,
                extent=[
                    -self.tdm.Lr * self.potential.sim_length_to_oqt,
                    self.tdm.Lr * self.potential.sim_length_to_oqt,
                    -self.tdm.Lr * self.potential.sim_length_to_oqt,
                    self.tdm.Lr * self.potential.sim_length_to_oqt,
                ],
                aspect="auto",
                cmap="viridis",
            )
            plt.title(
                f"Column densities at time {time / self.potential.oqt_time_to_sim} msec"
            )
            plt.xlabel("$Y$-Position (microns)")
            plt.ylabel("$Z$-Position (microns)")
            fig.colorbar(im1, ax=ax1, orientation="vertical")

            ax2 = fig.add_subplot(222)
            im2 = ax2.imshow(
                column_zx,
                extent=[
                    -self.potential.sim_length_to_oqt * self.tdm.Lx / 2,
                    self.potential.sim_length_to_oqt * self.tdm.Lx / 2,
                    -self.potential.sim_length_to_oqt * self.tdm.Lr,
                    self.potential.sim_length_to_oqt * self.tdm.Lr,
                ],
                aspect="auto",
                cmap="viridis",
            )
            plt.xlabel("$X$-Position (microns)")
            plt.ylabel("$Z$-Position (microns)")
            fig.colorbar(im2, ax=ax2, orientation="vertical")

            # slices
            ax3 = fig.add_subplot(223)
            ax3.plot(self.tdm.z[0, :] * self.potential.sim_length_to_oqt, slice_z)
            ax3.set_title(
                f"Slices at time {time / self.potential.oqt_time_to_sim} msec"
            )
            ax3.set_xlabel("$Z$-Position (microns)")

            #           #######TBD ADD show_potential output here!
            ax4 = fig.add_subplot(224)
            ax4.plot(self.tdm.x[0, :] * self.potential.sim_length_to_oqt, slice_x_2)
            ax4.set_xlabel("$X$-Position (microns)")

            plt.tight_layout()
            plt.show()

    def show_phase(self, timesteps, TOF=False) -> None:
        """
        Plot the phase for a given list of timesteps
        This can only be displayed in cylindrical coordinates.
        It is a helpful tool still for the user.  The aspect ratio is still a bit weird.

        Args:
            timesteps (list): List of times to display
            TOF (bool): True to rescale grids in TOF mode.
        Returns:
            None
        """
        converted_timesteps = self.convert_timesteps(timesteps)

        for time in converted_timesteps:
            # convert to simulation indices for the nearest timestep, loop over timesteps
            i = int(time / (self.time_step * self.sampling_rate))

            # if TOF:  # rescale grids in TOF mode.
            #     self.TOF_mode(i)

            self.potential.update_potential(self.times[i])

            self.wavefunction.psi = self.psi_history[i]

            plt.figure(figsize=(10, 7))
            plt.imshow(
                self.wavefunction.phase,
                extent=[
                    self.tdm.x[0, 0] * self.potential.sim_length_to_oqt,
                    self.tdm.x[0, -1] * self.potential.sim_length_to_oqt,
                    0,
                    self.tdm.r[-1, 0] * self.potential.sim_length_to_oqt,
                ],
                aspect="auto",
            )
            plt.colorbar(label="Phase")
            plt.clim(-np.pi, np.pi)
            plt.title(f"Phase at time {time / self.potential.oqt_time_to_sim} msec")
            plt.xlabel("$X$-Position (microns)")
            plt.ylabel("$R$-Position (microns)")
            plt.show()

    def show_current(self, timesteps, TOF=False):
        """
        Plot the flow for a given list of timesteps
        two separate sub plots

        Args:
            timesteps (list): List of times to display
            TOF (bool): True to rescale grids in TOF mode.

        Returns:
            None
        """
        converted_timesteps = self.convert_timesteps(timesteps)

        for time in converted_timesteps:
            i = int(time / (self.time_step * self.sampling_rate))

            # if TOF:  # rescale grids in TOF mode.
            #     self.TOF_mode(i)

            self.potential.update_potential(self.times[i])

            self.wavefunction.psi = self.psi_history[i]

            plt.figure(1)
            plt.plot(
                self.tdm.x_1d * self.potential.sim_length_to_oqt,
                self.number_of_atoms
                * self.wavefunction.current
                / self.potential.sim_time_to_oqt,
            )
            plt.title(f"Current at time {time / self.potential.oqt_time_to_sim} msec")
            plt.xlabel("$X$-Position (microns)")
            plt.ylabel("Atom Current (# of Atoms / msec)")
            plt.show()


#    # TBD Include flow_r in plot also.
#    def animate_flow(self, frame_interval=50):
#        """
#        Animate the change in flow
#        int frame_interval: number of frames to skip each interval, determines smoothness
#        """
#        fig, ax = plt.subplots()
#        flow_r, flow_z = self.wavefunction.flow
#        density = self.wavefunction.density
#        extent = extent = [
#            self.wavefunction.z[0, 0],
#            self.wavefunction.z[0, -1],
#            -self.wavefunction.r[-1, 0],
#            self.wavefunction.r[-1, 0],
#        ]
#        im = ax.imshow(
#            np.concatenate((np.flip(flow_z * density, axis=0), flow_z * density)),
#            aspect="auto",
#            extent=extent,
#            cmap="seismic",
#        )

#        cont1 = ax.contour(
#            self.wavefunction.z,
#            self.wavefunction.r,
#            self.potential.harmonicPotential(),
#            colors="white",
#        )
#        cont2 = ax.contour(
#            self.wavefunction.z,
#            -self.wavefunction.r,
#            self.potential.harmonicPotential(),
#            colors="white",
#        )
#        levels = [self.potential.barrier_height / 2]
#        cont3 = ax.contour(
#            self.wavefunction.z,
#            self.wavefunction.r,
#            self.potential.painted_barrier(),
#            levels,
#            colors="red",
#        )
#        cont4 = ax.contour(
#            self.wavefunction.z,
#            -self.wavefunction.r,
#            self.potential.painted_barrier(),
#            levels,
#            colors="red",
#        )
#        plt.colorbar(im, ax=ax, label="current - z")
#        im.set_clim(-1, 1)

#        def update(frame):
#            nonlocal cont1, cont2, cont3, cont4
#            self.potential.adjust_potential(self.times[frame])
#            self.wavefunction.psi = self.psi_history[frame]
#            density = self.wavefunction.density
#            flow_r, flow_z = self.wavefunction.flow
#            im.set_array(
#                np.concatenate((np.flip(flow_z * density, axis=0), flow_z * density))
#            )
#            for c in cont1.collections:
#                c.remove()
#            for c in cont2.collections:
#                c.remove()
#            for c in cont3.collections:
#                c.remove()
#            for c in cont4.collections:
#                c.remove()
#            cont1 = ax.contour(
#                self.wavefunction.z,
#                self.wavefunction.r,
#                self.potential.harmonicPotential(),
#                colors="white",
#            )
#            cont2 = ax.contour(
#                self.wavefunction.z,
#                -self.wavefunction.r,
#                self.potential.harmonicPotential(),
#                colors="white",
#            )
#            levels = [self.potential.barrier_height / 2]
#            cont3 = ax.contour(
#                self.wavefunction.z,
#                self.wavefunction.r,
#                self.potential.painted_barrier(),
#                levels,
#                colors="red",
#            )
#            cont4 = ax.contour(
#                self.wavefunction.z,
#                -self.wavefunction.r,
#                self.potential.painted_barrier(),
#                levels,
#                colors="red",
#            )
#            #
#            return im, cont1, cont2, cont3, cont4

#        anim = FuncAnimation(
#            fig,
#            update,
#            frames=range(0, len(self.psi_history), frame_interval),
#            interval=50,
#            blit=False,
#        )

#        return anim

# This function is specific to doing time-of-flight.  We will implement after getting in-trap to work.  The coordinates need to be updated.
#    def TOF_mode(self, time, interp_psi=False):
#        """
#        Switches off the confining potential and the barriers.
#        Scales the grids and grid spacings in time as the gas is released from the trap.
#        Interpolates the wave function onto the rescaled grids at each time step.
#        time:  expansion time
#        interp_psi:  if 'True', the wave function is interpolated between grids.
#        set to 'False' to dilate just grids for plotting purposes.
#        """
#        # timestamp
#        t = self.times[time]

#        # confining potentials and barriers are switched off.
#        self.potential.w0z, self.potential.w0r, self.potential.barrier_height = [
#            0,
#            0,
#            0,
#        ]

#        # a fixed dilation factor.   #####CHANGE THIS FOR CIGAR IN LONG DIRECTION!
#        if self.interaction_strength == 0:
#            vz, vr = [
#                2 * np.sqrt(2 * self.w0z),
#                np.sqrt(2 * self.w0r),
#            ]  # ideal condensate expansion rates
#        else:
#            vz, vr = [
#                2 * self.R_tf_x * self.w0z,
#                self.R_tf_y * self.w0r,
#            ]  # TF expansion rates
#            # vx, vy = [8, 2 * self.R_tf_y * self.w0y] # ideal in x, TF in y

#        # rescale grid lengths linearly
#        self.potential.Lz = self.Lz + t * vz  # grid lengths expand at rates vx, vy
#        self.potential.Lr = self.Lr + t * vr

#        # dilate grids
#        self.potential.z = self.z * (self.potential.Lz / self.Lz)
#        self.potential.r = self.r * (self.potential.Lr / self.Lr)

#        # rescale grid-spacings
#        self.potential.dz = self.potential.z[0, 1] - self.potential.z[0, 0]
#        self.potential.dr = self.potential.r[1, 0] - self.potential.r[0, 0]

#        # interpolating function for the real and imaginary parts of the wave function.  Keep at least cubic order in the interpolator.
#        if interp_psi:
#            ip_real = RectBivariateSpline(
#                self.wavefunction.r[:, 0],
#                self.wavefunction.z[0, :],
#                np.real(self.wavefunction.psi),
#                kx=3,
#                ky=3,
#            )  # cubic spline interpolation
#            ip_imag = RectBivariateSpline(
#                self.wavefunction.r[:, 0],
#                self.wavefunction.z[0, :],
#                np.imag(self.wavefunction.psi),
#                kx=3,
#                ky=3,
#            )  # cubic spline interpolation

#        # dilate wave function class grids
#        self.wavefunction.r, self.wavefunction.z = self.potential.r, self.potential.z
#        self.wavefunction.Lr, self.wavefunction.Lz = (
#            self.potential.Lr,
#            self.potential.Lz,
#        )
#        self.wavefunction.dr, self.wavefunction.dz = (
#            self.potential.dr,
#            self.potential.dz,
#        )

#        # wave function interpolated onto dilated grids
#        if interp_psi:
#            self.wavefunction.psi = ip_real(
#                self.wavefunction.r[:, 0], self.wavefunction.z[0, :]
#            ) + 1j * ip_imag(self.wavefunction.r[:, 0], self.wavefunction.z[0, :])

#    def animate_phase(self, frame_interval=15):
#        """
#        Animate the change in phase
#        int frame_interval: number of frames to skip each interval, determines smoothness
#        """
#        fig, ax = plt.subplots()
#        phase = self.wavefunction.phase

#        extent = [
#            self.wavefunction.z[0, 0],
#            self.wavefunction.z[0, -1],
#            -self.wavefunction.r[-1, 0],
#            self.wavefunction.r[-1, 0],
#        ]
#        im = ax.imshow(
#            np.concatenate((np.flip(phase, axis=0), phase)),
#            extent=extent,
#            vmin=-np.pi,
#            vmax=np.pi,
#            cmap="nipy_spectral",
#        )

#        cont1 = ax.contour(
#            self.wavefunction.z,
#            self.wavefunction.r,
#            self.potential.harmonicPotential(),
#            colors="white",
#        )
#        cont2 = ax.contour(
#            self.wavefunction.z,
#            -self.wavefunction.r,
#            self.potential.harmonicPotential(),
#            colors="white",
#        )
#        levels = [self.potential.barrier_height / 2]
#        cont3 = ax.contour(
#            self.wavefunction.z,
#            self.wavefunction.r,
#            self.potential.painted_barrier(),
#            levels,
#            colors="red",
#        )
#        cont4 = ax.contour(
#            self.wavefunction.z,
#            -self.wavefunction.r,
#            self.potential.painted_barrier(),
#            levels,
#            colors="red",
#        )
#        plt.colorbar(im, ax=ax, label="phase")

#        def update(frame):
#            nonlocal cont1, cont2, cont3, cont4
#            self.potential.adjust_potential(self.times[frame])
#            self.wavefunction.psi = self.psi_history[frame]
#            phase = self.wavefunction.phase()
#            im.set_array(np.concatenate((np.flip(phase, axis=0), phase)))
#            for c in cont1.collections:
#                c.remove()
#            for c in cont2.collections:
#                c.remove()
#            for c in cont3.collections:
#                c.remove()
#            for c in cont4.collections:
#                c.remove()
#            cont1 = ax.contour(
#                self.wavefunction.z,
#                self.wavefunction.r,
#                self.potential.harmonicPotential(),
#                colors="white",
#            )
#            cont2 = ax.contour(
#                self.wavefunction.z,
#                -self.wavefunction.r,
#                self.potential.harmonicPotential(),
#                colors="white",
#            )
#            levels = [self.potential.barrier_height / 2]
#            cont3 = ax.contour(
#                self.wavefunction.z,
#                self.wavefunction.r,
#                self.potential.painted_barrier(),
#                levels,
#                colors="red",
#            )
#            cont4 = ax.contour(
#                self.wavefunction.z,
#                -self.wavefunction.r,
#                self.potential.painted_barrier(),
#                levels,
#                colors="red",
#            )
#            #
#            return im, cont1, cont2, cont3, cont4

#        anim = FuncAnimation(
#            fig,
#            update,
#            frames=range(0, len(self.psi_history), frame_interval),
#            interval=50,
#            blit=False,
#        )

#        return anim

# A useful function for when we do time-of-flight, but not needed now.
#
#    # Evolution of the widths and COM of the condensate
#    def plot_widths(self, TOF=False, COM=False):
#        """
#        Plots the change in the condensate width over time.  Comparison is made against the width of
#        a non-interacting BEC.  If TOF = True, we compare against the expansion of a non-interacting and TF BEC.
#        """

#        width_z = np.zeros(len(self.psi_history))
#        width_r = np.zeros_like(width_z)
#        width_z_ideal = np.zeros_like(width_z)
#        width_r_ideal = np.zeros_like(width_z)
#        R_z_TF = np.zeros_like(width_z)
#        R_r_TF = np.zeros_like(width_z)
#        com_z = np.zeros_like(width_z)

#        for i in range(0, len(self.psi_history)):
#            self.wavefunction.psi = self.psi_history[i]
#            if TOF:  # rescale grids in TOF mode.
#                self.TOF_mode(i)
#                scale_r = np.sqrt(1 + self.w0r**2 * self.times[i] ** 2)
#                scale_z = np.sqrt(1 + self.w0z**2 * self.times[i] ** 2)
#                width_r_ideal[i] = (
#                    self.width_r_ideal * scale_r
#                )  # non-interacting widths
#                width_z_ideal[i] = self.width_z_ideal * scale_z
#                R_r_TF[i] = self.R_tf_r * scale_r
#                R_z_TF[i] = self.R_tf_z * scale_z

#            else:
#                width_z_ideal[i], width_r_ideal[i] = (
#                    self.width_z_ideal,
#                    self.width_r_ideal,
#                )
#                R_z_TF[i], R_r_TF[i] = self.R_tf_z, self.R_tf_r

#            width_z[i], width_r[i] = self.wavefunction.widths()
#            com_z[i] = self.wavefunction.com_position()

#        TF_z_to_width = np.sqrt(
#            1 / 7
#        )  # Conversion between thomas fermi radii and widths
#        TF_r_to_width = np.sqrt(2 / 7)

#        # plot evolution of widths against analytic comparisons
#        plt.figure(1)
#        plt.plot(self.times, width_z, color="red", ls="-", label="width_z")
#        plt.plot(self.times, width_r, color="blue", linestyle="-", label="width_r")
#        plt.plot(self.times, width_z_ideal, color="red", ls="--", label="width_z_ideal")
#        plt.plot(self.times, width_r_ideal, color="blue", ls="--", label="width_r_ideal")
#        plt.plot(
#            self.times, R_z_TF * TF_z_to_width, color="red", ls=":", label="width_z_TF"
#        )
#        plt.plot(
#            self.times, R_r_TF * TF_r_to_width, color="blue", ls=":", label="width_r_TF"
#        )
#        plt.xlabel("time (oscillator units)")
#        plt.ylabel("widths (oscillator units)")
#        plt.legend()

#        if COM:
#            # plot com in the z-direction
#            plt.figure(2)
#            plt.plot(self.times, com_z, label="com - z")
#            plt.xlabel("time (oscillator units)")
#            plt.ylabel("widths (oscillator units)")
#            plt.legend()

# Animations will come after we get the basics working...
#
#    def animate_density(self, frame_interval=50, rlim=None, zlim=None):
#        """
#        Animates the change in density and potential over time
#        int frame_interval: number of frames to skip each interval, determines smoothness
#        xlim and ylim allow you to zoom in the X or Y directions
#        Returns an animation
#        """
#        fig, ax = plt.subplots()
#        density = self.wavefunction.density()

#        extent = [
#            self.wavefunction.z[0, 0],
#            self.wavefunction.z[0, -1],
#            -self.wavefunction.r[-1, 0],
#            self.wavefunction.r[-1, 0],
#        ]
#        if zlim is not None:
#            extent[0], extent[1] = zlim
#        if rlim is not None:
#            extent[2], extent[3] = rlim

#        # vmin and vmax normalize the colorbar, making the cloud more visible
#        im = ax.imshow(
#            np.concatenate((np.flip(density, axis=0), density)),
#            extent=extent,
#            cmap="nipy_spectral",
#        )  # normalize in here with vmin and vmax
#        cont1 = ax.contour(
#            self.wavefunction.z,
#            self.wavefunction.r,
#            self.potential.harmonicPotential(),
#            colors="white",
#        )
#        cont2 = ax.contour(
#            self.wavefunction.z,
#            -self.wavefunction.r,
#            self.potential.harmonicPotential(),
#            colors="white",
#        )
#        levels = [self.potential.barrier_height / 2]
#        cont3 = ax.contour(
#            self.wavefunction.z,
#            self.wavefunction.r,
#            self.potential.painted_barrier(),
#            levels,
#            colors="red",
#        )
#        cont4 = ax.contour(
#            self.wavefunction.z,
#            -self.wavefunction.r,
#            self.potential.painted_barrier(),
#            levels,
#            colors="red",
#        )
#        plt.colorbar(im, ax=ax, label="density")
#        # cb.remove()
#        # plt.tick_params(left = False, right = False , labelleft = False ,
#        #        labelbottom = False, bottom = False)

#        if zlim is not None:
#            ax.set_ylim(zlim)
#        if rlim is not None:
#            ax.set_xlim(rlim)

#        def update(frame):
#            nonlocal cont1, cont2, cont3, cont4
#            self.potential.adjust_potential(self.times[frame])
#            self.wavefunction.psi = self.psi_history[frame]
#            density = self.wavefunction.density()
#            im.set_array(np.concatenate((np.flip(density, axis=0), density)))
#            for c in cont1.collections:
#                c.remove()
#            for c in cont2.collections:
#                c.remove()
#            for c in cont3.collections:
#                c.remove()
#            for c in cont4.collections:
#                c.remove()
#            cont1 = ax.contour(
#                self.wavefunction.z,
#                self.wavefunction.r,
#                self.potential.harmonicPotential(),
#                colors="white",
#            )
#            cont2 = ax.contour(
#                self.wavefunction.z,
#                -self.wavefunction.r,
#                self.potential.harmonicPotential(),
#                colors="white",
#            )
#            levels = [self.potential.barrier_height / 2]
#            cont3 = ax.contour(
#                self.wavefunction.z,
#                self.wavefunction.r,
#                self.potential.painted_barrier(),
#                levels,
#                colors="red",
#            )
#            cont4 = ax.contour(
#                self.wavefunction.z,
#                -self.wavefunction.r,
#                self.potential.painted_barrier(),
#                levels,
#                colors="red",
#            )
#            #
#            return im, cont1, cont2, cont3, cont4

#        anim = FuncAnimation(
#            fig,
#            update,
#            frames=range(0, len(self.psi_history), frame_interval),
#            interval=50,
#            blit=False,
#        )

#        return anim

#    def animate_profiles(self, frame_interval=50):
#        """
#        Animates the density profiles and change in potentials over time
#        int frame_interval: number of frames to skip each interval, determines smoothness
#        xlim and ylim allow you to zoom in the X or Y directions
#        Returns an animation
#        """
#        fig, (ax1, ax2) = plt.subplots(2, 1)

#        (line1,) = ax1.plot([], [], lw=2, color="b", label="Density Profile - z")
#        (line2,) = ax2.plot([], [], lw=2, color="b", label="Density Profile - r")
#        vl1 = ax1.axvline(color="r")
#        vl2 = ax1.axvline(color="r")
#        line = [line1, line2]

#        ax1.set_ylim(0, 0.5)
#        ax1.set_xlim(-self.wavefunction.Lz / 2, self.wavefunction.Lz / 2)
#        ax2.set_ylim(0, 10)
#        ax2.set_xlim(0, self.wavefunction.Lr)
#        ax1.grid()
#        ax2.grid()
#        ax1.legend()
#        ax1.set_xlabel("z")
#        ax1.set_ylabel("Density Profile - z")
#        ax2.legend()
#        ax2.set_xlabel("r")
#        ax2.set_ylabel("Density Profile - r")

#        def init():
#            line[0].set_data([], [])
#            line[1].set_data([], [])
#            return line

#        def update(frame):
#            self.potential.adjust_potential(self.times[frame])
#            barrier_right = (
#                self.potential.barrier_position + 2.355 * self.potential.barrier_width
#            )  # FWHM
#            barrier_left = (
#                self.potential.barrier_position - 2.355 * self.potential.barrier_width
#            )
#            self.wavefunction.psi = self.psi_history[frame]
#            x1 = self.wavefunction.z[0]
#            x2 = self.wavefunction.r[:, 0]
#            y1, y2 = self.wavefunction.density_profiles
#            line[0].set_data(x1, y1)
#            line[1].set_data(x2, y2)
#            vl1.set_xdata([barrier_right])
#            vl2.set_xdata([barrier_left])
#            return (line,)

#        anim = FuncAnimation(
#            fig,
#            update,
#            init_func=init,
#            frames=range(0, len(self.psi_history), frame_interval),
#            interval=50,
#            blit=False,
#        )

#        return anim
