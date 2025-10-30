import os 
import shutil

def copy_job(src, dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
        os.mkdir(dst_dir)
    else:
        os.mkdir(dst_dir)
    path_list = os.listdir(src)
    print(path_list)
    if len(path_list) != 0:
        for path in path_list:
            src_path = os.path.join(src, path)
            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_dir)
            else:
                dest_path = os.path.join(dst_dir, path)
                copy_job(src_path, dest_path)