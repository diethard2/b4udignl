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

AANDUIDINGEV = "AanduidingEisVoorzorgsmaatregel"
ANNOTATIE = "Annotatie"
APPURTENANCE = "Appurtenance"
BEHEERDER = "Beheerder"
BELANG = "Belang"
BELANGHEBBENDE = "Belanghebbende"
BIJLAGE = "Bijlage"
BOUNDEDBY = "BoundedBy"
DIEPTETOVMAAIVELD = "DiepteTovMaaiveld"
DIEPTENAP = "DiepteNAP"
DUCT="Duct"
EIGENTOPOGRAFIE="EigenTopografie"
ELEKTRICITEITSKABEL="Elektriciteitskabel"
EVBIJLAGE = "EisVoorzorgsmaatregelBijlage"
EXTRADETAILINFO = "ExtraDetailinfo"
EXTRAGEOMETRY = "ExtraGeometrie"
FEATURECOLLECTION = "FeatureCollection"
GEBIEDSINFORMATIEAANVRAAG = "GebiedsinformatieAanvraag"
GEBIEDSINFORMATIELEVERING = "GebiedsinformatieLevering"
GRAAFPOLYGOON = "Graafpolygoon"
KABELBED = "Kabelbed"
KAST = "Kast"
LEVERINGSINFORMATIE = "Leveringsinformatie"
MAATVOERING = "Maatvoering"
MANGAT = "Mangat"
MANTELBUIS = "Mantelbuis"
MAST = "Mast"
OLIEGASCHEMICALIENPIJPLEIDING = "OlieGasChemicalienPijpleiding"
OVERIG = "Overig"
RIOOLLEIDING = "Rioolleiding"
TECHNISCHGEBOUW = "TechnischGebouw"
TELECOMMUNICATIEKABEL = "Telecommunicatiekabel"
THERMISCHEPIJPLEIDING = "ThermischePijpleiding"
TOREN = "Toren"
UTILITEITSNET = "Utiliteitsnet"
UTILITYLINK = "UtilityLink"
WATERLEIDING = "Waterleiding"


def tag2function():
    return {AANDUIDINGEV: aanduidingEisVoorzorgsmaatregel,
            ANNOTATIE: annotatie,
            APPURTENANCE: appurtenance,
            BELANG: belang,
            BELANGHEBBENDE: belanghebbende,
            BEHEERDER: beheerder,
            BIJLAGE: bijlage,
            BOUNDEDBY: boundedBy,
            DIEPTETOVMAAIVELD: diepteTovMaaiveld,
            DIEPTENAP: diepteNAP,
            DUCT: duct,
            EIGENTOPOGRAFIE: eigenTopografie,
            ELEKTRICITEITSKABEL: elektriciteitskabel,
            EVBIJLAGE: eisVoorzorgsmaatregelBijlage,
            EXTRADETAILINFO: extraDetailinfo,
            EXTRAGEOMETRY: extraGeometrie,
            GEBIEDSINFORMATIEAANVRAAG: gebiedsinformatieAanvraag,
            GEBIEDSINFORMATIELEVERING: gebiedsinformatieLevering,
            GRAAFPOLYGOON: graafpolygoon,
            KABELBED: kabelbed,
            KAST: kast,
            LEVERINGSINFORMATIE: leveringsinformatie,
            MAATVOERING: maatvoering,
            MANGAT: mangat,
            MANTELBUIS: mantelbuis,
            MAST: mast,
            OLIEGASCHEMICALIENPIJPLEIDING: olieGasChemicalienPijpleiding,
            OVERIG: overig,
            RIOOLLEIDING: rioolleiding,
            TECHNISCHGEBOUW: technischGebouw,
            TELECOMMUNICATIEKABEL: telecomKabel,
            THERMISCHEPIJPLEIDING: thermischePijpleiding,
            TOREN: toren,
            UTILITEITSNET: utiliteitsnet,
            UTILITYLINK: utilityLink,
            WATERLEIDING: waterleiding}

def tags_pipes_and_cables():
    return (DUCT,ELEKTRICITEITSKABEL,KABELBED,MANTELBUIS,
            OLIEGASCHEMICALIENPIJPLEIDING,OVERIG,RIOOLLEIDING,
            TELECOMMUNICATIEKABEL,THERMISCHEPIJPLEIDING,WATERLEIDING)

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
    obj = imkl_basis()
    obj.name = "EisVoorzorgsmaatregel"
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

def annotatie():
    obj = imkl_basis()
    obj.name = "Annotatie"
    obj.add_field(B_Field("label", "TEXT", "Label"))
    obj.add_field(B_Field("omschrijving", "TEXT", "Omschrijving"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("annotatieType", "TEXT", "AnnotatieType",
                          from_attribute='Href'))
    obj.add_field(B_Field("rotatiehoek", "TEXT", "Rotatiehoek"))
    obj.add_field(B_Field("labelpositie", "CONTAINER",
                          "Labelpositie", to_object=labelpositie))
    obj.add_field(B_Field("thema", "TEXT", "Theme"))
    obj.add_field(B_Field("geometry", "POINT", "Ligging",
                          to_object=gml.Point))
    obj.add_tags_to_process()
    return obj

def maatvoering():
    obj = imkl_basis()
    obj.name = "Maatvoering"
    obj.add_field(B_Field("label", "TEXT", "Label"))
    obj.add_field(B_Field("omschrijving", "TEXT", "Omschrijving"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("maatvoeringsType", "TEXT", "MaatvoeringsType",
                          from_attribute='Href'))
    obj.add_field(B_Field("rotatiehoek", "TEXT", "Rotatiehoek"))
    obj.add_field(B_Field("labelpositie", "CONTAINER",
                          "Labelpositie", to_object=labelpositie))
    obj.add_field(B_Field("thema", "TEXT", "Theme"))
    obj.add_field(B_Field("geometry", "POINT", "Ligging",
                          to_object=gml.Point))
    obj.add_tags_to_process()
    return obj


def bijlage_basis():
    obj = imkl_basis()
    obj.name = "BijlageBasis"
    obj.add_field(B_Field("bijlageType", "TEXT", "BijlageType",
                          from_attribute='Href'))
    obj.add_field(B_Field("bestandlocatie", "TEXT", "BestandLocatie"))
    obj.add_field(B_Field("bestandMediaType", "TEXT", "BestandMediaType",
                          from_attribute='Href'))
    obj.add_field(B_Field("bestandIdentificator", "TEXT",
                          "BestandIdentificator"))
    return obj

def bijlage_v2():
    obj = bijlage_basis()
    obj.name = "Bijlage"
    obj.add_tags_to_process()
    return obj

def eisVoorzorgsmaatregelBijlage():
    obj = bijlage_basis()
    obj.name = "EisVoorzorgsmaatregelBijlage"
    obj.add_field(B_Field("thema", "TEXT", "Thema",
                          from_attribute='Href'))
    obj.add_field(B_Field("eisVoorzorgsmaatregel", "TEXT",
                          "EisVoorzorgsmaatregel"))
    obj.add_field(B_Field("toelichting", "TEXT",
                          "Toelichting"))
    obj.add_tags_to_process()
    return obj

def boundedBy():
    obj = B_Object("boundedBy")
    obj.add_field(B_Field("envelope", "POLYGON", "Envelope",
                          to_object=gml.Envelope))
    obj.add_tags_to_process()
    return obj

def diepte():
    obj = imkl_basis()
    obj.add_field(B_Field("label", "TEXT", "Label"))
    obj.add_field(B_Field("omschrijving", "TEXT", "Omschrijving"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("diepteNauwkeurigheid", "TEXT", "DiepteNauwkeurigheid",
                          from_attribute='Href'))
    obj.add_field(B_Field("dieptePeil", "TEXT", "DieptePeil"))
    obj.add_field(B_Field("datumOpmetingDieptePeil", "TEXT",
                          "DatumOpmetingDieptePeil"))
    obj.add_field(B_Field("diepteAangrijpingspunt", "TEXT",
                          "DiepteAangrijpingspunt",
                          from_attribute='Href'))
    obj.add_field(B_Field("thema", "TEXT", "Theme"))
    obj.add_field(B_Field("geometry", "POINT", "Ligging",
                          to_object=gml.Point))
    return obj

def diepteTovMaaiveld():
    obj = diepte()
    obj.name = "DiepteTovMaaiveld"
    obj.add_tags_to_process()
    return obj
    
def diepteNAP():
    obj = diepte()
    obj.name = "DiepteNAP"
    obj.add_field(B_Field("maaiveldPeil", "TEXT", "MaaiveldPeil"))
    obj.add_field(B_Field("datumOpmetingMaaiveldPeil", "TEXT",
                          "DatumOpmetingMaaiveldPeil"))
    obj.add_tags_to_process()
    return obj

def kabelOfLeiding():
    obj = B_Object("KabelOfLeiding")
    obj.add_field(B_Field("id", "TEXT", "InspireId",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("link_id", "TEXT", "Link",
                          from_attribute='Href'))
    obj.add_field(B_Field("status", "TEXT", "CurrentStatus",
                          from_attribute='Href'))
    obj.add_field(B_Field("validFrom", "TEXT", "ValidFrom"))
    obj.add_field(B_Field("validTo", "TEXT", "ValidTo"))
    obj.add_field(B_Field("verticalPosition", "TEXT", "VerticalPosition"))
    obj.add_field(B_Field("thema", "TEXT", "Theme"))
    obj.add_field(B_Field("geom_id", "TEXT", "ExtraGeometrie",
                          from_attribute='Href'))
    obj.add_field(B_Field("label", "TEXT", "Label"))
    obj.add_field(B_Field("geometry", "LINESTRING", "CentrelineGeometry",
                          to_object=gml.LineString))
    return obj

def duct():
    obj = kabelOfLeiding()
    obj.name = "Duct"
    obj.add_field(B_Field("utilityDeliveryType", "TEXT", "UtilityDeliveryType",
                          from_attribute='Href'))
    obj.add_field(B_Field("warningType", "TEXT", "WarningType",
                          from_attribute='Href'))
    obj.add_field(B_Field("ductWidth", "TEXT", "DuctWidth"))
    obj.add_tags_to_process()
    return obj

def elektriciteitskabel():
    obj = kabelOfLeiding()
    obj.name = "Elektriciteitskabel"
    obj.add_field(B_Field("warningType", "TEXT", "WarningType",
                          from_attribute='Href'))
    obj.add_field(B_Field("operatingVoltage", "TEXT", "OperatingVoltage"))
    obj.add_field(B_Field("nominalVoltage", "TEXT", "NominalVoltage"))
    obj.add_field(B_Field("geoNauwkeurigheidXY", "TEXT", "GeoNauwkeurigheidXY",
                          from_attribute='Href'))
    obj.add_field(B_Field("kabelDiameter", "TEXT", "KabelDiameter"))
    obj.add_tags_to_process()
    return obj

def kabelbed():
    obj = kabelOfLeiding()
    obj.name = "Kabelbed"
    obj.add_field(B_Field("warningType", "TEXT", "WarningType",
                          from_attribute='Href'))
    obj.add_field(B_Field("ductWidth", "TEXT", "DuctWidth"))
    obj.add_field(B_Field("omschrijving", "TEXT", "Omschrijving"))
    obj.add_tags_to_process()
    return obj

def mantelbuis():
    obj = kabelOfLeiding()
    obj.name = "Mantelbuis"
    obj.add_field(B_Field("warningType", "TEXT", "WarningType",
                          from_attribute='Href'))
    obj.add_field(B_Field("diameter", "TEXT", "PipeDiameter"))
    obj.add_field(B_Field("materiaal", "TEXT", "BuismateriaalType",
                          from_attribute='Href'))
    obj.add_tags_to_process()
    return obj

def olieGasChemicalienPijpleiding():
    obj = kabelOfLeiding()
    obj.name = "OlieGasChemicalienPijpleiding"
    obj.add_field(B_Field("diameter", "TEXT", "PipeDiameter"))
    obj.add_field(B_Field("druk", "TEXT", "Pressure"))
    obj.add_field(B_Field("fluid", "TEXT", "OilGasChemicalsProductType",
                          from_attribute='Href'))
    obj.add_tags_to_process()
    return obj

def overig():
    obj = kabelOfLeiding()
    obj.name = "Overig"
    obj.add_field(B_Field("warningType", "TEXT", "WarningType",
                          from_attribute='Href'))
    obj.add_field(B_Field("geoNauwkeurigheidXY", "TEXT", "GeoNauwkeurigheidXY",
                          from_attribute='Href'))
    obj.add_field(B_Field("kabelDiameter", "TEXT", "KabelDiameter"))
    obj.add_field(B_Field("materiaal", "TEXT", "BuismateriaalType",
                          from_attribute='Href'))
    obj.add_field(B_Field("buisDiameter", "TEXT", "PipeDiameter"))
    obj.add_field(B_Field("druk", "TEXT", "Pressure"))
    obj.add_field(B_Field("producttype", "TEXT", "Producttype"))
    obj.add_tags_to_process()
    return obj

def rioolleiding():
    obj = kabelOfLeiding()
    obj.name = "Rioolleiding"
    obj.add_field(B_Field("warningType", "TEXT", "WarningType",
                          from_attribute='Href'))
    obj.add_field(B_Field("diameter", "TEXT", "PipeDiameter"))
    obj.add_field(B_Field("druk", "TEXT", "Pressure"))
    obj.add_field(B_Field("fluid", "TEXT", "SewerWaterType",
                          from_attribute='Href'))
    obj.add_tags_to_process()
    return obj

def telecomKabel():
    obj = kabelOfLeiding()
    obj.name = "Telecommunicatiekabel"
    obj.add_field(B_Field("utilityFacilityReference", "TEXT",
                          "UtilityFacilityReference"))
    obj.add_field(B_Field("utilityDeliveryType", "TEXT", "UtilityDeliveryType",
                          from_attribute='Href'))
    obj.add_field(B_Field("geoNauwkeurigheidXY", "TEXT", "GeoNauwkeurigheidXY",
                          from_attribute='Href'))
    obj.add_field(B_Field("warningType", "TEXT", "WarningType",
                          from_attribute='Href'))
    obj.add_field(B_Field("materiaal", "TEXT",
                          "TelecommunicationsCableMaterialType",
                          from_attribute='Href'))
    obj.add_field(B_Field("diameter", "TEXT", "KabelDiameter"))
    obj.add_field(B_Field("omschrijving", "TEXT", "Omschrijving"))
    obj.add_field(B_Field("toelichting", "TEXT", "Toelichting"))
    obj.add_tags_to_process()
    return obj

def thermischePijpleiding():
    obj = kabelOfLeiding()
    obj.name = "ThermischePijpleiding"
    obj.add_field(B_Field("warningType", "TEXT", "WarningType",
                          from_attribute='Href'))
    obj.add_field(B_Field("diameter", "TEXT", "PipeDiameter"))
    obj.add_field(B_Field("druk", "TEXT", "Pressure"))
    obj.add_field(B_Field("producttype", "TEXT", "ThermalProductType"))
    obj.add_field(B_Field("geoNauwkeurigheidXY", "TEXT", "GeoNauwkeurigheidXY",
                          from_attribute='Href'))
    obj.add_field(B_Field("omschrijving", "TEXT", "Omschrijving"))
    obj.add_field(B_Field("toelichting", "TEXT", "Toelichting"))
    obj.add_tags_to_process()
    return obj

def waterleiding():
    obj = kabelOfLeiding()
    obj.name = "Waterleiding"
    obj.add_field(B_Field("warningType", "TEXT", "WarningType",
                          from_attribute='Href'))
    obj.add_field(B_Field("diameter", "TEXT", "PipeDiameter"))
    obj.add_field(B_Field("druk", "TEXT", "Pressure"))
    obj.add_field(B_Field("fluid", "TEXT", "WaterType",
                          from_attribute='Href'))
    obj.add_tags_to_process()
    return obj

def utilityLink():
    obj = B_Object("UtilityLink")
    obj.add_field(B_Field("id", "TEXT", "InspireId",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("status", "TEXT", "CurrentStatus",
                          from_attribute='Href'))
    obj.add_field(B_Field("validFrom", "TEXT", "ValidFrom"))
    obj.add_field(B_Field("verticalPosition", "TEXT", "VerticalPosition"))
    obj.add_field(B_Field("geometry", "LINESTRING", "CentrelineGeometry",
                          to_object=gml.LineString))
    obj.add_tags_to_process()
    return obj

def PuntOpNet():
    obj = B_Object("PuntOpNet")
    obj.add_field(B_Field("id", "TEXT", "InspireId",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("status", "TEXT", "CurrentStatus",
                          from_attribute='Href'))
    obj.add_field(B_Field("validFrom", "TEXT", "ValidFrom"))
    obj.add_field(B_Field("validTo", "TEXT", "ValidTo"))
    obj.add_field(B_Field("verticalPosition", "TEXT", "VerticalPosition"))
    obj.add_field(B_Field("thema", "TEXT", "Theme"))
    obj.add_field(B_Field("geometry", "POINT", "Geometry",
                          to_object=gml.Point))
    obj.add_field(B_Field("geom_id", "TEXT", "ExtraGeometrie",
                          from_attribute='Href'))
    obj.add_field(B_Field("label", "TEXT", "Label"))
    return obj

def appurtenance():
    obj = PuntOpNet()
    obj.name = "Leidingelement"
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("appurtenanceType", "TEXT", "AppurtenanceType",
                          from_attribute='Href'))
    obj.add_tags_to_process()
    return obj

def kast():
    obj = PuntOpNet()
    obj.name = "Kast"
    obj.add_field(B_Field("bovengrondsZichtbaar", "TEXT", "BovengrondsZichtbaar"))
    obj.add_field(B_Field("geoNauwkeurigheidXY", "TEXT", "GeoNauwkeurigheidXY",
                          from_attribute='Href'))   
    obj.add_tags_to_process()
    return obj

def mangat():
    obj = PuntOpNet()
    obj.name = "Mangat"
    obj.add_tags_to_process()
    return obj

def mast():
    obj = PuntOpNet()
    obj.name = "Mast"
    obj.add_field(B_Field("hoogte", "TEXT", "PoleHeight"))
    obj.add_tags_to_process()
    return obj

def technischGebouw():
    obj = kast()
    obj.name = "TechnischGebouw"
    return obj

def toren():
    obj = PuntOpNet()
    obj.name = "Toren"
    obj.add_field(B_Field("hoogte", "TEXT", "TowerHeight"))
    obj.add_tags_to_process()
    return obj

def eigenTopografie():
    obj = imkl_basis()
    obj.name = "EigenTopografie"
    obj.add_field(B_Field("thema", "TEXT", "Theme"))
    obj.add_field(B_Field("label", "TEXT", "Label"))
    obj.add_field(B_Field("omschrijving", "TEXT", "Omschrijving"))
    obj.add_field(B_Field("status", "TEXT", "Status",
                          from_attribute='Href'))
    obj.add_field(B_Field("typeTopografischObject", "TEXT",
                          "TypeTopografischObject",
                          from_attribute='Href'))
    obj.add_field(B_Field("geometry", "POINT", "Ligging",
                          to_object=gml.Point))
    obj.add_tags_to_process()
    return obj

def extraGeometrie():
    obj = imkl_basis()
    obj.name = "ExtraGeometrie"
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("thema", "TEXT", "Theme"))
    obj.add_field(B_Field("object", "TEXT", "Object"))
    obj.add_field(B_Field("geometry", "POLYGON", "Vlakgeometrie2D",
                          to_object=gml.Polygon))
    obj.add_tags_to_process()
    return obj

def extraDetailinfo():
    obj = imkl_basis()
    obj.name = "ExtraDetailinfo"
    obj.add_field(B_Field("thema", "TEXT", "Theme"))
    obj.add_field(B_Field("label", "TEXT", "Label"))
    obj.add_field(B_Field("omschrijving", "TEXT", "Omschrijving"))
    obj.add_field(B_Field("network_id", "TEXT", "InNetwork",
                          from_attribute='Href'))
    obj.add_field(B_Field("adres", "CONTAINER", "Adres",
                          to_object=adres))
    obj.add_field(B_Field("extraInfoType", "TEXT",
                          "ExtraInfoType",
                          from_attribute='Href'))
    obj.add_field(B_Field("bestandIdentificator", "TEXT",
                          "BestandIdentificator"))
    obj.add_field(B_Field("geometry", "POINT", "Ligging",
                          to_object=gml.Point))
    obj.add_tags_to_process()
    return obj

def gebiedsinformatieAanvraag():
    obj = imkl_basis()
    obj.name = "GebiedsinformatieAanvraag"
    obj.add_field(B_Field("ordernummer", "TEXT","Ordernummer"))
    obj.add_field(B_Field("positienummer", "TEXT","Positienummer"))
    obj.add_field(B_Field("klicnummer", "TEXT","KlicMeldnummer"))
    obj.add_field(B_Field("aanvragers", "CONTAINER","Aanvrager",
                          to_object=aanvrager))
    obj.add_field(B_Field("referentie", "TEXT", "Referentie"))
    obj.add_field(B_Field("opdrachtgevers", "CONTAINER", "Opdrachtgever",
                          to_object=opdrachtgever))
    obj.add_field(B_Field("aanvraagsoort", "TEXT", "AanvraagSoort",
                          from_attribute='Href'))
    obj.add_field(B_Field("aanvraagdatum", "TEXT", "AanvraagDatum"))
    obj.add_field(B_Field("soortWerkzaamheden", "TEXT", "SoortWerkzaamheden",
                          from_attribute='Href'))
    obj.add_field(B_Field("locatieWerkzaamheden", "TEXT", "LocatieWerkzaamheden"))
    obj.add_field(B_Field("startDatum", "TEXT", "StartDatum"))
    obj.add_field(B_Field("eindDatum", "TEXT", "EindDatum"))
    obj.add_tags_to_process()
    return obj

def gebiedsinformatieLevering():
    obj = imkl_basis()
    obj.name = "GebiedsinformatieLevering"
    obj.add_field(B_Field("leveringsvolgnummer", "INTEGER",
                          "Leveringsvolgnummer"))
    obj.add_field(B_Field("datumLeveringSamengesteld", "TEXT",
                          "DatumLeveringSamengesteld"))
    obj.add_field(B_Field("indicatieLeveringCompleet", "TEXT",
                          "IndicatieLeveringCompleet"))
    obj.add_field(B_Field("achtergrondkaarten", "CONTAINER",
                          "Achtergrondkaart", to_object=achtergrondkaart))
    obj.add_tags_to_process()
    return obj

def beheerder():
    obj = imkl_basis()
    obj.name = "Beheerder"
    obj.add_field(B_Field("bronhoudercode", "TEXT", "Bronhoudercode"))
    obj.add_field(B_Field("organisatie", "CONTAINER",
                          "Organisatie", to_object=organisatie2))
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

def opdrachtgever():
    obj = aanvrager()
    obj.name = "Opdrachtgever"
    return obj

def achtergrondkaart():
    obj = B_Object("Achtergrondkaart")
    obj.add_field(B_Field("achtergrondkaartSoort", "TEXT",
                                "AchtergrondkaartSoort", from_attribute='Href'))
    obj.add_field(B_Field("kaartreferentie", "TEXT", "Kaartreferentie"))
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

def organisatie2():
    obj = B_Object("Organisatie")
    obj.add_field(B_Field("naam", "TEXT", "Naam"))
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
    obj.add_field(B_Field("geometry", "POLYGON", "Geometrie",
                          to_object=gml.Polygon))
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
    obj = imkl_basis()
    obj.name = "Belanghebbende"
    obj.add_field(B_Field("bronhoudercode", "TEXT", "Bronhoudercode"))
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
    obj = imkl_basis()
    obj.name = "Belang"
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

def labelpositie():
    obj = B_Object("Labelpositie")
    obj.add_field(B_Field("aangrijpingHorizontaal", "TEXT",
                          "AangrijpingHorizontaal",
                          from_attribute="Href"))
    obj.add_field(B_Field("aangrijpingVerticaal", "TEXT",
                          "AangrijpingVerticaal",
                          from_attribute="Href"))
    obj.add_tags_to_process()
    return obj

def themabijlagePerNetbeheerder():
    a_bijlage = bijlagePerLevering()
    a_bijlage.name = "ThemabijlagePerNetbeheerder"
    return a_bijlage

def imkl_basis():
    obj = B_Object("imkl_basis")
    obj.add_field(B_Field("id", "TEXT", "Identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("vervaldatum", "TEXT", "EndLifespanVersion"))
    return obj

def utiliteitsnet():
    obj = B_Object("Utiliteitsnet")
    obj.add_field(B_Field("id", "TEXT", "Identificatie",
                          to_object=IMKL_Id, is_key_field=True))
    obj.add_field(B_Field("registratiedatum", "TEXT", "BeginLifespanVersion"))
    obj.add_field(B_Field("utilityNetworkType", "TEXT", "UtilityNetworkType",
                          from_attribute="Href"))
    obj.add_field(B_Field("authorityRole", "TEXT", "AuthorityRole"))
    obj.add_field(B_Field("thema", "TEXT", "Thema", from_attribute="Href"))
    obj.add_field(B_Field("standaardDieptelegging", "TEXT",
                          "StandaardDieptelegging"))
    obj.add_tags_to_process()
    return obj

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

