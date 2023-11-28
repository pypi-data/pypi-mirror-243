import shutil
import os


def copytree_with_error_handling(src, dst, symlinks=False, ignore=None):
    try:
        shutil.copytree(src=src, dst=dst, symlinks=symlinks, ignore=ignore)
    except shutil.Error as e:
        for src, dst, reason in e.args[0]:
            if os.path.exists(src):
                print(f"Failed to copy: {src} to {dst} - Reason: {reason}")
            else:
                print(f"Source file not found: {src}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return dst

