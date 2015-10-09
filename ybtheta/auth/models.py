from __future__ import absolute_import, unicode_literals

from sqlalchemy.ext.declarative import declared_attr

from ..app import db
from ..util import AutoID, unistr


class Identity(db.Model, AutoID):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    #: The :py:class:`User` this identity refers to.
    user = db.relationship('User', back_populates='identity')

    #: Polymorphic inheritance type discriminator
    type_ = db.Column(db.String(30), convert_unicode=True)

    @declared_attr
    def __mapper_args__(cls):
        """Helper function that sets up Polymorphic inheritance for subclases.
        """
        cls_name = unicode(cls.__name__)
        args = {'polymorphic_identity': cls_name}
        if cls_name == 'Identity':
            args['polymorphic_on'] = cls.type_
        return args


@unistr
class User(db.Model, AutoID):

    #: A :py:class:`list` of the identites for this :py:class:`User`
    identities = db.relationship('Identity', back_populates='user')

    primary_identity_id = db.Column(db.Integer, db.ForeignKey('identity.id'),
                                    nullable=True)

    #: The primary :py:class:`Identity` the user has chosen.
    primary_identity = db.relationship('Identity')

    @property
    def name(self):
        if self.primary_identity and hasattr(self.primary_identity, 'name')
            return self.primary_identity.name
        return str(self)

    def __unicode__(self):
        return 'User({})'.format(self.id)
