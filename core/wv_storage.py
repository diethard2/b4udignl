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
import os
from core.wv_objects import Rectangle, Company, Person, Theme, PdfFile, Layer
from core import imkl

class Storage(object):
    def __init__(self, parent):
        """Superclass for storing common objects for all Klic IMKL versions"""
        self.__parent = parent
        self.__klicnummer = None
        self.__meldingsoort = None
        self.__netOwners = []
        self.__pdfFiles = []
        self.__layers = []

    '''parent properties, only use get functions'''
        
    def _path(self):
        """return private attribute path of parent wv

        purpose is to use it to set some properties owned by Storage"""
        return self.__parent.path

    path = property(fget=_path)

    def _imkls(self):
        """return private attribute imkls of parent wv

        purpose is to have access to imkl elements allready gathered by
        wv.doc, this includes information of which version of wv_storage
        should be created and process to store it in other properties
        defined here!"""
        return self.__parent.imkls

    imkls = property(fget=_imkls)

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

    def _pdfFiles(self):
        """return private attribute pdfFiles"""
        return self.__pdfFiles
    
    pdfFiles = property(fget=_pdfFiles)

    def _layers(self):
        """return private attribute layers"""
        return self.__layers
    
    layers = property(fget=_layers)

    def fill(self):
        """fills the storage attributes from imkl objects retrieved
        from parent.

        this super method is called from children to set common attributes"""
        self._fill_klicnummer()
        self._fill_meldingsoort()
        self._fill_rectangle()
        self._fill_graafpolygoon()
        self._fill_netowners()

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

    def _fill_rectangle(self, imkl_obj=None):
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
        self.__graafpolygoon = imkl_obj.field("graafpolygoon").value

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
                self.layers.append(Layer(self, layer_file))

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
        theme._set_theme_layers(self.path, imkl_theme)
        theme._set_theme_docs(self.path, imkl_theme)
        return theme

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
        imkl_obj = self.imkls[imkl.LEVERINGSINFORMATIE][0]
        imkl_obj = imkl_obj.field("pngFormaat").value
        super(Storage2, self)._fill_rectangle(imkl_obj)

        
