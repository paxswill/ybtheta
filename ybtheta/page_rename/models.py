from __future__ import absolute_import

from sqlalchemy.ext.declarative import declared_attr

from ..database import db
from ..util import AutoID, AutoName


class RenamedPage(db.Model, AutoID, AutoName):

    renamed_path = db.Column('original_path', db.String(255), nullable=True,
            unique=True)

    renamed_canonical = db.Column(db.Boolean, default=False, nullable=False)

    type_ = db.Column(db.String(50))

    @declared_attr
    def __mapper_args__(cls):
        cls_name = cls.__name__
        args = {'polymorphic_identity': cls_name}
        if cls_name == 'RenamedPage':
            args['polymorphic_on'] = cls.type_
        return args

    def __repr__(self):
        return 'RenamedPage({}, {})'.format(self.renamed_path,
                self.renamed_canonical)
