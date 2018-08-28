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
    obj.add_field(B_Field("klicnummer", "TEXT", "Klicnummer",
                          is_key_field=True))
    obj.add_field(B_Field("ordernummer", "TEXT", "Ordernummer"))
    obj.add_field(B_Field("meldingsoort", "TEXT", "Meldingsoort"))
    obj.add_field(B_Field("datumTijdAanvraag", "TEXT", "DatumTijdAanvraag"))
    obj.add_field(B_Field("klantReferentie", "TEXT", "KlantReferentie"))
    obj.add_field(B_Field("graafpolygoon", "POLYGON", "Locatie",
                          to_object=gml.Polygon))
    obj.add_field(B_Field("omsluitendeRechthoek", "OBJECT", "Pngformaat",
                          to_object=pngformaat))
    obj.add_field(B_Field("netbeheerderLeveringen", "CONTAINER",
                          "NetbeheerderLeveringen",
                          to_object=netbeheerderLevering))
    obj.add_tags_to_process()
    return obj

def pngformaat():
    pngFormaat = B_Object("Pngformaat")
    pngFormaat.add_field(B_Field("omsluitendeRechthoek", "POLYGON",
                                       "OmsluitendeRechthoek",
                                       to_object=gml.Envelope))
    pngFormaat.add_field(B_Field("pixelsBreed", "TEXT", "PixelsBreed"))
    pngFormaat.add_field(B_Field("pixelsHoog", "TEXT", "PixelsHoog"))
    pngFormaat.add_tags_to_process()
    return pngFormaat

def netbeheerderLevering():
    obj = B_Object("NetbeheerderLevering")
    obj.add_field(B_Field("bedrijfsnaam", "TEXT", "Bedrijfsnaam"))
    obj.add_field(B_Field("bedrijfsnaamAfkorting", "TEXT",
                          "BedrijfsnaamAfkorting"))
    obj.add_field(B_Field("contact", "OBJECT", "Contact", to_object=contact))
    obj.add_field(B_Field("contactpersoon", "OBJECT",
                          "ContactPersoon", to_object=contact))
    obj.add_field(B_Field("belangAanwezig", "TEXT", "BelangAanwezig"))
    obj.add_field(B_Field("storingsnummer", "TEXT", "Storingsnummer"))
    obj.add_field(B_Field("beschadigingsnummer", "TEXT", "Beschadigingsnummer"))
    obj.add_field(B_Field("themas", "CONTAINER", "Themas", to_object=thema))
    obj.add_field(B_Field("bijlagen", "CONTAINER", "Bijlagen",
                          to_object=bijlage))
    obj.add_tags_to_process()
    return obj

def contact():
    obj = B_Object("Contact")
    obj.add_field(B_Field("naam", "TEXT", "Naam"))
    obj.add_field(B_Field("telefoon", "TEXT",
                                    "Telefoon"))
    obj.add_field(B_Field("Email", "TEXT", "Email"))
    obj.add_tags_to_process()
    return obj                    

def toezichthouder():
    obj = contact()
    obj.name = "Toezichthouder"
    return obj

def bijlage():
    a_bijlage = B_Object("Bijlage")
    a_bijlage.add_field(B_Field("bestandsnaam", "TEXT", "Bestandsnaam"))
    a_bijlage.add_tags_to_process()
    return a_bijlage

def huisaansluiting():
    obj = bijlage()
    obj.name = "Huisaansluitschets"
    return obj

def themaBijlage():
    obj = bijlage()
    obj.name = "ThemaBijlage"
    return obj

def thema():
    a_thema = B_Object("Thema")
    a_thema.add_field(B_Field("themanaam", "TEXT", "Themanaam"))
    a_thema.add_field(B_Field("toezichthouders", "CONTAINER",
                              "Toezichthouders", to_object=toezichthouder))
    a_thema.add_field(B_Field("EisVoorzorgmaatregel", "TEXT",
                              "EisVoorzorgmaatregel"))
    a_thema.add_field(B_Field("ligging", "OBJECT",
                              "Ligging", to_object=bijlage))
    a_thema.add_field(B_Field("maatvoering", "OBJECT",
                              "Maatvoering", to_object=bijlage))
    a_thema.add_field(B_Field("annotatie", "OBJECT",
                              "Annotatie", to_object=bijlage))
    a_thema.add_field(B_Field("huisaansluitschetsen", "CONTAINER",
                              "Huisaansluitschetsen", to_object=huisaansluiting))
    a_thema.add_field(B_Field("themaBijlagen", "CONTAINER",
                              "ThemaBijlagen", to_object=themaBijlage))
    a_thema.add_tags_to_process()
    return a_thema                    

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

