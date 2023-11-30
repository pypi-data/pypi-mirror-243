def read_SyConn_info():
    SyConn_info = """
SyConn is a comprehensive toolkit for analyzing connectomics data derived from volume electron microscopy (VEM) and potentially augmented by flood-filling networks (FFN). It facilitates semantic segmentation of cellular structures and their assembly into a connectome at the cellular level. The toolkit is designed for high-performance computing environments and cloud computing clusters.

The core components of SyConn are `SegmentationDatasets` and `SegmentationObjects`, managed by `segmentation.py` within the `syconn.reps` package. These components are supported by helper functions in `segmentation_helper.py` and `rep_helper.py` for basic operations like loading and storing data, and by `sd_proc.py` in `syconn.proc` for parallelized intensive processing.

`SegmentationDatasets` typically start by voxel storage creation, often through object extraction. Each `SegmentationObject` contains voxels, attributes, a skeleton, and a mesh, each stored in separate dictionaries (`VoxelDict`, `AttributeDict`, `SkeletonDict`, `MeshDict`). These dictionaries compress data from multiple objects for efficient storage, and the number of dictionaries per data type can be set with `n_folders_fs`.

To initialize a `SegmentationDataset`, at minimum, the `obj_type` must be defined, with defaults for other parameters like `version` and `working_dir` stored in `config.ini` and `config.global_params`.

After creating a `SegmentationDataset`, it's recommended to run `sd_proc.dataset_analysis(...)` to create global numpy arrays for fast attribute access and calculate attributes like `size` and `bounding box`. This can be seen as a distributed column store for the underlying database.

For usage, if `sd_proc.dataset_analysis(...)` has been applied, attributes of all objects can be accessed as arrays. For example, the `size` attribute can be accessed via `sizes = sd_cell_sv.load_numpy_data("size")`. The `SegmentationDataset` also allows easy access to its `SegmentationObjects`.

Each `SegmentationObject` has four additional data structures: `VoxelStorage`, `AttributeDict`, `MeshStorage`, and `SkeletonStorage`. Typically, every `SegmentationObject` has the first three, while only supervoxels (`sv`) have a skeleton. Attributes are a key-value store and should be consistent across the `SegmentationDataset`.

For extracting connectivity, synaptic classification is performed using a Random Forest Classifier (RFC) based on contact sites combined with `syn_ssv` `SegmentationObjects`. The code for this process is located in `syconn.extraction.cs_processing_steps`, `syconn.proc.sd_proc`, and `syconn.proc.ssd_proc`, with the execution script at `SyConn/scripts/syns/syn_gen.py`.

The prerequisites for classifying synapse objects include a `SegmentationDataset` of type `syn_ssv`, synapse type predictions, and labeled cellular compartments. The classification process involves mapping other objects like vesicle clouds and mitochondria by proximity, creating ground truth for the RFC, and classifying `syn_ssv` `SegmentationObjects`.

Cellular compartment information is assigned to each `syn_ssv` `SegmentationObject`, and connectivity information can be written to the `SuperSegmentationDataset` for efficient look-ups. The connectivity matrix can be exported in various formats.

The `syconn.exec` package contains submodules for different execution tasks, and the `syconn.proc` package contains submodules for general processing, graphs, image processing, mapping, meshes, rendering, and statistics.

For contact site extraction, the main functionality is in `syconn.extraction.cs_extraction_steps` and `syconn.extraction.cs_processing_steps`, with the execution script at `SyConn/scripts/syns/syn_gen.py`. The process involves finding and extracting contact sites between supervoxels and combining them between supersegmentation objects.

The `syconn.reps` package contains submodules for handling `SuperSegmentationObjects` and `SuperSegmentationDatasets`, including helper modules for additional functionality.

For skeletonization, the process involves initializing `SuperSegmentationObjects`, reskeletonizing SSVs, and extracting skeleton-based features for classification tasks like predicting cell type, compartments, and spines.

The `syconn.mp` package contains submodules for batch job utilities and multiprocessing utilities.

The `syconn.handler` package includes submodules for handling basics, compression, prediction, configuration, and logging.

Lastly, the `syconn.backend` package contains submodules for the base backend functionality and storage management.

Additional Tools:
- Skeletons: The skeletonization process is used to create a sparse representation of the segmentation, which is essential for classifying cell compartments and types.
- Glia Removal: Scripts for analyzing neuron segmentation and removing glial cells are provided in `SyConn/scripts/multiviews_glia/`.
- Contact Site Extraction: The extraction of contact sites is a crucial step in the analysis pipeline and is handled by scripts in `syconn.extraction`.
"""

    return SyConn_info