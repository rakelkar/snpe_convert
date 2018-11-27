import os, sys
import shutil
import random
from shutil import copyfile

#folder which contains the sub directories
source_dir = sys.argv[1]
output_dir = sys.argv[2]

#list sub directories 
for root, dirs, files in os.walk(source_dir):

    #iterate through them
    for i in dirs: 

        #create a new folder with the name of the iterated sub dir
        path = output_dir + "./%s/" % i
        os.makedirs(path)

        #take random sample, here 3 files per sub dir
        filenames = random.sample(os.listdir(source_dir + "./%s/" % i ), 5)

        #copy the files to the new destination
        for j in filenames:
            shutil.copy2(source_dir + "%s/" % i  + j, path)

