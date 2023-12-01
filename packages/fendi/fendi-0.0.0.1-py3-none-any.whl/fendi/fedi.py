from streamlit.web import bootstrap as bs
import os
import json
from pathlib import Path
def create_app(info, cv_path)->None:
    (info, cv_path) = (info, cv_path)
    #print((info, cv_path))
    app_path = os.path.join(Path(__file__).parent.absolute(), "create.py")
    bs.run(app_path, '', args=["--info", json.dumps(info), "--cv_path", cv_path], flag_options={})
    #sys.argv = ["streamlit", f"run", app_path, "-- --info info --cv_path cv_path"]
    #runpy.run_module("streamlit", run_name="__main__", alter_sys=True)

if __name__ == "__main__":
    create_app()