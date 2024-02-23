import os
import sys

import traceback

from kivy.resources import resource_add_path

from alkvin.main import main


if __name__ == "__main__":
    try:
        if hasattr(sys, "_MEIPASS"):
            os.environ["KIVY_NO_CONSOLELOG"] = "1"
            resource_add_path(os.path.join(sys._MEIPASS))
        main()
    except Exception:
        error = traceback.format_exc()
        with open("ERROR.log", "w") as error_file:
            error_file.write(error)

        print(error)
        input("Press enter.")
