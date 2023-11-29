import os
import typer
import json
import yaml
from typing import Union

import cerebrium.utils as utils
import cerebrium.api as api
from cerebrium.datatypes import (
    DEFAULT_COOLDOWN,
    DEFAULT_HARDWARE_SELECTION,
    DEFAULT_PYTHON_VERSION,
    MIN_CPU,
    MIN_MEMORY,
    Hardware,
    MAX_GPU_COUNT,
    MAX_MEMORY,
    MAX_CPU,
    DEFAULT_CPU,
    DEFAULT_MEMORY,
)
from cerebrium import __version__ as cerebrium_version
from cerebrium.core import app
from cerebrium.utils import assign_param, cerebriumLog
from cerebrium.verification import validate_and_update_cortex_params

_EXAMPLE_MAIN = """
from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    # Add your input parameters here
    prompt: str
    your_param: Optional[str] = None # an example optional parameter


def predict(item, run_id, logger):
    item = Item(**item)

    ### ADD YOUR CODE HERE
    my_results = {"prediction": item.prompt, "your_optional_param": item.your_param} 
    my_status_code = 200 # if you want to return some status code 

    ### RETURN YOUR RESULTS
    return {"my_result": my_results, "status_code": my_status_code} # return your results
"""


@app.command()
def init(
    init_dir: str = typer.Argument(
        "",
        help="Directory where you would like to init a Cortex project.",
    ),
    overwrite: bool = typer.Option(
        False, help="Flag to overwrite contents of the init_dir."
    ),
    requirements_list: str = typer.Option(
        "",
        help=(
            "Optional list of requirements. "
            "Example: \"['transformers', 'torch==1.31.1']\""
        ),
    ),
    pkg_list: str = typer.Option(
        "", help=("Optional list of apt packages. For example: \"['git', 'ffmpeg' ]\"")
    ),
    conda_pkglist: str = typer.Option("", help="Optional list of conda packages."),
    api_key: str = typer.Option(
        "", help="Private API key for the user. Not included in config by default."
    ),
    hardware: str = typer.Option(
        "AMPERE_A5000",
        help=(
            "Hardware to use for the Cortex deployment. "
            "Defaults to 'GPU'. "
            f"Can be one of: {Hardware.available_hardware()} "
        ),
    ),
    cpu: int = typer.Option(
        2,
        min=MIN_CPU,
        max=MAX_CPU,
        help=(
            "Number of CPUs to use for the Cortex deployment. "
            "Defaults to 2. Can be an integer between 1 and 48"
        ),
    ),
    memory: float = typer.Option(
        DEFAULT_MEMORY,
        min=MIN_MEMORY,
        max=MAX_MEMORY,
        help=(
            "Amount of memory (in GB) to use for the Cortex deployment. "
            "Defaults to 14.5GB. "
            "Can be a float between 2.0 and 256.0 depending on hardware selection."
        ),
    ),
    gpu_count: int = typer.Option(
        1,
        min=0,
        max=MAX_GPU_COUNT,
        help=(
            "Number of GPUs to use for the Cortex deployment. "
            "Defaults to 1. Can be an integer between 1 and 8."
        ),
    ),
    include: str = typer.Option(
        "[./*, main.py, requirements.txt, pkglist.txt, conda_pkglist.txt]",
        help=(
            "Comma delimited string list of relative paths to files/folder to include. "
            "Defaults to all visible files/folders in project root."
        ),
    ),
    exclude: str = typer.Option(
        "[./.*, ./__*]",
        help=(
            "Comma delimited string list of relative paths to files/folder to exclude. "
            "Defaults to all hidden files/folders in project root."
        ),
    ),
    log_level: str = typer.Option(
        "INFO",
        help="Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'",
    ),
    predict_data: Union[str, None] = typer.Option(
        None,
        help="JSON string containing all the parameters that will be used to run your "
        "deployment's predict function on build to ensure your new deployment will work "
        "as expected before replacing your existing deployment.",
    ),
    disable_animation: bool = typer.Option(
        bool(os.getenv("CI")),
        help="Whether to use TQDM and yaspin animations.",
    ),
):
    """
    Initialize an empty Cerebrium Cortex project.
    """

    if hardware:
        vals = Hardware.available_hardware()
        if hardware not in vals:
            utils.cerebriumLog(message=f"Hardware must be one of {vals}", level="ERROR")
        hardware = getattr(Hardware, hardware).name

    if not os.path.exists(init_dir):
        os.makedirs(init_dir)
    elif os.listdir(init_dir) and not overwrite:
        utils.cerebriumLog(
            level="ERROR",
            message="Directory is not empty. "
            "Use an empty directory or use the `--overwrite` flag.",
        )
    with open(os.path.join(init_dir, "main.py"), "w") as f:
        f.write(_EXAMPLE_MAIN)

    requirements = requirements_list.strip("[]").split(",")
    with open(os.path.join(init_dir, "requirements.txt"), "w") as f:
        for r in requirements:
            f.write(f"{r}\n")

    pkg_list = pkg_list.strip("[]").replace(",", "\n")
    with open(os.path.join(init_dir, "pkglist.txt"), "w") as f:
        for p in pkg_list:
            f.write(p)

    conda_pkglist = conda_pkglist.strip("[]").replace(",", "\n")
    with open(os.path.join(init_dir, "conda_pkglist.txt"), "w") as f:
        for c in conda_pkglist:
            f.write(c)

    config = {
        "hardware": hardware,
        "cpu": cpu,
        "memory": memory,
        "log_level": log_level,
        "include": include,
        "exclude": exclude,
        "cooldown": DEFAULT_COOLDOWN,
        "gpu_count": gpu_count,
        "predict_data": predict_data
        or '{"prompt": "Here is some example predict data for your config.yaml which will be used to test your predict function on build."}',
        "min_replicas": 0,
    }
    if disable_animation is not None:
        config["disable_animation"] = disable_animation
    if api_key:
        config["api_key"] = api_key
    with open(os.path.join(init_dir, "config.yaml"), "w") as f:
        yaml.dump(config, f, version=(1, 2), sort_keys=False)


def setup_app(
    name,
    api_key,
    cpu,
    config_file,
    exclude,
    hardware,
    include,
    force_rebuild,
    gpu_count,
    hide_public_endpoint,
    python_version,
    memory,
    disable_animation,
    disable_build_logs,
    disable_syntax_check,
    cerebrium_function="deploy",
    cooldown=DEFAULT_COOLDOWN,
    disable_predict_data=None,
    init_debug=False,
    log_level="INFO",
    min_replicas=None,
    max_replicas=None,
    predict_data=None,
):
    # Set default params
    params = {
        "hardware": DEFAULT_HARDWARE_SELECTION,
        "cpu": DEFAULT_CPU,
        "memory": DEFAULT_MEMORY,
        "cooldown": DEFAULT_COOLDOWN,
        "python_version": DEFAULT_PYTHON_VERSION,
        "include": "[./*, ./main.py, ./requirements.txt, ./pkglist.txt, ./conda_pkglist.txt]",
        "exclude": "[./.*, ./__*]",  # ignore .git etc. by default
        "init_debug": False,
        "pre_init_debug": False,
        "disable_animation": os.getenv("CI", None),
    }

    # If a config file is provided, load it in.
    if config_file == "" or config_file is None:
        config_file = "config.yaml"
    else:
        if not os.path.exists(config_file):
            utils.cerebriumLog(
                level="ERROR",
                message=f"Config file {config_file} not found.",
                prefix="Argument Error:",
            )

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    config = utils.remove_null_values(config)
    disable_animation = disable_animation if disable_animation is not None else False
    # Override the default params with the config file params
    params.update(config)
    params = assign_param(params, "name", name)
    params = assign_param(params, "hardware", hardware)
    params = assign_param(params, "cpu", cpu)
    params = assign_param(params, "memory", memory)
    params = assign_param(params, "python_version", python_version)
    params = assign_param(params, "gpu_count", gpu_count)
    params = assign_param(params, "cooldown", cooldown)
    params = assign_param(params, "force_rebuild", force_rebuild, False)
    params = assign_param(params, "min_replicas", min_replicas)
    params = assign_param(params, "max_replicas", max_replicas)
    params = assign_param(params, "include", include)
    params = assign_param(params, "exclude", exclude)
    params = assign_param(
        params, "log_level", log_level, "DEBUG" if api.env == "dev" else "INFO"
    )
    params = assign_param(params, "init_debug", init_debug, False)
    params = assign_param(params, "disable_animation", disable_animation, False)
    params = assign_param(params, "disable_build_logs", disable_build_logs, False)
    params = assign_param(params, "hide_public_endpoint", hide_public_endpoint, False)
    params = assign_param(params, "disable_syntax_check", disable_syntax_check, False)

    # Set api_key using login API Key if not provided
    api_key = api_key or params.get("api_key", "")
    if not api_key:
        print("No API key provided...\nGetting your API Key from your Cerebrium config. 🗝️")
        api_key = utils.get_api_key()
    params["api_key"] = api_key
    params = validate_and_update_cortex_params(params)
    name = params["name"]
    hardware = params["hardware"]
    hardware = hardware.upper() if isinstance(hardware, str) else hardware
    gpu_count = params["gpu_count"]

    if "predict_data" in params:
        predict_data = (
            predict_data if predict_data is not None else params.get("predict_data")
        )

    disable_predict_data = (
        disable_predict_data
        if disable_predict_data is not None
        else params.get("disable_predict")
    )

    function_pprint = "🏃" if cerebrium_function == "run" else "🌍"
    print(
        f"{function_pprint} {cerebrium_function.capitalize()} {name} with {gpu_count}x '{hardware}'"
        " GPUs on Cerebrium..."
    )

    if not os.path.exists("./main.py"):
        utils.cerebriumLog(
            level="ERROR",
            message="main.py not found in current directory. " "This file is required.",
            prefix="Deployment Requirements Error:",
        )

    with open("./main.py", "r") as f:
        main_py = f.read()
        if "def predict(" not in main_py:
            utils.cerebriumLog(
                level="ERROR",
                message="main.py does not contain a predict function."
                " This function is required.",
                prefix="Deployment Requirements Error:",
            )
    requirements_hash = utils.content_hash(["./requirements.txt"])
    pkglist_hash = utils.content_hash(["./pkglist.txt"])
    file_list = utils.determine_includes(
        include=params["include"], exclude=params["exclude"]
    )

    if disable_predict_data:
        predict_data = None
    else:
        predict_data = predict_data if predict_data is not None else None
        if predict_data is None:
            utils.cerebriumLog(
                level="ERROR",
                message="No predict data provided. "
                "Please provide predict_data in json format to your config.yaml.\n"
                "This data is used to test your predict function on build to ensure "
                "your new deployment will work as you expect before replacing your "
                "existing deployment.\n"
                "Otherwise, use the `--disable-predict` flag to disable the check",
                prefix="Argument Error:",
            )

    # Include the predict data in the content hash to trigger a rebuild if the predict changes
    files_hash = utils.content_hash(file_list, strings=predict_data)

    params["upload_hash"] = files_hash
    params["requirements_hash"] = requirements_hash
    params["pkglist_hash"] = pkglist_hash
    params["cerebrium_version"] = cerebrium_version
    params = utils.remove_null_values(params)
    params["function"] = cerebrium_function

    if params["log_level"] == "DEBUG":
        print("🚧 Deployment parameters:")
        print(json.dumps(params, indent=2)[2:-1])

    if disable_predict_data:
        print("🔮 Testing predict function is  disabled. Skipping ...")
    elif predict_data is not None:
        print(
            "🔮 Testing your deployment's predict function with the following data at the end of the build:")
        try:
            print(json.dumps(json.loads(predict_data), indent=4)[2:-1])
        except json.decoder.JSONDecodeError:
            utils.cerebriumLog(
                message="Invalid JSON string",
                level="ERROR",
                prefix="Could not parse predict data:",
            )

    setup_response = api._setup_app(
        headers={"Authorization": api_key},
        body=params,
    )
    build_status = setup_response["status"]
    project_id = setup_response["projectId"]
    build_id = setup_response["buildId"]
    jwt = setup_response["jwt"]
    if build_status == "pending":
        zip_file_name = setup_response["keyName"]
        upload_url = setup_response["uploadUrl"]
        if api.upload_cortex_files(
            upload_url=upload_url,
            zip_file_name=zip_file_name,
            file_list=file_list,
            disable_syntax_check=disable_syntax_check,
            disable_animation=disable_animation,
            predict_data=predict_data,
        ):
            api._poll_app_status(
                api_key=api_key,
                build_id=build_id,
                name=name,
                project_id=project_id,
                jwt=jwt,
                disable_animation=bool(params["disable_animation"]),
                disable_build_logs=bool(params["disable_build_logs"]),
                hide_public_endpoint=bool(params["hide_public_endpoint"]),
                is_run=cerebrium_function == "run",
                hardware=hardware,
            )
    elif build_status == "running":
        print("🤷 No file changes detected. Getting logs for previous build...")
        api._poll_app_status(
            api_key=api_key,
            build_id=build_id,
            name=name,
            project_id=project_id,
            jwt=jwt,
            disable_animation=bool(params["disable_animation"]),
            disable_build_logs=bool(params["disable_build_logs"]),
            hide_public_endpoint=bool(params["hide_public_endpoint"]),
            is_run=cerebrium_function == "run",
            hardware=hardware,
        )

    else:
        cerebriumLog("ERROR", "No content has changed and previous build failed.")

    print(f"🆔 Build ID: {build_id}")


@app.command()
def deploy(
    name: str = typer.Argument(..., help="Name of the Cortex deployment."),
    api_key: str = typer.Option("", help="Private API key for the user."),
    disable_syntax_check: bool = typer.Option(
        False, help="Flag to disable syntax check."
    ),
    hardware: str = typer.Option(
        "",
        help=(
            "Hardware to use for the Cortex deployment. "
            "Defaults to 'AMPERE_A6000'. "
            "Can be one of "
            "'TURING_4000', "
            "'TURING_5000', "
            "'AMPERE_A4000', "
            "'AMPERE_A5000', "
            "'AMPERE_A6000', "
            "'AMPERE_A100'"
        ),
    ),
    cpu: Union[int, None] = typer.Option(
        None,
        min=MIN_CPU,
        max=MAX_CPU,
        help=(
            "Number of vCPUs to use for the Cortex deployment. Defaults to 2. "
            "Can be an integer between 1 and 48."
        ),
    ),
    memory: float = typer.Option(
        None,
        min=MIN_MEMORY,
        max=MAX_MEMORY,
        help=(
            "Amount of memory(GB) to use for the Cortex deployment. Defaults to 16. "
            "Can be a float between 2.0 and 256.0 depending on hardware selection."
        ),
    ),
    gpu_count: int = typer.Option(
        None,
        min=1,
        max=MAX_GPU_COUNT,
        help=(
            "Number of GPUs to use for the Cortex deployment. Defaults to 1. "
            "Can be an integer between 1 and 8."
        ),
    ),
    min_replicas: int = typer.Option(
        None,
        min=0,
        max=200,
        help=(
            "Minimum number of replicas to create on the Cortex deployment. "
            "Defaults to 0."
        ),
    ),
    max_replicas: int = typer.Option(
        None,
        min=1,
        max=200,
        help=(
            "A hard limit on the maximum number of replicas to allow. "
            "Defaults to 2 for free users. "
            "Enterprise and standard users are set to maximum specified in their plan"
        ),
    ),
    predict_data: Union[str, None] = typer.Option(
        None,
        help="JSON string containing all the parameters that will be used to run your "
        "deployment's predict function on build to ensure your new deployment will work "
        "as expected before replacing your existing deployment.",
    ),
    python_version: str = typer.Option(
        "",
        help=(
            "Python version to use. "
            "Currently, we support '3.8' to '3.11'. Defaults to '3.10'"
        ),
    ),
    include: str = typer.Option(
        "",
        help=(
            "Comma delimited string list of relative paths to files/folder to include. "
            "Defaults to all visible files/folders in project root."
        ),
    ),
    exclude: str = typer.Option(
        "",
        help="Comma delimited string list of relative paths to files/folder to exclude. "
        "Defaults to all hidden files/folders in project root.",
    ),
    cooldown: int = typer.Option(
        None,
        help="Cooldown period in seconds before an inactive replica of your deployment is scaled down. Defaults to 60s.",
    ),
    force_rebuild: bool = typer.Option(
        None,
        help="Force rebuild. Clears rebuilds deployment from scratch as if it's a clean deployment.",
    ),
    init_debug: bool = typer.Option(
        None,
        help="Stops the container after initialization.",
    ),
    log_level: Union[str, None] = typer.Option(
        None,
        help="Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'",
    ),
    config_file: str = typer.Option(
        "",
        help="Path to config.yaml file. You can generate a config using `cerebrium init-cortex`. The contents of the deployment config file are overridden by the command line arguments.",
    ),
    disable_predict: Union[bool, None] = typer.Option(
        None, help="Flag to disable running predict function."
    ),
    disable_animation: bool = typer.Option(
        None,
        help="Whether to use TQDM and yaspin animations.",
    ),
    disable_build_logs: bool = typer.Option(
        False, help="Whether to disable build logs during a deployment."
    ),
    hide_public_endpoint: bool = typer.Option(
        False,
        help="Whether to hide the public endpoint of the deployment when printing the logs.",
    ),
):
    """
    Deploy a Cortex deployment to Cerebrium
    """
    setup_app(
        name=name,
        api_key=api_key,
        hardware=hardware,
        cpu=cpu,
        memory=memory,
        gpu_count=gpu_count,
        min_replicas=min_replicas,
        max_replicas=max_replicas,
        python_version=python_version,
        include=include,
        exclude=exclude,
        cooldown=cooldown,
        force_rebuild=force_rebuild,
        init_debug=init_debug,
        log_level=log_level,
        disable_animation=disable_animation,
        disable_build_logs=disable_build_logs,
        disable_predict_data=disable_predict,
        disable_syntax_check=disable_syntax_check,
        hide_public_endpoint=hide_public_endpoint,
        config_file=config_file,
        predict_data=predict_data,
    )


@app.command()
def build(
    name: str = typer.Argument(..., help="Name of the Cortex deployment."),
    api_key: str = typer.Option("", help="Private API key for the user."),
    disable_syntax_check: bool = typer.Option(
        False, help="Flag to disable syntax check."
    ),
    hardware: str = typer.Option(
        "",
        help=(
            "Hardware to use for the Cortex deployment. "
            "Defaults to 'AMPERE_A6000'. "
            "Can be one of "
            "'TURING_4000', "
            "'TURING_5000', "
            "'AMPERE_A4000', "
            "'AMPERE_A5000', "
            "'AMPERE_A6000', "
            "'AMPERE_A100'"
        ),
    ),
    cpu: Union[int, None] = typer.Option(
        None,
        min=MIN_CPU,
        max=MAX_CPU,
        help=(
            "Number of vCPUs to use for the Cortex deployment. Defaults to 2. "
            "Can be an integer between 1 and 48."
        ),
    ),
    memory: Union[float, None] = typer.Option(
        None,
        min=MIN_MEMORY,
        max=MAX_MEMORY,
        help=(
            "Amount of memory(GB) to use for the Cortex deployment. Defaults to 16. "
            "Can be a float between 2.0 and 256.0 depending on hardware selection."
        ),
    ),
    gpu_count: Union[int, None] = typer.Option(
        None,
        min=1,
        max=MAX_GPU_COUNT,
        help=(
            "Number of GPUs to use for the Cortex deployment. Defaults to 1. "
            "Can be an integer between 1 and 8."
        ),
    ),
    python_version: str = typer.Option(
        "",
        help=(
            "Python version to use. "
            "Currently, we support '3.8' to '3.11'. Defaults to '3.10'"
        ),
    ),
    predict: Union[str, None] = typer.Option(
        None,
        help="JSON string containing all the parameters that will be used to run your "
        "deployment's predict function on build to ensure your new deployment will work "
        "as expected before replacing your existing deployment.",
    ),
    include: str = typer.Option(
        "",
        help=(
            "Comma delimited string list of relative paths to files/folder to include. "
            "Defaults to all visible files/folders in project root."
        ),
    ),
    exclude: str = typer.Option(
        "",
        help="Comma delimited string list of relative paths to files/folder to exclude. Defaults to all hidden files/folders in project root.",
    ),
    force_rebuild: Union[bool, None] = typer.Option(
        None,
        help="Force rebuild. Clears rebuilds deployment from scratch as if it's a clean deployment.",
    ),
    config_file: str = typer.Option(
        "",
        help="Path to config.yaml file. You can generate a config using `cerebrium init-cortex`. The contents of the deployment config file are overridden by the command line arguments.",
    ),
    log_level: Union[str, None] = typer.Option(
        None, help="Log level for the Cortex build. Can be one of 'DEBUG' or 'INFO'"
    ),
    disable_predict: Union[bool, None] = typer.Option(
        None, help="Flag to disable running predict function."
    ),
    disable_animation: Union[bool, None] = typer.Option(
        None,
        help="Whether to use TQDM and yaspin animations.",
    ),
    disable_build_logs: bool = typer.Option(
        False, help="Whether to disable build logs during a deployment."
    ),
    hide_public_endpoint: bool = typer.Option(
        False,
        help="Whether to hide the public endpoint of the deployment when printing the logs.",
    ),
):
    """
    Build and run your Cortex files on Cerebrium to verify that they're working as expected.
    """
    setup_app(
        name=name,
        api_key=api_key,
        hardware=hardware,
        cpu=cpu,
        memory=memory,
        gpu_count=gpu_count,
        python_version=python_version,
        include=include,
        exclude=exclude,
        force_rebuild=force_rebuild,
        log_level=log_level,
        disable_animation=disable_animation,
        disable_build_logs=disable_build_logs,
        disable_predict_data=disable_predict,
        disable_syntax_check=disable_syntax_check,
        hide_public_endpoint=hide_public_endpoint,
        config_file=config_file,
        cerebrium_function="run",
        predict_data=predict,
    )
