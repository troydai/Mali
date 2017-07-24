import os
from typing import Dict

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from mali.modules import Project, ProjectSetting, create_tables

Session = sessionmaker()  # pylint: disable=invalid-name


def get_engine() -> Engine:
    from sqlalchemy import create_engine
    return create_engine(os.environ['MALI_CONNECTION_STRING'])


def get_session(engine: Engine = None) -> Session:
    Session.configure(bind=engine or get_engine())
    return Session()


def get_or_add_project(project_name: str, session: Session, description: str = None) -> Project:
    project = session.query(Project).filter(Project.name == project_name).one_or_none()
    if not project:
        project = Project(name=project_name, description=description or project_name)
        session.add(project)
        session.commit()
    return project


def set_project_settings(project: Project, settings: Dict[str, str], session: Session) -> None:
    for name, value in settings.items():
        setting = session.query(ProjectSetting).filter(ProjectSetting.name == name,
                                                       ProjectSetting.project_id == project.id).one_or_none()
        if not setting:
            setting = ProjectSetting(project=project, name=name, value=value)
            session.add(setting)
        elif value != setting.value:
            setting.value = value

    session.commit()


def main():
    engine = get_engine()
    session = get_session(engine)

    create_tables(engine)

    project = get_or_add_project('Azure CLI', session=session)
    for setting in project.settings:
        print(setting)

    # settings = {parts[0].strip(): parts[1].strip() for parts in
    #             (line.strip().split('=', 1) for line in open('env.txt', 'r'))}
    # set_project_settings(project, settings)


if __name__ == '__main__':
    main()
