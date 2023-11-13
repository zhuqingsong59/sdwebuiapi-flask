import os
from datetime import datetime
from huggingface_hub import snapshot_download
from ia_logging import ia_logging


class IAFileManager:
    DOWNLOAD_COMPLETE = "Download complete"

    def __init__(self) -> None:
        self._ia_outputs_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                            "outputs",
                                            datetime.now().strftime("%Y-%m-%d"))

        self._ia_models_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "models")

    @property
    def outputs_dir(self) -> str:
        """Get inpaint-anything outputs directory.

        Returns:
            str: inpaint-anything outputs directory
        """
        if not os.path.isdir(self._ia_outputs_dir):
            os.makedirs(self._ia_outputs_dir, exist_ok=True)
        return self._ia_outputs_dir

    @property
    def models_dir(self) -> str:
        """Get inpaint-anything models directory.

        Returns:
            str: inpaint-anything models directory
        """
        if not os.path.isdir(self._ia_models_dir):
            os.makedirs(self._ia_models_dir, exist_ok=True)
        return self._ia_models_dir

    @property
    def savename_prefix(self) -> str:
        """Get inpaint-anything savename prefix.

        Returns:
            str: inpaint-anything savename prefix
        """
        return datetime.now().strftime("%Y%m%d-%H%M%S")


ia_file_manager = IAFileManager()


def download_model_from_hf(hf_model_id, local_files_only=False):
    """Download model from HuggingFace Hub.

    Args:
        sam_model_id (str): HuggingFace model id
        local_files_only (bool, optional): If True, use only local files. Defaults to False.

    Returns:
        str: download status
    """
    if not local_files_only:
        ia_logging.info(f"Downloading {hf_model_id}")
    try:
        snapshot_download(repo_id=hf_model_id, local_files_only=local_files_only)
    except FileNotFoundError:
        return f"{hf_model_id} not found, please download"
    except Exception as e:
        return str(e)

    return IAFileManager.DOWNLOAD_COMPLETE
