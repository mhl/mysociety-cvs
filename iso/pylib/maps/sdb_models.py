
import simpledb

import mysociety.config

connection = simpledb.SimpleDB(
    mysociety.config.get('AWS_KEY'), 
    mysociety.config.get('AWS_SECRET')
    )

maps_domain = mysociety.config.get('SIMPLEDB_DOMAIN')

if not connection.has_domain(maps_domain):
    connection.create_domain(maps_domain)


class CantChangeIdentifier(Exception):
    """Exception raised if we're trying to same something with
    the identifier as None."""

class UnstorableValue(Exception):
    """Tried to store in a field a value that can't be put there."""

class NullableField(simpledb.models.Field):
    """This field allows the storing and recovery of a Python None.
    (obviously, it will all go horribly wrong if you try to store 
    _NONE_VALUE, so don't do that!)"""

    # This is the value we'll use in SimpleDB to represent a Python None
    _NONE_VALUE = '(*None*)'

    def encode(self, value):
        if value is None:
            return self._NONE_VALUE
        elif value == self._NONE_VALUE:
            raise UnstorableValue("Can't store '%s', we're using that for None." %self._NONE_VALUE)
        else:
            return value

    def decode(self, value):
        if value == self._NONE_VALUE:
            return None
        else:
            return value

class IntegerField(simpledb.models.NumberField):
    def decode(self, value):
        """
        Decoding converts a string into an int then shifts it by the
        offset.
        """
        return int(value) - self.offset

class SDBMap(simpledb.models.Model):
    """Represents the Map as stored in SimpleDB."""

    identifier = simpledb.models.ItemName()

    target_e = IntegerField(padding=6, precision=0, required=True)
    target_n = IntegerField(padding=7, precision=0, required=True) # Need 7 for Orkney
    postcode = simpledb.models.Field()
    station_text_id = NullableField()
    target_time = IntegerField(padding=4, precision=0, required=True) # Minutes after midnight
    target_limit_time = IntegerField(padding=4, precision=0, required=True)
    arrive_by = simpledb.models.BooleanField(required=True) # Depart after if False
    queued_at = simpledb.models.DateTimeField()
    working_started = simpledb.models.DateTimeField()
    working_finished = simpledb.models.DateTimeField()
    file_location = simpledb.models.Field()
    failure_message = simpledb.models.Field()

    class Meta:
        connection = connection
        domain = maps_domain

    def get_identifier(self):
        """This will return the identifier we will use to name this object
        in simpledb and in sqs (or indeed anywhere else)."""
        return "%s_%s_%s_%s_%s_%s" %(
            self.fields['target_e'].encode(self.target_e),
            self.fields['target_n'].encode(self.target_n),
            self.fields['station_text_id'].encode(self.station_text_id),
            self.fields['arrive_by'].encode(self.arrive_by),
            self.fields['target_time'].encode(self.target_time),
            self.fields['target_limit_time'].encode(self.target_limit_time),
            )

    def save(self, *args, **kwargs):
        """Save is overridden to automatically create the identifier."""

        new_identifier = self.get_identifier()

        # If we don't yet have an identifier, then create it.
        if not self.identifier:
            self.identifier = new_identifier
        
        # Don't allow a save which changes the identifier.
        if self.identifier != new_identifier:
            raise CantChangeIdentifier(
                """Trying to save a Map in a way that would change the identifier.
Old identifier: %s
New identifier: %s """ %(self.identifier, new_identifier)
                )

        return super(SDBMap, self).save(*args, **kwargs)

