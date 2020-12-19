# build.py

import os
from pathlib import Path

import spacy

from .version import __version__

def download_spacy_models(sizes=('sm', 'md', 'lg')):
    """ Download spacy-provided models. """

    for name in (f"en_core_web_{size}" for size in sizes):
        spacy.cli.download("en_core_web_sm")

def init_vector_models():
    """ Initialize vector models from conceptnet embeddings. """

    lang = "en"
    type_ = "vectors_numberbatch"
    vectors_loc="./data/numberbatch-en-19.08.txt"

    sizes = {
        'sm': 100000,
        'md': 250000,
        'lg': -1 }    # No pruning

    for (size, vectors) in sizes.items():
        model_name = f"{type_}_{size}"
        filename = f"{lang}_{model_name}"
        path = Path(f"./models/{filename}")

        spacy.cli.init_model(
            lang,
            path,
            vectors_loc=vectors_loc,
            vectors_name=f"{filename}.vectors",
            model_name=model_name,
            prune_vectors=vectors )

def patch_spacy_models(sizes=('sm', 'md', 'lg')):
    """ Patch spacy models to replace their word vectors. """

    vec_prefix = "vectors_numberbatch"
    new_type = "core_numberbatch"
    models = {}

    for size in sizes:
        nlp = spacy.load(f"en_core_web_{size}")
        nlp_vec = spacy.load(f"./models/en_{vec_prefix}_{size}")

        nlp.vocab.vectors = nlp_vec.vocab.vectors

        nlp.meta["name"] = f"{new_type}_{size}"
        nlp.meta["version"] = __version__
        nlp.meta["parent_package"] = "spacy_numberbatch"

        nlp.meta["description"] = ""
        nlp.meta["author"] = ""
        nlp.meta["email"] = ""
        nlp.meta["url"] = ""
        nlp.meta["license"] = ""

        nlp.to_disk(f"./models/en_{new_type}_{size}")
        models[size] = nlp

    return models

def package_all_models(sizes=('sm', 'md', 'lg')):
    """ Package models to be used by spacy.link """

    types = ["core", "vectors"]
    output_dir = "./models"

    for path in [
        f"./models/en_{type_}_numberbatch_{size}"

        for type_ in types
        for size in sizes ]:

        spacy.cli.package(path, output_dir=output_dir, force=True)

def create_tarballs(sizes=('sm', 'md', 'lg')):
    """ Package all models into tarballs. """

    types = ["core", "vectors"]
    command = "tar -czf"

    for path in [
        f"./models/en_{type_}_numberbatch_{size}-"
        + (__version__ if type_ == "core" else "0.0.0")

        for type_ in types
        for size in sizes ]:

        os.system(
            f"{command} {path}.tar.gz {path}" )

def build():
    """ Run all build steps. """

    download_spacy_models()
    init_vector_models()
    patch_spacy_models()
    package_all_models()
    create_tarballs()
