# Load packages
# 1. Standard/Built-in library imports
# 2. Related third party library imports
# 3. Local application/library specific imports.
import os
import sys
import warnings

import flopy
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interactive

os.chdir("..")

from topic_func.postprocess import *

# sys.path.append("C:/GW_GitHub/TUD_GW_MOD/basic_func")
# from basic_func.postprocess import *

warnings.filterwarnings("ignore")


def predefined_model(hk, chd_l, chd_r, prt, nlay, nr_cells, celGlo, lay_CHD):
    # Create a MODFLOW-2005 model
    model_ws = os.getcwd()
    modelname = "01_EX"
    mf = flopy.modflow.Modflow(
        modelname=modelname, exe_name="mf2005.exe", verbose=True, model_ws=model_ws
    )

    celGlo = celGlo  # Grid cell size in meters
    cells = nr_cells  # Number of cells in x and y direction
    nlay = nlay  # Number of layers
    top = 10  # Top elevation
    if nlay > 1:
        botm = np.linspace(top, 0, nlay + 1)[1:]  # Bottom elevation of each layer
    else:
        botm = [0]

    nper = 1  # Number of stress periods
    nstp = np.ones(nper)  # Number of time steps in each stress period
    perlen = 1  # [1., 3600., 86400.] # Length of each stress period
    steady = np.zeros(nper, dtype=np.bool_)  # Is each stress period steady state?
    steady[0] = 1  # Ensure stationary first stress period

    """DIS"""
    # Create the discretization package
    dis = flopy.modflow.ModflowDis(
        model=mf,  # The flopy model object
        itmuni=1,  # Time unit (1 = seconds)
        lenuni=2,  # Length unit (2 = meters)
        nlay=nlay,  # Number of layers
        nrow=cells,  # Number of rows
        ncol=cells,  # Number of columns
        delr=celGlo,  # Column spacing
        delc=celGlo,  # Row spacing
        top=top,  # Top elevation
        botm=botm,  # Bottom elevation of each layer
        nper=nper,  # Number of stress periods
        perlen=perlen,  # Simulation time
        nstp=nstp,  # Number of time steps
        steady=steady,  # Steady state simulation
    )

    # Plot the discretization
    # mapview = flopy.plot.PlotMapView(model=mf, layer=0)
    # quadmesh = mapview.plot_array(dis.top.array)
    # cbar = plt.colorbar(quadmesh)
    # cbar.ax.set_ylabel("Elevation [m]")
    # mapview.plot_grid(color="black")

    # mf.dis.plot()

    """BAS"""
    # Define the basic package
    ibound = np.ones((mf.dis.ncol, mf.dis.nrow), dtype=np.int32)  # Create ibound array
    strt = (
        np.ones((mf.dis.ncol, mf.dis.nrow), dtype=np.float32)
        * mf.dis.top.array.min()
        / 2
    )  # Create starting head array
    # Define the basic package
    bas = flopy.modflow.ModflowBas(mf, ibound=ibound, strt=strt)

    """CHD"""
    # Define the left boundary
    left_row = np.arange(0, mf.dis.nrow).tolist()
    left_col = [0] * mf.dis.ncol

    # Define the right boundary
    right_row = np.arange(0, mf.dis.nrow).tolist()
    right_col = [mf.dis.ncol - 1] * mf.dis.nrow

    # Define the heads
    left_chd = chd_l
    right_chd = chd_r

    # Write the stress period data
    spd_list = []

    for kper in range(mf.dis.nper):
        spd_kper = []

        if lay_CHD == 0:
            for lay in range(mf.dis.nlay):
                for row, col in zip(left_row, left_col):
                    # {0: [[lay, row, col, shead, ehead],
                    # print(row, col)
                    spd_layer = [[lay, row, col, left_chd, left_chd]]
                    spd_kper.extend(spd_layer)
                for row, col in zip(right_row, right_col):
                    spd_layer = [[lay, row, col, right_chd, right_chd]]
                    spd_kper.extend(spd_layer)

        else:
            for lay in [lay_CHD - 1]:
                for row, col in zip(left_row, left_col):
                    # {0: [[lay, row, col, shead, ehead],
                    # print(row, col)
                    spd_layer = [[lay, row, col, left_chd, left_chd]]
                    spd_kper.extend(spd_layer)
                for row, col in zip(right_row, right_col):
                    spd_layer = [[lay, row, col, right_chd, right_chd]]
                    spd_kper.extend(spd_layer)

        spd_list.append(spd_kper)
    stress_period_data = {kper: spd_list[kper] for kper in range(mf.dis.nper)}

    # Define the CHD package
    chd = flopy.modflow.mfchd.ModflowChd(mf, stress_period_data=stress_period_data)

    # Plot the CHD package
    # mf.chd.plot()

    """RCH"""
    # Define the RCH package (optional)
    # rch = flopy.modflow.ModflowRch(mf, rech=5e-8)  # Example recharge value

    """LPF"""
    lpf = flopy.modflow.ModflowLpf(mf, hk=hk, vka=1e-6, ipakcb=53)

    """PCG"""
    # Define the solver package
    pcg = flopy.modflow.ModflowPcg(mf)

    """OC"""
    # Define the output control package
    per_dict = {
        (kper, 0): ["print head", "save head", "save budget"]
        for kper in range(mf.dis.nper)
    }
    # create output control file using dictionary
    oc = flopy.modflow.ModflowOc(mf, stress_period_data=per_dict)

    # Write the MODFLOW model input files
    mf.write_input()
    # Check the MODFLOW model input files
    # mf.check()
    # Run the MODFLOW model
    success, buff = mf.run_model(silent=True)

    # Plot the model results
    hds_name = modelname + ".hds"

    cbc_name = modelname + ".cbc"

    hdobj = flopy.utils.HeadFile(os.path.join(model_ws, hds_name))
    cbb = flopy.utils.CellBudgetFile(os.path.join(model_ws, cbc_name))

    # Define the settings for the plot
    settings = {
        "cmap": "viridis_r",
        "cmap_show": True,
        "vmin": 7,
        "vmax": 10,
        "cmap_alpha": 0.5,
        "cbar_show": True,
        "cbar_label": "Head [m]",
        "masked_values": [-1.0e20, -2.0e20],
        "cbar_shrink": 1,
        "contour_colors": "whitesmoke",
        "cbar_rotation": 90,
        "cbar_labelpad": 10,
        "contourlabel_format": "%.1fm",
        "normalize": True,
        "vector_alpha": 0.9,
        "vector_color": "navy",
        "vector_scale": 25,
        "istep": 2,
        "jstep": 2,
        "hstep": 2,
    }

    levels = np.linspace(
        settings["vmin"],
        settings["vmax"],
        (settings["vmax"] - settings["vmin"]) * 10 + 1,
    )

    if chd_l == chd_r:
        settings["normalize"] = False
        levels = [-999]

    col = 5
    row = 10

    # Plot the model results
    mf_plot = plot_model(
        model=mf,
        layer=0,
        time=mf.dis.get_totim()[0],
        hdobj=hdobj,
        cbb=cbb,
        settings=settings,
    )

    if lay_CHD == 0:
        localx, localy, localz, partlocs = partlocs_structured_grid(
            mf,
            # cell,
            mf.chd.stress_period_data.data[0][
                int(round(mf.dis.nlay / 2, 0))
                * mf.dis.nrow
                * 2 : int(round(mf.dis.nlay / 2, 0))
                * mf.dis.nrow
                * 2
                + mf.dis.nrow * 2
            ],
            PointsOnCircle(r=0.25, N=1),
            d8=False,
            steps=3,
        )  # each

    else:
        localx, localy, localz, partlocs = partlocs_structured_grid(
            mf,
            # cell,
            mf.chd.stress_period_data.data[0],
            PointsOnCircle(r=0.25, N=1),
            d8=False,
            steps=3,
        )

    # localz = [0]
    # localz = [0] * mf.chd.stress_period_data.data[0].shape[0]

    particledata = flopy.modpath.ParticleData(
        partlocs,
        structured=True,
        localx=localx,
        localy=localy,
        localz=localz,
        timeoffset=0,
        drape=0,
    )

    pg = flopy.modpath.ParticleGroup(particledata=particledata)

    mp = flopy.modpath.Modpath7(
        modelname=f"{modelname}_modpath",
        model_ws=model_ws,
        flowmodel=mf,
        headfilename=hds_name,
        budgetfilename=cbc_name,
        exe_name="mpath7.exe",
        verbose=True,
    )

    mpbas = flopy.modpath.Modpath7Bas(mp, porosity=0.3)

    if chd_l != chd_r:
        mpsim = flopy.modpath.Modpath7Sim(
            mp,
            particlegroups=pg,
            simulationtype="pathline",  #'combined',
            # weaksinkoption='pass_through',
            weaksourceoption="pass_through",
            stoptimeoption="extend",  # "extend",  #'specified',
            trackingdirection="forward",
        )
    else:
        mpsim = flopy.modpath.Modpath7Sim(
            mp,
            particlegroups=pg,
            simulationtype="pathline",  #'combined',
            # weaksinkoption='pass_through',
            weaksourceoption="pass_through",
            stoptimeoption="specified",  # "extend",  #'specified',
            stoptime=prt * 86400,
            trackingdirection="forward",
        )
    # Write the MODPATH model input files
    mp.write_input()
    # Run the MODPATH model
    mp.run_model(silent=True)

    mppth_path = os.path.join(model_ws, f"{modelname}_modpath.mppth")

    # Create a plot
    fig, ax = plt.subplots()

    for i, t in enumerate(mf.dis.get_totim()[0:1]):
        mf_plot_ss = plot_model(
            model=mf, layer=1, time=t, hdobj=hdobj, cbb=cbb, settings=settings
        )

        mf_plot_ss.head_map(ax=ax)
        mf_plot_ss.contour_map(ax=ax, levels=levels)
        mf_plot_ss.vector_map(ax=ax, vec="specific")

    plot_pathlines_col(
        mppth_path=mppth_path,
        lw=5,
        ax=ax,
        cmap="plasma",
        vmin=0,
        vmax=prt * 86400,
        label="Particle runtime [d]",
    )

    plt.title("Map view")

    # Cross section
    fig, ax = plt.subplots()
    mf_plot.crosssection_map(
        ax=ax,
        levels=levels,
        line={"row": row},  # contour_colors="black"
    )

    plot_pathlines_col_cross(
        mppth_path=mppth_path,
        lw=10,
        ax=ax,
        cmap="plasma",
        vmin=0,
        vmax=prt * 86400,
        label="Particle runtime [d]",
    )
    plt.title("Cross section")

    modelxsect = flopy.plot.PlotCrossSection(model=mf, line={"row": row}, ax=ax)

    modelxsect.plot_bc("CHD", color="Blue", alpha=0.5)


hk_slider = widgets.FloatLogSlider(
    value=2.5e-5,
    base=10,
    min=-7,  # max of base
    max=-3,  # min exponent of base
    step=0.2,  # exponent step
    description="Kh [m/s]:",
    continuous_update=False,
)

chd_r_slider = widgets.FloatSlider(
    value=9.5,
    min=7.5,  # max
    max=10.0,  # min
    step=0.1,  # step
    description="CHD E [m]:",
    continuous_update=False,
)

chd_l_slider = widgets.FloatSlider(
    value=9.0,
    min=7.5,  # max
    max=10.0,  # min
    step=0.1,  # step
    description="CHD W [m]:",
    continuous_update=False,
)

prt_slider = widgets.FloatSlider(
    value=365,
    min=1,  # max
    max=365 * 10,  # min
    step=1,  # step
    description="P time [d]:",
    continuous_update=False,
)

nlay_slider = widgets.IntSlider(
    value=3,
    min=2,  # max
    max=10,  # min
    step=1,  # step
    description="Nr lay [-]:",
    continuous_update=False,
)

nr_cells_slider = widgets.IntSlider(
    value=20,
    min=10,  # max
    max=50,  # min
    step=1,  # step
    description="Nr cells [-]:",
    continuous_update=False,
)

celGlo_slider = widgets.IntSlider(
    value=2,
    min=1,  # max
    max=10,  # min
    step=1,  # step
    description="Cell size [m]:",
    continuous_update=False,
)

lay_CHD_slider = widgets.IntSlider(
    value=0,
    min=0,  # max
    max=10,  # min
    step=1,  # step
    description="CHD lay [-]:",
    continuous_update=False,
)
