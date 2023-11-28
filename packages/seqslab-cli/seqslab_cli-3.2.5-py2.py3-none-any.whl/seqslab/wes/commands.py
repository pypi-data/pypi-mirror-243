import errno
import json
import logging
import math
import os
import re
import random
import time
from functools import lru_cache

import requests
from nubia import argument
from nubia import command
from nubia import context
from requests_toolbelt.multipart.encoder import MultipartEncoder
from seqslab.auth.commands import BaseAuth
from seqslab.exceptions import exception_handler
from seqslab.runsheet.runsheet import RunSheet, Run
from seqslab.trs.register.common import trs_register
from seqslab.wes import __version__, API_HOSTNAME
from seqslab.wes.internal import parameters
from tenacity import retry, wait_fixed, stop_after_attempt
from termcolor import cprint

from .internal.common import get_factory

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


class BaseJobs:
    WES_PARAMETERS_URL = f"https://{API_HOSTNAME}/wes/{__version__}/schedules/parameters/"
    OPERATOR_PIPELINE_URL = f"https://{API_HOSTNAME}/wes/{__version__}/operator-pipelines/{{pipeline_id}}/"

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
    @lru_cache(maxsize=16)
    def parameter(primary_descriptor: str, zip_file: str):
        token = BaseAuth.get_token().get('tokens').get('access')
        files = {'file': (f"{os.path.basename(zip_file)}",
                          open(zip_file, 'rb'),
                          'application/zip'),
                 "PRIMARY_DESCRIPTOR": ("", primary_descriptor)}
        with requests.patch(url=BaseJobs.WES_PARAMETERS_URL,
                            files=files,
                            headers={"Authorization": f"Bearer {token}"}) as response:
            if response.status_code not in [requests.codes.ok]:
                raise requests.HTTPError(response.text)
            return json.loads(response.content)

    @property
    def proxy(self) -> str:
        """web proxy server"""
        return context.get_context().args.proxy

    @command
    @argument("working_dir",
              type=str,
              positional=False,
              description="Specify the working directory path that contains request.json.  All files end with "
                          "request.json will be identify and execute (optional)."
              )
    @argument("request_path",
              type=str,
              positional=False,
              description="Specify the request.json file to run (optional)."
              )
    @argument("response_path",
              type=str,
              positional=False,
              description="Specify the path of response.json in relation to the working directory (optional)."
              )
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    def run(self,
            workspace: str,
            working_dir: str = '',
            request_path: str = '',
            response_path: str = 'response.json'
            ) -> int:
        """
        Run a workflow by calling seqslab-api/wes/runs API.
        """

        reqs = []
        if working_dir:
            if not os.path.isdir(working_dir):
                logging.error("working dir is not a directory")
                cprint("working dir is not a directory", "red")
                return errno.EINVAL
            else:
                reqs += [os.path.join(working_dir, f) for f in os.listdir(working_dir) if os.path.isfile(
                    os.path.join(working_dir, f)) and f.endswith('request.json')]

        if request_path:
            if not os.path.isfile(request_path):
                logging.error("request_path is not a file")
                cprint("request_path is not a file", "red")
                return errno.EINVAL
            else:
                reqs += [request_path]

        if not len(reqs):
            cprint("no request.json are found", "yellow")
            return errno.EINVAL

        run_list = []

        for value in enumerate(reqs):
            # add random delay, based on reqs.index for run submission to avoid overloading SeqsLab-API server
            if value[0]:
                floor = math.log((value[0] + 1), 2)
                step = (value[0] + 1) * 0.1
                time.sleep(random.uniform(floor, floor + step))

            try:
                with open(value[1], 'r') as f:
                    request = json.load(f)
            except json.decoder.JSONDecodeError as e:
                cprint(f"given request not in json format - {e}", "red")

            mp = MultipartEncoder(
                fields={
                    "name": request.get('name'),
                    "workflow_type": request.get('workflow_type'),
                    "workflow_type_version": request.get('workflow_type_version'),
                    "workflow_url": request.get('workflow_url'),
                    'workflow_params': json.dumps(request.get('workflow_params')),
                    'workflow_backend_params': json.dumps(request.get('workflow_backend_params'))
                }
            )
            resource = get_factory().load_resource(workspace)
            ret = resource.sync_run_jobs(data=mp,
                                         headers={'Content-Type': mp.content_type},
                                         run_request_id=None,
                                         run_name=request.get('name'))
            res = json.loads(ret.content.decode('utf-8'))
            res['run_name'] = request.get('name')
            run_list.append(res)
            cprint(f"{res}", "yellow")

        return 0

    @command
    @argument("run_request_id",
              type=str,
              positional=False,
              description="Specify a previously scheduled run request ID (required). "
              )
    @argument("schedule_tag",
              type=str,
              positional=False,
              description="Specify a tag marked on previously uploaded samples for a scheduled WES run (required)."
              )
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    def schedule(self,
                 run_request_id: str,
                 schedule_tag: str,
                 workspace: str
                 ) -> int:
        """
        Run a WES run based on a previously registered run request. Typically, the run request
        is designed for a scheduled WES run, where the FQN-DRS connection of sequencing samples
        are left blank for future runtime sample-resolving. Thus, by specifying a sample-resolving rule,
        the run request can be used to serve a scheduled WES run use case.
        """
        mp = MultipartEncoder(fields={})
        resource = get_factory().load_resource(workspace)
        ret = resource.sync_run_jobs(data=mp,
                                     headers={'Content-Type': mp.content_type},
                                     run_request_id=run_request_id,
                                     run_name=schedule_tag)
        cprint(f"{ret.content.decode('utf-8')}", "yellow")
        return 0

    @command(aliases=["state"])
    @argument("run_id",
              type=str,
              positional=False,
              description="Specify a previously executed WES run ID (required)."
              )
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    def run_state(self, run_id: str, workspace: str) -> int:
        """
        Get WES run information based on run ID.
        """
        result = get_factory().load_resource(workspace).get_run_status(run_id)
        cprint(json.dumps(result), "yellow")

        return 0

    @command(aliases=["runsheet"])
    @argument("working_dir",
              type=str,
              description="Specify the absolute output directory for generated request.json for WES runs (required). ",
              aliases=["o"])
    @argument("run_sheet",
              type=str,
              description="Specify the absolute output path for Run Sheet (required). ",
              aliases=["r"])
    @argument("integrity",
              type=bool,
              description="Specify whether to enable data and runtime integrity check for the workflow engine "
                          "(optional, default = False).")
    @argument("trust",
              type=bool,
              description="Specify whether to enable content trust for container runtime "
                          "(optional, default = False).")
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    @argument("kernel_version",
              type=str,
              description="Specify the SeqsLab kernel version (optional).")
    def request_runsheet(self,
                         working_dir: str,
                         run_sheet: str,
                         workspace: str,
                         integrity: bool = False,
                         trust: bool = False,
                         kernel_version: str = ''
                         ):
        """
        Parse run_sheet.csv and create a request.json file for each WES run.
        """
        if not os.path.isdir(working_dir):
            logging.error("working dir is not a directory")
            cprint("working dir is not a directory", "red")
            return errno.EINVAL
        try:
            run_sheet = RunSheet(run_sheet)
        except ValueError as e:
            cprint(e, 'red')
            return -1
        for run in run_sheet.runs:
            self._runs_routine(run=run, working_dir=working_dir, workspace=workspace, execs=None, integrity=integrity,
                               trust=trust, is_runsheet_template=True, is_single_end=run_sheet.is_single_end,
                               kernel_version=kernel_version)
        return 0

    def _runs_routine(self, run: Run, working_dir: str, workspace: str, execs: str = None,
                      integrity: bool = False, trust: bool = False,
                      is_runsheet_template: bool = False, is_single_end: bool = True, kernel_version: str = ''):

        def label_field_validation(label):
            message = f'label Name ({label}) can only contain alphanumeric characters ' \
                      f'and other special characters (#_`~!@%^*()+-. :).'
            regex = re.compile(r'(\w|[#_`~!@%^*()+-. :])+')
            if not regex.fullmatch(label):
                raise ValueError(message)

        for sample in run.samples:
            for lbl in [sample.run_name, sample.Read1_Label, sample.Read2_Label]:
                for item in lbl.split('/'):
                    label_field_validation(item)

        pattern = r'[# `~!@%^*()+.:/]'
        rpath = re.sub(pattern, '_', run.run_name)
        execs_path = f'{working_dir}/{rpath}-execs.json'
        request_path = f'{working_dir}/{rpath}-request.json'
        wf_info = run.workflow_url.split('versions')[1].strip('/').split('/')

        if not execs:
            trs_register().load_resource().get_execs_json(
                workflow_url=run.workflow_url,
                download_path=execs_path
            )
        else:
            execs_path = f'{working_dir}/{execs}'

        params = parameters.workflow_params(execs_path, run, is_runsheet_template, is_single_end)
        if not isinstance(params, dict):
            raise Exception(f'Unable to generate workflow_params based on given exec_path, with error code {params}')

        request = {
            "name": run.run_name,
            'workflow_params': params,
            'workflow_backend_params': parameters.workflow_backend_params(execs_path, workspace, run.runtimes,
                                                                          integrity, trust, kernel_version),
            'workflow_url': run.workflow_url,
            "workflow_type_version": wf_info[0],
            'workflow_type': wf_info[1],
        }
        with open(request_path, 'w') as f:
            json.dump(request, f, indent=4)

    @command
    @argument("run_name",
              type=str,
              description="Define the run name for a single run (required). ",
              aliases=["name"])
    @argument("working_dir",
              type=str,
              description="Specify the absolute output directory for generated request.json (required). ",
              aliases=["dir"])
    @argument("workflow_url",
              type=str,
              description="Specify a workflow URL for a run. "
                          "For example, https://api.seqslab.net/trs/v2/tools/trs_id/versions/1.0/WDL/files/ (required). ",
              aliases=["url"])
    @argument("execs",
              type=str,
              description="Specify the execs.json needed to create a WES request.  If not given, the command will "
                          "get the execs.json from the TRS object specified by the workflow_url "
                          "(optional, default = None).")
    @argument("runtimes",
              type=str,
              description="Key:value pairs indicating the workflow name -> SeqsLab supported runtime_options names. "
                          "Multiple configuration pairs can be provided using ':' as separator, "
                          "e.g. main=acu-m8:subworkflow=acu-m4 "
                          "(optional, default = None, which indicates running the whole workflow.wdl using acu-m16 for "
                          "a single node cluster on the Azure backend).")
    @argument("integrity",
              type=bool,
              description="Specify whether to enable data and runtime integrity check for the workflow engine "
                          "(optional, default = False).")
    @argument("trust",
              type=bool,
              description="Specify whether to enable content trust for container runtime "
                          "(optional, default = False).")
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    @argument("kernel_version",
              type=str,
              description="Specify the SeqsLab kernel version (optional, default = None).")
    def request(self, run_name: str, working_dir: str, workflow_url: str, workspace: str,
                execs=None, runtimes=None, integrity=False,
                trust=False, kernel_version=''):
        """
        Create WES run request.
        """
        if not os.path.isdir(working_dir):
            logging.error("working dir is not a directory")
            cprint("working dir is not a directory", "red")
            return errno.EINVAL
        try:
            single_run = Run(list(), run_name, workflow_url, runtimes)
        except ValueError as e:
            cprint(e, "red")
            return -1
        self._runs_routine(run=single_run, working_dir=working_dir, workspace=workspace, execs=execs,
                           integrity=integrity, trust=trust, kernel_version=kernel_version)
        return 0

    @command
    @argument("run_id",
              type=str,
              positional=False,
              description="Specify a previously executed WES run ID (required)."
              )
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    def get(self, run_id: str, workspace: str) -> int:
        """
        Get WES run information based on run ID.
        """
        try:
            result = get_factory().load_resource(workspace).get_run_id(run_id)
            cprint(json.dumps(result, indent=4), "yellow")
        except requests.HTTPError:
            cprint(f"given run_id {run_id} is not valid.", "red")
            return -1

        return 0

    @exception_handler
    def _get_run_id(self, workspace, rerun_id):
        return get_factory().load_resource(workspace).get_run_id(rerun_id)

    @command
    @argument("rerun_id",
              type=str,
              positional=False,
              description="Specify the run_id that is going to be rerun (required)."
              )
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    def rerun(self,
              rerun_id: str,
              workspace: str
              ) -> int:
        """
        Rerun an existing run by calling the seqslab-api/wes/runs API.
        """
        run_obj = self._get_run_id(workspace=workspace, rerun_id=rerun_id)
        if isinstance(run_obj, int):
            return run_obj

        mp = MultipartEncoder(fields={})
        resource = get_factory().load_resource(workspace)
        ret = resource.sync_run_jobs(data=mp,
                                     headers={'Content-Type': mp.content_type},
                                     run_request_id=None,
                                     run_name=None,
                                     rerun_id=rerun_id)
        res = json.loads(ret.content.decode('utf-8'))
        cprint(f"{res}", "yellow")
        return 0

    @command
    @argument("run_id",
              type=str,
              positional=False,
              description="Specify the run_id that is going to be cancelled (required)."
              )
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    def cancel(self, run_id: str, workspace: str) -> int:
        """
        Cancel WES run based on run ID.
        """
        try:
            result = get_factory().load_resource(workspace).cancel_run(run_id)
            cprint(json.dumps(result, indent=4), "yellow")
        except requests.HTTPError:
            cprint(f"given run_id {run_id} is not valid.", "red")
            return -1

        return 0

    @command
    @argument("run_id",
              type=str,
              positional=False,
              description="Specify the run_id that you are trying to validate (required)."
              )
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    @argument("output_path",
              type=str,
              description="Specify the absolute output path for keeping the WES run detail_config.json. If not given, "
                          "the command will return the detail_config.json to stdout (optional). ")
    def detail(self, run_id: str, workspace: str, output_path: str = '') -> int:
        """
        Get WES run detail_config.json with a run ID.
        """
        try:
            result = get_factory().load_resource(workspace).wes_files(run_id)
            if output_path:
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=4)
            else:
                cprint(json.dumps(result, indent=4), "yellow")
        except requests.HTTPError:
            cprint(f"given run_id {run_id} is not valid.", "red")
            return -1

        return 0


@command
class Jobs(BaseJobs):
    """Workflow execution commands"""

    @command
    @argument("working_dir",
              type=str,
              positional=False,
              description="Specify the working directory path that contains request.json (required)."
              )
    @argument("workspace",
              type=str,
              description="Specify the workspace based on the signed in account (required).")
    def dryrun(self,
               working_dir: str,
               workspace: str
               ) -> int:
        """
        Workflow dry run to see if the given request.json files are properly configured by calling seqslab-api/wes/runs/dryrun and seqslab-api/wes/runs/files API.
        """
        if not os.path.isdir(working_dir):
            logging.error("working dir is not a directory")
            cprint("working dir is not a directory", "red")
            return errno.EINVAL

        reqs = [os.path.join(working_dir, f) for f in os.listdir(working_dir) if
                os.path.isfile(os.path.join(working_dir, f)) and f.endswith('request.json')]

        for value in enumerate(reqs):
            try:
                with open(value[1], 'r') as f:
                    request = json.load(f)
            except json.decoder.JSONDecodeError as e:
                cprint(f"given request not in json format - {e}", "red")

            # wes/${run_id}/dryrun
            mp = MultipartEncoder(
                fields={
                    "name": request.get('name'),
                    "workflow_type": request.get('workflow_type'),
                    "workflow_type_version": request.get('workflow_type_version'),
                    "workflow_url": request.get('workflow_url'),
                    'workflow_params': json.dumps(request.get('workflow_params')),
                    'workflow_backend_params': json.dumps(request.get('workflow_backend_params'))
                }
            )
            resource = get_factory().load_resource(workspace)
            dry_ret = resource.dry_run(data=mp,
                                       headers={'Content-Type': mp.content_type},
                                       run_request_id=None,
                                       run_name=request.get('name'))
            dry_res = json.loads(dry_ret.content.decode('utf-8'))

            # wes/${run_id}/files
            res = resource.wes_files(dry_res['run_id'])

            with open(os.path.join(working_dir, f'{dry_res["run_id"]}_files.json'), 'w') as f:
                json.dump(res, f, indent=4)

            cprint(f"{request.get('name')} verified with dryrun id {dry_res['run_id']}", "yellow")

        return 0
