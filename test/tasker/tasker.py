import unittest
import lazylab
import zipfile
import sys
import os
from lazylab.tasker.tasker import Tasker
from lazylab.constants import LAB_CONFIG_PATH, PATH_TO_MODULE

class DeployAndSave(unittest.TestCase):
    def setUp(self):
        self.lab_name = 'Juniper_vmx14'
        task = Tasker()
        task.deploy_lab(self.lab_name)

    def test_save(self):
        old_lab_name = self.lab_name
        new_lab_name = self.lab_name
        SAVED_LAB_PATH = PATH_TO_MODULE + '/../test/'
        task = Tasker()
        task.save_lab(old_lab_name, new_lab_name, SAVED_LAB_PATH)
        path1 = LAB_CONFIG_PATH + old_lab_name + '.lazy'
        path2 = SAVED_LAB_PATH + new_lab_name + '.lazy'
        with zipfile.ZipFile(path1, 'r') as archive1, zipfile.ZipFile(path2, 'r') as archive2: 
            filelist1 = archive1.namelist() 
            filelist2 = archive2.namelist() 
            flag = (filelist1 == filelist2)
            for filename in filelist1: 
                with archive1.open(filename) as file1, archive2.open(filename) as file2: 
                    filestring1 = file1.read() 
                    filestring2 = file2.read() 
                    flag = flag and (filestring1 == filestring2) 
        self.assertTrue(flag)
        os.remove(path2)
        
        return 0
    
    def tearDown(self):
        task = Tasker()
        task.delete_lab('Juniper_vmx14')
        
        return 0
