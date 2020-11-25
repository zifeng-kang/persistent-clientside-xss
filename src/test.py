# Copyright (C) 2019 Ben Stock & Marius Steffens
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, sys, io, codecs
# import io
import ast
from generator import generate_exploit_for_finding
from examples.EXAMPLE1 import EXAMPLE1
from examples.EXAMPLE2 import EXAMPLE2
from examples.EXAMPLE3 import EXAMPLE3
from examples.EXAMPLE4 import EXAMPLE4
from examples.EXAMPLE5 import EXAMPLE5
from examples.EXAMPLE6 import EXAMPLE6
from pprint import pprint

sep = '---------------------'
marker = "TAINTFINDING"

def process_log(path):
    finding_list = []
    with io.open(path, 'r', encoding='iso-8859-1') as f: #, encoding='iso-8859-1', errors='ignore'
        line_list = f.read().splitlines()
        for each in line_list:
            if marker in each:
                finding = each.split(marker)[1]
                finding = finding[:finding.rfind('"')]
                try:
                    finding_list.append(ast.literal_eval(finding)) #TODO: pick unique findings
                except Exception as e: # the string cannot be parsed
                    continue
    return finding_list

def main():
    log = -1
    stem = "/media/data1/zfk/Documents/persistent-clientside-xss/"
    path = os.path.join(stem, "taintchrome/chrome/log_file")
    # Example 1 is annotated with the structure of a `finding` and `source`
    print 'Running Exploit generation on example {log}, which consist of a flow from ... ' \
          'Annotated flow can be found in examples/EXAMPLE{log}.py'
    print sep
    
    if log == 0:
        example_list = process_log(path)
        for exmpl in example_list:
            print 'Flow:'
            pprint(exmpl)
            print sep
            print 'Generated Exploit:'
            print generate_exploit_for_finding(exmpl)
        return
    elif log == -1: # get statistics
        root = os.path.join(stem, 'taintchrome/chrome/p_logs')
        finding_id = 0; id = 0 ; file_counter = 0; counts = {}
        for each_file in os.listdir(root):
            file_counter += 1
            if os.path.isfile(os.path.join(root, each_file)) and 'log_file' in each_file: # and file_counter<=1000:
                print file_counter, each_file
                each_path = os.path.join(root, each_file)
                example_list = process_log(each_path)
                for example_id, exmpl in enumerate(example_list):
                    finding_id += 1
                    print example_id
                    exmpl['finding_id'] = finding_id
                    if exmpl['sink_id'] not in counts.keys():
                        counts[exmpl['sink_id']] = {}
                    # key replacement
                    for found_source in exmpl['sources']:
                        if not type(found_source) is dict or 'hasEncodeURI' not in found_source.keys():
                            continue
                        found_source['hasEncodingURI'] = found_source.pop('hasEncodeURI')
                        found_source['hasEncodingURIComponent'] = found_source.pop('hasEncodeURIComponent')
                        id += 1
                        found_source['finding_id'] = finding_id
                        found_source['id'] = id
                        if found_source['source_name'] not in counts[exmpl['sink_id']].keys():
                            counts[exmpl['sink_id']][found_source['source_name']] = {'unexploitable':1}
                        else:
                            if 'unexploitable' not in counts[exmpl['sink_id']][found_source['source_name']].keys():
                                counts[exmpl['sink_id']][found_source['source_name']]['unexploitable'] = 1
                            else:
                                counts[exmpl['sink_id']][found_source['source_name']]['unexploitable'] += 1
                    # add back '=' in some cases
                    for i, found_cookie in enumerate(exmpl['storage']['cookies']):
                        if len(found_cookie) > 3:
                            exmpl['storage']['cookies'][i] = [found_cookie[0], '='.join(found_cookie[1:-1]),-1]
                    exploits = generate_exploit_for_finding(exmpl)
                    
                    # create distinct list for 'finding_source_id' attribute
                    source_id_list = []; new_exploits_list = []
                    for exploit in exploits:
                        if exploit['finding_source_id'] not in source_id_list:
                            source_id_list.append(exploit['finding_source_id'])
                            new_exploits_list.append(exploit)

                    # record them (distinct) into dict 'counts'
                    for exploit in new_exploits_list:
                        source_type = exploit.get('storage_type', '')
                        if source_type == '':
                            continue
                        counts[exmpl['sink_id']][source_type]['unexploitable'] -= 1
                        if 'exploitable' not in counts[exmpl['sink_id']][source_type].keys():
                            counts[exmpl['sink_id']][source_type]['exploitable'] = 1
                        else:
                            counts[exmpl['sink_id']][source_type]['exploitable'] += 1
        pprint(counts)
        print 'finding_id ', finding_id, 'id ', id
        return
    elif log == 1:
        exmpl = EXAMPLE1
    elif log == 2:
        exmpl = EXAMPLE2
    elif log == 3:
        exmpl = EXAMPLE3
    elif log == 4:
        exmpl = EXAMPLE4
    elif log == 5:
        exmpl = EXAMPLE5
    elif log == 6:
        exmpl = EXAMPLE6
    else:
        raise ValueError
    pprint(exmpl)
    print sep
    print 'Generated Exploit:'
    fff = generate_exploit_for_finding(exmpl)
    print fff

    # print len(generate_exploit_for_finding(EXAMPLE2))
    # print len(generate_exploit_for_finding(EXAMPLE3))
    # print len(generate_exploit_for_finding(EXAMPLE4))
    # print len(generate_exploit_for_finding(EXAMPLE5))
    # Example 6 generates 7 exploits due to the value ending up in the sink being '26'
    # this value can be found in various storage entries such that for each one there will be an exploit generated
    # print len(generate_exploit_for_finding(EXAMPLE6))


if __name__ == '__main__':
    main()

