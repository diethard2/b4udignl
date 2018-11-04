<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="2.14.6-Essen" minimumScale="1" maximumScale="10000" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="1" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
  <edittypes>
    <edittype widgetv2type="TextEdit" name="id">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="network_id">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="status">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="validFrom">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="validTo">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="verticalPosition">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="thema">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="geom_id">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="label">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="bovengrondsZichtbaar">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="geoNauwkeurigheidXY">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
  </edittypes>
  <renderer-v2 forceraster="0" symbollevels="0" type="RuleRenderer" enableorderby="0">
    <rules key="{67030d46-2b51-49f0-b680-93680e100449}">
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'datatransport'" key="{b8c3746b-16ef-4837-80fc-da885751ceeb}" symbol="0" scalemindenom="1" label="datatransport 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'gasLageDruk'" key="{e20ba385-6a77-463d-ac98-42f787752e64}" symbol="1" scalemindenom="1" label="gasLageDruk 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'gasHogeDruk'" key="{0434abd4-0270-418b-953e-6f7fb192386b}" symbol="2" scalemindenom="1" label="gasHogeDruk 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'buisleidingGevaarlijkeInhoud'" key="{292ec306-5174-4422-a883-0996ff7b60eb}" symbol="3" scalemindenom="1" label="buisleidingGevaarlijkeInhoud 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  in ('hoogspanning', 'landelijkHoogspanningsnet')" key="{6a75bc87-426b-43ba-a77d-56f0f03ead3b}" symbol="4" scalemindenom="1" label="hoogspanning 1"/>
      <rule scalemaxdenom="500" filter=" &quot;thema&quot;  =  'middenspanning' " key="{711e2094-e201-4223-8b2d-12c18204752f}" symbol="5" scalemindenom="1" label="middenspanning 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'laagspanning'" key="{6240c6d7-90d6-4c8f-986b-c4ec2d235335}" symbol="6" scalemindenom="1" label="laagspanning 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'petrochemie'" key="{085ee70a-53df-440c-afee-f4cefb348f1d}" symbol="7" scalemindenom="1" label="petrochemie 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'rioolVrijverval'" key="{db5f81ff-c4a5-44d4-9245-93e3022ef00f}" symbol="8" scalemindenom="1" label="rioolVrijverval 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'rioolOnderOverOfOnderdruk'" key="{3131915f-3221-4e53-b9fa-feee10b1e5fe}" symbol="9" scalemindenom="1" label="rioolOnderOverOfOnderdruk 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'warmte'" key="{03514372-9605-4647-a562-1fc1204a5bfb}" symbol="10" scalemindenom="1" label="warmte 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'water'" key="{0c8ca284-2996-4d1e-9e35-aa791c932154}" symbol="11" scalemindenom="1" label="water 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'wees'" key="{a33adf91-ef4e-423b-a834-598b649c745d}" symbol="12" scalemindenom="1" label="wees 1"/>
      <rule scalemaxdenom="500" filter="&quot;thema&quot;  =  'overig'" key="{f44837a0-e5e9-4b98-98ed-ad82d426222c}" symbol="13" scalemindenom="1" label="overig 1"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'datatransport'" key="{85b66a9b-5e22-4885-94fa-48670157a1ba}" symbol="14" scalemindenom="1500" label="datatransport 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'gasLageDruk'" key="{fbedfe74-195b-49a7-a1ce-a28d46265483}" symbol="15" scalemindenom="1500" label="gasLageDruk 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'gasHogeDruk'" key="{49a3ff93-523f-4ba7-9c0f-6601723d4b17}" symbol="16" scalemindenom="1500" label="gasHogeDruk 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'buisleidingGevaarlijkeInhoud'" key="{e74b24d7-4a88-4498-8565-3968b4776b6e}" symbol="17" scalemindenom="1500" label="buisleidingGevaarlijkeInhoud 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  in ('hoogspanning', 'landelijkHoogspanningsnet')" key="{636c90f8-c61b-4d9b-986f-99517775a017}" symbol="18" scalemindenom="1500" label="hoogspanning 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'middenspanning'" key="{bb01e119-830b-43df-b38f-66a92ef882eb}" symbol="19" scalemindenom="1500" label="middenspanning 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'laagspanning'" key="{3d12b9dd-fa05-4743-b3ee-774a3a7a7cee}" symbol="20" scalemindenom="1500" label="laagspanning 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'petrochemie'" key="{dda4b6c3-a92e-4227-9d50-0dd825fb8691}" symbol="21" scalemindenom="1500" label="petrochemie 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'rioolVrijverval'" key="{72dac32d-f87a-40a9-99e0-bb4c1fb285a2}" symbol="22" scalemindenom="1500" label="rioolVrijverval 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'rioolOnderOverOfOnderdruk'" key="{94e620cd-e28f-4934-8d23-0e285d7e2b58}" symbol="23" scalemindenom="1500" label="rioolOnderOverOfOnderdruk 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'warmte'" key="{8a2ab1e4-ea0d-4de1-ac9c-3e969ddbf69e}" symbol="24" scalemindenom="1500" label="warmte 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'water'" key="{94078402-bf81-4efb-80ff-40b6dff15822}" symbol="25" scalemindenom="1500" label="water 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'wees'" key="{20ff5a3e-b1a3-44b3-abf9-2ad454cb80ed}" symbol="26" scalemindenom="1500" label="wees 2"/>
      <rule scalemaxdenom="1250" filter="&quot;thema&quot;  =  'overig'" key="{08010e68-8d07-4a85-b6ab-5a5ff27fa071}" symbol="27" scalemindenom="1500" label="overig 2"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'datatransport'" key="{1695a997-2000-423a-b2cf-8f628220d8c5}" symbol="28" scalemindenom="1250" label="datatransport 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'gasLageDruk'" key="{aeb03adc-7892-4f86-b03f-af1c39cc52f2}" symbol="29" scalemindenom="1250" label="gasLageDruk 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'gasHogeDruk'" key="{af739e3f-e64f-41c7-9c98-9ae4904edf6e}" symbol="30" scalemindenom="1250" label="gasHogeDruk 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'buisleidingGevaarlijkeInhoud'" key="{1ca1e618-ee71-4b04-bedb-9e0131c2a08c}" symbol="31" scalemindenom="1250" label="buisleidingGevaarlijkeInhoud 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  in ('hoogspanning', 'landelijkHoogspanningsnet')" key="{2ecb74a9-9965-40f7-b862-cd6b7993ce40}" symbol="32" scalemindenom="1250" label="hoogspanning 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'middenspanning'" key="{5b02049d-3201-44a2-8cd4-0822a22c403f}" symbol="33" scalemindenom="1250" label="middenspanning 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'laagspanning'" key="{e0f640ea-edcc-451d-8064-4978afd26a30}" symbol="34" scalemindenom="1250" label="laagspanning 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'petrochemie'" key="{679f2475-f3f0-4848-9a1e-249040f473cc}" symbol="35" scalemindenom="1250" label="petrochemie 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'rioolVrijverval'" key="{b086c5a4-d93e-4246-b66b-e5f703004238}" symbol="36" scalemindenom="1250" label="rioolVrijverval 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'rioolOnderOverOfOnderdruk'" key="{05cc29b5-3733-42ca-b66a-b693a2329345}" symbol="37" scalemindenom="1250" label="rioolOnderOverOfOnderdruk 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'warmte'" key="{c12801f1-7888-4049-8d7e-9a8da8e375a4}" symbol="38" scalemindenom="1250" label="warmte 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'water'" key="{d28dad3e-05ec-4d55-a4a1-cfe41563a5f4}" symbol="39" scalemindenom="1250" label="water 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'wees'" key="{388d94df-67a9-4556-8b42-8067a904316c}" symbol="40" scalemindenom="1250" label="wees 3"/>
      <rule scalemaxdenom="2500" filter="&quot;thema&quot;  =  'overig'" key="{1c657dd3-ec19-47f9-b17f-b2df88bca89f}" symbol="41" scalemindenom="1250" label="overig 3"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'datatransport'" key="{47322607-aa63-4854-bb99-35d9c523627e}" symbol="42" scalemindenom="2500" label="datatransport 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'gasLageDruk'" key="{2469ac4d-5965-4015-8d2f-b301dc208287}" symbol="43" scalemindenom="2500" label="gasLageDruk 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'gasHogeDruk'" key="{6d521040-3659-4573-95e9-d5e447898009}" symbol="44" scalemindenom="2500" label="gasHogeDruk 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'buisleidingGevaarlijkeInhoud'" key="{e2f4caa2-72c0-45b3-a178-b852f6666e94}" symbol="45" scalemindenom="2500" label="buisleidingGevaarlijkeInhoud 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  in ('hoogspanning', 'landelijkHoogspanningsnet')" key="{301e6bee-f3de-4242-b6d8-6b44c347fedb}" symbol="46" scalemindenom="2500" label="hoogspanning 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'middenspanning'" key="{46878ced-51fc-4647-9e08-12a0cc1aee58}" symbol="47" scalemindenom="2500" label="middenspanning 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'laagspanning'" key="{fc7a43b5-27de-41dc-8049-d4503bbe7a0b}" symbol="48" scalemindenom="2500" label="laagspanning 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'petrochemie'" key="{fdd2c263-5e8c-428a-b0d0-6fd848825525}" symbol="49" scalemindenom="2500" label="petrochemie 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'rioolVrijverval'" key="{99910df6-e38c-435b-8abf-f8376b0de210}" symbol="50" scalemindenom="2500" label="rioolVrijverval 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'rioolOnderOverOfOnderdruk'" key="{51baaa8e-ecf0-488f-a0bb-006cb3defc63}" symbol="51" scalemindenom="2500" label="rioolOnderOverOfOnderdruk 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'warmte'" key="{cf46ad44-a9d9-44bd-aab0-716aa1246058}" symbol="52" scalemindenom="2500" label="warmte 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'water'" key="{6471023e-c21c-4ee7-a5c3-ebe516701b75}" symbol="53" scalemindenom="2500" label="water 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'wees'" key="{fbed4273-964c-4350-be71-029f3a43d0a1}" symbol="54" scalemindenom="2500" label="wees 4"/>
      <rule scalemaxdenom="10000" filter="&quot;thema&quot;  =  'overig'" key="{22e7fea9-0dd6-4bb0-8671-2833026cd0ce}" symbol="55" scalemindenom="2500" label="overig 4"/>
    </rules>
    <symbols>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="0">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,255,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="1">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,215,80,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="10">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,128,128,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="11">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,0,255,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="12">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="145,138,111,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="13">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="111,92,16,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="14">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,255,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="15">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,215,80,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="16">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,175,60,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="17">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,127,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="18">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="19">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="200,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="2">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,175,60,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="20">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="150,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="21">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="182,74,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="22">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="186,56,168,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="23">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="128,0,128,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="24">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,128,128,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="25">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,0,255,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="26">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="145,138,111,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="27">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="111,92,16,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="11"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="28">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,255,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="29">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,215,80,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="3">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,127,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="30">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,175,60,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="31">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,127,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="32">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="33">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="200,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="34">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="150,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="35">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="182,74,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="36">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="186,56,168,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="37">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="128,0,128,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="38">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,128,128,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="39">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,0,255,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="4">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="40">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="145,138,111,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="41">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="111,92,16,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="8"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="42">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,255,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="43">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,215,80,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="44">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,175,60,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="45">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,127,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="46">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="47">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="200,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="48">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="150,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="49">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="182,74,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="5">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="200,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="50">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="186,56,168,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="51">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="128,0,128,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="52">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,128,128,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="53">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,0,255,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="54">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="145,138,111,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="55">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="111,92,16,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="rectangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="6">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="150,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="7">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="182,74,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="8">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="186,56,168,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="9">
        <layer pass="0" class="SvgMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="128,0,128,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="technischgebouw.svg"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="Pixel"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="50"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="Pixel"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple"/>
  <customproperties>
    <property key="labeling" value="pal"/>
    <property key="labeling/addDirectionSymbol" value="false"/>
    <property key="labeling/angleOffset" value="0"/>
    <property key="labeling/blendMode" value="0"/>
    <property key="labeling/bufferBlendMode" value="0"/>
    <property key="labeling/bufferColorA" value="255"/>
    <property key="labeling/bufferColorB" value="255"/>
    <property key="labeling/bufferColorG" value="255"/>
    <property key="labeling/bufferColorR" value="255"/>
    <property key="labeling/bufferDraw" value="false"/>
    <property key="labeling/bufferJoinStyle" value="64"/>
    <property key="labeling/bufferNoFill" value="false"/>
    <property key="labeling/bufferSize" value="1"/>
    <property key="labeling/bufferSizeInMapUnits" value="false"/>
    <property key="labeling/bufferSizeMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/bufferTransp" value="0"/>
    <property key="labeling/centroidInside" value="false"/>
    <property key="labeling/centroidWhole" value="false"/>
    <property key="labeling/decimals" value="3"/>
    <property key="labeling/displayAll" value="false"/>
    <property key="labeling/dist" value="0"/>
    <property key="labeling/distInMapUnits" value="false"/>
    <property key="labeling/distMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/drawLabels" value="false"/>
    <property key="labeling/enabled" value="false"/>
    <property key="labeling/fieldName" value=""/>
    <property key="labeling/fitInPolygonOnly" value="false"/>
    <property key="labeling/fontCapitals" value="0"/>
    <property key="labeling/fontFamily" value="MS Shell Dlg 2"/>
    <property key="labeling/fontItalic" value="false"/>
    <property key="labeling/fontLetterSpacing" value="0"/>
    <property key="labeling/fontLimitPixelSize" value="false"/>
    <property key="labeling/fontMaxPixelSize" value="10000"/>
    <property key="labeling/fontMinPixelSize" value="3"/>
    <property key="labeling/fontSize" value="8.25"/>
    <property key="labeling/fontSizeInMapUnits" value="false"/>
    <property key="labeling/fontSizeMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/fontStrikeout" value="false"/>
    <property key="labeling/fontUnderline" value="false"/>
    <property key="labeling/fontWeight" value="50"/>
    <property key="labeling/fontWordSpacing" value="0"/>
    <property key="labeling/formatNumbers" value="false"/>
    <property key="labeling/isExpression" value="true"/>
    <property key="labeling/labelOffsetInMapUnits" value="true"/>
    <property key="labeling/labelOffsetMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/labelPerPart" value="false"/>
    <property key="labeling/leftDirectionSymbol" value="&lt;"/>
    <property key="labeling/limitNumLabels" value="false"/>
    <property key="labeling/maxCurvedCharAngleIn" value="20"/>
    <property key="labeling/maxCurvedCharAngleOut" value="-20"/>
    <property key="labeling/maxNumLabels" value="2000"/>
    <property key="labeling/mergeLines" value="false"/>
    <property key="labeling/minFeatureSize" value="0"/>
    <property key="labeling/multilineAlign" value="0"/>
    <property key="labeling/multilineHeight" value="1"/>
    <property key="labeling/namedStyle" value="Normal"/>
    <property key="labeling/obstacle" value="true"/>
    <property key="labeling/obstacleFactor" value="1"/>
    <property key="labeling/obstacleType" value="0"/>
    <property key="labeling/offsetType" value="0"/>
    <property key="labeling/placeDirectionSymbol" value="0"/>
    <property key="labeling/placement" value="0"/>
    <property key="labeling/placementFlags" value="10"/>
    <property key="labeling/plussign" value="false"/>
    <property key="labeling/predefinedPositionOrder" value="TR,TL,BR,BL,R,L,TSR,BSR"/>
    <property key="labeling/preserveRotation" value="true"/>
    <property key="labeling/previewBkgrdColor" value="#ffffff"/>
    <property key="labeling/priority" value="5"/>
    <property key="labeling/quadOffset" value="4"/>
    <property key="labeling/repeatDistance" value="0"/>
    <property key="labeling/repeatDistanceMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/repeatDistanceUnit" value="1"/>
    <property key="labeling/reverseDirectionSymbol" value="false"/>
    <property key="labeling/rightDirectionSymbol" value=">"/>
    <property key="labeling/scaleMax" value="10000000"/>
    <property key="labeling/scaleMin" value="1"/>
    <property key="labeling/scaleVisibility" value="false"/>
    <property key="labeling/shadowBlendMode" value="6"/>
    <property key="labeling/shadowColorB" value="0"/>
    <property key="labeling/shadowColorG" value="0"/>
    <property key="labeling/shadowColorR" value="0"/>
    <property key="labeling/shadowDraw" value="false"/>
    <property key="labeling/shadowOffsetAngle" value="135"/>
    <property key="labeling/shadowOffsetDist" value="1"/>
    <property key="labeling/shadowOffsetGlobal" value="true"/>
    <property key="labeling/shadowOffsetMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/shadowOffsetUnits" value="1"/>
    <property key="labeling/shadowRadius" value="1.5"/>
    <property key="labeling/shadowRadiusAlphaOnly" value="false"/>
    <property key="labeling/shadowRadiusMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/shadowRadiusUnits" value="1"/>
    <property key="labeling/shadowScale" value="100"/>
    <property key="labeling/shadowTransparency" value="30"/>
    <property key="labeling/shadowUnder" value="0"/>
    <property key="labeling/shapeBlendMode" value="0"/>
    <property key="labeling/shapeBorderColorA" value="255"/>
    <property key="labeling/shapeBorderColorB" value="128"/>
    <property key="labeling/shapeBorderColorG" value="128"/>
    <property key="labeling/shapeBorderColorR" value="128"/>
    <property key="labeling/shapeBorderWidth" value="0"/>
    <property key="labeling/shapeBorderWidthMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/shapeBorderWidthUnits" value="1"/>
    <property key="labeling/shapeDraw" value="false"/>
    <property key="labeling/shapeFillColorA" value="255"/>
    <property key="labeling/shapeFillColorB" value="255"/>
    <property key="labeling/shapeFillColorG" value="255"/>
    <property key="labeling/shapeFillColorR" value="255"/>
    <property key="labeling/shapeJoinStyle" value="64"/>
    <property key="labeling/shapeOffsetMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/shapeOffsetUnits" value="1"/>
    <property key="labeling/shapeOffsetX" value="0"/>
    <property key="labeling/shapeOffsetY" value="0"/>
    <property key="labeling/shapeRadiiMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/shapeRadiiUnits" value="1"/>
    <property key="labeling/shapeRadiiX" value="0"/>
    <property key="labeling/shapeRadiiY" value="0"/>
    <property key="labeling/shapeRotation" value="0"/>
    <property key="labeling/shapeRotationType" value="0"/>
    <property key="labeling/shapeSVGFile" value=""/>
    <property key="labeling/shapeSizeMapUnitScale" value="0,0,0,0,0,0"/>
    <property key="labeling/shapeSizeType" value="0"/>
    <property key="labeling/shapeSizeUnits" value="1"/>
    <property key="labeling/shapeSizeX" value="0"/>
    <property key="labeling/shapeSizeY" value="0"/>
    <property key="labeling/shapeTransparency" value="0"/>
    <property key="labeling/shapeType" value="0"/>
    <property key="labeling/textColorA" value="255"/>
    <property key="labeling/textColorB" value="0"/>
    <property key="labeling/textColorG" value="0"/>
    <property key="labeling/textColorR" value="0"/>
    <property key="labeling/textTransp" value="0"/>
    <property key="labeling/upsidedownLabels" value="0"/>
    <property key="labeling/wrapChar" value=""/>
    <property key="labeling/xOffset" value="0"/>
    <property key="labeling/yOffset" value="0"/>
    <property key="labeling/zIndex" value="0"/>
    <property key="variableNames" value="_fields_"/>
    <property key="variableValues" value=""/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerTransparency>0</layerTransparency>
  <displayfield>id:(0,0)</displayfield>
  <label>0</label>
  <labelattributes>
    <label fieldname="" text="Label"/>
    <family fieldname="" name="MS Shell Dlg 2"/>
    <size fieldname="" units="pt" value="12"/>
    <bold fieldname="" on="0"/>
    <italic fieldname="" on="0"/>
    <underline fieldname="" on="0"/>
    <strikeout fieldname="" on="0"/>
    <color fieldname="" red="0" blue="0" green="0"/>
    <x fieldname=""/>
    <y fieldname=""/>
    <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
    <angle fieldname="" value="0" auto="0"/>
    <alignment fieldname="" value="center"/>
    <buffercolor fieldname="" red="255" blue="255" green="255"/>
    <buffersize fieldname="" units="pt" value="1"/>
    <bufferenabled fieldname="" on=""/>
    <multilineenabled fieldname="" on=""/>
    <selectedonly on=""/>
  </labelattributes>
  <SingleCategoryDiagramRenderer diagramType="Pie">
    <DiagramCategory penColor="#000000" labelPlacementMethod="XHeight" penWidth="0" diagramOrientation="Up" minimumSize="0" barWidth="5" penAlpha="255" maxScaleDenominator="1e+08" backgroundColor="#ffffff" transparency="0" width="15" scaleDependency="Area" backgroundAlpha="255" angleOffset="1440" scaleBasedVisibility="0" enabled="0" height="15" sizeType="MM" minScaleDenominator="1">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings yPosColumn="-1" linePlacementFlags="10" placement="0" dist="0" xPosColumn="-1" priority="0" obstacle="0" zIndex="0" showAll="1"/>
  <annotationform>.</annotationform>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <attributeactions/>
  <editform>.</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
Formulieren van QGIS mogen een functie van Python hebben die wordt aangeroepen wanneer het formulier wordt geopend.

Gebruik deze functie om extra logica aan uw formulieren toe te voegen.

Voer de naam van de functie in in het veld "Python Init functie".
Een voorbeeld volgt:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <layerGeometryType>0</layerGeometryType>
</qgis>
