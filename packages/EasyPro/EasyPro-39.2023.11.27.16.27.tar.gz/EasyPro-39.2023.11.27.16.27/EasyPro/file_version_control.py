# -*- coding: utf-8 -*-
# @Time    : 2023/1/12 12:03
# @Author  : Quanfa
# @Desc    :

from .path_tool import MyPath
from .matlab import save_mat, load_mat
from .project import Project
import torch as saver
import sys


def save(object, path, name, suffix):
    if suffix == 'Figure':
        object.savefig(path)
    if suffix == 'mat':
        save_mat(object, path, name)
    else:
        saver.save(object, path)
    print('save ', name, ' at ', path)


class ScriptFileSaver:
    def __init__(self, script_file, locals, version: int = None):
        """
        A combination of database and saver in framework.

        :param root_path: local path
        :param date_mark:
        :param version:
        :param author:
        """

        if version is None:
            version = 1
        self._locals = locals

        # region calculate version
        script_path = MyPath.from_file(script_file)
        project_path = Project(script_path.get_level(0, -3))
        author_name = script_path.get_level(-2)
        script_name = script_path.get_name()[:-3]
        if script_path.get_parent() == project_path.scripts_path:  # 如果是脚本生成脚本
            project_path = Project(script_path.get_level(0, -2))
            author_name = 'auto'
            script_name = 'script_create'

        save_path_parent = project_path.locals_path.cat(author_name).cat(script_name).ensure()

        # endregion
        self._local_path = save_path_parent.cat('s' + str(version))
        self._version = version
        self._local_path.ensure()
        self._root_path = project_path

        # region append project path to system
        if not project_path in sys.path:
            sys.path.append(project_path)
        # endregion

    def path_of(self, file_name='auto_save_result', suffix='sus'):
        """

        :param file_name:
        :return:
        """
        if suffix == '':
            path = self._local_path.cat(file_name)
        else:
            path = self._local_path.cat(file_name + '.' + suffix)

        return path

    def save(self, name, object=None, suffix=None, path=None):
        """
        保存变量，任意类型的python对象
        :param name: 保存的名字
        :param object: 如果没给定，就自动从内存中搜索
        :param suffix: sus, sci util saved; mat, matlab
        :return:
        """
        if object is None:
            object = self._locals[name]
        if suffix is None:
            suffix = str(type(object)).split("'")[1].split('.')[-1]
        if path is None:
            path = self.path_of(name, suffix)
        else:
            path = MyPath(path)

        save(object, path, name, suffix)
        return path

    def load(self, name=None, suffix=None, object_sample=None, path=None):
        """
        load from specified version.
        :param name:
        :return:
        """
        if path is None:
            if suffix is None:
                path = self._local_path.get_files(mark=name, list_r=True)[0]
                suffix = path.split('.')[-1]
            else:
                path = self.path_of(name, suffix)
        print('load ', suffix, ' from ', path)
        if object_sample is not None:
            return object_sample.load(path)
        if suffix == 'mat':
            return load_mat(path)
        else:
            return saver.load(path)

    def __getitem__(self, name):
        return self.load(path=self.path_of(name, ''))
