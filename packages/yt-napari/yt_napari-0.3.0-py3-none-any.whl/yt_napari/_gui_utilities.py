from collections import defaultdict
from typing import Callable, List, Optional, Union

import pydantic
from magicgui import type_map, widgets

from yt_napari import _data_model
from yt_napari.logging import ytnapari_log


def set_default(variable, default):
    if variable is None:
        return default
    return variable


# the following class builds a registry framework for converting from pydantic
# field to a magicgui widget and back. This is useful for modifying the type
# of widgets used for specific pydantic model fields without over-riding the
# default widget selection of magicgui.
class MagicPydanticRegistry:
    def __init__(self):
        self.registry = defaultdict(dict)

    def register(
        self,
        pydantic_model: Union[pydantic.BaseModel, pydantic.main.ModelMetaclass],
        field: str,
        magicgui_factory: Callable = None,
        magicgui_args: Optional[tuple] = None,
        magicgui_kwargs: Optional[dict] = None,
        pydantic_attr_factory: Callable = None,
        pydantic_attr_args: Optional[tuple] = None,
        pydantic_attr_kwargs: Optional[dict] = None,
    ):
        """

        Parameters
        ----------
        pydantic_model :
            the pydantic model to register
        field :
            the attribute from the pydantic model to register
        magicgui_factory :
            a callable function that must return a magicgui widget
        magicgui_args :
            a tuple containing arguments to magicgui_factory
        magicgui_kwargs :
            a dict containing keyword arguments to magicgui_factory
        pydantic_attr_factory :
            a function that takes a magicgui widget instance and returns the
            arguments for a pydantic attribute
        pydantic_attr_args :
            a tuple containing arguments to pydantic_attr_factory
        pydantic_attr_kwargs :
            a dict containing keyword arguments to pydantic_attr_factory
        """
        magicgui_args = set_default(magicgui_args, ())
        magicgui_kwargs = set_default(magicgui_kwargs, {})
        pydantic_attr_args = set_default(pydantic_attr_args, ())
        pydantic_attr_kwargs = set_default(pydantic_attr_kwargs, {})

        self.registry[pydantic_model][field] = {}
        new_entry = {
            "magicgui": (magicgui_factory, magicgui_args, magicgui_kwargs),
            "pydantic": (
                pydantic_attr_factory,
                pydantic_attr_args,
                pydantic_attr_kwargs,
            ),
        }

        self.registry[pydantic_model][field] = new_entry

    def is_registered(self, pydantic_model, field: str, required: bool = False):
        # check if a pydantic model and field is registered, will error if required=True

        in_registry = False
        model_exists = False
        if pydantic_model in self.registry:
            model_exists = True
            in_registry = field in self.registry[pydantic_model]

        if required:
            if model_exists is False:
                raise KeyError(f"registry does not contain {pydantic_model}.")
            elif in_registry is False:
                raise KeyError(f"{pydantic_model} registry does not contain {field}.")

        return in_registry

    def get_widget_instance(self, pydantic_model, field: str):
        # return a widget instance for a given pydantic model and field
        if self.is_registered(pydantic_model, field, required=True):
            func, args, kwargs = self.registry[pydantic_model][field]["magicgui"]
            return func(*args, **kwargs)

    def get_pydantic_attr(self, pydantic_model, field: str, widget_instance):
        # given a widget instance, return an object that can be used to set a
        # pydantic field
        if self.is_registered(pydantic_model, field, required=True):
            func, args, kwargs = self.registry[pydantic_model][field]["pydantic"]
            return func(widget_instance, *args, **kwargs)

    def add_pydantic_to_container(
        self,
        py_model: Union[pydantic.BaseModel, pydantic.main.ModelMetaclass],
        container: widgets.Container,
        ignore_attrs: Optional[Union[str, List[str]]] = None,
    ):
        # recursively traverse a pydantic model adding widgets to a container.
        # When a nested pydantic model is encountered, add a new container

        if not isinstance(ignore_attrs, list):
            ignore_attrs = [
                ignore_attrs,
            ]

        for field, field_def in py_model.__fields__.items():
            if field in ignore_attrs:
                continue
            ftype = field_def.type_
            if isinstance(ftype, pydantic.BaseModel) or isinstance(
                ftype, pydantic.main.ModelMetaclass
            ):
                # the field is a pydantic class, add a container for it and fill it
                new_widget_cls = widgets.Container
                new_widget = new_widget_cls(name=field_def.name)
                self.add_pydantic_to_container(ftype, new_widget)
            elif self.is_registered(py_model, field):
                new_widget = self.get_widget_instance(py_model, field)
            else:
                new_widget = get_magicguidefault(field_def)
                if isinstance(new_widget, widgets.EmptyWidget):
                    msg = "magicgui could not identify a widget for "
                    msg += f" {py_model}.{field}, which has type {ftype}"
                    ytnapari_log.warning(msg)
            container.append(new_widget)

    def get_pydantic_kwargs(
        self,
        container: widgets.Container,
        py_model,
        pydantic_kwargs: dict,
        ignore_attrs: Optional[Union[str, List[str]]] = None,
    ):
        # given a container that was instantiated from a pydantic model, get
        # the arguments needed to instantiate that pydantic model
        if not isinstance(ignore_attrs, list):
            ignore_attrs = [
                ignore_attrs,
            ]

        # traverse model fields, pull out values from container
        for field, field_def in py_model.__fields__.items():
            if field in ignore_attrs:
                continue
            ftype = field_def.type_
            if isinstance(ftype, pydantic.BaseModel) or isinstance(
                ftype, pydantic.main.ModelMetaclass
            ):
                new_kwargs = {}  # new dictionary for the new nest level
                # any pydantic class will be a container, so pull that out to pass
                # to the recursive call
                sub_container = getattr(container, field_def.name)
                self.get_pydantic_kwargs(sub_container, ftype, new_kwargs)
                if "typing.List" in str(field_def.outer_type_):
                    new_kwargs = [
                        new_kwargs,
                    ]
                pydantic_kwargs[field] = new_kwargs

            elif self.is_registered(py_model, field):
                widget_instance = getattr(
                    container, field_def.name
                )  # pull from container
                pydantic_kwargs[field] = self.get_pydantic_attr(
                    py_model, field, widget_instance
                )
            else:
                # not a pydantic class, just pull the field value from the container
                if hasattr(container, field_def.name):
                    value = getattr(container, field_def.name).value
                    pydantic_kwargs[field] = value


# set some functions for handling specific pydantic fields.


def get_file_widget(*args, **kwargs):
    # could remove the need for this if the model uses pathlib.Path for typing
    return widgets.FileEdit(*args, **kwargs)


def get_filename(file_widget: widgets.FileEdit):
    return str(file_widget.value)


def get_magicguidefault(field_def: pydantic.fields.ModelField):
    # returns an instance of the default widget selected by magicgui
    ftype = field_def.type_
    new_widget_cls, ops = type_map.get_widget_class(
        None,
        ftype,
        dict(name=field_def.name, value=field_def.default, annotation=ftype),
        raise_on_unknown=False,
    )
    if field_def.default is None:
        # for some widgets, explicitly passing None as a default will error
        _ = ops.pop("value", None)

    return new_widget_cls(**ops)


def embed_in_list(widget_instance) -> list:
    # for when the widget value should be embedded in a list
    returnval = [widget_instance.value]
    return returnval


def split_comma_sep_string(widget_instance) -> List[str]:
    files = widget_instance.value
    for ch in " []":
        files = files.replace(ch, "")
    return files.split(",")


def _get_pydantic_model_field(py_model, field: str) -> pydantic.fields.ModelField:
    return py_model.__fields__[field]


# the following model-field tuples will be embedded in containers
_models_to_embed_in_list = (
    (_data_model.Slice, "fields"),
    (_data_model.Region, "fields"),
    (_data_model.DataContainer, "selections"),
    (_data_model.SelectionObject, "regions"),
    (_data_model.SelectionObject, "slices"),
)


def _register_yt_data_model(translator: MagicPydanticRegistry):
    # registers some special cases for pydantic fields.
    translator.register(
        _data_model.DataContainer,
        "filename",
        magicgui_factory=get_file_widget,
        magicgui_kwargs={"name": "filename"},
        pydantic_attr_factory=get_filename,
    )

    for py_model, field in _models_to_embed_in_list:
        translator.register(
            py_model,
            field,
            magicgui_factory=get_magicguidefault,
            magicgui_args=(py_model.__fields__[field]),
            pydantic_attr_factory=embed_in_list,
        )
    translator.register(
        _data_model.MetadataModel,
        "filename",
        magicgui_factory=get_file_widget,
        magicgui_kwargs={"name": "filename"},
        pydantic_attr_factory=get_filename,
    )

    translator.register(
        _data_model.TimeSeriesFileSelection,
        "file_list",
        magicgui_factory=get_magicguidefault,
        magicgui_args=(_data_model.TimeSeriesFileSelection.__fields__["file_list"],),
        pydantic_attr_factory=split_comma_sep_string,
    )


translator = MagicPydanticRegistry()
_register_yt_data_model(translator)


def get_yt_data_container(
    ignore_attrs: Optional[Union[str, List[str]]] = None,
    pydantic_model_class: Optional[
        Union[pydantic.BaseModel, pydantic.main.ModelMetaclass]
    ] = None,
) -> widgets.Container:
    if pydantic_model_class is None:
        pydantic_model_class = _data_model.DataContainer

    data_container = widgets.Container()
    translator.add_pydantic_to_container(
        pydantic_model_class,
        data_container,
        ignore_attrs=ignore_attrs,
    )
    return data_container


_valid_selections = ("Region", "Slice")


def get_yt_selection_container(selection_type: str, return_native: bool = False):
    # return a container for a single selection
    if selection_type not in _valid_selections:
        raise ValueError(
            f"selection_type must be one of {_valid_selections}, "
            f"found {selection_type}"
        )

    selection_container = widgets.Container()
    pydantic_model = getattr(_data_model, selection_type)
    translator.add_pydantic_to_container(pydantic_model, selection_container)
    if return_native:
        return selection_container.native
    return selection_container


def get_yt_metadata_container():
    data_container = widgets.Container()
    translator.add_pydantic_to_container(_data_model.MetadataModel, data_container)
    return data_container
