"""This module contains classes that are part of OVITO's data pipeline system.

Pipelines:

  * :py:class:`Pipeline`
  * :py:class:`Modifier` (base class of all built-in modifiers)
  * :py:class:`ModifierInterface` (abstract base class for user-defined modifiers)

Data sources:

  * :py:class:`StaticSource`
  * :py:class:`FileSource`
  * :py:class:`PipelineSourceInterface` (abstract base class for user-defined pipeline sources)
  * :py:class:`PythonSource` (encapsulates a :py:class:`PipelineSourceInterface` or user-defined pipeline source function)"""
__all__ = ['Pipeline', 'Modifier', 'StaticSource', 'FileSource', 'PythonSource', 'ModifierInterface', 'PipelineSourceInterface', 'PipelineNode', 'ModificationNode', 'ModifierGroup', 'ReferenceConfigurationModifier']
from __future__ import annotations
from typing import Optional, Any, Union, Sequence, MutableSequence, Callable, List, Generator, overload, Callable, Mapping, Dict, TYPE_CHECKING
import ovito.data
import ovito.modifiers
import enum
import abc
from dataclasses import dataclass

@dataclass(kw_only=True)
class PipelineNode:
    """to be written"""

    @property
    def num_frames(self) -> int:
        """This read-only attribute reports the number of frames found in the input file or sequence of input files. The data for the individual frames can be obtained using the :py:meth:`.compute` method."""
        ...

    def get_pipelines(self, in_scene_only: bool=False) -> List[Pipeline]:
        ...

    def compute(self, frame: Optional[int]=None) -> ovito.data.DataCollection:
        """Requests data from this pipeline node.

The optional *frame* parameter determines the frame to retrieve, which must be in the range 0 through (:py:attr:`num_frames`-1).
If you don't specify any frame number, the current time slider position will be used (always frame 0 for automation scripts not running in the context
of an interactive OVITO session).

The pipeline node uses a caching mechanism to keep the data for one or more trajectory frames in memory. Thus, invoking :py:meth:`compute`
repeatedly to retrieve the same frame will typically be very fast.

:param int|None frame: The trajectory frame to retrieve or compute.
:return: A new :py:class:`DataCollection` containing the frame's data."""
        ...

@dataclass(kw_only=True)
class ModificationNode(PipelineNode):
    """Base: :py:class:`ovito.pipeline.PipelineNode`"""
    modifier: Modifier
    group: Optional[ModifierGroup]
    input: PipelineNode

class ModifierInterface:
    """Base: :py:class:`traits.has_traits.HasTraits`

Abstract base class for Python-based modifiers that follow the advanced programming interface.

.. seealso:: :ref:`example_custom_time_average`"""

    class InputSlot:
        """Represents the upstream pipeline generating the input data for a custom modifier implementation."""

        @property
        def num_frames(self) -> int:
            ...

        def compute(self, frame: int) -> ovito.data.DataCollection:
            ...

    @abc.abstractmethod
    def modify(self, data: ovito.data.DataCollection, *, frame: int, input_slots: Dict[str, InputSlot], data_cache: ovito.data.DataCollection, pipeline_node: ModificationNode, **kwargs: Any) -> Optional[Generator[str | float, None, None]]:
        """The actual work function which gets called by the pipeline system to let the modifier do its thing.

:param data: Data snapshot which should be modified by the modifier function in place.
:param frame: Zero-based trajectory frame number.
:param input_slots: One or more :py:class:`InputSlot` objects representing the upstream data pipeline(s) connected to this modifier.
:param data_cache: A data container (initially empty) which may be used by the modifier function to store intermediate results.
:param pipeline_node: An object representing the use of this modifier in the pipeline that is currently being evaluated.
:param kwargs: Any further arguments that may be passed in by the pipeline system. This parameter should always be part of the function signature for forward compatibility with future versions of OVITO."""
        ...

    def notify_trajectory_length_changed(self) -> None:
        """Notifies the pipeline system that the number of output animation frames this modifier can compute has changed.
The modifier class should call this method whenever the return value of its :py:meth:`compute_trajectory_length` method
changes, for example, as a consequence of a parameter change."""
        ...

class PipelineSourceInterface:
    """Base: :py:class:`traits.has_traits.HasTraits`

Abstract base class for custom pipeline sources in Python.
Implementations of the interface must at least provide the :py:meth:`create` method.

Example:

```python
  from ovito.data import DataCollection
  from ovito.pipeline import PipelineSourceInterface
  
  class ExampleSource(PipelineSourceInterface):
      def create(self, data: DataCollection, **kwargs):
          cell_matrix = [
              [10,0,0,0],
              [0,10,0,0],
              [0,0,10,0]
          ]
          data.create_cell(cell_matrix, pbc=(False, False, False))
```

Then build a :py:class:`Pipeline` with this pipeline source by wrapping it in a :py:class:`PythonSource` object:

```python
  from ovito.pipeline import Pipeline, PythonSource
  
  example_source = ExampleSource()
  pipeline = Pipeline(source=PythonSource(delegate=example_source))
```"""

    @abc.abstractmethod
    def create(self, data: ovito.data.DataCollection, *, frame: int, **kwargs: Any) -> Optional[Generator[str | float, None, None]]:
        """The generator function which gets called by the pipeline system to let the source do its thing and produce a data collection.

:param data: Data collection which should be populated by the function. It may already contain data from previous runs.
:param frame: Zero-based trajectory frame number.
:param kwargs: Any further arguments that may be passed in by the pipeline system. This parameter should always be part of the function signature for forward compatibility with future versions of OVITO."""
        ...

    def notify_trajectory_length_changed(self) -> None:
        """Notifies the pipeline system that the number of output animation frames this source can generate has changed.
The class should call this method whenever the return value of its :py:meth:`compute_trajectory_length` method
changes, for example, as a consequence of a parameter change."""
        ...

@dataclass(kw_only=True)
class StaticSource(PipelineNode):
    """Base: :py:class:`ovito.pipeline.PipelineNode`

Serves as a data :py:attr:`~Pipeline.source` for a :py:class:`Pipeline`.
A :py:class:`StaticSource` manages a :py:class:`DataCollection`, which it will pass to the :py:class:`Pipeline` as input data.
One typically initializes a :py:class:`StaticSource` with a collection of data objects, then wiring it to a :py:class:`Pipeline` as follows:

```python
  from ovito.pipeline import StaticSource, Pipeline
  from ovito.data import DataCollection, SimulationCell, Particles
  from ovito.modifiers import CreateBondsModifier
  from ovito.io import export_file
  
  # Insert a new SimulationCell object into a data collection:
  data = DataCollection()
  cell = SimulationCell(pbc = (False, False, False))
  cell[:,0] = (4,0,0)
  cell[:,1] = (0,2,0)
  cell[:,2] = (0,0,2)
  data.objects.append(cell)
  
  # Create a Particles object containing two particles:
  particles = Particles()
  particles.create_property('Position', data=[[0,0,0],[2,0,0]])
  data.objects.append(particles)
  
  # Create a new Pipeline with a StaticSource as data source:
  pipeline = Pipeline(source = StaticSource(data = data))
  
  # Apply a modifier:
  pipeline.modifiers.append(CreateBondsModifier(cutoff = 3.0))
  
  # Write pipeline results to an output file:
  export_file(pipeline, 'output/structure.data', 'lammps/data', atom_style='bond')
```"""
    data: Optional[ovito.data.DataCollection] = None
    'The :py:class:`DataCollection` managed by this object, which will be fed to the pipeline. \n\nDefault: ``None``'

@dataclass(kw_only=True)
class FileSource(PipelineNode):
    """Base: :py:class:`ovito.pipeline.PipelineNode`

This object type serves as a :py:attr:`Pipeline.source` and takes care of reading the input data for a :py:class:`Pipeline` from an external file.

You normally do not need to create an instance of this class yourself; the :py:func:`import_file` function does it for you and wires the fully configured :py:class:`FileSource`
to the new :py:attr:`Pipeline`. However, if needed, the :py:meth:`FileSource.load` method allows you to load a different input file later on and replace the
input of the existing pipeline with a new dataset:

```python
  from ovito.io import import_file
  
  # Create a new pipeline with a FileSource:
  pipeline = import_file('input/first_file.dump')
  
  # Get the data from the first file:
  data1 = pipeline.compute()
  
  # Use FileSource.load() method to replace the pipeline's input with a different file 
  pipeline.source.load('input/second_file.dump')
  
  # Now the pipeline gets its input data from the new file:
  data2 = pipeline.compute()
```

Furthermore, you will encounter other :py:class:`FileSource` objects in conjunction with certain modifiers that need secondary input data from a separate file.
The :py:class:`CalculateDisplacementsModifier`, for example, manages its own :py:class:`FileSource` for loading reference particle positions from a separate input file.
Another example is the :py:class:`LoadTrajectoryModifier`,
which employs its own separate :py:class:`FileSource` instance to load the particle trajectories from disk and combine them
with the topology data previously loaded by the main :py:class:`FileSource` of the data pipeline.

Data access

A :py:class:`FileSource` is a :py:class:`PipelineNode`, which provides a :py:meth:`~PipelineNode.compute` method
returning a copy of the data loaded from the external input file(s). The :py:meth:`~PipelineNode.compute` method loads
the data of a specific trajectory frame from the input file(s) and returns it as a :py:class:`DataCollection` object:

```python
  # This creates a new Pipeline with an attached FileSource.
  pipeline = import_file('input/simulation.dump')
  
  # Request data of trajectory frame 0 from the FileSource.
  data = pipeline.source.compute(0)
  print(data.particles.positions[...])
```

To modify or amend the :py:class:`DataCollection` loaded by the :py:class:`FileSource`, you have to
insert a user-defined modifier function into the pipeline.
A typical use case is assigning the radii and names to particle types loaded from a simulation file that doesn't contain named atom types:

```python
  pipeline = import_file('input/simulation.dump')
  
  # User-defined modifier function that assigns names and radii to numeric atom types:
  def setup_atom_types(frame, data):
      types = data.particles_.particle_types_
      types.type_by_id_(1).name = "Cu"
      types.type_by_id_(1).radius = 1.35
      types.type_by_id_(2).name = "Zr"
      types.type_by_id_(2).radius = 1.55
  
  pipeline.modifiers.append(setup_atom_types)
```"""

    def load(self, location: Union[str, Sequence[str]], **params: Any) -> None:
        """Sets a new input file, from which this data source will retrieve its data from.

The function accepts additional keyword arguments, which are forwarded to the format-specific file reader.
For further information, please see the documentation of the :py:func:`import_file` function,
which has the same function interface as this method.

:param str|os.PathLike|Sequence[str] location: The local file(s) or remote URL to load.
:param params: Additional keyword parameters to be passed to the file reader."""
        ...

    @property
    def data(self) -> Optional[ovito.data.DataCollection]:
        """This field provides access to the internal :py:class:`DataCollection`, i.e. the master copy of the data loaded from the input file (at frame 0)."""
        ...

    @property
    def source_path(self) -> Union[str, Sequence[str]]:
        """This read-only attribute returns the path(s) or URL(s) of the file(s) where this :py:class:`FileSource` retrieves its input data from.
You can change the source path by calling :py:meth:`.load`."""
        ...

@dataclass(kw_only=True)
class PythonSource(PipelineNode):
    """Base: :py:class:`ovito.pipeline.PipelineNode`

Code example:

```python
  from ovito.pipeline import Pipeline, PythonSource
  from ovito.io import export_file
  from ovito.data import DataCollection
  import numpy
  
  # User-defined data source function, which populates an empty DataCollection with
  # some data objects:
  def create_model(frame: int, data: DataCollection):
      particles = data.create_particles(count=20)
      coordinates = particles.create_property('Position')
      coordinates[:,0] = numpy.linspace(0.0, 50.0, particles.count)
      coordinates[:,1] = numpy.cos(coordinates[:,0]/4.0 + frame/5.0)
      coordinates[:,2] = numpy.sin(coordinates[:,0]/4.0 + frame/5.0)
  
  # Create a data pipeline with a PythonSource, which executes our
  # script function defined above.
  pipeline = Pipeline(source = PythonSource(function = create_model))
  
  # Export the results of the data pipeline to an output file.
  # The system will invoke the Python function defined above once per animation frame.
  export_file(pipeline, 'output/trajectory.xyz', format='xyz',
      columns=['Position.X', 'Position.Y', 'Position.Z'],
      multiple_frames=True, start_frame=0, end_frame=10)
```"""
    function: Optional[Callable[[int, ovito.data.DataCollection], Any]] = None
    'The Python function to be called each time the data pipeline is evaluated by the system.\n\nThe function must have a signature as shown in the example above. The *frame* parameter specifies the current animation frame number at which the data pipeline is being evaluated. The :py:class:`DataCollection` *data* is initially empty should be populated with data objects by the user-defined source function. \n\nDefault: ``None``'
    delegate: Optional[ovito.pipeline.PipelineSourceInterface] = None
    'A :py:class:`PipelineSourceInterface` object implementing the logic of the user-defined pipeline source. \n\nDefault: ``None``'
    working_dir: str = ''
    "A path that will be set as active working directory while the Python function is executed by the pipeline system. This setting mainly plays a role if the source function is used within the GUI of OVITO and if it performs some file I/O. Relative file paths will then get resolved with respect to this working directory. \n\nIf no specific working directory is set, the application's current working directory will be used. \n\nDefault: ``''``"

@dataclass(kw_only=True)
class Modifier:
    """This is the base class for all modifier types in OVITO. See the :py:mod:`ovito.modifiers` module for a list of concrete modifier types that can be inserted into a data :py:class:`Pipeline`."""
    enabled: bool = True
    'Controls whether the modifier is applied to the data. Disabled modifiers are skipped during evaluation of a data pipeline. \n\nDefault: ``True``'
    title: str = ''
    "A human-readable name for the modifier to be displayed in the pipeline editor of the OVITO desktop application. If left unspecified (empty string), the display title is automatically determined by OVITO based on the modifier's concrete class type. \n\nDefault: ``''``"

@dataclass(kw_only=True)
class ModifierGroup:
    collapsed: bool = False
    enabled: bool = True
    title: str = ''

@dataclass(kw_only=True)
class ReferenceConfigurationModifier(Modifier):
    """Base: :py:class:`ovito.pipeline.Modifier`

This is the common base class of analysis modifiers that perform some kind of comparison
of the current particle configuration with a reference configuration. For example,
the :py:class:`CalculateDisplacementsModifier`, the :py:class:`AtomicStrainModifier`
and the :py:class:`WignerSeitzAnalysisModifier` are modifier types that require
a reference configuration as additional input.

Constant and sliding reference configurations

The :py:class:`ReferenceConfigurationModifier` base class provides various fields that
allow you to specify the reference particle configuration. By default, frame 0 of the currently loaded
simulation sequence is used as reference. You can select any other frame with the :py:attr:`reference_frame` field.
Sometimes an incremental analysis is desired, instead of a fixed reference configuration. That means the sliding reference configuration and the current configuration
are separated along the time axis by a constant period (*delta t*). The incremental analysis mode is activated by
setting the :py:attr:`use_frame_offset` flag and specifying the desired :py:attr:`frame_offset`.

External reference configuration file

By default, the reference particle positions are obtained by evaluating the same data pipeline that also
provides the current particle positions, i.e. which the modifier is part of. That means any modifiers preceding this modifier in the pipeline
will also act upon the reference particle configuration, but not modifiers that follow in the pipeline.

Instead of taking it from the same data pipeline, you can explicitly provide a reference configuration by loading it from a separate data file.
To this end the :py:attr:`reference` field contains a :py:class:`FileSource` object and you can
use its :py:meth:`load` method to load the reference particle positions from a separate file.

Handling of periodic boundary conditions and cell deformations

Certain analysis modifiers such as the :py:class:`CalculateDisplacementsModifier` and the :py:class:`AtomicStrainModifier`
calculate the displacements particles experienced between the reference and the current configuration.
Since particle coordinates in periodic simulation cells are often stored in a *wrapped* form,
calculating the displacement vectors is non-trivial when particles have crossed the periodic boundaries.
By default, the *minimum image convention* is used in these cases, but you can turn if off by
setting :py:attr:`minimum_image_convention` to ``False``, for example if the input particle coordinates
are given in unwrapped form.

Furthermore, if the simulation cell of the reference and the current configuration are different, it makes
a slight difference whether displacements are calculated in the reference or in the current frame.
The :py:attr:`affine_mapping` property controls the type of coordinate mapping that is used."""

    class AffineMapping(enum.Enum):
        """"""
        Off = enum.auto()
        ToReference = enum.auto()
        ToCurrent = enum.auto()
    affine_mapping: ReferenceConfigurationModifier.AffineMapping = AffineMapping.Off
    'Selects the type of affine deformation applied to the particle coordinates of either the reference or the current configuration prior to the actual analysis computation. Must be one of the following modes:\n * ``ReferenceConfigurationModifier.AffineMapping.Off``\n * ``ReferenceConfigurationModifier.AffineMapping.ToReference``\n * ``ReferenceConfigurationModifier.AffineMapping.ToCurrent``\n\n\nWhen affine mapping is disabled (``AffineMapping.Off``), particle displacement vectors are simply calculated from the difference of current and reference positions, irrespective of the cell shape the reference and current configuration. Note that this can introduce a small geometric error if the shape of the periodic simulation cell changes considerably. The mode ``AffineMapping.ToReference`` applies an affine transformation to the current configuration such that all particle positions are first mapped to the reference cell before calculating the displacement vectors. The last option, ``AffineMapping.ToCurrent``, does the reverse: it maps the reference particle positions to the deformed cell before calculating the displacements. \n\nDefault: ``ReferenceConfigurationModifier.AffineMapping.Off``'
    frame_offset: int = -1
    'The relative frame offset when using a sliding reference configuration (if :py:attr:`use_frame_offset` == ``True``). Negative frame offsets correspond to reference configurations that precede the current configuration in time. \n\nDefault: ``-1``'
    minimum_image_convention: bool = True
    'If ``False``, then displacements are calculated from the particle coordinates in the reference and the current configuration as is. Note that in this case the calculated displacements of particles that have crossed a periodic simulation cell boundary will be wrong if their coordinates are stored in a wrapped form. If ``True``, then the minimum image convention is applied when calculating the displacements of particles that have crossed a periodic boundary. \n\nDefault: ``True``'
    reference: Optional[FileSource] = None
    "A pipeline :py:attr:`source` object that provides the reference particle positions. By default this field is ``None``, in which case the modifier obtains the reference particle positions from data pipeline it is part of. You can explicitly assign a data source object such as a :py:class:`FileSource` or a :py:class:`StaticSource` to this field to specify an explicit reference configuration. \n\n```python\n  # The modifier that requires a reference config:\n  mod = CalculateDisplacementsModifier()\n  \n  # Load the reference config from a separate input file.\n  mod.reference = FileSource() # Note: You may have to import FileSource from the ovito.pipeline module. \n  mod.reference.load('input/simulation.0.dump')\n```\n\nDefault: ``None``"
    reference_frame: int = 0
    'The frame number to use as reference configuration. Ignored if :py:attr:`use_frame_offset` is set.\n\nDefault: ``0``'
    use_frame_offset: bool = False
    'Determines whether a sliding reference configuration is taken at a constant time offset (specified by :py:attr:`frame_offset`) relative to the current frame. If ``False``, a constant reference configuration is used (set by the :py:attr:`reference_frame` parameter) irrespective of the current frame.\n\nDefault: ``False``'

class _PipelineModifiersList(MutableSequence[Modifier]):

    @overload
    def append(self, value: Modifier) -> None: # type: ignore
        ...

    @overload
    def append(self, value: ModifierInterface) -> None: # type: ignore
        ...

    @overload
    def append(self, value: Callable[[int, ovito.data.DataCollection], Optional[Generator[str | float, None, None]]]) -> None:
        ...

@dataclass(kw_only=True)
class Pipeline:
    """This class encapsulates a data pipeline, consisting of a *data source* and a chain of zero or more *modifiers*,
which manipulate the data on the way through the pipeline.

Pipeline creation

Every pipeline has a *data source*, which loads or dynamically generates the input data entering the
pipeline. This source is accessible through the :py:attr:`Pipeline.source` field and may be replaced with a different kind of source object if needed.
For pipelines created by the :py:func:`import_file` function, the data source is automatically set to be a
:py:class:`FileSource` object, which loads the input data
from the external file and feeds it into the pipeline. Another kind of data source is the
:py:class:`StaticSource`, which can be used if you want to programmatically specify the input data for the pipeline
instead of loading it from a file.

The modifiers that are part of the pipeline are accessible through the :py:attr:`Pipeline.modifiers` field.
This list is initially empty and you can populate it with the modifier types found in the :py:mod:`ovito.modifiers` module.
Note that it is possible to employ the same :py:class:`Modifier` instance in more than one pipeline. And it is
okay to use the same data source object for several pipelines, letting them process the same input data.

Pipeline evaluation

Once the pipeline is set up, its computation results can be requested by calling :py:meth:`.compute`, which means that the input data will be loaded/generated by the :py:attr:`source`
and all modifiers of the pipeline are applied to the data one after the other. The :py:meth:`.compute` method
returns a new :py:class:`DataCollection` storing the data objects produced by the pipeline.
Under the hood, an automatic caching system ensures that unnecessary file accesses and computations are avoided.
Repeatedly calling :py:meth:`.compute` will not trigger a recalculation of the pipeline's results unless you
alter the pipeline's data source, the chain of modifiers, or a modifier's parameters.

Usage example

The following code example shows how to create a new pipeline by importing an MD simulation file and inserting a :py:class:`SliceModifier` to
cut away some of the particles. Finally, the total number of remaining particles is printed.

```python
  from ovito.io import import_file
  from ovito.modifiers import SliceModifier
  
  # Import a simulation file. This creates a Pipeline object.
  pipeline = import_file('input/simulation.dump')
  
  # Insert a modifier that operates on the data:
  pipeline.modifiers.append(SliceModifier(normal=(0,0,1), distance=0))
  
  # Compute the effect of the slice modifier by evaluating the pipeline.
  output = pipeline.compute()
  print("Remaining particle count:", output.particles.count)
```

To access the unmodified input data of the pipeline, i.e. *before* it has been processed by any of the modifiers,
you can call the :py:meth:`PipelineNode.compute` method of the pipeline's :py:attr:`source` node:

```python
  # Access the pipeline's input data provided by the FileSource:
  input = pipeline.source.compute()
  print("Input particle count:", input.particles.count)```

Data visualization

If you intend to produce graphical renderings of a output data produced by a pipeline,
you must make the pipeline part of the current three-dimensional scene by calling the :py:meth:`Pipeline.add_to_scene` method.

Data export

To export the generated data of the pipeline to an output file, simply call the :py:func:`ovito.io.export_file` function with the pipeline."""
    source: Optional[PipelineNode] = None
    'The object that provides the data entering the pipeline. This typically is a :py:class:`FileSource` instance if the pipeline was created by a call to :py:func:`import_file`. You can assign a new source to the pipeline if needed. See the :py:mod:`ovito.pipeline` module for a list of available pipeline source types. Note that you can even make several pipelines share the same source object.'
    head: Optional[PipelineNode] = None
    preliminary_updates: bool = True
    'This flag controls whether interactive :py:class:`Viewport` windows should get refreshed while a pipeline computation is in progress to display intermediate computation results produced by modifiers. This flag only has an effect in a graphical user interface in case the pipeline is part of the visualization scene. Setting it to ``False`` turns off frequent, sometimes unwanted viewport updates. Then an automatic refresh will only occur once the final pipeline outputs have been fully computed. \n\nDefault: ``True``'
    trajectory_caching: bool = False

    def add_to_scene(self) -> None:
        """Inserts the pipeline into the three-dimensional scene by appending it to the :py:attr:`ovito.Scene.pipelines` list. The visual representation of the pipeline's output data will appear in rendered images and in the interactive viewports. 

You can remove the pipeline from the scene again using :py:meth:`.remove_from_scene`."""
        ...

    def remove_from_scene(self) -> None:
        """Removes the visual representation of the pipeline from the scene by deleting it from the :py:attr:`ovito.Scene.pipelines` list. The output data of the pipeline will disappear from viewports."""
        ...

    def compute(self, frame: Optional[int]=None) -> ovito.data.DataCollection:
        """Computes and returns the output of this data pipeline (for one trajectory frame).

This method requests an evaluation of the pipeline and blocks until the input data has been obtained from the
data :py:attr:`source`, e.g. a simulation file, and all modifiers have been applied to the data. If you invoke the :py:meth:`compute` method repeatedly
without changing the modifiers in the pipeline between calls, the pipeline may serve subsequent requests by returning cached output data.

The optional *frame* parameter specifies the animation frame at which the pipeline should be evaluated. Frames are always consecutively numbered (0, 1, 2, ...).
If you don't specify any frame number, the current time slider position is used -- or frame 0 if not running in the context of an interactive OVITO Pro session.

The :py:meth:`compute` method raises a ``RuntimeError`` if the pipeline could not be successfully evaluated for some reason.
This may happen due to invalid modifier settings or file I/O errors, for example.

:param int frame: The animation frame number at which the pipeline should be evaluated.
:returns: A :py:class:`DataCollection` produced by the data pipeline.

.. attention::

    This method returns a snapshot of the results of the current pipeline, representing an independent data copy.
    That means snapshot will *not* reflect changes you subsequently make to the pipeline or the modifiers within the pipeline.
    After changing the pipeline, you have to invoke :py:meth:`compute` again to let the pipeline produce a new updated snapshot.

.. attention::

    The returned :py:class:`DataCollection` represents a copy of the pipeline's internal data, which means,
    if you subsequently make any changes to the objects in the :py:class:`DataCollection`, those changes will *not*
    be visible to the modifiers *within* the pipeline -- even if you add those modifiers to the pipeline after the :py:meth:`compute`
    call as in this example::

        data = pipeline.compute()
        data.particles_.create_property('Foo', data=...)

        pipeline.modifiers.append(ExpressionSelectionModifier(expression='Foo > 0'))
        new_data = pipeline.compute() # ERROR

    The second call to :py:meth:`compute` will raise an error, because the :py:class:`ExpressionSelectionModifier`
    references the new particle property ``Foo``, which does not exist in the original data seen by the pipeline.
    That' because we've added the property ``Foo`` only to the :py:class:`Particles` object that is stored
    in our snapshot ``data``. This :py:class:`DataCollection` is independent from the transient data the pipeline operates on.

    To make the property ``Foo`` available to modifiers in the pipeline, we thus need to create the property *within*
    the pipeline. This can be accomplished by performing the modification step as a Python modifier function
    that is inserted into the pipeline::

        def add_foo(frame, data):
            data.particles_.create_property('Foo', data=...)
        pipeline.modifiers.append(add_foo)
        pipeline.modifiers.append(ExpressionSelectionModifier(expression='Foo > 0'))

    Downstream modifiers now see the new particle property created by our user-defined modifier function ``add_foo``,
    which operates on a transient data collection managed by the pipeline system."""
        ...

    @property
    def modifiers(self) -> _PipelineModifiersList:
        """The sequence of modifiers in the pipeline.

This list contains any modifiers that are applied to the input data provided by the pipeline's data :py:attr:`source`. You
can add and remove modifiers as needed using standard Python ``append()`` and ``del`` operations. The
head of the list represents the beginning of the pipeline, i.e. the first modifier receives the data from the
data :py:attr:`source`, manipulates it and passes the results on to the second modifier in the list and so forth.

Example: Adding a new modifier to the end of a data pipeline::

   pipeline.modifiers.append(WrapPeriodicImagesModifier())"""
        ...