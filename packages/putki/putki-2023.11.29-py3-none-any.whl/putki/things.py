"""Identification of parts given an area and perspectives from the declaration of structures."""
import os
import pathlib
import sys
from typing import Any, Union

import yaml

# server
PIPE_TOOL_BASE = pathlib.Path('/opt/pipe')
PIPE_NAME = 'pipe'
PIPE_SRC = PIPE_TOOL_BASE / PIPE_NAME
PIPE_PERMS = 0o755
LOG_HEAD_NAME = 'log_head.html'
LOG_HEAD_SRC = PIPE_TOOL_BASE / LOG_HEAD_NAME
LOG_TAIL_NAME = 'log_tail.html'
LOG_TAIL_SRC = PIPE_TOOL_BASE / LOG_TAIL_NAME
LOG_PERMS = 0o644

# client
STRUCTURE = 'structure'
STRUCTURES = f'{STRUCTURE}s'


def read_structures(path: Union[str, pathlib.Path]) -> Union[dict[str, dict[str, str]], Any]:
    """Return the data of the structures."""
    with open(path, 'rt', encoding='utf-8') as handle:
        return yaml.safe_load(handle)


def elucidate(area: str, perspectives: list[str]) -> int:
    """Discover and verify the parts of the given area and perspectives."""
    if not area:
        return 2
    if not perspectives:
        return 2
    d = read_structures(f'{STRUCTURES}.yml')
    s = d[STRUCTURES]
    parts = []
    for k, v in s.items():
        val = v.strip()
        if val.startswith(f'{area}/') and val.endswith(f'/{STRUCTURES}.yml'):
            p = val.replace(f'{area}/', '').replace(f'/{STRUCTURES}.yml', '')
            if p not in parts:
                parts.append(p)
    parts.sort()

    for part in parts:
        print(f'{area} {part}:', file=sys.stderr)
        part_path = pathlib.Path(area) / part
        if not part_path.is_dir():
            print('- folder is missing in file system', file=sys.stderr)
        else:
            print('+ folder present in file system', file=sys.stderr)
            part_structure_path = part_path / f'{STRUCTURES}.yml'
            if not part_structure_path.is_file():
                print(f'  - folder is missing the {STRUCTURES}.yml file', file=sys.stderr)
            else:
                print(f'  + folder provides a {STRUCTURES}.yml file', file=sys.stderr)
                print(f'    perspectives of {part}:', file=sys.stderr)
                cd = read_structures(part_structure_path)
                cs = cd[STRUCTURES]
                for k, v in cs.items():
                    val = v.strip()
                    vp = part_path / val
                    if not vp.is_file():
                        print(f'    - {STRUCTURE} path ({vp}) does not exist - skipping target ({k})', file=sys.stderr)
                        continue
                    known = False
                    for perspective in perspectives:
                        if val == f'{perspective}/{STRUCTURE}.yml':
                            known = True
                            print(f'    + target ({k}) -> {perspective}', file=sys.stderr)
                            perspective_pdf_path = part_path / perspective / 'render/pdf'
                            if not perspective_pdf_path.is_dir():
                                print(f'      - is missing {perspective} render folder', file=sys.stderr)
                                render_path = perspective_pdf_path
                                render_path.mkdir(parents=True, exist_ok=True)

                                src = PIPE_SRC
                                dest = render_path / PIPE_NAME
                                dest.write_text(src.read_text())
                                os.chmod(dest, PIPE_PERMS)

                                print(f'        * created {perspective} pipe script at ({dest})', file=sys.stderr)

                                src = LOG_HEAD_SRC
                                dest = render_path / LOG_HEAD_NAME
                                dest.write_text(src.read_text())
                                os.chmod(dest, LOG_PERMS)

                                src = PIPE_SRC
                                dest = render_path / LOG_TAIL_NAME
                                dest.write_text(src.read_text())
                                os.chmod(dest, LOG_PERMS)
                            else:
                                print(f'      + has {perspective} render folder', file=sys.stderr)
                    if not known:
                        print(f'    ? ignored target ({k}) --> ({val})', file=sys.stderr)

    print(' '.join(parts))

    return 0


if __name__ == '__main__':
    sys.exit(elucidate(sys.argv[1], sys.argv[2:]))
