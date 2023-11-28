#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-08-03 14:22:04
LastEditors  : Kofi
LastEditTime : 2023-08-03 14:22:05
Description  : 
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


class BaseRepository:
    def __init__(self, session, model_class):
        self.session = session
        self.model_class = model_class

    def add(self, model):
        try:
            self.session.add(model)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def update(self, model):
        try:
            current = (
                self.session.query(self.model_class).filter_by(id=model.id).first()
            )
            if current:
                self.session.merge(model)
            else:
                self.session.add(model)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def delete(self, model):
        try:
            current = (
                self.session.query(self.model_class).filter_by(id=model.id).first()
            )
            self.session.delete(current)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get(self, **kwargs):
        return self.session.query(self.model_class).filter_by(**kwargs).first()

    def list_all(self):
        return self.session.query(self.model_class).all()

    def filter_list(self, filters):
        query = self.session.query(self.model_class)
        for item in filters:
            query = query.filter(item)
        return query.all()

    def paginate(self, current_page=1, page_size=10):
        query = self.session.query(self.model_class)
        data = query.limit(page_size).offset(page_size * (current_page - 1)).all()
        total_count = query.count()
        total_pages = total_count // page_size + (total_count % page_size > 0)
        return {
            "datas": data,
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": current_page,
        }

    def execute_query(self, query):
        return self.session.execute(query)


def transactional(fn):
    def wrapper(*args, **kwargs):
        session = Session()
        try:
            session.begin()
            result = fn(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper
