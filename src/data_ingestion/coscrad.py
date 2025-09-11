import json
import os
import subprocess

"""
# Testing
We do not have an automated test for this. It is an internal, developer facing utility for bulk data ingestion. It's API will be strongly
coupled to COSCRAD backend, which is well tested. If any of the functionality breaks, the developer using this tool will push the fix and manually
test it for this use case. This ensures we invest minimal time into this tool.

# Design
Note that for convenience we currently have implemented our Python client as a binding to the COSCRAD CLI. In the future, we may want to use
an API token instead. Only the constructor (configuration), but not the public API of this class should change in case we make that change.
"""
class CoscradClient:
    def __init__(self,coscradPath):
        """
        This is a sanity check as a convenience to the client so that they can catch this issue early. We check a couple of required
        environment variables that we don't anticipate will be removed from COSCRAD in the future. We don't want to do
        this check comprehensively to avoid maintainence. 
        """
        if not "NODE_ENV" in os.environ or not "ARANGO_DB_NAME" in os.environ:
            raise Exception("You need to set your environment. \n`from dotenv import load_dotenv`\n`load_dotenv(path_to_env)`")

        local_dist = "dist"
        local_node_modules = "node_modules"

        if os.path.islink(local_dist):
            os.unlink(local_dist)

        os.symlink(os.path.join(coscradPath,"dist"),local_dist)

        if os.path.islink(local_node_modules):
            os.unlink(local_node_modules)

        os.symlink(os.path.join(coscradPath,"node_modules"),local_node_modules)
        
        # TODO run fresh build
        self.cliPath = f'dist/apps/coscrad-cli'

    def executeBulkJob(self,bulkJobCreationDto):
        # TODO support passing serialized JSON instead of using JSON files as a means of interprocess communication!
        temp_dir = 'tmp'

        if not os.path.isdir(temp_dir):
            os.makedirs(temp_dir)

        fileprefix = bulkJobCreationDto.get("name",None)

        if fileprefix is None:
            raise Exception("Cannot execute a bulk job that is missing a name")

        filename = f'{fileprefix}.json'

        input_file = os.path.join(temp_dir,filename)

        with open(input_file,'w') as wf:
            json.dump(bulkJobCreationDto,wf)

        wrapped_filename = f'"{input_file}"'

        cli_command = f'manage-bulk-jobs {self.ddArg("data-file",wrapped_filename)}'

        result = self.command(cli_command)

        print(result)

        # TODO parse error \ success state 

    def checkCliStatus(self):
        print(self.command("",[]))

    def command(self,command_name,clargs=[]):    
        fullCliCommand = f'node {os.path.join(self.cliPath,"main.js")} {command_name}'

        args_for_subprocess = [fullCliCommand]

        args_for_subprocess.extend(clargs)
        
        result = subprocess.run(args_for_subprocess,shell=True)

        return result

    def ddArg(self,arg_name,value):
        return f'--{arg_name}={value}'