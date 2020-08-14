import logging
import os
import pathlib

from flask import Flask, request
from pipeline_runner.tasks.celery_tasks import run_command

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

# TODO: change to an environment variable
STITCHING_PIPELINE_DIR = "/nfs/team283_imaging/test_stitching/Anton/acapella-singularity"


@app.route('/ping', methods=['GET'])
def ping():
    return "Service alive", 200


@app.route('/path', methods=['GET'])
def check_path():
    from pipeline_runner.path_checker import check_path

    rootdir = request.args.get('rootdir')
    regex_pattern = request.args.get('regex_pattern')
    if rootdir:
        measurement_path = check_path(rootdir, regex_pattern)
        if measurement_path:
            return measurement_path, 200
        else:
            return "Files not found", 200
    return "No root directory", 400


@app.route('/stitching', methods=['POST'])
def run():
    data = request.get_json()
    input_dir = data.get("input_dir", "")
    output_dir = data.get("output_dir", "/nfs/team283_imaging/0HarmonyStitched")
    if not os.path.exists(input_dir):
        return "Input directory does not exist", 400
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    project_dir = os.path.curdir
    cmd = f'cd "{STITCHING_PIPELINE_DIR}" && NXF_VER="20.07.1" NXF_OPTS="-Dleveldb.mmap=false" nextflow -trace nextflow.executor run acapella_path.nf ' \
          f'--root "{input_dir}" --out_dir "{output_dir}"' \
          f'-with-report work/report.html -profile standard,singularity -resume;'
    _ = run_command.delay(cmd)
    os.chdir(project_dir)
    return "Pipeline started", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
