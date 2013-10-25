from framework import StoredObject, fields


class Guid(StoredObject):

    _id = fields.StringField()
    referent = fields.AbstractForeignField(backref='guid')

    _meta = {
        'optimistic': True
    }


class GuidStoredObject(StoredObject):

    def __init__(self, *args, **kwargs):
        """Overridden constructor. When a GuidStoredObject is instantiated,
        create a new Guid if the object doesn't already have one, then attach
        the Guid to the StoredObject.

        Note: This requires saving the StoredObject once and the Guid twice to
        ensure correct back-references; this could be made more efficient if
        modular-odm could handle back-references of objects that have not been
        saved.

        """
        # Call superclass constructor
        super(GuidStoredObject, self).__init__(*args, **kwargs)

        # Done if primary key exists
        if self._primary_key:
            return

        # Create GUID
        guid = Guid()
        guid.save()

        # Set primary key to GUID key
        self._primary_key = guid._primary_key
        self.save()

        # Add self to GUID
        guid.referent = self
        guid.save()

    @property
    def annotations(self):
        """ Get meta-data annotations associated with object. """
        return self.metadata__annotated