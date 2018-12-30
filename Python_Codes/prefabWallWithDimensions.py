#importing required modules
import FreeCAD
import Arch
import Draft
import DraftTools
import PartDesign
import PartDesignGui
import Sketcher

#creating new document
FreeCAD.newDocument("prefabWall")

#setting parameters
lengthOfPanel = 6000
heightOfPanel = 3000
sillHeightOfOpening = 1000
heightOfOpening = 500
widthOfOpening = 1000
thicknessOfPanel = 500

#adding body and sketch objects to the active document
FreeCAD.activeDocument().addObject('PartDesign::Body','prefabWall')
FreeCAD.activeDocument().prefabWall.newObject('Sketcher::SketchObject','Sketch')
FreeCAD.activeDocument().Sketch.Support = (FreeCAD.activeDocument().XZ_Plane, [''])
FreeCAD.activeDocument().Sketch.MapMode = 'FlatFace'
FreeCAD.ActiveDocument.recompute()

#adding first list of geometries to the sketch
geoList0 = []
geoList0.append(Part.LineSegment(FreeCAD.Vector(-20,0,0),FreeCAD.Vector(0,20,0)))
geoList0.append(Part.LineSegment(FreeCAD.Vector(0,20,0),FreeCAD.Vector(20,0,0)))
geoList0.append(Part.LineSegment(FreeCAD.Vector(20,0,0),FreeCAD.Vector(-20,0,0)))
FreeCAD.ActiveDocument.Sketch.addGeometry(geoList0,False)

#adding first list of constraints to the sketch
conList0 = []
conList0.append(Sketcher.Constraint('PointOnObject',0,1,-1)) 
conList0.append(Sketcher.Constraint('PointOnObject',0,2,-2))
conList0.append(Sketcher.Constraint('Coincident',0,2,1,1))
conList0.append(Sketcher.Constraint('Coincident',1,2,2,1)) 
conList0.append(Sketcher.Constraint('Coincident',2,2,0,1))
conList0.append(Sketcher.Constraint('Symmetric',0,1,1,2,-2))
conList0.append(Sketcher.Constraint('DistanceX',0,1,1,2,lengthOfPanel))
conList0.append(Sketcher.Constraint('DistanceY',-1,1,0,2,heightOfPanel))
FreeCAD.ActiveDocument.Sketch.addConstraint(conList0) 

#adding second list of geometries to the sketch(for opening)
geoList1 = []
geoList1.append(Part.LineSegment(FreeCAD.Vector(-5,5,0),FreeCAD.Vector(5,5,0)))
geoList1.append(Part.LineSegment(FreeCAD.Vector(5,5,0),FreeCAD.Vector(5,2,0)))
geoList1.append(Part.LineSegment(FreeCAD.Vector(5,2,0),FreeCAD.Vector(-5,2,0)))
geoList1.append(Part.LineSegment(FreeCAD.Vector(-5,2,0),FreeCAD.Vector(-5,5,0)))
FreeCAD.ActiveDocument.Sketch.addGeometry(geoList1,False)

#adding second list of constraints to the sketch(for opening)
conList1 = []
conList1.append(Sketcher.Constraint('Coincident',3,2,4,1))
conList1.append(Sketcher.Constraint('Coincident',4,2,5,1))
conList1.append(Sketcher.Constraint('Coincident',5,2,6,1))
conList1.append(Sketcher.Constraint('Coincident',6,2,3,1))
conList1.append(Sketcher.Constraint('Horizontal',5))
conList1.append(Sketcher.Constraint('Vertical',4))
conList1.append(Sketcher.Constraint('Vertical',6))
conList1.append(Sketcher.Constraint('Symmetric',3,1,3,2,-2)) 
conList1.append(Sketcher.Constraint('DistanceY',-1,1,4,2,sillHeightOfOpening))
conList1.append(Sketcher.Constraint('DistanceY',4,2,4,1,heightOfOpening)) 
conList1.append(Sketcher.Constraint('DistanceX',3,1,3,2,widthOfOpening))
FreeCAD.ActiveDocument.Sketch.addConstraint(conList1) 

#creating pad from the sketch
FreeCAD.getDocument('prefabWall').recompute()
FreeCAD.activeDocument().prefabWall.newObject("PartDesign::Pad","Pad")
FreeCAD.activeDocument().Pad.Profile = FreeCAD.activeDocument().Sketch
FreeCAD.activeDocument().Pad.Length = thicknessOfPanel
FreeCAD.ActiveDocument.Pad.Length2 = 0
FreeCAD.ActiveDocument.Pad.Type = 0
FreeCAD.ActiveDocument.Pad.UpToFace = None
FreeCAD.ActiveDocument.Pad.Reversed = 0
FreeCAD.ActiveDocument.Pad.Midplane = 0
FreeCAD.ActiveDocument.Pad.Offset = 0
FreeCAD.ActiveDocument.recompute()

#setting the axometric view
FreeCAD.getDocument('prefabWall').recompute()
Gui.getDocument("prefabWall").getObject("Sketch").Visibility = False
Gui.activeDocument().activeView().viewAxometric()
Gui.SendMsgToActiveView("ViewFit")

#creating wall object
wall = Arch.makeWall(FreeCAD.ActiveDocument.prefabWall)
Draft.autogroup(wall)

#setting working plane
FreeCAD.DraftWorkingPlane.alignToPointAndAxis(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,-1,0), thicknessOfPanel)

#creating dimensions
dim1 = Draft.makeDimension(FreeCAD.Vector(-lengthOfPanel/2,-thicknessOfPanel,0),FreeCAD.Vector(lengthOfPanel/2,-thicknessOfPanel,0),FreeCAD.Vector(0,-thicknessOfPanel,-300))
Draft.autogroup(dim1)

FreeCAD.ActiveDocument.ActiveObject.Label = "Length"
FreeCADGui.ActiveDocument.ActiveObject.ArrowType = u"Arrow"
FreeCADGui.ActiveDocument.ActiveObject.ArrowSize = '30 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtLines = '250 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtOvershoot = '125 mm'
FreeCADGui.ActiveDocument.ActiveObject.FontSize = '150 mm'
FreeCADGui.ActiveDocument.ActiveObject.TextSpacing = '50 mm'
FreeCADGui.ActiveDocument.ActiveObject.ShowUnit = False
FreeCADGui.ActiveDocument.ActiveObject.Decimals = 0

dim2 = Draft.makeDimension(FreeCAD.Vector(0,-thicknessOfPanel,0),FreeCAD.Vector(0,-thicknessOfPanel,heightOfPanel),FreeCAD.Vector(-(lengthOfPanel/2+300),-thicknessOfPanel,0))
Draft.autogroup(dim2)

FreeCAD.ActiveDocument.ActiveObject.Label = "Height"
FreeCADGui.ActiveDocument.ActiveObject.ArrowType = u"Arrow"
FreeCADGui.ActiveDocument.ActiveObject.ArrowSize = '30 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtLines = '250 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtOvershoot = '125 mm'
FreeCADGui.ActiveDocument.ActiveObject.FontSize = '150 mm'
FreeCADGui.ActiveDocument.ActiveObject.TextSpacing = '50 mm'
FreeCADGui.ActiveDocument.ActiveObject.ShowUnit = False
FreeCADGui.ActiveDocument.ActiveObject.Decimals = 0

dim3 = Draft.makeDimension(FreeCAD.Vector(0,-thicknessOfPanel,0),FreeCAD.Vector(0,-thicknessOfPanel,sillHeightOfOpening),FreeCAD.Vector((lengthOfPanel/2+300),-thicknessOfPanel,0))
Draft.autogroup(dim3)

FreeCAD.ActiveDocument.ActiveObject.Label = "sillHeightOfOpening"
FreeCADGui.ActiveDocument.ActiveObject.ArrowType = u"Arrow"
FreeCADGui.ActiveDocument.ActiveObject.ArrowSize = '30 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtLines = '250 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtOvershoot = '125 mm'
FreeCADGui.ActiveDocument.ActiveObject.FontSize = '150 mm'
FreeCADGui.ActiveDocument.ActiveObject.TextSpacing = '50 mm'
FreeCADGui.ActiveDocument.ActiveObject.ShowUnit = False
FreeCADGui.ActiveDocument.ActiveObject.Decimals = 0

dim4 = Draft.makeDimension(FreeCAD.Vector(0,-thicknessOfPanel,sillHeightOfOpening),FreeCAD.Vector(0,-thicknessOfPanel,sillHeightOfOpening+heightOfOpening),FreeCAD.Vector(widthOfOpening/2+300,-thicknessOfPanel,0))
Draft.autogroup(dim4)

FreeCAD.ActiveDocument.ActiveObject.Label = "heightOfOpening"
FreeCADGui.ActiveDocument.ActiveObject.ArrowType = u"Arrow"
FreeCADGui.ActiveDocument.ActiveObject.ArrowSize = '30 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtLines = '250 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtOvershoot = '125 mm'
FreeCADGui.ActiveDocument.ActiveObject.FontSize = '150 mm'
FreeCADGui.ActiveDocument.ActiveObject.TextSpacing = '50 mm'
FreeCADGui.ActiveDocument.ActiveObject.ShowUnit = False
FreeCADGui.ActiveDocument.ActiveObject.Decimals = 0

dim5 = Draft.makeDimension(FreeCAD.Vector(-widthOfOpening/2,-thicknessOfPanel,sillHeightOfOpening),FreeCAD.Vector(widthOfOpening/2,-thicknessOfPanel,sillHeightOfOpening),FreeCAD.Vector(0,-thicknessOfPanel,sillHeightOfOpening-300))
Draft.autogroup(dim5)

FreeCAD.ActiveDocument.ActiveObject.Label = "widthOfOpening"
FreeCADGui.ActiveDocument.ActiveObject.ArrowType = u"Arrow"
FreeCADGui.ActiveDocument.ActiveObject.ArrowSize = '30 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtLines = '250 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtOvershoot = '125 mm'
FreeCADGui.ActiveDocument.ActiveObject.FontSize = '150 mm'
FreeCADGui.ActiveDocument.ActiveObject.TextSpacing = '50 mm'
FreeCADGui.ActiveDocument.ActiveObject.ShowUnit = False
FreeCADGui.ActiveDocument.ActiveObject.Decimals = 0

FreeCAD.DraftWorkingPlane.alignToPointAndAxis(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), heightOfPanel)

dim6 = Draft.makeDimension(FreeCAD.Vector(0,-thicknessOfPanel,heightOfPanel),FreeCAD.Vector(0,0,heightOfPanel),FreeCAD.Vector(-300,0,heightOfPanel))
Draft.autogroup(dim6)

FreeCAD.ActiveDocument.ActiveObject.Label = "thicknessOfPanel"
FreeCADGui.ActiveDocument.ActiveObject.ArrowType = u"Arrow"
FreeCADGui.ActiveDocument.ActiveObject.ArrowSize = '30 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtLines = '250 mm'
FreeCADGui.ActiveDocument.ActiveObject.ExtOvershoot = '125 mm'
FreeCADGui.ActiveDocument.ActiveObject.FontSize = '150 mm'
FreeCADGui.ActiveDocument.ActiveObject.TextSpacing = '50 mm'
FreeCADGui.ActiveDocument.ActiveObject.ShowUnit = False
FreeCADGui.ActiveDocument.ActiveObject.Decimals = 0
