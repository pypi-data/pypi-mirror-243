"""PTR Command Line Interface module."""
import os
import sys
import shutil as sh
from argparse import ArgumentParser

from .utils import create_structure
from .utils import remove_directory_if_empty

from osve import osve


def execute(root_scenario_path, session_file_path):
    sim = osve.osve()
    execution = sim.execute(root_scenario_path, session_file_path)
    return execution


def cli(test=False):
    """CLI Resolve a PTR and generate a SPICE CK."""
    parser = ArgumentParser(description='Pointing Tool Wrapper (PTWrapper) simulates a PTR and generates the corresponding resolved PTR, SPICE CK kernels,'
                                        'and other attitude related files. PTWrapper uses OSVE to simulate the PTR.')

    # Exclusive group for session-file and the other parameters
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    exclusive_group.add_argument("-s", "--session-file", help="Path to the session file to run the simulation. "
                                 "If provided the other arguments are ignored.")

    parser.add_argument("-m", "--meta-kernel", help="Path to the meta-kernel file.")
    parser.add_argument("-p", "--ptr", help="Path to the PTR/PTX file input file.")
    parser.add_argument("-w", "--working-dir", default=os.getcwd(),
                        help="Path to the working directory. Default is the current directory.")
    parser.add_argument("-o", "--output-dir", help="Path to the output directory. Overwrites "
                        "default output file names. Default is the structure of the built-in session file.")
    parser.add_argument("-t", "--time-step", default=5,
                        help="Output CK file time step in seconds. Default is 5s.")
    parser.add_argument("-np", "--no-power", action="store_true", help="Indicates not to calculate available power. "
                        "Default is that the Available Power will be computed.")
    parser.add_argument("-sa", "--sa-ck", action="store_true", help="Generate the Solar Arrays SPICE CK. "
                        "Default is that the SA CK is not generated.")
    parser.add_argument("-mga", "--mga-ck", action="store_true", help="Generate the Medium Gain Antenna SPICE CK. "
                        "Default is that the MGA CK is not generated.")
    parser.add_argument("-q", "--quaternions", action="store_true", help="Calculate the quaternions. "
                        "Default is that the quaternions will not be computed.")
    parser.add_argument("-f", "--fixed-definitions",
                        help="Print the AGM Fixed Definitions in use for PTR design.",
                        action="store_true")
    parser.add_argument("-v", "--version",
                        help="OSVE, AGM, and EPS libraries version.",
                        action="store_true")

    args = parser.parse_args()

    # Process the arguments and perform further actions
    if args.version:
        the_osve = osve.osve()
        print("")
        print("OSVE LIB VERSION:       ", the_osve.get_app_version())
        print("OSVE AGM VERSION:       ", the_osve.get_agm_version())
        print("OSVE EPS VERSION:       ", the_osve.get_eps_version())
        print("")
        sys.exit(1)

    if args.fixed_definitions:
        fixed_definitions_filepath = os.path.join(
            os.path.dirname(__file__), "config/age", "cfg_agm_jui_multibody_fixed_definitions.xml"
        )
        try:
            with open(fixed_definitions_filepath, 'r') as file:
                content = file.read()
                print(content)
        except FileNotFoundError:
            print("The file could not be found.")
        except Exception as e:
            print("An error occurred:", e)
        sys.exit(1)

    if args.session_file:
        # Handle session-file exclusively
        # Do something with args.session_file
        session_file_path = args.session_file
        if not os.path.exists(session_file_path):
            raise ValueError("session-file does not exist")

        session_file_path = os.path.abspath(session_file_path)
        root_scenario_path = os.path.dirname(os.path.abspath(session_file_path))
    else:
        # Handle the other parameters exclusively
        if args.ptr is None:
            parser.error("PTR argument is missing")

        if args.meta_kernel is None:
            parser.error("META_KERNEL argument is missing")

        try:
            with open(args.ptr, 'r') as p:
                ptr_content = p.read()
        except FileNotFoundError:
            raise ValueError("PTR/PTX file not found")

        if not os.path.exists(args.meta_kernel):
            raise ValueError("meta-kernel does not exist")

        session_file_path = create_structure(args.working_dir, args.meta_kernel, ptr_content,
                                             step=int(args.time_step),
                                             no_power=args.no_power,
                                             sa_ck=args.sa_ck,
                                             mga_ck=args.mga_ck,
                                             quaternions=args.quaternions)
        root_scenario_path = os.path.dirname(session_file_path)

    print("PTWrapper session execution ")

    execution = execute(root_scenario_path, session_file_path)
    if execution != 0:
        print("PTWrapper session ended with ERRORS check your input files")
        if test:
            return parser
        sys.exit(-1)

    if args.output_dir:
        # Post-process the result
        fname = args.ptr.split(os.sep)[-1]
        if '.xml' in fname:
            fname = fname.split('.xml')[0]
        elif '.XML' in fname:
            fname = fname.split('.XML')[0]
        elif '.PTX' in fname:
            fname = fname.split('.PTX')[0]
        elif '.ptx' in fname:
            fname = fname.split('.ptx')[0]
        elif '.ptr' in fname:
            fname = fname.split('.ptr')[0]
        elif '.PTR' in fname:
            fname = fname.split('.PTR')[0]
        else:
            raise ValueError('Input PTR extension incorrect (not .xml, .XML ,.ptr, .PTR, .ptx or .PTX)')

        fname = fname.lower()
        mkname = args.meta_kernel.split(os.sep)[-1]
        output_dir = os.path.abspath(args.output_dir)

        if args.quaternions:
            print(f'Renaming quaternions.csv to {fname}_quaternions.csv')
            sh.move(f'{root_scenario_path}/output/quaternions.csv', f'{output_dir}/{fname}_quaternions.csv')

        if args.sa_ck:
            if os.path.exists(f'{root_scenario_path}/output/juice_sa_ptr.bc'):
                print(f'Renaming juice_sa_ptr.bc/csv to juice_sa_{fname}.bc/csv')
                sh.move(f'{root_scenario_path}/output/juice_sa_ptr.bc', f'{output_dir}/juice_sa_{fname}.bc')
                sh.move(f'{root_scenario_path}/output/juice_sa_ptr.csv', f'{output_dir}/juice_sa_{fname}.csv')
            else:
                print(f'SA CSV and CK files not generated.')

        if args.mga_ck:
            if os.path.exists(f'{root_scenario_path}/output/juice_mga_ptr.bc'):
                print(f'Renaming juice_mga_ptr.bc/csv to juice_mga_{fname}.bc/csv')
                sh.move(f'{root_scenario_path}/output/juice_mga_ptr.bc', f'{output_dir}/juice_mga_{fname}.bc')
                sh.move(f'{root_scenario_path}/output/juice_mga_ptr.csv', f'{output_dir}/juice_mga_{fname}.csv')
            else:
                print(f'MGA CSV and CK files not generated.')

        if not args.no_power:
            print(f'Renaming power.csv to {fname}_power.csv')
            sh.move(f'{root_scenario_path}/output/power.csv', f'{output_dir}/{fname}_power.csv')

        print(f'Renaming ptr_resolved.ptx to {fname}_resolved.ptx')
        sh.move(f'{root_scenario_path}/output/ptr_resolved.ptx', f'{output_dir}/{fname}_resolved.ptx')

        print(f'Renaming juice_sc_ptr.bc to {fname}.bc')
        sh.move(f'{root_scenario_path}/output/juice_sc_ptr.bc', f'{output_dir}/juice_sc_{fname}.bc')

        print(f'Renaming log.json to {fname}_log.json')
        sh.move(f'{root_scenario_path}/output/log.json', f'{output_dir}/{fname}_log.json')

        print('Cleaning up OSVE execution files and directories')
        os.remove(f'{root_scenario_path}/input/PTR_PT_V1.ptx')
        os.remove(f'{root_scenario_path}/input/downlink.evf')
        os.remove(f'{root_scenario_path}/input/TOP_events.evf')
        sh.rmtree(f'{root_scenario_path}/input/edf')
        sh.rmtree(f'{root_scenario_path}/input/itl')
        os.remove(f'{root_scenario_path}/session_file.json')
        sh.rmtree(f'{root_scenario_path}/config/age')
        sh.rmtree(f'{root_scenario_path}/config/ise')

        if args.meta_kernel != f'{root_scenario_path}/kernel/{mkname}':
            os.remove(f'{root_scenario_path}/kernel/{mkname}')

        for directory in ['kernel', 'output', 'input', 'config']:
            remove_directory_if_empty(f'{root_scenario_path}/{directory}')

    print("PTWrapper session ended successfully")

    if test:
        return parser
