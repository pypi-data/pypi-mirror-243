"""
PyTorch MRNN model for the time-series imputation task.
Some part of the code is from https://github.com/WenjieDu/SAITS.

"""

# Created by Wenjie Du <wenjay.du@gmail.com>
# License: BSD-3-Clause


from typing import Union, Optional

import h5py
import numpy as np
import torch
from torch.utils.data import DataLoader

from .data import DatasetForMRNN
from .modules import _MRNN
from ..base import BaseNNImputer
from ...optim.adam import Adam
from ...optim.base import Optimizer
from ...utils.logging import logger


class MRNN(BaseNNImputer):
    """The PyTorch implementation of the MRNN model :cite:`yoon2019MRNN`.

    Parameters
    ----------
    rnn_hidden_size :
        The size of the RNN hidden state, also the number of hidden units in the RNN cell.

    batch_size :
        The batch size for training and evaluating the model.

    epochs :
        The number of epochs for training the model.

    patience :
        The patience for the early-stopping mechanism. Given a positive integer, the training process will be
        stopped when the model does not perform better after that number of epochs.
        Leaving it default as None will disable the early-stopping.

    optimizer :
        The optimizer for model training.
        If not given, will use a default Adam optimizer.

    num_workers :
        The number of subprocesses to use for data loading.
        `0` means data loading will be in the main process, i.e. there won't be subprocesses.

    device :
        The device for the model to run on. It can be a string, a :class:`torch.device` object, or a list of them.
        If not given, will try to use CUDA devices first (will use the default CUDA device if there are multiple),
        then CPUs, considering CUDA and CPU are so far the main devices for people to train ML models.
        If given a list of devices, e.g. ['cuda:0', 'cuda:1'], or [torch.device('cuda:0'), torch.device('cuda:1')] , the
        model will be parallely trained on the multiple devices (so far only support parallel training on CUDA devices).
        Other devices like Google TPU and Apple Silicon accelerator MPS may be added in the future.

    saving_path :
        The path for automatically saving model checkpoints and tensorboard files (i.e. loss values recorded during
        training into a tensorboard file). Will not save if not given.

    model_saving_strategy :
        The strategy to save model checkpoints. It has to be one of [None, "best", "better"].
        No model will be saved when it is set as None.
        The "best" strategy will only automatically save the best model after the training finished.
        The "better" strategy will automatically save the model during training whenever the model performs
        better than in previous epochs.

    References
    ----------
    .. [1] `J. Yoon, W. R. Zame and M. van der Schaar,
        "Estimating Missing Data in Temporal Data Streams Using Multi-Directional Recurrent Neural Networks,"
        in IEEE Transactions on Biomedical Engineering,
        vol. 66, no. 5, pp. 1477-1490, May 2019, doi: 10.1109/TBME.2018.2874712.
        <https://arxiv.org/pdf/1711.08742>`_

    """

    def __init__(
        self,
        n_steps: int,
        n_features: int,
        rnn_hidden_size: int,
        batch_size: int = 32,
        epochs: int = 100,
        patience: Optional[int] = None,
        optimizer: Optional[Optimizer] = Adam(),
        num_workers: int = 0,
        device: Optional[Union[str, torch.device, list]] = None,
        saving_path: str = None,
        model_saving_strategy: Optional[str] = "best",
    ):
        super().__init__(
            batch_size,
            epochs,
            patience,
            num_workers,
            device,
            saving_path,
            model_saving_strategy,
        )

        self.n_steps = n_steps
        self.n_features = n_features
        self.rnn_hidden_size = rnn_hidden_size

        # set up the model
        self.model = _MRNN(
            self.n_steps,
            self.n_features,
            self.rnn_hidden_size,
            self.device,
        )
        self._send_model_to_given_device()
        self._print_model_size()

        # set up the optimizer
        self.optimizer = optimizer
        self.optimizer.init_optimizer(self.model.parameters())

    def _assemble_input_for_training(self, data: list) -> dict:
        # fetch data
        (
            indices,
            X,
            missing_mask,
            deltas,
            back_X,
            back_missing_mask,
            back_deltas,
        ) = self._send_data_to_given_device(data)

        # assemble input data
        inputs = {
            "indices": indices,
            "forward": {
                "X": X,
                "missing_mask": missing_mask,
                "deltas": deltas,
            },
            "backward": {
                "X": back_X,
                "missing_mask": back_missing_mask,
                "deltas": back_deltas,
            },
        }

        return inputs

    def _assemble_input_for_validating(self, data: list) -> dict:
        return self._assemble_input_for_training(data)

    def _assemble_input_for_testing(self, data: list) -> dict:
        return self._assemble_input_for_validating(data)

    def fit(
        self,
        train_set: Union[dict, str],
        val_set: Optional[Union[dict, str]] = None,
        file_type: str = "h5py",
    ) -> None:
        # Step 1: wrap the input data with classes Dataset and DataLoader
        training_set = DatasetForMRNN(
            train_set, return_labels=False, file_type=file_type
        )
        training_loader = DataLoader(
            training_set,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
        )
        val_loader = None
        if val_set is not None:
            if isinstance(val_set, str):
                with h5py.File(val_set, "r") as hf:
                    # Here we read the whole validation set from the file to mask a portion for validation.
                    # In PyPOTS, using a file usually because the data is too big. However, the validation set is
                    # generally shouldn't be too large. For example, we have 1 billion samples for model training.
                    # We won't take 20% of them as the validation set because we want as much as possible data for the
                    # training stage to enhance the model's generalization ability. Therefore, 100,000 representative
                    # samples will be enough to validate the model.
                    val_set = {
                        "X": hf["X"][:],
                        "X_intact": hf["X_intact"][:],
                        "indicating_mask": hf["indicating_mask"][:],
                    }

            # check if X_intact contains missing values
            if np.isnan(val_set["X_intact"]).any():
                val_set["X_intact"] = np.nan_to_num(val_set["X_intact"], nan=0)
                logger.warning(
                    "X_intact shouldn't contain missing data but has NaN values. "
                    "PyPOTS has imputed them with zeros by default to start the training for now. "
                    "Please double-check your data if you have concerns over this operation."
                )

            val_set = DatasetForMRNN(val_set, return_labels=False, file_type=file_type)
            val_loader = DataLoader(
                val_set,
                batch_size=self.batch_size,
                shuffle=False,
                num_workers=self.num_workers,
            )

        # Step 2: train the model and freeze it
        self._train_model(training_loader, val_loader)
        self.model.load_state_dict(self.best_model_dict)
        self.model.eval()  # set the model as eval status to freeze it.

        # Step 3: save the model if necessary
        self._auto_save_model_if_necessary(training_finished=True)

    def predict(
        self,
        test_set: Union[dict, str],
        file_type="h5py",
    ) -> dict:
        self.model.eval()  # set the model as eval status to freeze it.
        test_set = DatasetForMRNN(test_set, return_labels=False, file_type=file_type)
        test_loader = DataLoader(
            test_set,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
        )
        imputation_collector = []

        with torch.no_grad():
            for idx, data in enumerate(test_loader):
                inputs = self._assemble_input_for_testing(data)
                results = self.model.forward(inputs, training=False)
                imputed_data = results["imputed_data"]
                imputation_collector.append(imputed_data)

        imputation = torch.cat(imputation_collector).cpu().detach().numpy()
        result_dict = {
            "imputation": imputation,
        }
        return result_dict

    def impute(
        self,
        X: Union[dict, str],
        file_type="h5py",
    ) -> np.ndarray:
        """Impute missing values in the given data with the trained model.

        Warnings
        --------
        The method impute is deprecated. Please use `predict()` instead.

        Parameters
        ----------
        X :
            The data samples for testing, should be array-like of shape [n_samples, sequence length (time steps),
            n_features], or a path string locating a data file, e.g. h5 file.

        file_type :
            The type of the given file if X is a path string.

        Returns
        -------
        array-like, shape [n_samples, sequence length (time steps), n_features],
            Imputed data.
        """
        logger.warning(
            "🚨DeprecationWarning: The method impute is deprecated. Please use `predict` instead."
        )
        results_dict = self.predict(X, file_type=file_type)
        return results_dict["imputation"]
