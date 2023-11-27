# -*- coding: utf-8 -*-
"""
功能：一次性引入SIAT的所有模块
作者：王德宏，北京外国语大学国际商学院
版权：2021-2024(C) 仅限教学使用，商业使用需要授权
联络：wdehong2000@163.com
"""

#==============================================================================
#屏蔽所有警告性信息
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
from siat.allin import *
#==============================================================================
#同一命令行多个输出，主要用于Jupyter Notebook
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity='all'
#==============================================================================
# 检查是否存在新版本
import pkg_resources
current_version=pkg_resources.get_distribution("siat").version
import luddite
latest_version=luddite.get_version_pypi("siat")

if latest_version != current_version:
    print("Welcome to Security Investment Analysis Toolkit (siat)")
    print("The siat version in your computer is",current_version,"\b, latest version is",latest_version,'\n')
    print("*** If you expect to upgrade siat, use the instruction below in a command window:")
    print("    pip install siat --upgrade")
    print("*** If you expect to upgrade in Jupyter, add a \'!\' right before the instruction above",'\n')
    
    print("*** If you encounter incompatible plug-in, uninstall siat first and reinstall it:")
    print("    pip uninstall siat")
    print("    pip install siat",'\n')
    
    print("*** If you have a slow internet connection, add an option after the instruction above:")
    print("    -i https://mirrors.aliyun.com/pypi/simple/",'\n')

    print("If you have done any of the above, restart the Python (eg. restarting the kernel)")
    print("Provided you still need additional help, please contact wdehong2000@163.com")
#==============================================================================
