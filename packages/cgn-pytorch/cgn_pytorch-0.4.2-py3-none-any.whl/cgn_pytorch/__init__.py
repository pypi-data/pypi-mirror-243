from .contact_graspnet import CGN
import torch
import cgn_pytorch.util.config_utils as config_utils
import numpy as np
from importlib.resources import files
from torch_geometric.nn import fps


def from_pretrained(
    cpu: bool = False, checkpoint_path: str = None
) -> tuple[CGN, torch.optim.Adam, dict]:
    """Loads a pretrained model and optimizer.

    Args:

      cpu (bool, optional): Whether to force use the cpu or not.
      checkpoint_path (str, optional): The path to the checkpoint file. If None,
       a pretrained model based on https://github.com/NVlabs/contact_graspnet
         will be loaded.

    Returns:
        tuple[CGN, torch.optim.Adam, dict]: CGN model, optimizer and config dict.
    """
    print("initializing net")
    torch.cuda.empty_cache()
    config_dict = config_utils.load_config()
    device = torch.device("cuda:0" if torch.cuda.is_available() and not cpu else "cpu")
    model = CGN(config_dict, device).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    if checkpoint_path is None:
        checkpoint_path = files("cgn_pytorch").joinpath("checkpoints/current.pth")
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    print("initialized net")
    return model, optimizer, config_dict


class CgnInference(torch.nn.Module):
    """Wraps Cgn with a forward function that takes point clouds and returns a
    tuple of a list of grasps and a list of the corresponding confidence values.
    """

    def __init__(self, cgn: CGN):
        super().__init__()
        self.cgn = cgn

    def forward(self, pcd, threshold=0.5):
        # if pcd.shape[0] > 20000:
        #     downsample =torch.tensor(random.sample(range(pcd.shape[0] - 1), 20000))
        # else:
        #     downsample = torch.arange(20000)
        # pcd = pcd[downsample, :]

        # pcd = torch.Tensor(pcd).to(dtype=torch.float32).to(self.cgn.device)
        batch = torch.zeros(pcd.shape[0]).to(dtype=torch.int64).to(self.cgn.device)
        idx = fps(pcd, batch, 2048 / pcd.shape[0])
        # idx = torch.linspace(0, pcd.shape[0]-1, 2048).to(dtype=torch.int64).to(cgn.device)

        # obj_mask = torch.ones(idx.shape[0])

        points, pred_grasps, confidence, pred_widths, _, pred_collide = self.cgn(
            pcd[:, 3:], pos=pcd[:, :3], batch=batch, idx=idx
        )
        sig = torch.nn.Sigmoid()
        confidence = sig(confidence)
        confidence = confidence.reshape((-1,))
        pred_grasps = torch.flatten(pred_grasps, start_dim=0, end_dim=1)
        # confidence = (obj_mask * confidence).reshape((-1,))
        pred_widths = torch.flatten(pred_widths, start_dim=0, end_dim=1)
        points = torch.flatten(points, start_dim=0, end_dim=1)

        success_mask = (confidence > threshold).nonzero()[0]

        return pred_grasps[success_mask], confidence[success_mask]


def inference(model: CGN, pcd: np.ndarray, threshold: float = 0.5):
    """Infer grasps from a point cloud.

    Args:
        model (CGN): The model to use for inference.
        pcd (np.ndarray): The point cloud to infer grasps from.
        threshold (float, optional): The confidence threshold to use. Defaults to 0.5.

    Returns:
        tuple[np.ndarray, np.ndarray]: The inferred grasps and their confidence.
    """
    model.eval()
    wrapped_cgn = CgnInference(model)
    wrapped_cgn.eval()
    pcd = torch.Tensor(pcd).to(dtype=torch.float32).to(model.device)
    grasps, confidence = wrapped_cgn(pcd, threshold)
    grasps = grasps.cpu().detach().numpy()
    confidence = confidence.cpu().detach().numpy()
    return grasps, confidence


# def to_onnx(model: CGN, save_path: str = "contact_graspnet.onnx"):
#     dynamic_axes_dict = {
#         "input": {
#             0: "npoints",
#         },
#         "grasps": {
#             0: "ngrasps",
#         },
#         "confidence": {
#             0: "ngrasps",
#         },
#     }
#     model.eval()
#     wrapped_cgn = WrappedCGN(model)
#     wrapped_cgn.eval()
#     dummy_input = torch.randn(20000, 3)
#     torch.onnx.export(
#         wrapped_cgn,
#         dummy_input,
#         save_path,
#         verbose=False,
#         input_names=["input"],
#         output_names=["grasps", "confidence"],
#         dynamic_axes=dynamic_axes_dict,
#         export_params=True,
#     )


__all__ = ["CGN", "from_pretrained"]
