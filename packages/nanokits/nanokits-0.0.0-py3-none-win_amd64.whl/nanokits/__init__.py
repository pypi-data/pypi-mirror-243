import os
import subprocess
from packaging import version

def get_unique_dependencies(dependencies):
    """获取去重后的库名称列表，保留最大版本号"""
    max_versions = {}
    for dep in dependencies:
        name, version_str = dep.split('==')
        dep_version = version.parse(version_str)
        if name not in max_versions or dep_version > version.parse(max_versions[name]):
            max_versions[name] = version_str
    unique_dependencies_list = [f"{name}=={version}" for name, version in max_versions.items()]
    return unique_dependencies_list


def setup_project(project_dir):
    """设置项目并生成 requirements 列表"""
    cur_dir = os.getcwd()
    os.chdir(project_dir)
    
    subprocess.run(["pip", "install", "pipreqs", "poetry"])  # 安装 pipreqs 和 poetry
    subprocess.run(["pipreqs", "."])
    subprocess.run(["curl", "-sSL", "https://install.python-poetry.org", "|", "python", "-"]) # 初始化 poetry 项目
    subprocess.run(["poetry", "install"]) # 安装项目依赖项

    # 读取生成的 requirements.txt 文件并转化为列表
    requirements_list = subprocess.check_output(["pipreqs", "--print", "."], text=True).splitlines()
    requirements_list = get_unique_dependencies(requirements_list)
    
    # 把 requirements_list 写入 requirements.txt 文件
    with open("requirements.txt", "w") as f:
        for line in requirements_list:
            f.write(line + "\n")

    os.chdir(cur_dir)
    return requirements_list


if __name__ == "__main__":

    requirements_list = setup_project(os.getcwd())
    requirements_list = [item.split('==')[0] for item in requirements_list]
    print(requirements_list)

