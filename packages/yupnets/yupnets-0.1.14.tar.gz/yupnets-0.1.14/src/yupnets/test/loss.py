import torch
from torch import nn
from torch.utils.data import DataLoader
import tqdm

from .utils import _desc

__all__ = [
    "LossTest",
]


class LossTest:
    def __init__(
            self,
            batch_size: int = 1,
            use_cuda: bool = False,
            verbose: bool = False,
    ) -> None:
        self.batch_size = batch_size
        self.use_cuda = use_cuda
        self.machine = "cuda" if use_cuda else "cpu"
        self.verbose = verbose

        self.criterion = nn.CrossEntropyLoss(reduction="none")

    def __call__(
            self,
            model,
            dataset,
    ) -> torch.Tensor:
        dataloader = DataLoader(
            dataset=dataset,
            batch_size=self.batch_size,
        )
        model = getattr(model, self.machine)()

        losses = []

        for (data, targets) in tqdm.tqdm(
                dataloader,
                desc=_desc(f"Loss test", model, dataset),
                disable=not self.verbose,
        ):
            data, targets = data.to(self.machine), targets.to(self.machine)

            outputs = model(data).detach()

            loss = self.criterion(outputs, targets)
            losses.append(loss)

        return torch.cat(losses, dim=0)
