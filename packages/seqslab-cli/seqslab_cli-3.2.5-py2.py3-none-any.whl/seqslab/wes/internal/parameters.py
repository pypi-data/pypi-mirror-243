import errno
import json
import os
import re
from termcolor import cprint
from seqslab.runsheet.runsheet import RunSheet, Run
from seqslab.wes.template.base import WorkflowParamsTemplate, WorkflowBackendParamsTemplate, \
    WorkflowBackendParamsClusterTemplate
import zipfile

from seqslab.wes.internal.common import get_factory

"""
Copyright (C) 2022, Atgenomix Incorporated.

All Rights Reserved.

This program is an unpublished copyrighted work which is proprietary to
Atgenomix Incorporated and contains confidential information that is not to
be reproduced or disclosed to any other person or entity without prior
written consent from Atgenomix, Inc. in each and every instance.

Unauthorized reproduction of this program as well as unauthorized
preparation of derivative works based upon the program or distribution of
copies by sale, rental, lease or lending are violations of federal copyright
laws and state trade secret laws, punishable by civil and criminal penalties.
"""


def validate_label_column(run: Run):
    r1fqn = set(['.'.join(re.sub(r'(/\d+)*$', '', sample.Read1_Label).split('/')) for sample in run.samples])
    assert len(r1fqn) == 1
    r2fqn = set(['.'.join(re.sub(r'(/\d+)*$', '', sample.Read2_Label).split('/')) for sample in run.samples])
    assert len(r2fqn) == 1
    if not r1fqn and not r2fqn:
        raise Exception('runsheet template without Read1_Label and Read2_Label assignment')
    return r1fqn.pop(), r2fqn.pop()


def is_castable_to_int(s):
    try:
        int(s)  # Try to convert the string to an integer
        return True  # If successful, it's castable to an integer
    except ValueError:
        return False


def populate_fqn(labels: list, names: list):
    dim = []
    sample_indices = []

    for idx in range(len(labels)):
        lb1s = labels[idx].split('/')

        # label without indices => len(Samples) should be one
        if not is_castable_to_int(lb1s[-1]):
            assert len(labels) == 1
            return f'{names[idx]}.fastq.gz'

        # label with 1d indices
        if not is_castable_to_int(lb1s[-2]):
            dim.append(1)
            sample_indices.append([int(lb1s[-1]) - 1])
        else:
            if is_castable_to_int(lb1s[-3]):
                raise ValueError("SeqsLab does not support FQN higher than 2 dimension")
            dim.append(2)
            sample_indices.append([int(lb1s[-2]) - 1, int(lb1s[-1]) - 1])

    assert len(set(dim)) == 1

    if dim[0] == 2:
        d1_size = max([ind[0] for ind in sample_indices]) + 1
        d2_size = max([ind[1] for ind in sample_indices]) + 1
        ret = [['' for _ in range(d2_size)] for _ in range(d1_size)]
        for i in range(len(labels)):
            indices = sample_indices[i]
            ret[indices[0]][indices[1]] = f'{names[i]}.fastq.gz'
    else:
        d1_size = max([ind[0] for ind in sample_indices]) + 1
        ret = ['' for i in range(d1_size)]
        for i in range(len(labels)):
            index = sample_indices[i]
            ret[index[0]] = f'{names[i]}.fastq.gz'

    return ret


def workflow_params(execs_json: str, run: Run, is_runsheet_template: bool, is_single_end: bool) -> dict:
    """
        Create workflow_params.json.
    """
    # TODO: write DRS id to workflow_params based run_sheet content
    if not os.path.isfile(execs_json):
        cprint(f"{execs_json} does not exist", "red")
        return errno.ENOENT

    try:
        with open(execs_json, 'r') as f:
            t_content = json.loads(f.read())

        params = WorkflowParamsTemplate().create(
            ex_template=t_content
        )

        if is_runsheet_template:
            r1fqn, r2fqn = validate_label_column(run)
            lb1 = [sa.Read1_Label for sa in run.samples]
            lb2 = [sa.Read2_Label for sa in run.samples]
            na1 = [f'{sa.Sample_Name}_S{sa.Sample_ID}_r1.fastq.gz' for sa in run.samples]
            na2 = [f'{sa.Sample_Name}_S{sa.Sample_ID}_r2.fastq.gz' for sa in run.samples]

            if r1fqn == r2fqn:
                params["inputs"][r1fqn] = populate_fqn(lb1 + lb2, na1 + na2)
                return params
            else:
                params["inputs"][r1fqn] = populate_fqn(lb1, na1)

            if r2fqn:
                assert is_single_end is False
                params["inputs"][r2fqn] = populate_fqn(lb2, na2)
        return params
    except zipfile.BadZipfile as error:
        cprint(f"{error}", "red")
        return errno.EPIPE
    except json.JSONDecodeError as error:
        cprint(f"{error}", "red")
        return errno.EPIPE
    except KeyError as error:
        cprint(f"{error}", "red")
        return errno.ESRCH
    except LookupError as error:
        cprint(f"{error}", "red")
        return errno.ESRCH


def workflow_backend_params(execs_json: str,
                            workspace: str,
                            runtimes: str = None,
                            integrity: bool = False,
                            trust: bool = False,
                            kernel_version: str = '',
                            ) -> dict:
    """
    Create workflow_backend_params.json.
    """
    if not os.path.isfile(execs_json):
        cprint(f"{execs_json} does not exist", "red")
        return errno.ENOENT
    try:
        with open(execs_json, 'r') as f:
            execs = json.loads(f.read())
            workflow = execs.get('workflows')
            primary_obj = [item for item in workflow if item.get('file_type') == 'PRIMARY_DESCRIPTOR'][0]
            primary_workflow_name = primary_obj.get('workflow_name') if primary_obj.get(
                'workflow_name') else primary_obj.get('name').replace('.wdl', '')
            call_names_list = execs.get('calls', None)
            # use sub-workflow names if no call section given
            if not call_names_list:
                calls = [item.get('name').replace('.wdl', '') for item in workflow
                         if item.get('file_type') == 'SECONDARY_DESCRIPTOR'] + [primary_workflow_name]
            else:
                calls = call_names_list
    except json.JSONDecodeError as error:
        cprint(f"{error}", "red")
        return errno.EPIPE

    rt_dict = {}
    if not runtimes:
        rt_dict = {primary_workflow_name: 'acu-m16'}
    else:
        rtcs = runtimes.split(':')
        for rtc in rtcs:
            c = rtc.split('=')
            rt_dict[c[0]] = c[1]

    resource = get_factory().load_resource(workspace)
    clusters = []
    for k, v in rt_dict.items():
        if k not in calls:
            raise RuntimeError(f'given call name {k} not in TRS registered call name list {calls}!')
        clusters.append(WorkflowBackendParamsClusterTemplate(run_time=resource.get_runtime_setting(v),
                                                             workflow_name=k,
                                                             kernel_version=kernel_version))

    bk_template = WorkflowBackendParamsTemplate(
        graph=execs.get('graph'),
        clusters=clusters,
        workspace=workspace,
        integrity=integrity,
        trust=trust,
    )
    return bk_template

