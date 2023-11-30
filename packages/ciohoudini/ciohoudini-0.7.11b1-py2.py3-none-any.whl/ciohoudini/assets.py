import hou
import re
import os
from ciopath.gpath_list import PathList, GLOBBABLE_REGEX
from ciopath.gpath import Path
from ciohoudini import common
import logging
logger = logging.getLogger(__name__)


def resolve_payload(node, do_asset_scan, **kwargs):
    """
    Resolve the upload_paths field for the payload.
    """
    # print("Assets resolve_payload ... ")
    path_list = PathList()
    path_list.add(*auxiliary_paths(node))
    path_list.add(*extra_paths(node))
    if do_asset_scan:
        path_list.add(*scan_paths(node))
    # path_list.add(extract_all_referenced_asset_paths())

    # Make sure none of the paths are in the output folder.
    output_folder = Path(node.parm('output_folder').eval())
    hip_file = hou.hipFile.path()
    # get the hip file folder
    hip_folder = os.path.dirname(hip_file)
    hip_folder = hip_folder.replace("\\", "/")

    current_assets = [str(path) for path in path_list]  # Convert paths to strings
    # print("current_assets: {}".format(current_assets))

    # Add top-level folders and files in the hip folder to current_assets
    for item in os.listdir(hip_folder):
        item_path = os.path.join(hip_folder, item)
        if os.path.isdir(item_path) or os.path.isfile(item_path):
            current_assets.append(item_path.replace("\\", "/"))
    # print("current_assets 2: {}".format(current_assets))

    # Filter out paths that are within the output folder
    filtered_paths = [path for path in current_assets if not is_within_output_folder(path, output_folder)]
    # print("filtered_paths before removing the hip folder: {}".format(filtered_paths))
    # Filter out paths that are the "hip file folder"
    filtered_paths = [path for path in filtered_paths if not path == hip_folder]

    # print("filtered assets: {}".format(filtered_paths))

    return {"upload_paths": filtered_paths}


def is_within_output_folder(path, output_folder):
    # Normalize the paths to handle different platforms and spaces
    normalized_path = os.path.normpath(str(path))  # Convert path to string
    normalized_output_folder = os.path.normpath(str(output_folder))  # Convert path to string

    # Check if the normalized path is within the normalized output folder
    result = normalized_path.startswith(normalized_output_folder)
    return result


def auxiliary_paths(node, **kwargs):
    """
    Add the hip file, the OCIO file, and the render script to the list of assets.
    """
    path_list = PathList()

    path_list.add(hou.hipFile.path())
    
    ocio_file = os.environ.get("OCIO")
    if ocio_file:
        path_list.add(os.path.dirname(ocio_file))
    
    render_script = node.parm("render_script").eval()
    if render_script:
        # Make the render script optional, by putting the last char in sq brackets 
        render_script = "{}[{}]".format(render_script[:-1], render_script[-1])
        path_list.add(render_script)

    if path_list:
        path_list = _resolve_absolute_existing_paths(path_list)

    exclude_pattern = node.parm("asset_excludes").unexpandedString()
    if exclude_pattern:
        path_list.remove_pattern(exclude_pattern)

    return path_list


def extra_paths(node, **kwargs):
    path_list = PathList()
    num = node.parm("extra_assets_list").eval()
    for i in range(1, num + 1):
        asset = node.parm("extra_asset_{:d}".format(i)).eval()
        if asset:
            path_list.add(asset)

    if path_list:
        path_list = _resolve_absolute_existing_paths(path_list)

    return path_list


def extract_all_referenced_asset_paths():
    """
    Extract all asset paths referenced or linked in a Houdini scene file, including custom parameters,
    specific node types, .abc (Alembic) files, .usd (Universal Scene Description) files, and locked assets.
    """
    asset_paths = set()
    path_list = PathList()

    try:
        # Scan all nodes for file parameters and add their paths
        for node in hou.node('/').allSubChildren():
            for parm in node.parms():
                # Check if the parameter is a file parameter or locked
                if (parm.parmTemplate().type() == hou.parmTemplateType.String and 'filechooser' in parm.parmTemplate().tags()) or parm.isLocked():

                    # file_path = parm.eval()
                    file_path = parm.unexpandedString()
                    if file_path and os.path.exists(file_path):
                        asset_paths.add(file_path)

                # Additional checks for custom parameters and node types
                if parm.name() == 'custom_path' or node.type().name() in ['custom_node_type1', 'custom_node_type2']:
                    # custom_path = parm.eval()
                    custom_path = parm.unexpandedString()
                    if custom_path and os.path.exists(custom_path):
                        asset_paths.add(custom_path)

                # Todo: add further custom checks

        if asset_paths:
            for asset_path in asset_paths:
                if asset_path and os.path.exists(asset_path):
                    path_list.add(asset_path)

        if path_list:
            path_list = _resolve_absolute_existing_paths(path_list)
    except Exception as e:
        print("Error extracting asset paths: {}".format(e))

    return path_list

def scan_paths(node):
    """
    Scan for assets.

    If we are generating data for the preview panel, then only show assets if the button was
    explicitly clicked, since dep scan may be expensive.
    """

    result = PathList()
    parms = _get_file_ref_parms()

    # regex to find all patterns in an evaluated filename that could represent a varying parameter.
    regex = node.parm("asset_regex").unexpandedString()
    REGEX = re.compile(regex, re.IGNORECASE)

    for parm in parms:
        evaluated = parm.eval()
        if evaluated:
            pth = REGEX.sub(r"*", evaluated)
            result.add(pth)

    result = _resolve_absolute_existing_paths(result)

    exclude_pattern = node.parm("asset_excludes").unexpandedString()
    if exclude_pattern:
        result.remove_pattern(exclude_pattern)
    return result


def _get_file_ref_parms():
    parms = []
    refs = hou.fileReferences()
    for parm, _ in refs:
        if not parm:
            continue
        if parm.node().type().name().startswith("conductor::job"):
            continue
        parms.append(parm)
    return parms


def clear_all_assets(node, **kwargs):
    node.parm("extra_assets_list").set(0)


def browse_files(node, **kwargs):
    files = hou.ui.selectFile(
        title="Browse for files to upload",
        collapse_sequences=True,
        file_type=hou.fileType.Any,
        multiple_select=True,
        chooser_mode=hou.fileChooserMode.Read,
    )
    if not files:
        return
    files = [f.strip() for f in files.split(";") if f.strip()]
    add_entries(node, *files)


def browse_folder(node, **kwargs):

    files = hou.ui.selectFile(title="Browse for folder to upload", file_type=hou.fileType.Directory)
    if not files:
        return
    files = [f.strip() for f in files.split(";") if f.strip()]
    add_entries(node, *files)



def add_entries(node, *entries):
    """
    Add entries to the asset list.
    
    These new entries and the existing entries are deduplicated. PathList object automatically
    deduplicates on access.
    """

    path_list = PathList()
    
    num = node.parm("extra_assets_list").eval()
    for i in range(1, num + 1):
        asset = node.parm("extra_asset_{:d}".format(i)).eval()
        if asset:
            path_list.add(asset)

    for entry in entries:
        path_list.add(entry)

    paths = [p.fslash() for p in path_list]

    node.parm("extra_assets_list").set(len(paths))
    for i, arg in enumerate(paths):
        index = i + 1
        node.parm("extra_asset_{:d}".format(index)).set(arg)

def remove_asset(node, index):
    curr_count = node.parm("extra_assets_list").eval()
    for i in range(index + 1, curr_count + 1):
        from_parm = node.parm("extra_asset_{}".format(i))
        to_parm = node.parm("extra_asset_{}".format(i - 1))
        to_parm.set(from_parm.unexpandedString())
    node.parm("extra_assets_list").set(curr_count - 1)

def add_hdas(node, **kwargs):
    """
    Add all hda folders to the asset list.

    Called from a button in the UI. It's just a convenience. User could also browse for HDAs by
    hand.
    """
 
    hda_paths = [hda.libraryFilePath() for hda in common.get_plugin_definitions()]
    if not hda_paths:
        return

    add_entries(node, *hda_paths)


def _resolve_absolute_existing_paths(path_list):
    """
    Resolve all absolute paths in the list to their canonical form.

    This is necessary because Houdini stores absolute paths in the file references, but the
    canonical form is what we want to upload.

    Prefix any relative paths with HIP. It's the best we can do for now.
    However, some relative paths may be internal stuff like op:blah or temp:blah,
    we'll ignore them for now.
    """
    hip = hou.getenv("HIP")
    job = hou.getenv("JOB")
    internals = ("op:", "temp:")

    resolved  = PathList()
    for path in path_list:
        if path.relative:
            if not path.fslash().startswith(internals):
                resolved.add(
                    os.path.join(hip, path.fslash()),
                    os.path.join(job, path.fslash()),
                    )
        else:
            resolved.add(path)
 
    resolved.remove_missing()
    resolved.glob()
    return resolved
    