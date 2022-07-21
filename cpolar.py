# -*- coding: UTF-8 -*-
# Version: v1.0
# Created by lstcml on 2022/07/21
import os

path = os.path.split(os.path.realpath(__file__))[0]
log_name = os.path.join(path, "nwct_cpolar_log", "cpolar")
app_path = os.path.join(path, "cpolar")
commond = app_path + " -log=" + log_name + " 5700"
os.system(commond)