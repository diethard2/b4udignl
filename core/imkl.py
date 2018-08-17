"""
/***************************************************************************
 imkl module is used to creat all imkl objects defined in de xml-files.
 - unet(utility net)
 - unet_element (connects utilitynet with utilitylink 1..n relation)
 - ulink (utility link, holds geometry + status/precision)
 - imkl_waterleiding (water main)
 - imkl_mantelbuis (sleeve pipe)
 -------------------
 begin                : 2018-06-01
 copyright            : (C) 2018 by Diethard Jansen
 email                : hulp at GIS-hulp.nl
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
import gml
from basis import B_Object, B_Field
from xml_utils import B_XmlProcessor, clean_tag

# for old version of IMKL messages (before 1-1-2019)
def leveringsInformatie():
    obj = B_Object("LeveringsInformatie")
    obj.add_field(B_Field("version", "TEXT", "Version"))
    obj.add_field(B_Field("klicnummer", "TEXT", "Klicnummer", is_key_field=True)))
    obj.add_field(B_Field("orderNummer", "TEXT", "Ordernummer"))
    obj.add_field(B_Field("meldingsoort", "TEXT", "Meldingsoort"))
    obj.add_field(B_Field("graafpolygoon", "POLYGON", "IMKL_Locatie",
                          to_object=gml.Polygon))
    obj.add_field(B_Field("omsluitendeRechthoek", "POLYGON", "Pngformaat",
                          to_object=Pngformaat))    
    obj.add_tags_to_process()
    return obj

class IMKL_Locatie(B_XmlProcessor):
    """ To process an xml_element as an object, because structure is a
    bit too complicated to extract value from
    """
    def __init__(self):
        B_XmlProcessor.__init__(self)
        self.geom_text=''

    def process(self, xml_element):
        polygon = gml.Polygon()
        polygon._process_polygon(xml_element)
        self.geom_text = polygon.as_wkt()

     def as_text(self):
        return self.geom_text    
    
class Pngformaat(B_XmlProcessor):
    """ To process an xml_element as an object, because structure is a
    bit too complicated to extract value from
    """
    
    def __init__(self):
        B_XmlProcessor.__init__(self)
        self.geom_text=''
        self.pixels_width=0
        self.pixels_heigth=0

    def process(self, xml_element):
        for i_elem in xml_element:
            tag = clean_tag(i_elem)
            if tag == 'OmsluitendeRechthoek':
                polygon = gml.Envelope()
                polygon.process(i_elem)
                self.geom_text = polygon.as_wkt()

    def as_text(self):
        return self.geom_text


# for new version of IMKL messages (after 1-1-2019)
def aanduidingEisVoorzorgsmaatregel():
    obj = B_Object("AanduidingEisVoorzorgsmaatregel")
    obj.add_field(B_Field("id", "TEXT", "identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_tags_to_process()
    return obj

def extraGeometrie():
    obj = B_Object("ExtraGeometrie")
    obj.add_field(B_Field("id", "TEXT", "identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "beginLifespanVersion"))
    obj.add_field(B_Field("network_id", "TEXT", "inNetwork",
                          from_attribute='href'))
    obj.add_field(B_Field("vlakgeometrie", "POLYGON", "vlakgeometrie2D",
                          to_object=gml.Polygon))
    obj.add_tags_to_process()
    return obj

def olieGasChemicalienPijpleiding():
    obj = B_Object("OlieGasChemicalienPijpleiding")
    obj.add_field(B_Field("id", "TEXT", "inspireId",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "beginLifespanVersion"))
    obj.add_field(B_Field("network_id", "TEXT", "inNetwork",
                          from_attribute='href'))
    obj.add_field(B_Field("link_id", "TEXT", "link",
                          from_attribute='href'))
    obj.add_field(B_Field("status", "TEXT", "currentStatus",
                          from_attribute='href'))
    obj.add_field(B_Field("aanwezig_vanaf", "TEXT", "validFrom"))
    obj.add_field(B_Field("vertical_position", "TEXT", "verticalPosition"))
    obj.add_field(B_Field("diameter", "REAL", "pipeDiameter"))
##TODO maybe later, now I can not handle attribute and values in 1 XML-element
##     and output these in two separate fields.
##    obj.add_field(B_Field("diameter_eenheid", "TEXT", "pipeDiameter",
##                          from_attribute='uom'))
    obj.add_field(B_Field("druk", "REAL", "pressure"))
##    obj.add_field(B_Field("druk_eenheid", "TEXT", "pressure",
##                          from_attribute='uom'))
    obj.add_field(B_Field("fluid", "TEXT", "oilGasChemicalsProductType",
                          from_attribute='href'))
    obj.add_field(B_Field("geom_id", "TEXT", "extraGeometrie",
                          from_attribute='href'))
    obj.add_field(B_Field("label", "TEXT", "label"))
    obj.add_tags_to_process()
    return obj

def utiliteitsnet():
    obj = B_Object("utiliteitsnet")
    obj.add_field(B_Field("id", "TEXT", "inspireId",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("naam_contactpersoon", "TEXT",
                          "technischContactpersoon",
                          to_object=Unet_Contactpersoon))
    obj.add_field(B_Field("telefoon_contactpersoon", "TEXT",
                          "technischContactpersoon",
                          to_object=Unet_Contactpersoon))
    obj.add_field(B_Field("email_contactpersoon", "TEXT",
                          "technischContactpersoon",
                          to_object=Unet_Contactpersoon))
    obj.add_tags_to_process()
    return obj

def sql_creation_statements():
    sql_statements = []
    for i_object in imkl_objects.values():
        sql_statements.extend(i_object.sql_create_table_statements())
    return sql_statements

class IMKL_Id(B_XmlProcessor):
    """ To process xml_element with tag identifier or NEN3610ID
    which is part of many IMKL objects 
    """

    def __init__(self):
        B_XmlProcessor.__init__(self)
        self.id = ""                
        self._add_tags_to_process()

    def _add_tags_to_process(self):
        tags_methods = (("Identifier", self._process_id),
                        ("NEN3610ID", self._process_id))

        for i_tag, i_method in tags_methods:
            self.add_tag_method_to_process(i_tag, i_method)

    def _process_id(self, elem):
        for i_elem in elem:
            tag = clean_tag(i_elem.tag)
            if tag == 'namespace':
                self._process_namespace(i_elem)
            elif tag in ('lokaalID', 'localId'):
                self._process_localId(i_elem)

    def _process_namespace(self, elem):
        self.id = elem.text + self.id

    def _process_localId(self, elem):
        self.id = self.id + '-' + elem.text

    def as_text(self):
        return self.id

