import streamlit as st


st.title("Projects")
# st.write("You have entered", st.session_state["my_input"])


# provide options to either select an image form the gallery, upload one, or fetch from URL
gallery_tab, upload_tab, url_tab = st.tabs(["Gallery", "Upload", "Image URL"])

with gallery_tab:
    st.write("Gallery")

    st.title("FloPy Example:")

    import matplotlib as mpl
    import flopy

    # Load packages
    # 1. Standard/Built-in library imports
    # 2. Related third party library imports
    # 3. Local application/library specific imports.
    import os
    import sys

    import flopy
    import matplotlib.pyplot as plt
    import numpy as np
    import ipywidgets as widgets
    from ipywidgets import interactive
    import tempfile

    # from topic_func.EX_Modpath import *
    # from topic_func.postprocess import *

    # sys.path.append("C:/GW_GitHub/TUD_GW_MOD/basic_func")
    # from basic_func.postprocess import *

    # Create a MODFLOW-2005 model

    st.title("MODFLOW Simulation App")

    # Ask the user to provide a path for the working directory
    working_directory = st.text_input("Enter the path for the working directory:")

    # # Ask the user to upload an executable file
    # uploaded_file = st.file_uploader(
    #     "Upload the MODFLOW executable (EXE) file", type=["exe"]
    # )

    # # Check if a file is uploaded
    # if uploaded_file:
    #     # Create a temporary directory to store the uploaded EXE file
    #     temp_dir = st._upload_folder / st._config.report_folder / st._config.session_id
    #     os.makedirs(temp_dir, exist_ok=True)

    #     # Save the uploaded file to the temporary directory
    #     exe_path = os.path.join(temp_dir, "uploaded_modflow.exe")
    #     with open(exe_path, "wb") as exe_file:
    #         exe_file.write(uploaded_file.read())

    # # Set the working directory to the temporary directory
    # os.chdir(temp_dir)
    # Show the uploaded file
    # if uploaded_file is not None:
    #     st.write("Uploaded file:", uploaded_file.name)

    # Upload a MODFLOW exe file
    uploaded_exe = st.file_uploader("Upload a MODFLOW exe file", type="exe")

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tempdir:
        # Write the uploaded file to the temporary directory
        exe_path = os.path.join(tempdir, uploaded_exe.name)
        with open(exe_path, "wb") as f:
            f.write(uploaded_exe.getbuffer())

    st.write("Uploaded file:", exe_path)

    modelname = "01_EX"
    mf = flopy.modflow.Modflow(modelname=modelname, exe_name=exe_path, model_ws=tempdir)

    celGlo = 2  # Grid cell size in meters
    cells = 20  # Number of cells in x and y direction
    nlay = 1  # Number of layers
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
    fig, ax = plt.subplots()
    mapview = flopy.plot.PlotMapView(model=mf, layer=0)
    quadmesh = mapview.plot_array(dis.top.array)
    cbar = plt.colorbar(quadmesh)
    cbar.ax.set_ylabel("Elevation [m]")
    mapview.plot_grid(color="black")
    st.pyplot(fig)

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
    left_chd = 8
    right_chd = 9
    lay_CHD = 0

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
    lpf = flopy.modflow.ModflowLpf(mf, hk=1e-5, vka=1e-6, ipakcb=53)

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
    success, buff = mf.run_model(silent=False)
    st.write(mf.output)
