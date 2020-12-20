# util.py

from pathlib import Path
import os
import subprocess
import sys

from .version import __version__

def _require_package(name):
    """ Helper for force reloading package cache. """
    try:
        import pkg_resources

        pkg_resources.working_set.require(name)
        return True

    except:
        return False

def _get_download_url(model_name, version=__version__):
    """ Prepare download url from github releases. """

    version = "0.0.0" if "vectors" in model_name else version

    return (
        f"https://github.com/mauna-ai/spacy-numberbatch/releases/download/"
        f"{version}/{model_name}-{version}.tar.gz" )

def _download_model(download_url):
    """ Download model using pip. """

    pip_args = ["--no-cache-dir"]
    cmd = [sys.executable, "-m", "pip", "install"] + pip_args + [download_url]

    return subprocess.call(cmd, env=os.environ.copy())

def download(type_="core", size="sm", version=__version__):
    """ Download trained models. """

    model_name = (
        type_
        if type_.startswith("en_")
        else f"en_{type_}_numberbatch_{size}" )

    download_url = _get_download_url(model_name, version)

    _download_model(download_url)

    print(
        f"Download and installation successful"
        f"You can now load the model via spacy.load('{model_name}')" )

    if not _require_package(model_name):
        print()
        print("WARNING: You may need to manually refresh the package cache.")
