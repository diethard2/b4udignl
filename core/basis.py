"""
/***************************************************************************
 basis contains two classes B_Field and B_Object that together build up
 the basis_object.
 -------------------
 begin                : 2015-07-10
 copyright            : (C) 2015 by Diethard Jansen
 email                : Diethard.Jansen at Gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from xml_utils import *

class B_Field(object):
    """general attribute object, fields are created for target collection"""

    GEOMETRY_TYPES = ("POINT","LINESTRING","POLYGON","MULTIPOLYGON")
    ALL_TYPES = GEOMETRY_TYPES + ("TEXT", "INTEGER", "REAL")


    def __init__(self, field_name, field_type, from_tag, from_attribute=None,to_object=None, is_mandatory=True,
                 is_key_field=False):
        """create field object

        name: is name used in target table or CSV header
        type: is type used in sql table, and used by sql_value to deliver
              correct value to insert in table.
        is_key_field: is key field that should contain a unique value
        tag_to_object: to convert geometry from GML to WKT, an xml element
                       is passed to GML-object which returns correct WKT-value
        value: holds the raw tekst value which can be used to create csv-files
               to create a value to store in SQL db use sql_value.
        """
        self.__name = field_name
        self.__type = None
        self.__from_tag = from_tag
        self.__from_attribute = from_attribute
        # set field value using object.. i.e. gml polygon -> wkt geometry
        self.__to_object = to_object
        self.__is_mandatory = is_mandatory
        self.__is_key_field = is_key_field
        self.__sql_template = None
        self.__value = None
        # set type using property set function, will also set __sql_template!
        self.type = field_type

    def _name(self):
        return self.__name

    name = property(fget=_name, doc="name is attribute name in database")

    def _type(self):
        return self.__type

    def _set_type(self, field_type):
        self.__type = field_type
        self._set_sql_template()

    type = property(fget=_type, fset=_set_type,
                    doc="type is one of database type")

    def _value(self):
        return self.__value

    def _set_value(self, value):
        self.__value = value

    value = property(fget=_value, fset=_set_value,
                    doc="value is the raw textvalue")
    
    def _is_key_field(self):
        return self.__is_key_field

    is_key_field = property(fget=_is_key_field,
                    doc="Is this a key field --> boolean")

    def _is_mandatory(self):
        return self.__is_mandatory

    is_mandatory = property(fget=_is_mandatory,
                    doc="Is this a mandatory field --> boolean")

    def _from_tag(self):
        return self.__from_tag

    from_tag = property(fget=_from_tag,
                        doc="tag found in xml to create field from")

    def _from_attribute(self):
        return self.__from_attribute

    from_attribute = property(fget=_from_attribute,
                              doc="attribute to find in xml element")

    def _to_object(self):
        return self.__to_object

    to_object = property(fget=_to_object,
                          doc="object that needs to be created \
to get value frome")

    def _set_sql_template(self):
        sql_template = "%s"
        if self.type == 'TEXT':
            sql_template = "'%s'"
        elif self.type in B_Field.GEOMETRY_TYPES:
            sql_template = "GeomFromText('%s', 28992)"
        self.__sql_template = sql_template        
        
    def set_value_from_xml(self, xml_element):
        """Convert contents of xml_element into field value."""
        if self.to_object is not None:
            if self.from_tag == clean_tag(xml_element.tag):
                an_object = self.to_object()
                an_object.process(xml_element)
                self.value = an_object.as_text()            
        elif self.from_attribute is not None:
            for i_key, i_value in xml_element.attrib.items():
                if clean_tag(i_key) == self.from_attribute:
                    self.value = i_value
                    break
        else:
            self.value = xml_element.text
        if self.value is None:
            self.value = ''
            
    def sql_value(self):
        value = self.value
        if self.type == 'TEXT' and value is not None:
            value = value.replace("'", "''")
        return self.__sql_template % value
        
    def is_geometry(self):
        '''Depending on type returns true or false

        Purpose, for creation of datamodel from object.
        '''
        return self.type in B_Field.GEOMETRY_TYPES

    def sql_definition(self):
        """Returns definition for field in sql."""
        definition = self.name + " " + self.type
        if self.is_mandatory == True:
            definition += " NOT NULL"
        if self.is_key_field == True:
            definition += " PRIMARY KEY"
        return definition                        
     
class B_Object(B_XmlProcessor):
    """Parent class for all Basis Classes i.e. defined in bag.py."""

    def __init__(self, name):
        B_XmlProcessor.__init__(self)
        # attributes
        self.name = name
        self.fields = []
        self.tag2field = {}
        # for caching variable
        self.tag = None
 
    def add_field(self, field):
        self.fields.append(field)
        self.tag2field[field.from_tag] = field

    def process_field(self, xml_element):
        """Convert contents of xml_element into field_value."""
        a_field = self.tag2field[self.tag]
        a_field.set_value_from_xml(xml_element)

    def add_tags_to_process(self):
        """indicate which tags should be processed how"""
        for i_tag in self.tag2field.keys():
            self.add_tag_method_to_process(i_tag, self.process_field)
            
    def init_values(self):
        for i_field in self.fields:
            i_field.value = ""

    def geometry_field(self):
        """Returns the geometry field.
        """
        geometry_field = None
        for i_field in self.fields:
            if i_field.is_geometry():
                geometry_field = i_field
        return geometry_field

    def attribute_fields(self):
        attribute_fields = []
        for i_field in self.fields:
            if not i_field.is_geometry():
                attribute_fields.append(i_field)
        return attribute_fields

    def field_names(self):
        '''Gives a list of fieldnames.'''
        return [i_field.name for i_field in self.fields]

    def field_values(self):
        '''Gives a list of field values.'''
        return [i_field.value for i_field in self.fields]

    def field_types(self):
        '''Gives a list of field types.'''
        return [i_field.type for i_field in self.fields]

    def field_names_and_sql_values(self):
        '''Gives field names and field values to include in sql_statement
        for insert --> field_names, sql_values
        '''
        field_names = []
        sql_values = []
        for i_field in self.fields:
            field_names.append(i_field.name)
            sql_values.append(i_field.sql_value())
        return field_names, sql_values            

    def csv_header(self):
        """Return the csv_header."""
        csv_header = ""
        field_names_size = len(self.field_names())
        if field_names_size == 1:
            csv_header = self.field_names()[0]
        elif field_names_size > 1:
            csv_header = ";".join(self.field_names())
        return csv_header 

    def as_csv(self):
        '''Returns CSV line to write a record for current object.'''
        csv_header = ""
        field_names_size = len(self.field_names())
        if field_names_size == 1:
            csv_header = self.field_values()[0]
        elif field_names_size > 1:
            csv_header = ";".join(self.field_values())
        return csv_header 

    def as_sql(self):
        '''Gives SQL insert statement to insert record for current object'''
        field_names, sql_values = self.field_names_and_sql_values()        
        sql = "INSERT INTO %s (" % self.name
        sql += ", ".join(field_names)
        sql += ") VALUES ("
        sql += ", ".join(sql_values)
        sql += ")"
        return sql

    def sql_create_table_statements(self):
        """Returns a list of SQL statements to create table
        with geometry fields and spatial index"""
        sql_statements = [self.sql_drop_table_statement(),
                          self.sql_create_table_statement()]
        if self.geometry_field() is not None:
            sql_statements.append(self.sql_add_geometry_statement())
            sql_statements.append(self.sql_create_index_statement())
        return sql_statements

    def sql_drop_table_statement(self):
        return "DROP TABLE if exists " + self.name

    def sql_create_table_statement(self):
        """Returns sql statement to create table in sql database."""
        sql = "CREATE TABLE %s (" % self.name
        field_definitions = []
        for i_field in self.attribute_fields():
            field_definitions.append(i_field.sql_definition())
        sql += ",".join(field_definitions) + ")"
        return sql

    def sql_add_geometry_statement(self):
        """Returns sql statement to add a geometry column to sql table."""
        geom_field = self.geometry_field()
        sql = "SELECT AddGeometryColumn('%s', " % self.name
        sql += "'geometry', 28992, '%s', 'XY')" % geom_field.type
        return sql

    def sql_create_index_statement(self):
        """Returns sql statement to create spatial index."""
        return "SELECT CreateSpatialIndex('%s', 'geometry')" % self.name

    def is_active(self):
        """returns true if this object is active and should be added
        to spatialite database."""
        is_active = True
        inactive_field = None
        if self.tag2field.has_key("aanduidingRecordInactief"):
            inactive_field = self.tag2field["aanduidingRecordInactief"]
        if inactive_field is not None:
            is_active = inactive_field.value != 'J'
        return is_active
