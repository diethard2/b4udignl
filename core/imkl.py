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

AANDUIDINGEISVOORZORGSMAATREGEL = "AanduidingEisVoorzorgsmaatregel"
APPURTENANCE = "Appurtenance"
BELANG = "Belang"
BELANGHEBBENDE = "Belanghebbende"
BOUNDEDBY = "boundedBy"
EXTRAGEOMETRY = "ExtraGeometrie"
FEATURECOLLECTION = "FeatureCollection"
GRAAFPOLYGOON = "Graafpolygoon"
LEVERINGSINFORMATIE = "Leveringsinformatie"
OLIEGASCHEMICALIENPIJPLEIDING = "OlieGasChemicalienPijpleiding"
UTILITEITSNET = "Utiliteitsnet"


# for old version of IMKL messages (before 1-1-2019)
def leveringsinformatie():
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
    # imkl version 1.5
    obj.add_field(B_Field("omsluitendeRechthoek", "OBJECT", "Pngformaat",
                          to_object=pngformaat))
    obj.add_field(B_Field("netbeheerderLeveringen", "CONTAINER",
                          "NetbeheerderLeveringen",
                          to_object=netbeheerderLevering))
    # imkl version 2.1
    obj.add_field(B_Field("bijlagenPerLevering", "CONTAINER",
                          "BijlagePerLevering",
                          to_object=bijlagePerLevering,
                          is_virtual=True))
    obj.add_field(B_Field("pngFormaat", "OBJECT", "PngFormaat",
                          to_object=pngformaat))
    obj.add_field(B_Field("belanghebbenden", "CONTAINER",
                          "Belanghebbende",
                          to_object=belanghebbende,
                          is_virtual=True))
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
                          "Contactpersoon", to_object=contact))
    obj.add_field(B_Field("belangAanwezig", "TEXT", "BelangAanwezig"))
    obj.add_field(B_Field("storingsnummer", "TEXT", "Storingsnummer"))
    obj.add_field(B_Field("beschadigingsnummer", "TEXT", "Beschadigingsnummer"))
    obj.add_field(B_Field("themas", "CONTAINER", "Themas", to_object=thema))
    obj.add_field(B_Field("bijlagen", "CONTAINER", "Bijlagen",
                          to_object=bijlage))
    obj.add_field(B_Field("topo", "OBJECT", "EigenTopo", to_object=bijlage))
    obj.add_field(B_Field("plan_topo", "OBJECT", "PlanTopo", to_object=bijlage))
    obj.add_tags_to_process()
    return obj

def contact():
    obj = B_Object("Contact")
    obj.add_field(B_Field("naam", "TEXT", "Naam"))
    obj.add_field(B_Field("telefoon", "TEXT",
                                    "Telefoon"))
    obj.add_field(B_Field("email", "TEXT", "Email"))
    obj.add_field(B_Field("fax", "TEXT", "Fax"))
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

def detailkaart():
    obj = bijlage()
    obj.name = "Detailkaart"
    return obj

def huisaansluitschets():
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
    a_thema.add_field(B_Field("eisVoorzorgmaatregel", "TEXT",
                              "EisVoorzorgmaatregel"))
    a_thema.add_field(B_Field("ligging", "OBJECT",
                              "Ligging", to_object=bijlage))
    a_thema.add_field(B_Field("maatvoering", "OBJECT",
                              "Maatvoering", to_object=bijlage))
    a_thema.add_field(B_Field("annotatie", "OBJECT",
                              "Annotatie", to_object=bijlage))
    a_thema.add_field(B_Field("detailkaarten", "CONTAINER",
                              "Detailkaarten", to_object=detailkaart))
    a_thema.add_field(B_Field("huisaansluitschetsen", "CONTAINER",
                              "Huisaansluitschetsen", to_object=huisaansluitschets))
    a_thema.add_field(B_Field("themaBijlagen", "CONTAINER",
                              "ThemaBijlagen", to_object=themaBijlage))
    a_thema.add_tags_to_process()
    return a_thema                    

# for new version of IMKL messages (after 1-1-2019)
def aanduidingEisVoorzorgsmaatregel():
    obj = B_Object("AanduidingEisVoorzorgsmaatregel")
    obj.add_field(B_Field("id", "TEXT", "Identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("label", "TEXT", "Label"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("eisVoorzorgsmaatregel", "TEXT", "EisVoorzorgsmaatregel"))
    obj.add_field(B_Field("contactVoorzorgsmaatregel", "OBJECT",
                          "ContactVoorzorgsmaatregel",to_object=contactpersoon))
    obj.add_field(B_Field("netbeheerderNetOmschrijving", "TEXT", "NetbeheerderNetOmschrijving"))
    obj.add_field(B_Field("netbeheerderWerkAanduiding", "TEXT", "NetbeheerderWerkAanduiding"))
    obj.add_field(B_Field("geometrie", "POLYGON", "Geometrie",
                          to_object=gml.Polygon))
    obj.add_tags_to_process()
    return obj

def appurtenance():
    obj = B_Object("Appurtenance")
    obj.add_field(B_Field("id", "TEXT", "InspireId",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("currentStatus", "TEXT", "CurrentStatus",
                          from_attribute='Href'))
    obj.add_field(B_Field("validFrom", "TEXT", "ValidFrom"))
    obj.add_field(B_Field("validTo", "TEXT", "ValidTo"))
    obj.add_field(B_Field("verticalPosition", "TEXT", "VerticalPosition"))
    obj.add_field(B_Field("appurtenanceType", "TEXT", "AppurtenanceType",
                          from_attribute='Href'))
    obj.add_field(B_Field("label", "TEXT", "Label"))
    obj.add_field(B_Field("geometry", "POINT", "Geometry",
                          to_object=gml.Point))
    obj.add_tags_to_process()
    return obj


def boundedBy():
    obj = B_Object("boundedBy")
    obj.add_field(B_Field("envelope", "POLYGON", "Envelope",
                          to_object=gml.Envelope))
    obj.add_tags_to_process()
    return obj

def extraGeometrie():
    obj = B_Object("ExtraGeometrie")
    obj.add_field(B_Field("id", "TEXT", "Identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("vlakgeometrie", "POLYGON", "Vlakgeometrie2D",
                          to_object=gml.Polygon))
    obj.add_tags_to_process()
    return obj

def gebiedsinformatieAanvraag():
    obj = B_Object("GebiedsinformatieAanvraag")
    obj.add_field(B_Field("id", "TEXT", "Identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT",
                          "BeginLifespanVersion"))
    obj.add_field(B_Field("ordernummer", "TEXT",
                          "Ordernummer"))
    obj.add_field(B_Field("positienummer", "TEXT",
                          "Positienummer"))
    obj.add_field(B_Field("klicMeldnummer", "TEXT",
                          "KlicMeldnummer"))
    obj.add_field(B_Field("aanvragers", "CONTAINER",
                          "Aanvrager", to_object=aanvrager))
    obj.add_field(B_Field("referentie", "TEXT",
                          "Referentie"))
    obj.add_tags_to_process()
    return obj

def aanvrager():
    obj = B_Object("Aanvrager")
    obj.add_field(B_Field("contactpersoon", "OBJECT", "Contactpersoon",
                          to_object=contactpersoon))
    obj.add_field(B_Field("organisatie", "CONTAINER", "Organisatie",
                          to_object=organisatie))
    obj.add_tags_to_process()
    return obj

def contactpersoon():
    obj = B_Object("Contactpersoon")
    obj.add_field(B_Field("contact", "OBJECT", "Contact",
                          to_object=contact))
    obj.add_tags_to_process()
    return obj

def organisatie():
    obj = B_Object("Organisatie")
    obj.add_field(B_Field("bezoekadres", "OBJECT", "BezoekAdres",
                          to_object=bezoekadres))
    obj.add_tags_to_process()
    return obj

def bezoekadres():
    obj = B_Object("BezoekAdres")
    obj.add_field(B_Field("adres", "OBJECT", "Adres",
                          to_object=adres))
    obj.add_tags_to_process()
    return obj

def adres():
    obj = B_Object("Adres")
    obj.add_field(B_Field("openbareRuimte", "TEXT", "OpenbareRuimteNaam"))
    obj.add_field(B_Field("huisnummer", "TEXT", "Huisnummer"))
    obj.add_field(B_Field("woonplaats", "TEXT", "WoonplaatsNaam"))
    obj.add_field(B_Field("postcode", "TEXT", "Postcode"))
    obj.add_field(B_Field("landcode", "TEXT", "Landcode"))
    obj.add_tags_to_process()
    return obj

def graafpolygoon():
    obj = B_Object("Graafpolygoon")
    obj.add_field(B_Field("id", "TEXT", "Identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("geometrie", "POLYGON", "Geometrie",
                          to_object=gml.Polygon))
    obj.add_tags_to_process()
    return obj

def olieGasChemicalienPijpleiding():
    obj = B_Object("OlieGasChemicalienPijpleiding")
    obj.add_field(B_Field("id", "TEXT", "InspireId",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("link_id", "TEXT", "Link",
                          from_attribute='Href'))
    obj.add_field(B_Field("status", "TEXT", "CurrentStatus",
                          from_attribute='Href'))
    obj.add_field(B_Field("aanwezig_vanaf", "TEXT", "ValidFrom"))
    obj.add_field(B_Field("vertical_position", "TEXT", "VerticalPosition"))
    obj.add_field(B_Field("diameter", "REAL", "PipeDiameter"))
##TODO maybe later, now I can not handle attribute and values in 1 XML-element
##     and output these in two separate fields.
##    obj.add_field(B_Field("diameter_eenheid", "TEXT", "pipeDiameter",
##                          from_attribute='uom'))
    obj.add_field(B_Field("druk", "REAL", "Pressure"))
##    obj.add_field(B_Field("druk_eenheid", "TEXT", "pressure",
##                          from_attribute='uom'))
    obj.add_field(B_Field("fluid", "TEXT", "OilGasChemicalsProductType",
                          from_attribute='Href'))
    obj.add_field(B_Field("geom_id", "TEXT", "ExtraGeometrie",
                          from_attribute='Href'))
    obj.add_field(B_Field("label", "TEXT", "Label"))
    obj.add_tags_to_process()
    return obj

def utiliteitsnet():
    obj = B_Object("utiliteitsnet")
    obj.add_field(B_Field("id", "TEXT", "InspireId",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("naam_contactpersoon", "TEXT",
                          "TechnischContactpersoon",
                          to_object=Unet_Contactpersoon))
    obj.add_field(B_Field("telefoon_contactpersoon", "TEXT",
                          "TechnischContactpersoon",
                          to_object=Unet_Contactpersoon))
    obj.add_field(B_Field("email_contactpersoon", "TEXT",
                          "TechnischContactpersoon",
                          to_object=Unet_Contactpersoon))
    obj.add_tags_to_process()
    return obj

def bijlagePerLevering():
    a_bijlage = B_Object("BijlagePerLevering")
    a_bijlage.add_field(B_Field("soort_bijlage", "TEXT", "SoortBijlage"))
    a_bijlage.add_field(B_Field("bestandlocatie", "TEXT", "BestandLocatie"))
    a_bijlage.add_field(B_Field("bestandidentificator", "TEXT", "BestandIdentificator"))
    a_bijlage.add_tags_to_process()
    return a_bijlage

def bijlagePerNetbeheerder():
    a_bijlage = bijlagePerLevering()
    a_bijlage.name = "BijlagePerNetbeheerder"
    return a_bijlage

def belanghebbende():
    obj = B_Object("Belanghebbende")
    obj.add_field(B_Field("id", "TEXT", "Identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("bronhoudercode", "TEXT", "Bronhoudercode"))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("beheerdersinformatieGeleverd", "TEXT",
                          "BeheerdersinformatieGeleverd"))
    obj.add_field(B_Field("betrokkenBijAanvraag", "TEXT",
                          "BetrokkenBijAanvraag"))
    obj.add_field(B_Field("eisVoorzorgsmaatregel", "TEXT", "EisVoorzorgsmaatregel"))
    obj.add_field(B_Field("contactVoorzorgsmaatregel", "OBJECT",
                          "ContactVoorzorgsmaatregel",to_object=contactpersoon))
    obj.add_field(B_Field("netbeheerderNetOmschrijving", "TEXT", "NetbeheerderNetOmschrijving"))
    obj.add_field(B_Field("idGeraaktBelang", "TEXT",
                          "GeraaktBelangBijGraafpolygoon",
                          from_attribute='Href'))
    obj.add_field(B_Field("idNetbeheerder", "TEXT", "Netbeheerder",
                          from_attribute='Href'))
    obj.add_field(B_Field("bijlagen", "CONTAINER",
                          "BijlagePerNetbeheerder",
                          to_object=bijlagePerNetbeheerder,
                          is_virtual=True))
    obj.add_field(B_Field("beheerdersinformatie", "CONTAINER",
                          "Beheerdersinformatie",
                          to_object=beheerdersinformatie,
                          is_virtual=True))
    obj.add_tags_to_process()
    return obj

def belang():
    obj = B_Object("Belang")
    obj.add_field(B_Field("id", "TEXT", "Identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("omschrijving", "TEXT", "Omschrijving"))
    obj.add_field(B_Field("contactAanvraag", "OBJECT",
                          "ContactAanvraag",to_object=contactAanvraag))
    obj.add_field(B_Field("contactNetinformatie", "OBJECT",
                          "ContactNetinformatie",to_object=contactAanvraag))
    obj.add_field(B_Field("contactBeschadiging", "OBJECT",
                          "ContactBeschadiging",to_object=contactAanvraag))
    obj.add_tags_to_process()
    return obj

def contactAanvraag():
    obj = B_Object("ContactAanvraag")
    obj.add_field(B_Field("aanvraagSoortContact", "OBJECT",
                          "AanvraagSoortContact", to_object=contact))
    obj.add_field(B_Field("contact", "OBJECT",
                          "Contact", to_object=contact))
    obj.add_tags_to_process()
    return obj

def beheerdersinformatie():
    obj = B_Object("Beheerdersinformatie")
    obj.add_field(B_Field("thema", "TEXT", "Thema",
                          from_attribute='Href'))
    obj.add_field(B_Field("eisVoorzorgmaatregel", "TEXT",
                          "EisVoorzorgmaatregel"))
    obj.add_field(B_Field("themaBijlagen", "CONTAINER",
                          "ThemabijlagePerNetbeheerder",
                          to_object=themabijlagePerNetbeheerder,
                          is_virtual=True))
    obj.add_tags_to_process()
    return obj

def themabijlagePerNetbeheerder():
    a_bijlage = bijlagePerLevering()
    a_bijlage.name = "ThemabijlagePerNetbeheerder"
    return a_bijlage

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
            if tag == 'Namespace':
                self._process_namespace(i_elem)
            elif tag in ('LokaalID', 'LocalId'):
                self._process_localId(i_elem)
            elif tag == 'Versie':
                self._process_localId(i_elem)

    def _process_namespace(self, elem):
        self.id = elem.text + self.id

    def _process_localId(self, elem):
        self.id = self.id + '-' + elem.text

    def as_text(self):
        return self.id

