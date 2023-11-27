"""Main module to perform mapping"""

from map_apply.file_handler import open_file_if_exists, get_file_format


def clean_data(f, separator):
    """  splits, removes emptiness, new lines and BOM signature """
    lines = []
    for line_number, line in enumerate(f):

        list_line = [
            l.strip()
            .strip('\n')
            .strip('\ufeff')  # remove BOM from utf-8
            for l in line.split(separator)
        ]

        lines.append(list_line)

    return lines


# TODO - optimize algorithm
def find_substitution(search, mapping):
    # mapping - is a list of lists w/ 2 values
    # we need to find a line with the [0] that equals to search
    for number, line in enumerate(mapping):
        if line[0] == search:
            return line[1], number
    return None, None

# def get_new_filename(source_filename):
#
#     if get_file_format(source_filename).upper() == CSV.upper():
#
#     else:
#         raise
#
#


def apply_map(source_file, new_file, mapping, separator):

    # ROADMAP
    # Sort the source data file
    # improve the replacement search algorithm

    for line_number, line in enumerate(source_file):

        if line_number == 0:  # always write the header
            new_file.write(line)
            continue

        replacement, lnumb = find_substitution(line.split(separator)[0], mapping)
        if not replacement:
            continue
        else:  # remove used element from mapping
            del mapping[lnumb]

            li = [
                f'{replacement}'
                f'{separator}',
                *[
                    f'{x}{separator}'
                    for x
                    in line.split(separator)[1:]
                ]
            ]

            # line ends with \n
            # but our manipulation put SEPARATOR in the end of a line - \nSEPARATOR
            # eg:
            # 'ea9f45f4-706a-11eb-94e9-b06ebf391e91\n\t'
            if li[-1].endswith(f'\n{separator}'): # so we need to remove the last separator
                # eg:
                # 'ea9f45f4-706a-11eb-94e9-b06ebf391e91\n'
                li[-1] = f'{li[-1][:-2]}\n'



            new_file.writelines(
                li
            )


def map_apply(input_file, map_file, separator, out_file):

    if not out_file:
        out_file = f'{input_file}.out'

    # read the map and sort it
    with open_file_if_exists(map_file) as mf:  # fm - map_file
        sorted_map = sorted(
            clean_data(mf, separator),
            key=lambda x: x[0]
        )

    # creating a new file
    with open(f'{out_file}', mode='w+', encoding='utf-8') as nf:  # nf - new file
        with open_file_if_exists(input_file) as inf:  # inf - input_file
            apply_map(source_file=inf,
                      new_file=nf,
                      mapping=sorted_map,
                      separator=separator)

    return True
