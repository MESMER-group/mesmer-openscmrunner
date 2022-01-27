# MESMER-OpenSCM Runner, land-climate dynamics group, S.I. Seneviratne
# Copyright (c) 2021-2022 MESMER-OpenSCM Runner contributors, listed in AUTHORS, and ETH Zurich.
# Licensed under the GNU General Public License v3.0 or later; see LICENSE or https://www.gnu.org/licenses/

import datetime
import glob
import os.path

import pytest

LICENSE_TEMPLATE = """# MESMER-OpenSCM Runner, land-climate dynamics group, S.I. Seneviratne
# Copyright (c) 2021{} MESMER-OpenSCM Runner contributors, listed in AUTHORS, and ETH Zurich.
# Licensed under the GNU General Public License v3.0 or later; see LICENSE or https://www.gnu.org/licenses/"""


EXCLUDE = ["_version.py"]


def test_source_code_headers(repo_root_dir, update_copyright_notices, n_lines=None):
    n_lines = len(LICENSE_TEMPLATE.split("\n")) if n_lines is None else n_lines

    files_to_check = glob.glob(
        os.path.join(repo_root_dir, "tests", "**", "*.py"), recursive=True
    ) + glob.glob(os.path.join(repo_root_dir, "src", "**", "*.py"), recursive=True)

    files_to_check = [f for f in files_to_check if os.path.basename(f) not in EXCLUDE]

    now = datetime.datetime.now()
    current_year = now.year
    if current_year == 2021:
        license_template = LICENSE_TEMPLATE.format("")
    else:
        license_template = LICENSE_TEMPLATE.format("-{}".format(current_year))

    for f in files_to_check:
        with open(f) as fh:
            contents = fh.read()

        if not contents.startswith(license_template):
            if update_copyright_notices:
                contents = "\n".join(contents.split("\n")[n_lines:])
                contents = "{}\n\n{}".format(license_template, contents)
                with open(f, "w") as fh:
                    fh.write(contents)
            else:
                raise ValueError(
                    "Update headers in source files (failing file: {})".format(f)
                )

    if update_copyright_notices:
        pytest.skip("Updated copyright notices")
