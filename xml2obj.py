import string
"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from xml.parsers import expat

class Element:
    'A parsed XML element'
    def __init__(self,name,attributes):
        'Element constructor'
        # The element's tag name
        self.name = name
        # The element's attribute dictionary
        self.attributes = attributes
        # The element's cdata
        self.cdata = ''
        # The element's child element list (sequence)
        self.children = []
        
    def AddChild(self,element):
        'Add a reference to a child element'
        self.children.append(element)
        
    def getAttribute(self,key):
        'Get an attribute value'
        return self.attributes.get(key)
    
    def getData(self):
        'Get the cdata'
        return self.cdata
        
    def getElements(self,name=''):
        'Get a list of child elements'
        #If no tag name is specified, return the all children
        if not name:
            return self.children
        else:
            # else return only those children with a matching tag name
            elements = []
            for element in self.children:
                if element.name == name:
                    elements.append(element)
            return elements

class Xml2Obj:
    """XML to Object

    usage: 
    >>> parser = Xml2Obj()
    >>> el = parser.Parse(None, testXmlData)
    or  el = parser.Parse(xmlFileName)
    >>> for i_el in el.getElements():
	print i_el.name
	print i_el.attributes
	if i_el.name == "lev:Locatie":
		a = i_el.getAttribute("srsName")
		print "Attribute ",i_el.name," =", a
	print i_el.getData()
    
    	
    lev:Klicnummer
    {}
    09G267447
    lev:Meldingsoort
    {}
    Graafmelding
    lev:Locatie
    {u'axisLabels': u'x y', u'srsName': u'epsg:28992', u'uomLabels': u'm m', u'srsDimension': u'2'}
    Attribute  lev:Locatie  = epsg:28992

>>>  
    
    """

    def __init__(self):
        self.root = None
        self.nodeStack = []
        
    def StartElement(self,name,attributes):
        'SAX start element even handler'
        # Instantiate an Element object
        element = Element(name.encode(),attributes)
        
        # Push element onto the stack and make it a child of parent
        if len(self.nodeStack) > 0:
            parent = self.nodeStack[-1]
            parent.AddChild(element)
        else:
            self.root = element
        self.nodeStack.append(element)
        
    def EndElement(self,name):
        'SAX end element event handler'
        self.nodeStack = self.nodeStack[:-1]

    def CharacterData(self,data):
        'SAX character data event handler'
        if string.strip(data):
            data = data.encode()
            element = self.nodeStack[-1]
            element.cdata += data
            return

    def Parse(self,filename=None,xmldata=None):
        # Create a SAX parser
        Parser = expat.ParserCreate()

        # SAX event handlers
        Parser.StartElementHandler = self.StartElement
        Parser.EndElementHandler = self.EndElement
        Parser.CharacterDataHandler = self.CharacterData

        # Parse the XML File
        if filename != None:
            l_file = open(filename, 'r')
            xmldata = l_file.read()
            l_file.close()
        ParserStatus = Parser.Parse(xmldata, 1)
        
        return self.root

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # and load testXML for testing!!
    global testXmlData
    testXmlData = """<?xml version="1.0" encoding="UTF-8"?>
    <lev:Leveringsinfo xmlns:lev="http://www.kadaster.nl/schemas/klic/20080722/leveringsinfo">
      <lev:Klicnummer>09G267447</lev:Klicnummer>
      <lev:Meldingsoort>Graafmelding</lev:Meldingsoort>
      <lev:Locatie axisLabels="x y" srsDimension="2" srsName="epsg:28992" uomLabels="m m">
        <gml:exterior xmlns:gml="http://www.opengis.net/gml">
          <gml:LinearRing>
            <gml:posList>196723.0 311697.0 196724.0 311693.0 196927.0
            311495.0 196970.0 311534.0 196752.0 311731.0 196723.0 311697.0
            </gml:posList>
          </gml:LinearRing>
        </gml:exterior>
      </lev:Locatie>
    </lev:Leveringsinfo>"""





