import os
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mali.modules import Project, ProjectSetting

Session = sessionmaker()  # pylint: disable=invalid-name


def get_session() -> Session:
    return sessionmaker().configure(bind=create_engine(os.environ['MALI_CONNECTION_STRING']))


def get_or_add_project(project_name: str, description: str = None) -> Project:
    session = get_session()
    project = session.query(Project).filter(Project.name == project_name).one_or_none()
    if not project:
        project = Project(name=project_name, description=description or project_name)
        session.add(project)
        session.commit()
    return project


def set_project_settings(project: Project, settings: Dict[str, str]) -> None:
    session = get_session()
    for name, value in settings.items():
        setting = session.query(ProjectSetting).filter(ProjectSetting.name == name,
                                                       ProjectSetting.project_id == project.id).one_or_none()
        if not setting:
            setting = ProjectSetting(project=project, name=name, value=value)
            session.add(setting)
        elif value != setting.value:
            setting.value = value

    session.commit()


def list_project_settings(project: Project) -> None:
    for setting in project.settings:
        print(setting)


def main():
    project = get_or_add_project('Azure CLI')
    list_project_settings(project)

    # settings = {parts[0].strip(): parts[1].strip() for parts in
    #             (line.strip().split('=', 1) for line in open('env.txt', 'r'))}
    # set_project_settings(project, settings)


if __name__ == '__main__':
    main()
