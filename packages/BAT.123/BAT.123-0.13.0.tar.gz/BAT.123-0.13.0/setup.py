import sys,subprocess

class Var:
    nameA = 'BAT.123'
    nameB = '0.13.0'
    ### 修改參數 ###
    @classmethod
    def update_names(cls, name=None, vvv=None):
        """
        更新类变量 nameA 和 nameB 的值，并修改文件内容
        """
        if name is not None and vvv is not None:
            cls.nameA = name
            cls.nameB = vvv
          
            print(f"已更新类变量 nameA={cls.nameA}, nameB={cls.nameB}")
            print("-"*50)

            # 修改文件内容
            filename = __file__   # 替换成你的脚本文件名
            with open(filename, 'r+', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if "### 修改參數 ###" in line:
                        lines[i-2] = f"    nameA = '{name}'\n"
                        lines[i-1] = f"    nameB = '{vvv}'\n"
                        break  # 找到后就退出循环
                f.seek(0)
                f.writelines(lines)
                f.truncate()
        else:
            print("未提供足够的参数")
    
    @classmethod    
    def check_pypi(cls,module_name, module_version):
        cls.install_modules(['requests', 'twine'])
        cls.update_names('None',"None")
        pypi_url = f"https://pypi.org/pypi/{module_name}/json"
        import requests
        try:
            # 尝试发送 GET 请求到 PyPI，获取模块信息
            response = requests.get(pypi_url)
            
            # 如果请求成功（状态码为 200），继续执行
            response.raise_for_status()
            
            # 将响应解析为 JSON 格式
            package_info = response.json()
            
            # 获取 PyPI 上所有发布版本的版本号
            versions = package_info['releases'].keys()
            
            # 检查指定版本号是否存在于 PyPI 上
            if module_version in versions:
                print(f"模块 {module_name} 版本 {module_version} 存在于 PyPI。")
                cls.update_names(module_name,"None")
                return False
            else:
                print(f"模块 {module_name} 版本 {module_version} 不存在于 PyPI。")
                cls.update_names(module_name,module_version)
                return True
        except requests.exceptions.RequestException as e:
            # 如果请求过程中发生异常，捕获并打印错误信息
            print(f"模块 [不存在] 于 PyPI。")
            print(f"错误: {e}")
            cls.update_names(module_name,module_version)
            return True

    @classmethod
    def install_modules(cls, modules):
        """
        检查并安装指定的模块列表
        """
        for module in modules:
            try:
                import importlib
                globals()[module]=importlib.import_module(module)
                # __import__(module)
                print(f"@ import {module} @")
            except ImportError:
                print(f"找不到模块 '{module}'。正在尝试安装...")
                try:
                    subprocess.check_call(["pip", "install", module])
                    print(f"{module} 安装成功。")
                except Exception as install_error:
                    print(f"{module} 安装期间出现错误：{install_error}")
                    sys.exit(1)


    @classmethod
    def popen(cls,CMD):
        import subprocess,io,re
        # CMD = f"pip install cmd.py==999999"
        # CMD = f"ls -al"

        proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
        proc.wait()
        stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8').read()
        stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8').read()

        # True if stdout  else False , stdout if stdout  else stderr 
        return  stdout if stdout  else stderr 
    @classmethod
    def clear(cls):
        ###############################################################################
        import os
        if  str(os.name)=="nt":
            os.system("rmdir /q /s %LOCALAPPDATA%\pip\cache")
        else:
            os.system("rm -rf ~/.cache/pip/*")
        ################################################################################

    
    @classmethod
    def MD(cls,name,passs):
        import os
        if  str(os.name)=="nt":
            file= os.getcwd()+"\\.pypirc"
        else:
            # /root/.pypirc
            file= os.getcwd()+"/.pypirc"
        
        # print(file)
        text=[
                # 'echo >/content/cmd.py/cmds/__init__.py',
                # 'echo >/content/cmd.py/README.md',
                f'echo [pypi]> {file}',
                f'echo repository: https://upload.pypi.org/legacy/>>  {file}',
                f'echo username: {name}>>  {file}',
                f'echo password: {passs}>>  {file}'
        ]
        for i in text:
            # cls.popen(i)
            os.system(i)


    @classmethod
    def sdist(cls,module_name, module_version):
        BL= Var.check_pypi(module_name, module_version)
        if  BL:
            import os
            if  str(os.name)=="nt":
                os.system(f"rd /s /q .\\{module_name}.egg-info")
                os.system(f"rd /s /q .\\dist")
            else:
                os.system(f"rm -rf ./{module_name}.egg-info")
                os.system(f"rm -rf ./dist")


            if  os.system('python setup.py sdist')==0:
                # print(f"twine upload --skip-existing  dist/*  --config-file {os.getcwd()}\\.pypirc")
                if  os.system(f"twine upload --skip-existing  dist/*  --config-file {os.getcwd()}\\.pypirc")==0:
                    print("@ twine 成功 @")
                else:
                    print("@ twine 失敗 @")
                    print("@ twine 原因:可能 is 模組名稱 類似 @")


            
         

        print(f"@ [目前狀態:{BL}] : ",cls.nameA,cls.nameB)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py module_name module_version")
    else:
        module_name = sys.argv[1]
        module_version = sys.argv[2]
        # Var.update_names(module_name, module_version)
        
        Var.MD("moon-start","moon@516")
        Var.sdist( module_name, module_version)
     
        # check_pypi_module_version(module_name, module_version)



 

# install_requires=
from setuptools import setup, find_packages


##############################################
from setuptools.command.install import install
class PostCMD(install):
        """cmdclass={'install': XXCMD,'install': EEECMD }"""
        def  run(self):
            import sys
            print(123,sys.argv)
            print(333,f"{Var.nameA}" ,f"{Var.nameB}"  )                    
            import os
            def listDIR(PWD="/content"):
                data = {}
                import os
                ### 路徑   底下目錄  底下檔案
                for root , dirs , files in os.walk(PWD):
                    print( os.path.basename(root) in [i for i in os.listdir( PWD )if i[0]!="."] )
                    if  root.find(os.path.sep+".git")==-1:
                        print(root , dirs , files)
               
            # 呼叫基類的 run 方法，這樣可以保留原始的安裝行為
            print("#"*30, "安裝前:A ","#"*30 )
            listDIR( os.getcwd() )
            print("#"*30, "安裝前:B ","#"*30 )
            install.run(self)
            # 在安裝後執行一些自定義的操作
            print("#"*30, "安裝後:A ","#"*30 )
            listDIR( os.getcwd() )
            print("#"*30, "安裝後:B ","#"*30 )
            # Var.clear()
 

        
            # def DPIP(BL):
            #     if BL:
            #         ##################################################################
            #         import os
            #         ##################################################################
            #         FF = str(__file__).split("setup.py")[0]
            #         ### 刪除1
            #         if os.name=="nt":     ## Win10    
            #             print("@ DPIP-FF ::",FF )  
            #             os.system(f"rmdir /q /s {FF}") ## DEL
            #     else:
                
            #         ##################################################################
            #         import os
            #         ##################################################################
            #         FF = str(__file__).split("setup.py")[0]
            #         import os
            #         # print(os.popen("dir "+FF).read())
            #         ### 刪除1
            #         if os.name=="nt":     ## Win10    
            #             print("@ DPIP-FF ::",FF )  
            #             os.system(f"rmdir /q /s  {FF+os.path.sep}UNKNOWN-0.0.0-py3.7.egg-info") ## DEL
                



      



            import site,atexit                
            def  cleanup_function(siteOP):
                import os
                os.system("pip install git+http://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/{Var.nameA}@{Var.nameB}")
                print("# 小貓 1 號")
                def siteD():
                        import os,re
                        pip=os.popen("pip show pip")
                        return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 
                    
                print(f"rmdir /q /s  {siteD()+os.path.sep}{Var.nameA}-{Var.nameB}.dist-info")
                os.system(f"rmdir /q /s  {siteD()+os.path.sep}{Var.nameA}-{Var.nameB}.dist-info") ## DEL
                # BAT.123-0.9.0.dist-info
                    
                 
            atexit.register(cleanup_function,site)
            #################################
setup(
    name=f"{Var.nameA}",
    # name=f"cmd.oss",
    version=f"{Var.nameB}",
    description="My CMD 模組",
    long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
    long_description_content_type="text/markdown",
    license="LGPL",
    # packages=find_packages(),
    install_requires=[
    # setup_requires=[
        # 'requests',  # 这里列出需要在 setup.py 运行之前安装的包
        # 'cmd.py@git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/cmd.py@main',
        # 'BAT.oss@git+https://gitlab.com/moon-start/BAT.bat',
   
    ],

    #####################################
    cmdclass={ 'install': PostCMD  }
    #####################################
)



