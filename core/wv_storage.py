"""
/***************************************************************************
wv_storage (Wion Viewer)
begin                : 2018-09-15 
copyright            : (C) 2018 by Diethard Jansen
email                : diethard.jansen at gmail.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

Holds different classes to store and process imkl to content used by wv.doc.
It is an integral part of wv, but choosen is to separate the processing and
storing of imkl into wv-objects because we want to be able to process imkl to
doc attributes in a different way.

Author: Diethard Jansen, 15-9-2018
"""
import os, imkl
from wv_objects import Rectangle, Company, Person, Theme, PdfFile, Layer
from PyQt4.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry


class Storage(object):
    def __init__(self, parent):
        """Superclass for storing common objects for all Klic IMKL versions"""
        self.__parent = parent
        self.__klicnummer = None
        self.__meldingsoort = None
        self.__graafpolygoon = None
        self.__netOwners = []
        self.__netOwners_on_code = {}
        self.__pdfFiles = []
        self.__layers = {}

    '''parent properties, only use get functions'''
    def _parent(self):
        """return private attribute path of parent wv

        purpose is to use it to set some properties owned by Storage"""
        return self.__parent

    parent = property(fget=_parent)
        
    def _path(self):
        """return private attribute path of parent wv

        purpose is to use it to set some properties owned by Storage"""
        return self.__parent.path

    path = property(fget=_path)

    def _iface(self):
        """return private attribute iface of parent wv

        purpose is to have access to to wv.iface so you can use it!"""
        return self.__parent.iface

    iface = property(fget=_iface)
    
    def _imkls(self):
        """return private attribute imkls of parent wv

        purpose is to have access to imkl elements allready gathered by
        wv.doc, this includes information of which version of wv_storage
        should be created and process to store it in other properties
        defined here!"""
        return self.__parent.imkls

    imkls = property(fget=_imkls)

    def _imkls_on_id(self):
        """return private attribute imkls_on_id of parent wv

        purpose is to have access to imkl elements by keyvalue,
        allready gathered by wv.doc!"""
        return self.__parent.imkls_on_id

    imkls_on_id = property(fget=_imkls_on_id)

    '''my properties, all set from fill, use get functions to provide'''
    def _klicnummer(self):
        """return private attribute klicnummer"""
        return self.__klicnummer

    def _set_klicnummer(self, value):
        """return private attribute klicnummer"""
        self.__klicnummer = value
        
    klicnummer = property(fget=_klicnummer, fset=_set_klicnummer)
    
    def _meldingsoort(self):
        """return private attribute meldingsoort"""
        return self.__meldingsoort

    def _set_meldingsoort(self, value):
        """set private attribute meldingsoort"""
        self.__meldingsoort = value
        
    meldingsoort = property(fget=_meldingsoort, fset=_set_meldingsoort)

    def _rectangle(self):
        """return private attribute rectangle"""
        return self.__rectangle

    def _set_rectangle(self, value):
        """set private attribute rectangle"""
        self.__rectangle = value
        
    rectangle = property(fget=_rectangle, fset=_set_rectangle)
    
    def _graafpolygoon(self):
        """return private attribute graafpolygoon"""
        return self.__graafpolygoon

    def _set_graafpolygoon(self, value):
        """set private attribute graafpolygoon"""
        self.__graafpolygoon = value
        
    graafpolygoon = property(fget=_graafpolygoon, fset=_set_graafpolygoon)
    
    def _netOwners(self):
        """return private attribute netOwners"""
        return self.__netOwners
    
    netOwners = property(fget=_netOwners)

    def _netOwners_on_code(self):
        """return private attribute netOwners_on_code"""
        return self.__netOwners_on_code
    
    netOwners_on_code = property(fget=_netOwners_on_code)

    def _pdfFiles(self):
        """return private attribute pdfFiles"""
        return self.__pdfFiles
    
    pdfFiles = property(fget=_pdfFiles)

    def _layers(self):
        """return private attribute layers"""
        return self.__layers

    def _set_layers(self, layers):
        self.__layers = layers
    
    layers = property(fget=_layers, fset= _set_layers)

    def fill(self):
        """fills the storage attributes from imkl objects retrieved
        from parent.

        this super method is called from children to set common attributes"""
        self._fill_klicnummer()
        self._fill_meldingsoort()
        self._fill_rectangle()
        self._fill_graafpolygoon()
        self._fill_netowners()
        self._fill_layers()
        self._fill_pdf_files()

    def _fill_klicnummer(self):
        pass
    def _fill_meldingsoort(self):
        pass
    def _fill_rectangle(self):
        pass
    def _fill_graafpolygoon(self):
        pass
    def _fill_netowners(self):
        pass
    
    def _fill_layers(self):
        # find pgn files in themes
        layers = []
        for netowner in self.netOwners:
            for theme in netowner.themes:
                layers.extend(theme.layers)
        self._extend_layers(layers)

    def _fill_pdf_files(self):
        for netOwner in self.netOwners:
            for theme in netOwner.themes:
               self.pdfFiles.extend(theme.pdf_docs)
        self.pdfFiles.sort()
        
    def _extend_layers(self, layers):
        for layer in layers:
            name = layer.layerName
            self.layers[layer.layerName] = layer

    def _fill_rectangle(self, imkl_obj):
        if imkl_obj == None:
            return
        wkt = imkl_obj.field("omsluitendeRechthoek").value
        width = imkl_obj.field("pixelsBreed").value
        height = imkl_obj.field("pixelsHoog").value
        rectangle = Rectangle()
        rectangle.setFromWkt(wkt)
        rectangle.pixelsWidth = int(width)
        rectangle.pixelsHeight = int(height)
        self.__rectangle = rectangle        

class Storage1(Storage):

    def __init__(self, parent):
        super(Storage1, self).__init__(parent)

    def _fill_klicnummer(self):
        imkl_obj = self.imkls[imkl.LEVERINGSINFORMATIE][0]
        self.klicnummer = imkl_obj.field("klicnummer").value        

    def _fill_meldingsoort(self):
        imkl_obj = self.imkls[imkl.LEVERINGSINFORMATIE][0]
        self.meldingsoort = imkl_obj.field("meldingsoort").value

    def _fill_rectangle(self):
        imkl_obj = self.imkls[imkl.LEVERINGSINFORMATIE][0]
        imkl_obj = imkl_obj.field("omsluitendeRechthoek").value
        super(Storage1, self)._fill_rectangle(imkl_obj)
            
    def _fill_graafpolygoon(self):
        imkl_obj = self.imkls[imkl.LEVERINGSINFORMATIE][0]
        self.graafpolygoon = imkl_obj.field("graafpolygoon").value

    def _fill_netowners(self):
        imkl_obj = self.imkls[imkl.LEVERINGSINFORMATIE][0]
        netowner_deliveries = imkl_obj.field("netbeheerderLeveringen").value
        for netowner_delivery in netowner_deliveries:
            self._process_netowner_delivery(netowner_delivery)

    def _process_netowner_delivery(self, netowner):
        netOwner = Company()
        netOwner.name = netowner.field("bedrijfsnaam").value
        netOwner.shortName = netowner.field("bedrijfsnaam").value
        netOwner.telNrProblemIT = netowner.field("storingsnummer").value
        netOwner.telNrDamage = netowner.field("beschadigingsnummer").value
        
        contactpersoon = netowner.field("contactpersoon").value
        if contactpersoon is not None:
            person = self._process_person(contactpersoon)
            netOwner.contactPerson = person
            
        imkl_themes = netowner.field("themas").value
        if imkl_themes is not None:
            themes = self._process_themes(imkl_themes)
            netOwner.themes = themes

        imkl_docs = netowner.field("bijlagen").value
        if imkl_docs is not None:
            docs = self._process_imkl_docs(imkl_docs)
            self.pdfFiles.extend(docs)

        for topo_name in ("topo", "plan_topo"):
            imkl_topo = netowner.field(topo_name).value
            if imkl_topo is not None:
                filename = imkl_topo.field("bestandsnaam").value
                layer_file = os.path.join(self.path, filename)
                layer = Layer(self, layer_file)
                self.layers[layer.layerName] = layer
   
        self.netOwners.append(netOwner)
        
    def _process_themes(self, imkl_themes):
        """
        process a list of imkl_themes and return a list of wv.Theme objects
        """
        themes = []
        for imkl_theme in imkl_themes:
            theme = self._process_theme(imkl_theme)
            themes.append(theme)
        return themes

    def _process_theme(self, imkl_theme):
        theme = Theme(self)
        theme.name = imkl_theme.field("themanaam").value
        theme.supervisionNecessary = imkl_theme.field("eisVoorzorgmaatregel").value
        imkl_toezichthouders = imkl_theme.field("toezichthouders").value
        if imkl_toezichthouders is not None:
            persons = self._process_persons(imkl_toezichthouders)
            theme.supervisors = persons
        self._set_theme_layers(theme, imkl_theme)
        self._set_theme_docs(theme, imkl_theme)
        return theme

    def _set_theme_layers(self, theme, imkl_theme):
        layer_names = [name.lower() for name in Layer.layerGroupNames.keys()]
        layer_names.remove("topo")
        for layer_name in layer_names:
            imkl_layer = imkl_theme.field(layer_name).value
            if imkl_layer is not None:
                layer_file = imkl_layer.field('bestandsnaam').value
                layer_file = os.path.join(self.path, layer_file)
                layer = Layer(self, raster_file_name = layer_file)
                layer.addVisibility(theme.name)
                theme.layers.append(layer)

    def _set_theme_docs(self, theme, imkl_theme):
        pdf_files = []
        pdf_fields = ("detailkaarten", "huisaansluitschetsen", "themaBijlagen")
        for pdf_field in pdf_fields:
            a_container = imkl_theme.field(pdf_field).value
            if a_container is not None:
                for pdf_object in a_container:
                    file_name = pdf_object.field("bestandsnaam").value
                    pdfFile = PdfFile(file_name)
                    pdfFile.type = pdf_object.name
                    pdfFile.filePath = os.path.join(self.path, file_name)
                    theme.pdf_docs.append(pdfFile)  

    def _process_persons(self, imkl_persons):
        persons = []
        for imkl_person in imkl_persons:
            person = self._process_person(imkl_person)
            persons.append(person)
        return persons

    def _process_person(self, imkl_person):
        person = None
        if imkl_person is not None:
            person = Person()
            person.name = imkl_person.field("naam").value
            person.telephone = imkl_person.field("telefoon").value
            person.email = imkl_person.field("email").value
            person.fax = imkl_person.field("fax").value
        return person
                
    def _process_imkl_docs(self, imkl_docs):
        docs = []
        for imkl_doc in imkl_docs:
            pdf_name = imkl_doc.field("bestandsnaam").value
            pdf_file = PdfFile(pdf_name)
            pdf_file.type = imkl_doc.name
            pdf_file.filePath = os.path.join(self.path, pdf_name)
            docs.append(pdf_file)
        return docs

    def _fill_layers(self):
        super(Storage1, self)._fill_layers()
        layers = []
        kadaster_png =  'GB_' + self.klicnummer + '.png'
        file_png = os.path.join(self.path, kadaster_png)
        layer = Layer(self, file_png)
        layer.addVisibility('Topo')
        layers.append(layer)
        self._extend_layers(layers)
                
class Storage2(Storage):

    def __init__(self, parent):
        super(Storage2, self).__init__(parent)

    def _fill_klicnummer(self):
        imkl_obj = self.imkls[imkl.GEBIEDSINFORMATIEAANVRAAG][0]
        self.klicnummer = imkl_obj.field("klicnummer").value        

    def _fill_meldingsoort(self):
        imkl_obj = self.imkls[imkl.GEBIEDSINFORMATIEAANVRAAG][0]
        self.meldingsoort = imkl_obj.field("aanvraagsoort").value

    def _fill_rectangle(self):
        if self.imkls.has_key(imkl.LEVERINGSINFORMATIE):
            imkl_obj = self.imkls[imkl.LEVERINGSINFORMATIE][0]
            imkl_obj = imkl_obj.field("pngFormaat").value
            super(Storage2, self)._fill_rectangle(imkl_obj)

    def _fill_graafpolygoon(self):
        imkl_obj = self.imkls[imkl.GRAAFPOLYGOON][0]
        self.graafpolygoon = imkl_obj.field("geometry").value

    def _fill_netowners(self):
        belanghebbenden = self.imkls[imkl.BELANGHEBBENDE]
        for belanghebbende in belanghebbenden:
            self._process_belanghebbende(belanghebbende)
        for netOwner in self.netOwners:
            code = netOwner.bronhoudercode
            self.netOwners_on_code[code] = netOwner
        self._process_bijlagen_netbeheerders()

    def _fill_layers(self):
        ## all imkl objects that have a field geometry
        ## should be added to netowner..
        for layer_name, imkl_set in self.imkls.items():
            for imkl_object in imkl_set:
                if imkl_object.name in ('UtilityLink','boundedBy',
                                        'LeveringsInformatie'):
                    continue
                if imkl_object.geometry_field() is not None:
                    self._add_feature_to_layer(imkl_object)
        super(Storage2, self)._fill_layers()
        layers = []
        bijlagen = self._get_bijlagen_from_leveringsinfo()
        if bijlagen is None:
            return
        for bijlage in bijlagen:
            bijlage_type = self._get_type_from_bijlage(bijlage)
            if bijlage_type == 'PNG':
                location = bijlage.field("bestandlocatie").value
                file_png = os.path.join(self.path, location)
                layer = Layer(self, file_png)
                layers.append(layer)
        self._extend_layers(layers)

    def _fill_pdf_files(self):        
        bijlagen = self._get_bijlagen_from_leveringsinfo()
        if bijlagen is None:
            return
        for bijlage in bijlagen:
            bijlage_type = self._get_type_from_bijlage(bijlage)
            if bijlage_type == 'PDF':
                pdfFile = self._create_doc_from_imkl(bijlage)
                self.pdfFiles.append(pdfFile)
        super(Storage2, self)._fill_pdf_files()
 
    def _get_bijlagen_from_leveringsinfo(self):
        bijlagen = None
        if self.imkls.has_key(imkl.LEVERINGSINFORMATIE):
            leveringsinfo = self.imkls[imkl.LEVERINGSINFORMATIE][0]
            bijlagen = leveringsinfo.field("bijlagenPerLevering").value
        return bijlagen
            
    def _get_type_from_bijlage(self, bijlage):        
        bijlage_type = bijlage.field("bestandstype").value
        bijlage_type = bijlage_type.split('/')[-1]
        return bijlage_type

    def _process_belanghebbende(self, belanghebbende):
        id_beheerder = belanghebbende.field("idNetbeheerder").value
        id_belang = belanghebbende.field("idGeraaktBelang").value
        beheerder = self.imkls_on_id[id_beheerder]
        belang = self.imkls_on_id[id_belang]
        netOwner = Company()
        netOwner.process_imkl_object(beheerder)
        netOwner.process_imkl_object(belang)
        if self.imkls.has_key(imkl.UTILITEITSNET):
            utility_nets = self.imkls[imkl.UTILITEITSNET]
            self._process_themes(netOwner, utility_nets)
        self.netOwners.append(netOwner)

    def _process_themes(self, netOwner, utility_nets):
        search_string_in_id = 'nl.imkl-'+ netOwner.bronhoudercode + '.'
        theme_names = []
        for utility_net in utility_nets:
            id_utility_net = utility_net.field('id').value
            if search_string_in_id in id_utility_net:
                theme_name = utility_net.field('thema').value
                if theme_name not in theme_names:
                    theme_names.append(theme_name)
        for theme_name in theme_names:
            netOwner.themes.append(Theme(self.parent, theme_name))

    def _process_bijlagen_netbeheerders(self):
        if not self.imkls.has_key(imkl.LEVERINGSINFORMATIE):
            return
        leveringsinfo = self.imkls["Leveringsinformatie"][0]
        belanghebbenden = leveringsinfo.field("belanghebbenden").value
        if belanghebbenden is None:
            return
        for belanghebbende in belanghebbenden:
            code = belanghebbende.field("bronhoudercode").value
            netowner = self.netOwners_on_code[code]            
            bijlagen = belanghebbende.field("bijlagen").value
            beheerdersinfo = belanghebbende.field("beheerdersinformatie").value
            self._process_bijlagen_belanghebbende(netowner, bijlagen)
            self._process_bijlagen_beheerdersinfo(netowner, beheerdersinfo)
            
    def _process_bijlagen_belanghebbende(self, netowner, bijlagen):
        if bijlagen is None:
            return
        for bijlage in bijlagen:
            soort = bijlage.field("soort_bijlage").value
            lokatie = bijlage.field("bestandlocatie").value
            file_type = bijlage.field("bestandstype").value
            file_type = file_type.split('/')[-1]
            if file_type == 'PNG':
                theme = self._get_create_theme_netowner(netowner, 'topo')
                self._add_layer_to_theme(theme, bijlage)
            elif file_type == 'PDF':
                pdfFile = self._create_doc_from_imkl(bijlage)
                self.pdfFiles.append(pdfFile)
                    
    def _process_bijlagen_beheerdersinfo(self, netowner, beheerdersinfo):
        if beheerdersinfo is None:
            return
        for informatie in beheerdersinfo:
            theme_name = informatie.field("thema").value
            theme_name = theme_name.split('/')[-1]
            theme = self._get_create_theme_netowner(netowner, theme_name)
            themabijlagen = informatie.field("themaBijlagen").value
            for bijlage in themabijlagen:
                file_type = bijlage.field("bestandstype").value
                file_type = file_type.split('/')[-1]
                if file_type == 'PNG':
                    self._add_layer_to_theme(theme, bijlage)
                elif file_type == 'PDF':
                    pdfFile = self._add_doc_to_theme(theme, bijlage)
##            self.pdfFiles.extend(theme.pdf_docs)

    def _get_create_theme_netowner(self, netowner, theme_name):
        theme = netowner.get_theme(theme_name)
        if theme is None:
            theme = Theme(self, theme_name)
            netowner.themes.append(theme)
        return theme

    def _add_layer_to_theme(self, theme, imkl_object):
        file_location = imkl_object.field("bestandlocatie").value
        layer_file = os.path.join(self.path, file_location)
        layer = Layer(self, layer_file)
        layer.addVisibility(theme.name)
        theme.layers.append(layer)
                    
    def _add_doc_to_theme(self, theme, imkl_object):
        pdfFile = self._create_doc_from_imkl(imkl_object)
        theme.pdf_docs.append(pdfFile)

    def _create_doc_from_imkl(self, imkl_object):
        soort = imkl_object.field("soort_bijlage").value
        file_location = imkl_object.field("bestandlocatie").value
        file_name = file_location.split('/')[-1]
        pdfFile = PdfFile(file_name)
        pdfFile.type = soort
        pdfFile.filePath = os.path.join(self.path, file_location)
        return pdfFile
                    
    def _add_feature_to_layer(self, imkl_object):
##        print "add_feature:", imkl_object.name
        if not self.layers.has_key(imkl_object.name):
            self._create_layer_from_imkl(imkl_object)
        layer = self.layers[imkl_object.name]
        feature = QgsFeature()
        fields = imkl_object.attribute_fields()
        theme_field = imkl_object.field("thema")
        if theme_field is not None:
            layer.addVisibility(theme_field.value)        
        geom_field = imkl_object.geometry_field()
        if geom_field.value is not None:
            try:
                feature.setGeometry(QgsGeometry.fromWkt(geom_field.value))
                values = [field.value for field in fields]
                feature.setAttributes(values)
                layer.features.append(feature)
            except TypeError: pass

    def _create_layer_from_imkl(self, imkl_object):
        """create a layer from imkl and add it to self.layers"""
        layer = Layer(self)
        name = imkl_object.name
        layer.layerName = name
        vector_type = imkl_object.geometry_field().type
        layer.vectorType = vector_type
        theme_field = imkl_object.field("thema")
        if theme_field is not None:
            layer.addVisibility(theme_field.value)
        uri = layer.qgisVectorType() + '?crs=epsg:28992'
        layer.layer = QgsVectorLayer(uri, name, "memory")
        # now insert the fields..
        field_types = {"TEXT": QVariant.String,
                       "INTEGER": QVariant.Int,
                       "REAL": QVariant.Double}
        fields = imkl_object.attribute_fields()
        for field in fields:
            field = QgsField(field.name, field_types[field.type])
            layer.fields.append(field)
        self.layers[name] = layer
        
                
        
