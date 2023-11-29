from typing import List
import os, sys, uuid
from pnostic.structure import RepoObject, RepoResultObject, SeclusionEnv, SeclusionEnvOutput, Runner


class app(SeclusionEnv):
    def __init__(self, working_dir:str, docker_image:str, docker_name_prefix:str):
        working_dir = "/sync"
        super().__init__(working_dir=working_dir)
        self.imports = [
            "sdock[all]",
            "mystring",
        ]
        self.docker_image = docker_image
        self.total_imports = []
        self.total_files = []
        self.docker_name_prefix = docker_name_prefix
        self.initialized=False

    def initialize(self) -> bool:
        if not self.initialized:
            cmd = "docker pull {0}".format(self.docker_image)
            print(cmd);os.system(cmd)
            self.initialized=True
        return True

    def name(self) -> str:
        return "TitanSeclusion"

    @property
    def runner_file_name(self):
        return "seclusion_env_{0}_input.py".format(self.name())

    @property
    def runner_file_name_output(self):
        return "seclusion_env_{0}_output.zip".format(self.name())

    def clean(self) -> bool:
        return True

    def python_packages(self,packages:List[str]) -> bool:
        self.total_imports.extend(packages)
        return True

    def setup_files(self,files:List[str]) -> bool:
        self.total_files.extend(files)
        return True

    def __py_script_contents(self, runner, path_to_scan):
        import mystring
        runner_import, lookfor = "#IMPORT NOT IDENTIFIED", runner.name()+".py"
        for file_import in self.total_files:
            if file_import.endswith(lookfor):
                import_string = file_import.replace(lookfor,"").replace("/",".")
                if import_string.endswith("."):
                    import_string = import_string[:-1]
                runner_import = "from {0} import {1}".format(
                    import_string,
                    runner.name()
                )

        contents= """#!/usr/bin/env python3
import sys,os,json,pickle

os.system("{{0}} -m pip install --upgrade pip mystring[all] pnostic hugg[all] ephfile".format(
    sys.executable
))

import mystring,hugg
from ephfile import ephfile
from pnostic.structure import RepoResultObject, Runner

sys.path.insert(0,".");
{0}

app = {1}.app({2})

def err(string):
    with open("error_log.log", "w+") as writer:
        writer.write(str(string) + "\\n")

os.system("{{0}} -m pip install --upgrade {{1}}".format(
    sys.executable,
    " ".join(app.imports)
))

app.initialize()
results = app.scan("{3}") #List[RepoResultObject]

try:
    with hugg.zyp("{4}") as zyp:
        for repo_obj_itr, repo_result_object in enumerate(results):
            with ephfile(suffix=".pkl") as eph:
                try:
                    with open(eph(), "wb") as foil:
                        pickle.dump(repo_result_object, foil)
                    zyp["result_{{0}}.pkl".format(str(repo_obj_itr).zfill(8))] = eph()
                except Exception as e:
                    err(e)
except Exception as e:
    err(e)
""".format(
    runner_import,
    runner.name(),
    runner.arg_init_string(),
    path_to_scan,
    self.runner_file_name_output
)
        return mystring.string.of(contents).shellCore()

    def process(self, obj:RepoObject, runner:Runner)->SeclusionEnvOutput:
        self.initialize()
        from sdock import marina
        from ephfile import ephfile
        import hugg, pickle, os, sys, mystring

        exit_code, exe_logs = -1, []
        startTime,endTime = "",""

        # Create a temp file
        # Create a temp python script using the runner and its scan command
        # Save & Wrap the data to a common file
        # Grab the common file
        # UnWrap the data

        overall_content = ""

        if obj.content != None:
            overall_content = obj.content
            try:
                with ephfile(foil=obj.path, contents=obj.content) as to_scan:
                    try:
                        with ephfile(foil=self.runner_file_name, contents=self.__py_script_contents(
                            runner=runner,
                            path_to_scan=to_scan()
                        )) as eph:
                            try:
                                with marina.titan(
                                    image=self.docker_image,
                                    working_dir=self.working_dir,
                                    name="{0}_{1}".format(self.docker_name_prefix, str(uuid.uuid4())),
                                    mount_from_to={
                                        os.path.abspath(os.curdir):"/sync/"
                                    },
                                    to_be_local_files=self.total_files + [to_scan(), eph()],
                                    python_package_imports=self.total_imports
                                ) as ship:

                                    cmd_string = "python3 {0}/{1}".format(self.working_dir, self.runner_file_name)
                                    startTime = mystring.current_date()
                                    exit_code, exe_logs = ship.run(cmd_string)
                                    endTime = mystring.current_date()

                                    startTime,endTime=mystring.date_to_iso(startTime),mystring.date_to_iso(endTime)

                                    if self.runner_file_name_output in ship.storage.files():
                                        ship.storage.download(self.runner_file_name_output, self.runner_file_name_output)
                            except Exception as e:
                                print(f"1: {e}")
                    except Exception as e:
                        print(f"2: {e}")
            except Exception as e:
                print(f"3: {e}")
        

        output = []
        if os.path.exists(self.runner_file_name_output):
            with hugg.zyp(self.runner_file_name_output) as zyp:
                for foil in zyp.files():
                    with ephfile(suffix=".pkl") as zippickl:
                        zyp.download(foil, zippickl())
                        with open(zippickl(), "rb") as pickl:
                            temp_data = pickle.load(pickl)
                            temp_data.qual_name = obj.path
                            temp_data.fileContent = mystring.string.of(overall_content).tobase64(prefix=True)

                            output += [
                                temp_data
                            ]
            os.remove(self.runner_file_name_output)

        return SeclusionEnvOutput(
            start_date_time=startTime,
            scan_object=obj,
            result=output,
            exit_code=exit_code,
            exe_logs="\n".join(exe_logs),
            end_date_time=endTime
        )


