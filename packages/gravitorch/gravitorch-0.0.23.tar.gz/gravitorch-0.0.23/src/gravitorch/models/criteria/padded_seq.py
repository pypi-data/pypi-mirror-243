r"""This module defines a criterion wrapper to make PyTorch criteria
compatible with ``gravitorch.models.VanillaModel`` and padded
sequences."""

from __future__ import annotations

__all__ = ["PaddedSequenceLoss"]


import torch
from torch import Tensor
from torch.nn import Module

from gravitorch import constants as ct
from gravitorch.nn import setup_module


class PaddedSequenceLoss(Module):
    r"""Implements a wrapper to adapt PyTorch loss function (a.k.a.
    criterion) to deal with zero padded sequential inputs.

    This class works for most of the PyTorch criterion that has two
    inputs: prediction and target. It assumes that the valid time
    steps of the sequence are indicated with a mask. This loss
    function should have at least two inputs:

        - the prediction which is a ``torch.Tensor`` of shape
            ``(sequence_length, batch_size, *)`` or
            ``(batch_size, sequence_length, *)`` where ``*`` means
            any number of additional dimensions. This tensor is
            converted to a tensor of shape
            ``(sequence_length * batch_size, *)`` and then feeds to
            the PyTorch loss function.
        - the target which is a ``torch.Tensor`` of shape
            ``(sequence_length, batch_size, *)`` or
            ``(batch_size, sequence_length, *)`` where ``*`` means
            any number of additional dimensions.
            This tensor is converted to a tensor of shape
            ``(sequence_length * batch_size, *)`` and then feeds to
            the PyTorch loss function.

    The input mask is optional. If no mask is provided, all the steps
    are considered as valid. The mask is a ``torch.Tensor`` of shape
    ``(sequence_length, batch_size)`` or
    ``(batch_size, sequence_length)``. The type of the tensor can be
    ``torch.int`` or``torch.long`` or``torch.float`` or ``torch.bool``
    with the following values:

        - valid value: ``True`` or ``1`` if ``valid_value=True``,
            otherwise ``False`` or ``0``.
        - invalid value: ``False`` or ``0`` if ``valid_value=True``,
            otherwise ``True`` or ``1``.

    Note that this class may not be compatible which any PyTorch
    criterion. However, you should be able to adapt this
    implementation for your use-case.

    Args:
    ----
        criterion (``torch.nn.Module`` or dict): Specifies the loss
            function or its configuration.
        prediction_key (str): Specifies the prediction key.
            Default: ``"prediction"``.
        target_key (str): Specifies the target key.
            Default: ``"target"``.
        mask_key (str): Specifies the mask key. Default: ``"mask"``.
        valid_value (bool, optional): Indicates the valid values in
            the mask. If ``True``, the valid values are indicated by
            a ``True`` in the mask. If ``False``, the valid values are
            indicated by a ``False`` in the mask.
            Default: ``True``
        mask_in_batch (bool, optional): Indicates if the mask is in
            ``batch`` or ``net_out``. If ``True``, the mask is taken
            from the input ``batch``, otherwise it is taken from the
            input ``net_out``. Default: ``True``

    Example usage:

    .. code-block:: pycon

        >>> from torch import nn
        >>> from gravitorch.models.criteria import PaddedSequenceLoss
        >>> # Init with a nn.Module
        >>> criterion = PaddedSequenceLoss(criterion=nn.MSELoss())
        >>> criterion
        PaddedSequenceLoss(
          (criterion): MSELoss()
        )
        >>> # Init with a config
        >>> criterion = PaddedSequenceLoss(criterion={"_target_": "torch.nn.MSELoss"})
        >>> criterion
        PaddedSequenceLoss(
          (criterion): MSELoss()
        )
        >>> # Customize keys.
        >>> criterion = PaddedSequenceLoss(
        ...     criterion=nn.MSELoss(),
        ...     prediction_key="my_prediction",
        ...     target_key="my_target",
        ...     mask_key="my_mask",
        ... )
        >>> criterion
        PaddedSequenceLoss(
          (criterion): MSELoss()
        )
        >>> net_out = {"my_prediction": torch.randn(2, 4)}
        >>> batch = {"my_target": torch.randn(2, 4), "my_mask": torch.ones(2, 4)}
        >>> loss = criterion(net_out, batch)
        >>> loss
        {'loss': tensor(...)}
    """

    def __init__(
        self,
        criterion: Module | dict,
        prediction_key: str = ct.PREDICTION,
        target_key: str = ct.TARGET,
        mask_key: str = ct.MASK,
        valid_value: bool = True,
        mask_in_batch: bool = True,
    ) -> None:
        super().__init__()
        self.criterion = setup_module(criterion)
        self._prediction_key = prediction_key
        self._target_key = target_key
        self._mask_key = mask_key
        self._valid_value = bool(valid_value)
        self._mask_in_batch = bool(mask_in_batch)

    def forward(self, net_out: dict, batch: dict) -> dict[str, Tensor]:
        r"""Computes the loss value given the network output and the
        batch.

        Args:
        ----
            net_out (dict ): Specifies the network output which
                contains the prediction.
            batch (dict): Specifies the batch which contains the
                target and the mask.

        Returns:
        -------
            dict: A dict with the loss value.
        """
        # See the batch of sequences as a batch of examples
        prediction = self._get_prediction_from_net_out(net_out).flatten(0, 1)
        target = self._get_target_from_batch(batch).flatten(0, 1)

        # Get the mask and remove the examples that are masked
        mask = (
            batch.get(self._mask_key, None)
            if self._mask_in_batch
            else net_out.get(self._mask_key, None)
        )
        if mask is not None:
            mask = mask.flatten().bool()
            if not self._valid_value:
                mask = torch.logical_not(mask)
            prediction = prediction[mask]
            target = target[mask]

        return {ct.LOSS: self.criterion(prediction, target)}

    def _get_prediction_from_net_out(self, net_out: dict) -> Tensor:
        r"""Gets the prediction from the network output.

        Args:
        ----
            net_out (dict): Specifies the network output which
                contains the prediction.

        Returns:
        -------
            ``torch.Tensor``: the prediction
        """
        return net_out[self._prediction_key]

    def _get_target_from_batch(self, batch: dict) -> Tensor:
        r"""Gets the target from the batch. The target is the tensor with
        the key 'target'.

        Args:
        ----
            batch (dict): Specifies the batch which contains the
                target.

        Returns:
        -------
            ``torch.Tensor``: the target
        """
        return batch[self._target_key]
