from __future__ import absolute_import

from sqlalchemy.ext.declarative import declared_attr
from flask.ext.login import UserMixin

from ..database import db
from ..util import AutoID, AutoName


class Identity(db.Model, AutoName, AutoID, UserMixin):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    #: The :py:class:`User` this identity refers to.
    user = db.relationship('User', backref='identities',
            foreign_keys=[user_id])

    #: Polymorphic inheritance type discriminator
    type_ = db.Column(db.String(30, convert_unicode=True))

    @declared_attr
    def __mapper_args__(cls):
        """Helper function that sets up Polymorphic inheritance for subclases.
        """
        cls_name = unicode(cls.__name__)
        args = {'polymorphic_identity': cls_name}
        if cls_name == 'Identity':
            args['polymorphic_on'] = cls.type_
        return args

    def get_id(self):
        return unicode(self.id)


class GoogleIdentity(Identity):

    id = db.Column(db.Integer, db.ForeignKey('identity.id'), primary_key=True)

    token = db.Column(db.String(255), nullable=False)

    google_id = db.Column(db.String(255), nullable=False, index=True,
            unique=True)

    email = db.Column(db.String(255), nullable=True)

    name = db.Column(db.String(255), nullable=True)


class FacebookIdentity(Identity):

    id = db.Column(db.Integer, db.ForeignKey('identity.id'), primary_key=True)


class User(db.Model, AutoName, AutoID):

    primary_identity_id = db.Column(db.Integer, db.ForeignKey('identity.id'),
                                    nullable=True)

    #: The primary :py:class:`Identity` the user has chosen.
    primary_identity = db.relationship('Identity',
            foreign_keys=[primary_identity_id], uselist=False)

    @property
    def name(self):
        if self.primary_identity and hasattr(self.primary_identity, 'name'):
            return self.primary_identity.name
        return str(self)

    def __repr__(self):
        return 'User({})'.format(self.id)
