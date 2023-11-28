from pyiron_lammps.decorator import calculation
from atomistics.workflows import (
    ElasticMatrixWorkflow,
    EnergyVolumeCurveWorkflow,
    optimize_positions_and_volume,
)


def _run_simulation(structure, potential_dataframe, input_template, lmp):
    # write structure to LAMMPS
    lmp.interactive_structure_setter(
        structure=structure,
        units="metal",
        dimension=3,
        boundary=" ".join(["p" if coord else "f" for coord in structure.pbc]),
        atom_style="atomic",
        el_eam_lst=potential_dataframe.Species,
        calc_md=False,
    )

    # execute calculation
    for c in potential_dataframe.Config:
        lmp.interactive_lib_command(c)

    for l in input_template.split("\n"):
        lmp.interactive_lib_command(l)

    return lmp


def _optimize_structure_optional(
    lmp, structure, potential_dataframe, minimization_activated=True
):
    if minimization_activated:
        return optimize_structure(
            lmp=lmp, structure=structure, potential_dataframe=potential_dataframe
        )
    else:
        return structure


@calculation
def optimize_structure(lmp, structure, potential_dataframe):
    from atomistics.calculators import evaluate_with_lammps_library

    task_dict = optimize_positions_and_volume(structure=structure)
    structure_copy = evaluate_with_lammps_library(
        task_dict=task_dict,
        potential_dataframe=potential_dataframe,
        lmp=lmp,
        lmp_optimizer_kwargs={},
    )["structure_with_optimized_positions_and_volume"]

    # clean memory
    lmp.interactive_lib_command("clear")
    return structure_copy


@calculation
def calculate_elastic_constants(
    lmp,
    structure,
    potential_dataframe,
    num_of_point=5,
    eps_range=0.005,
    sqrt_eta=True,
    fit_order=2,
    minimization_activated=False,
):
    lammps_input_template_minimize_pos = """\
variable thermotime equal 100
thermo_style custom step temp pe etotal pxx pxy pxz pyy pyz pzz vol
thermo_modify format float %20.15g
thermo ${thermotime}
min_style cg
minimize 0.0 0.0001 100000 10000000"""

    # Optimize structure
    structure_opt = _optimize_structure_optional(
        lmp=lmp,
        structure=structure,
        potential_dataframe=potential_dataframe,
        minimization_activated=minimization_activated,
    )

    # Generate structures
    calculator = ElasticMatrixWorkflow(
        structure=structure_opt.copy(),
        num_of_point=num_of_point,
        eps_range=eps_range,
        sqrt_eta=sqrt_eta,
        fit_order=fit_order,
    )
    structure_dict = calculator.generate_structures()

    # run calculation
    energy_tot_lst = {}
    for key, struct in structure_dict["calc_energy"].items():
        lmp = _run_simulation(
            lmp=lmp,
            structure=struct,
            potential_dataframe=potential_dataframe,
            input_template=lammps_input_template_minimize_pos,
        )
        energy_tot_lst[key] = lmp.interactive_energy_tot_getter()
        lmp.interactive_lib_command("clear")

    # fit
    calculator.analyse_structures({"energy": energy_tot_lst})
    return calculator._data["C"]


@calculation
def calculate_energy_volume_curve(
    lmp,
    structure,
    potential_dataframe,
    num_points=11,
    fit_type="polynomial",
    fit_order=3,
    vol_range=0.05,
    axes=("x", "y", "z"),
    strains=None,
    minimization_activated=False,
):
    lammps_input_calc_static = """\
variable thermotime equal 100
thermo_style custom step temp pe etotal pxx pxy pxz pyy pyz pzz vol
thermo_modify format float %20.15g
thermo ${thermotime}
run 0"""

    # Optimize structure
    structure_opt = _optimize_structure_optional(
        lmp=lmp,
        structure=structure,
        potential_dataframe=potential_dataframe,
        minimization_activated=minimization_activated,
    )

    # Generate structures
    calculator = EnergyVolumeCurveWorkflow(
        structure=structure_opt.copy(),
        num_points=num_points,
        fit_type=fit_type,
        fit_order=fit_order,
        vol_range=vol_range,
        axes=axes,
        strains=strains,
    )
    structure_dict = calculator.generate_structures()

    # run calculation
    energy_tot_lst = {}
    for key, struct in structure_dict["calc_energy"].items():
        lmp = _run_simulation(
            lmp=lmp,
            structure=struct,
            potential_dataframe=potential_dataframe,
            input_template=lammps_input_calc_static,
        )
        energy_tot_lst[key] = lmp.interactive_energy_tot_getter()
        lmp.interactive_lib_command("clear")

    # fit
    calculator.analyse_structures({"energy": energy_tot_lst})
    return calculator.fit_dict
