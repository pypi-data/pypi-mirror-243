import argparse
import os
from argparse import Namespace
import torch
import pandas as pd
from torch.utils.data import DataLoader
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import sys
from tqdm import tqdm
import vtk

import src.saxi_eval as saxi_eval
import src.saxi_predict as saxi_predict
from src.saxi_folds import bcolors, get_argparse_dict
from src.saxi_dataset import SaxiDataset
from src.saxi_transforms import RandomRotation
from src.utils import ReadSurf, PolyDataToTensors
import src.saxi_nets as saxi_nets
import src.utils as utils


def main(args):
    print(bcolors.INFO, "Start evaluation of the model")
    out_channels = 34
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
    
    if args.model is None:
        model = saxi_nets.DentalModelSeg(args, out_channels, config_path)
    else:
        model = args.model

    # Check if the input is a vtk file or a csv file
    if args.csv:
        # If it is a csv file, we call saxi_predict.py
        saxi_predict_args = get_argparse_dict(saxi_predict.get_argparse())
        saxi_predict_args['csv'] = args.csv
        saxi_predict_args['model'] = model
        saxi_predict_args['nn'] = "SaxiSegmentation"
        saxi_predict_args['out'] = args.out
        saxi_predict_args = Namespace(**saxi_predict_args)
        fname = os.path.basename(args.csv)
        out_prediction = os.path.join(saxi_predict_args.out, os.path.basename(args.model), fname.replace(".csv", "_prediction" + ".csv"))
        saxi_predict.main(saxi_predict_args)

    elif args.vtk:
        # If it is a vtk file, we run these lines, the changes are in the last lines to save the data
        fname = os.path.basename(args.vtk) 
        df = pd.DataFrame([{"surf": args.vtk, "out": args.out}])
        ds = SaxiDataset(df, transform=RandomRotation(), surf_column="surf")
        dataloader = DataLoader(ds, batch_size=1, num_workers=args.num_workers, persistent_workers=True, pin_memory=True)
        device = torch.device('cuda')
        model.to(device)
        model.eval()
        softmax = torch.nn.Softmax(dim=2)

        with torch.no_grad():
            for idx, batch in tqdm(enumerate(dataloader), total=len(dataloader)):
                # The generated CAM is processed and added to the input surface mesh (surf) as a point data array
                V, F, CN = batch
                V = V.cuda(non_blocking=True)
                F = F.cuda(non_blocking=True)
                CN = CN.cuda(non_blocking=True).to(torch.float32)
                x, X, PF = model((V, F, CN))
                x = softmax(x*(PF>=0))
                P_faces = torch.zeros(out_channels, F.shape[1]).to(device)
                V_labels_prediction = torch.zeros(V.shape[1]).to(device).to(torch.int64)
                PF = PF.squeeze()
                x = x.squeeze()

                for pf, pred in zip(PF, x):
                    P_faces[:, pf] += pred

                P_faces = torch.argmax(P_faces, dim=0)
                faces_pid0 = F[0,:,0]
                V_labels_prediction[faces_pid0] = P_faces
                surf = ds.getSurf(idx)
                V_labels_prediction = numpy_to_vtk(V_labels_prediction.cpu().numpy())
                V_labels_prediction.SetName('PredictedID')
                surf.GetPointData().AddArray(V_labels_prediction)

                if not os.path.exists(args.out):
                    os.makedirs(args.out)        

                # Modify this line to save the result with the desired name
                output_fn = os.path.join(args.out, f"{os.path.splitext(fname)[0]}_prediction.vtk")

                # Save the result
                vtk_writer = vtk.vtkPolyDataWriter()
                vtk_writer.SetFileName(output_fn)
                vtk_writer.SetInputData(surf)
                vtk_writer.Write()


# Add 'array_name' argument to specify the name of the output array
def get_argparse():
    parser = argparse.ArgumentParser(description='Evaluate classification result')
    parser.add_argument('--model', type=str, help='Path to the model', default=None)
    parser.add_argument('--vtk', type=str, help='Path to your vtk file', default=None)
    parser.add_argument('--csv', type=str, help='Path to your csv file', default=None)
    parser.add_argument('--out', help='Output directory', type=str, default="./prediction")
    parser.add_argument('--num_workers', help='Number of workers for loading', type=int, default=4)


    if '--vtk' in sys.argv and '--csv' in sys.argv:
        parser.error("Only one of --vtk or --csv should be provided, not both.")

    return parser

def cml():
    parser = get_argparse()
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cml()