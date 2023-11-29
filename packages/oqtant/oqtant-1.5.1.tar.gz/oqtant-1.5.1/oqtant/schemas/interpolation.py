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

from bert_schemas import job as job_schema
from scipy.interpolate import interp1d


def interpolation_to_kind(interpolation: job_schema.InterpolationType) -> str:
    """Method to convert our InterpolationType to something scipy can understand

    Args:
        interpolation (bert_schemas.job.InterpolationType): Primitive job interpolation type

    Returns:
        str: A "kind" string to be used by scipy's interp1d
    """
    interpolation_map = {"OFF": "zero", "STEP": "previous", "SMOOTH": "cubic"}

    return interpolation_map.get(interpolation, interpolation.lower())


def interpolate_1d(
    xs: list[float],
    ys: list[float],
    x: float,
    interpolation: job_schema.InterpolationType = "LINEAR",
) -> float:
    """Method to interpolate a 1D list of pairs [xs, ys] at the evaluation point x

    Args:
        xs (list[float]): List of x values
        ys (list[float]): List of y values
        x (float): Desired x-coordinate to evaluate the resulting interpolation function
        interpolation (job_schema.InterpolationType, optional): Interpolation style

    Returns:
        float: Interpolation function value at the specified x-coordinate
    """
    f = interp1d(
        xs,
        ys,
        kind=interpolation_to_kind(interpolation),
        bounds_error=False,
        fill_value=(0.0, 0.0),
    )
    return f(x)[()]  # extract value


def interpolate_1d_list(
    xs: list[float],
    ys: list[float],
    x_values: list[float],
    interpolation: job_schema.InterpolationType = "LINEAR",
) -> list[float]:
    """Method to interpolate a 1d list of pairs [xs, ys] at the evaluation points given by x_values

    Args:
        xs (list[float]): List of x values
        ys (list[float]): List of y values
        x_values (list[float]): Desired x-coordinates to evaluate the resulting interpolation function
        interpolation (job_schema.InterpolationType, optional): Interpolation style

    Returns:
        list[float]: Floating point values corresponding to evaluation of the interpolation function
            value at the specified x_values
    """
    f = interp1d(
        xs,
        ys,
        kind=interpolation_to_kind(interpolation),
        bounds_error=False,
        fill_value=(0.0, 0.0),
    )
    return list(f(x_values))
