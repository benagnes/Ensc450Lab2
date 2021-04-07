#!/usr/bin/env python3
"""Slaps .cir files together to create modular simulation environment, runs simulations, and parses results."""

import sys
import re
import os

# TODO: consider using relative path instead
INC_PATH = "/local-scratch/localhome/escmc38/Desktop/ensc450/HSPICE/lab2/"
#CELL_NAMES = ["iv", "nd", "nr", "mux21", "xr"]
CELL_NAMES = ["iv", "nd", "nr", "xr", "ivlay", "ndlay", "nrlay", "xrlay"]


def gen_cir_files():
    for cell_name in CELL_NAMES:
        with open(INC_PATH + "sim_setup.cir") as f:
            sim_setup_lines = f.read()

        for trans_type in ["rise", "fall"]:
        #for trans_type in ["fall"]:
            with open(INC_PATH + "sim_{}.cir".format(trans_type)) as f:
                sim_meas_lines = f.read()


            cell_dir = INC_PATH + cell_name + "/" + trans_type + "/"

            with open(cell_dir + "sim_cells_{}.cir".format(trans_type)) as f:
                sim_cell_lines = f.read()


            sim_cir_file = "\n".join([sim_setup_lines, sim_meas_lines, sim_cell_lines])

            with open(cell_dir + "gen_{}_{}.cir".format(cell_name, trans_type), 'w') as f:
                f.write(sim_cir_file)


def run_cir_files():
    for cell_name in CELL_NAMES:
        for trans_type in ["rise", "fall"]:
        #for trans_type in ["fall"]:
            cell_dir = INC_PATH + cell_name + "/" + trans_type + "/"
            os.system("pushd " + cell_dir + " && "
                + "hspice gen_{}_{}.cir".format(cell_name, trans_type)
                + " |& tee out_{}_{}.txt".format(cell_name, trans_type)
                + " && popd")

def parse_out_files():
    parsed_lines = []

    for cell_name in CELL_NAMES:
        for trans_type in ["rise", "fall"]:
            cell_dir = INC_PATH + cell_name + "/" + trans_type + "/"
            out_file_name = cell_dir + "out_{}_{}.txt".format(cell_name, trans_type)

            cell = "empty"
            ttran = "empty"
            tpd = "empty"
            ttr = "empty"

            with open(out_file_name) as f:
                for line in f.readlines():
                    if any([
                        line.startswith(" inv_"),
                        line.startswith(" nand_"),
                        line.startswith(" nor_"),
                        line.startswith(" xor_"),
                        line.startswith(" invlay_"),
                        line.startswith(" nandlay_"),
                        line.startswith(" norlay_"),
                        line.startswith(" xorlay_")
                    ]):
                        cell = line.strip()
                        parsed_lines.append(cell)

                    if line.startswith("   *** parameter ttran =    1.000E-09 ***"):
                        ttran = "1ns"
                        parsed_lines.append(ttran)
                    elif line.startswith("   *** parameter ttran =    2.000E-09 ***"):
                        ttran = "2ns"
                        parsed_lines.append(ttran)

                    if line.startswith("   tpd=  "):
                        tpd = line.strip()
                        parsed_lines.append(tpd)
                    if line.startswith("   ttr=  "):
                        ttr = line.strip()
                        parsed_lines.append(ttr)

    #print("\n\n\n----------------------------\n\n")
    #print("\n".join(parsed_lines))

    # clean up output
    parsed_lines = "\n".join(parsed_lines)
    parsed_lines_cleaned = re.findall(r"(?:1|2)ns\n(?:inv|nand|nor|xor).*\ntpd.*\nttr.*", parsed_lines, re.MULTILINE)
    #parsed_lines_cleaned = "\n".join(parsed_lines_cleaned)
    print("\n".join(parsed_lines_cleaned))

    return parsed_lines_cleaned


def format_data_and_save(parsed_lines):
    assert len(parsed_lines) % 4 == 0, "blocks not multiple of 4"

    data_lines = []
    # for block in [parsed_lines[i:i+4] for i in range(0, len(parsed_lines), 4)]:
    for block in parsed_lines:
        block = block.splitlines()
        # line 0 is ttran
        # line 1 is cell name, drve strength, pin, and capacitance
        # line 2 is tpd
        # line 3 is ttr

        ttran = block[0]
        cell, ds, pin, edge, cap = block[1].split("_")
        tpd = "{:.3f}".format(float(re.match(r"tpd=  (\d\.\d{1,5}E-?\d{1,2})", block[2]).group(1))*1e9)
        ttr = "{:.3f}".format(float(re.match(r"ttr=  (\d\.\d{1,5}E-?\d{1,2})", block[3]).group(1))*1e9)

        data = {
            "cell": cell,
            "ds": ds,
            "pin": pin,
            "edge": edge,
            "cap": cap,
            "ttran": ttran,
            "tpd": tpd,
            "ttr": ttr
        }

        data_lines.append(data)

    #print("\n".join(map(repr,data_lines)))

    tables = []

    # for each cell
    for cell in ["inv", "nand", "nor", "xor", "invlay", "nandlay", "norlay", "xorlay"]:
        filter_cells = [entry for entry in data_lines if entry["cell"] == cell]
        # for each drive strength
        for ds in ["x1", "x4"]:
            filter_ds = [entry for entry in filter_cells if entry["ds"] == ds]
            # for each pin
            # TODO: get unique list of different pins and iterate on that, so can name pins anything
            for pin in ["a", "b", "c"]:
                filter_pins = [entry for entry in filter_ds if entry["pin"] == pin]
                if not filter_pins:
                    continue
                #print("\n".join(map(repr,filter_pins)))
                table_entry = """{}, drive strength {}, pin {} -------
                    cell_fall(Propagation_Delay{}) {{
                                index_1 ("1,  2");
                                index_2 ("2, 10");
                                values ("{},{}","{},{}");
                        }}
                    cell_rise(Propagation_Delay{}) {{
                                index_1 ("1,  2");
                                index_2 ("2, 10");
                                values ("{},{}","{},{}");
                        }}
                    fall_transition(Out_Transition{}) {{
                                index_1 ("1,  2");
                                index_2 ("2, 10");
                                values ("{},{}","{},{}");
                        }}
                    rise_transition(Out_Transition{}) {{
                                index_1 ("1,  2");
                                index_2 ("2, 10");
                                values ("{},{}","{},{}");
                        }}"""

                table_entry = table_entry.format(
                    cell,
                    ds,
                    pin,
                    "_x4" if ds == "x4" else "",
                    [d["tpd"] for d in filter_pins if all([d["edge"] == "fall", d["ttran"] == "1ns", d["cap"] == "2"])][0],
                    [d["tpd"] for d in filter_pins if all([d["edge"] == "fall", d["ttran"] == "1ns", d["cap"] == "10"])][0],
                    [d["tpd"] for d in filter_pins if all([d["edge"] == "fall", d["ttran"] == "2ns", d["cap"] == "2"])][0],
                    [d["tpd"] for d in filter_pins if all([d["edge"] == "fall", d["ttran"] == "2ns", d["cap"] == "10"])][0],

                    "_x4" if ds == "x4" else "",
                    [d["tpd"] for d in filter_pins if all([d["edge"] == "rise", d["ttran"] == "1ns", d["cap"] == "2"])][0],
                    [d["tpd"] for d in filter_pins if all([d["edge"] == "rise", d["ttran"] == "1ns", d["cap"] == "10"])][0],
                    [d["tpd"] for d in filter_pins if all([d["edge"] == "rise", d["ttran"] == "2ns", d["cap"] == "2"])][0],
                    [d["tpd"] for d in filter_pins if all([d["edge"] == "rise", d["ttran"] == "2ns", d["cap"] == "10"])][0],

                    "_x4" if ds == "x4" else "",
                    [d["ttr"] for d in filter_pins if all([d["edge"] == "fall", d["ttran"] == "1ns", d["cap"] == "2"])][0],
                    [d["ttr"] for d in filter_pins if all([d["edge"] == "fall", d["ttran"] == "1ns", d["cap"] == "10"])][0],
                    [d["ttr"] for d in filter_pins if all([d["edge"] == "fall", d["ttran"] == "2ns", d["cap"] == "2"])][0],
                    [d["ttr"] for d in filter_pins if all([d["edge"] == "fall", d["ttran"] == "2ns", d["cap"] == "10"])][0],

                    "_x4" if ds == "x4" else "",
                    [d["ttr"] for d in filter_pins if all([d["edge"] == "rise", d["ttran"] == "1ns", d["cap"] == "2"])][0],
                    [d["ttr"] for d in filter_pins if all([d["edge"] == "rise", d["ttran"] == "1ns", d["cap"] == "10"])][0],
                    [d["ttr"] for d in filter_pins if all([d["edge"] == "rise", d["ttran"] == "2ns", d["cap"] == "2"])][0],
                    [d["ttr"] for d in filter_pins if all([d["edge"] == "rise", d["ttran"] == "2ns", d["cap"] == "10"])][0]
                )
                tables.append(table_entry)


    #print("\n".join(tables))
    with open(INC_PATH + "spice_tables.txt", "w") as f:
        f.write("\n".join(tables))
        print("tables written to spice_tables.txt")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "full":
        gen_cir_files()
        run_cir_files()
    parsed_lines = parse_out_files()
    format_data_and_save(parsed_lines)

if __name__ == "__main__":
    main()

