import os
import re

from pipeline_runner.app import app

ROOT = "/nfs"


def check_path(rootdir: str, regex_pattern: str) -> str:
    app.logger.info(f"Rootdir: {rootdir}")
    app.logger.info(f"Regex pattern: {regex_pattern}")
    export_dir = os.path.join(ROOT, rootdir)
    app.logger.info(f"Export dir: {export_dir}")
    if os.path.exists(export_dir):
        regex = re.compile(regex_pattern)
        for mes_dir in os.listdir(export_dir):
            if regex.match(mes_dir):
                mes_path = os.path.join(export_dir, mes_dir)
                export_file = os.path.join(mes_path, "Images", "Index.idx.xml")
                app.logger.info(f"Export file: {export_file}")
                if os.path.exists(export_file):
                    return mes_path
    else:
        app.logger.info(f"Export dir does not exist")
