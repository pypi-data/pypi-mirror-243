import os

def path_maker(path_list,relative_path=''):
    p = os.path.abspath(os.path.join(os.getcwd(),relative_path))
    for i in path_list:
        p += '/'+str(i)
        if not os.path.exists(p):
            os.mkdir(p)
    return p
import zipfile
def zipfolder(zip_addr:str, target_dir): 
    if not zip_addr.endswith('.zip'):
        zip_addr=zip_addr + '.zip'
    zipobj = zipfile.ZipFile(zip_addr, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])
    return zip_addr
