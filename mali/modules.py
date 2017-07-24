from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.engine import Engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# pylint: disable=invalid-name, too-few-public-methods

Base = declarative_base()


class Project(Base):
    __tablename__ = 'db_project'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    settings = relationship('ProjectSetting', back_populates='project')

    def __repr__(self):
        return f'<Project(name={self.name})>'


class ProjectSetting(Base):
    __tablename__ = 'db_projectsetting'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    project_id = Column(Integer, ForeignKey('db_project.id'))
    project = relationship(Project, back_populates='settings')

    def __repr__(self):
        return f'<ProjectSetting(name={self.name},value={self.value})>'


class User(Base):
    __tablename__ = 'db_user'
    id = Column(String, primary_key=True)

    def __repr__(self):
        return f'<User(id={self.id})>'


def create_tables(engine: Engine) -> None:
    Base.metadata.create_all(engine)
