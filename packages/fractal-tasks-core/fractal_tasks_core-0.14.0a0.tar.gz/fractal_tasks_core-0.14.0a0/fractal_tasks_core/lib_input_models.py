# Copyright 2022 (C) Friedrich Miescher Institute for Biomedical Research and
# University of Zurich
#
# Original authors:
# Tommaso Comparin <tommaso.comparin@exact-lab.it>
#
# This file is part of Fractal and was originally developed by eXact lab S.r.l.
# <exact-lab.it> under contract with Liberali Lab from the Friedrich Miescher
# Institute for Biomedical Research and Pelkmans Lab from the University of
# Zurich.
"""
Pydantic models for some task parameters.
"""
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import validator


class Channel(BaseModel):
    """
    A channel which is specified by either `wavelength_id` or `label`.

    Attributes:
        wavelength_id: Unique ID for the channel wavelength, e.g. `A01_C01`.
        label: Name of the channel.
    """

    wavelength_id: Optional[str] = None
    label: Optional[str] = None

    @validator("label", always=True)
    def mutually_exclusive_channel_attributes(cls, v, values):
        """
        Check that either `label` or `wavelength_id` is set.
        """
        wavelength_id = values.get("wavelength_id")
        label = v
        if wavelength_id and v:
            raise ValueError(
                "`wavelength_id` and `label` cannot be both set "
                f"(given {wavelength_id=} and {label=})."
            )
        if wavelength_id is None and v is None:
            raise ValueError(
                "`wavelength_id` and `label` cannot be both `None`"
            )
        return v


class NapariWorkflowsInput(BaseModel):
    """
    A value of the `input_specs` argument in `napari_workflows_wrapper`.

    Attributes:
        type: Input type (either `image` or `label`).
        label_name: Label name (for label inputs only).
        channel: Channel object (for image inputs only).
    """

    type: Literal["image", "label"]
    label_name: Optional[str]
    channel: Optional[Channel]

    @validator("label_name", always=True)
    def label_name_is_present(cls, v, values):
        """
        Check that label inputs have `label_name` set.
        """
        _type = values.get("type")
        if _type == "label" and not v:
            raise ValueError(
                f"Input item has type={_type} but label_name={v}."
            )
        return v

    @validator("channel", always=True)
    def channel_is_present(cls, v, values):
        """
        Check that image inputs have `channel` set.
        """
        _type = values.get("type")
        if _type == "image" and not v:
            raise ValueError(f"Input item has type={_type} but channel={v}.")
        return v


class NapariWorkflowsOutput(BaseModel):
    """
    A value of the `output_specs` argument in `napari_workflows_wrapper`.

    Attributes:
        type: Output type (either `label` or `dataframe`).
        label_name: Label name (for dataframe outputs, this attribute is used
            to fill the `region["path"]` field).
        table_name: Table name (for dataframe outputs only).
    """

    type: Literal["label", "dataframe"]
    label_name: str
    table_name: Optional[str] = None

    @validator("table_name", always=True)
    def table_name_only_for_dataframe_type(cls, v, values):
        """
        Check that table_name is set only for dataframe outputs.
        """
        _type = values.get("type")
        if (_type == "dataframe" and (not v)) or (_type != "dataframe" and v):
            raise ValueError(
                f"Output item has type={_type} but table_name={v}."
            )
        return v
