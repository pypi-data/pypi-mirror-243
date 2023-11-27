from .path_tool import MyPath


class Project(MyPath):
    # region basic structure

    structure = [
        'mylocals',
        'myscripts',
        'myreadmes',

        'myreadmes/catalog.md',
        'myscripts/__init__.py',
        '.gitignore'
    ]

    @property
    def locals_path(self):
        return MyPath(self.cat(self.structure[0]))

    @property
    def scripts_path(self):
        return MyPath(self.cat(self.structure[1]))

    @property
    def readmes_path(self):
        return MyPath(self.cat(self.structure[2]))

    # endregion

    def check_project_path(self, next=False):
        name = self.get_name()
        if not 'T20' in name:
            print(self, '真的是项目根目录吗？')
            return next
        return True

    def check_project_structure(self, next=False):
        r = True
        if not self.check_project_path(next):
            return next

        for structure in self.structure:
            path = self.cat(structure)
            if not path.exist():
                r = False
                print('文件(夹)', structure, '不存在')

        if not r:
            return next
        return True

    # region create structure

    def create_structure(self):

        for structure in self.structure:
            path = self.cat(structure)
            if not path.exist():
                path.ensure()
                print('文件(夹)', structure, '已创建')

        with open(self.cat(self.structure[3]), 'w') as f:
            f.write("""# abstract

# authors
"""
                    )

        with open(self.cat(self.structure[4]), 'w') as f:
            f.write("""
from EasyPro import ScriptFileSaver, MyPath

sfs = ScriptFileSaver(__file__, locals())

p0 = 'master'

# endregion

if __name__ == '__main__':
    from EasyPro import Project

    project = Project(MyPath.from_file(__file__).get_parent().get_parent())
    project.create_script(p0, 'test')

            """)
        with open(self.cat(self.structure[5]), 'w') as f:
            f.write("""
.idea
mylocals
            """)
        self.add_author('master')
        self.create_script('master', 'test')

    def add_author(self, author):
        author_script_path = self.scripts_path.cat(author)
        if author_script_path.exist():
            print('author exist')
            return
        author_script_path.ensure()
        author_script_path.cat('__init__.py').ensure()

        author_md_folder = self.readmes_path.cat(author).ensure()
        author_md = author_md_folder.cat(f'{author}.md').ensure()
        with open(author_md, 'w') as f:
            f.write("""# abstract


# from
[catalog](../catalog.md)

# catalog
"""
                    )

        catalog_md = self.readmes_path.cat('catalog.md')
        with open(catalog_md, 'a') as f:
            f.write(f'\n\n[{author}]({author}/{author}.md)')

    def create_script(self, author_name, script_name):

        if not self.scripts_path.cat(author_name).exist():
            self.add_author(author_name)

        script_index = len(self.scripts_path.cat(author_name).get_files(list_r=True))
        script_name = 's' + str(script_index) + '_' + script_name

        script_path = self.scripts_path.cat(author_name).cat(script_name + '.py')
        markdown_path = self.readmes_path.cat(author_name).cat(script_name + '.md')

        if script_path.exist():
            print('script in this name has already existed in your scripts:', script_path,
                  'Try to use git if you want to edit your script to a new branch.')
            return False

        script_path.ensure()
        print('create script at', script_path)
        with open(script_path, 'w') as f:
            f.write(
                """# -*- coding: utf-8 -*-
from EasyPro import ScriptFileSaver
sfs = ScriptFileSaver(__file__, locals())

if __name__ == '__main__':
    print('Running has finished')
         """
            )

        markdown_path.ensure()
        print('create markdown at', markdown_path)
        with open(markdown_path, 'w') as f:
            f.write(f"""# [{script_name}.py](../../myscripts/{author_name}/{script_name}.py)
    

# from
[{author_name}]({author_name}.md)
    
    """
                    )

        catalog_md = self.readmes_path.cat(author_name).cat(f'{author_name}.md')
        with open(catalog_md, 'a') as f:
            f.write(f'\n\n[{script_name}]({script_name}.md)')

    # endregion

    # region create
    @classmethod
    def create_at(cls, projects_path, project_name):
        from datetime import datetime
        date = datetime.now().strftime("%Y%m%d")
        project_name = 'T' + date + '_' + project_name
        projects_path = MyPath(projects_path)
        project_path = projects_path.cat(project_name)
        project = cls(project_path)
        project.create_structure()
    # endregion
