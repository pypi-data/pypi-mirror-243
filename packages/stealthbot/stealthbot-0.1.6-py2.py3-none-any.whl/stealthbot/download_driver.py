import os
import shutil

import chromedriver_autoinstaller_fix
from chromedriver_autoinstaller_fix import get_chrome_version
from chromedriver_autoinstaller_fix.utils import get_major_version

# get path of current working directory
current_dir = os.getcwd()

main_dir = os.environ.get("PROJECT_ROOT_PATH", os.getcwd())

build_path = os.path.join(main_dir, "build")

print("main_dir: ", main_dir)


def is_windows():
    return os.name == 'nt'


def download_driver_in_path():
    path = chromedriver_autoinstaller_fix.install(path=build_path)
    print(path)


def recreate_build_dir():
    # Delete the build directory
    shutil.rmtree(build_path, ignore_errors=True)

    # Create the build directory again
    os.makedirs(build_path, exist_ok=True)


def get_filename(major_version):
    return f"chromedriver-{major_version}.exe" if is_windows() else f"chromedriver-{major_version}"


def move_driver():
    major_version = get_major_version(get_chrome_version())
    print(f'[INFO] Moving Chrome Driver to build/{major_version}/.')

    executable_name = get_filename(major_version)
    print(executable_name)
    executable_name_src = "chromedriver.exe" if is_windows() else "chromedriver"

    def move_chromedriver():
        # Define the source and destination paths
        src_path = f"{build_path}/{major_version}/{executable_name_src}"
        print(src_path)
        dest_path = f"{build_path}/{executable_name}"
        print(dest_path)

        # Use the shutil.move() function to move the file
        shutil.move(src_path, dest_path)

    move_chromedriver()
    shutil.rmtree(f"{build_path}/{major_version}/")


def download_driver():
    recreate_build_dir()
    print(f'[INFO] Downloading Chrome Driver. This is a one-time process. Download in progress...')

    download_driver_in_path()
    move_driver()


if __name__ == '__main__':
    download_driver()
