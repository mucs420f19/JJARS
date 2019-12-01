// ScrUML
// diagram.js
// Team JJARS

const CLASS_WIDTH = 150;
const CLASS_HEIGHT = 50;

class Diagram {


    // ----------
    // Constructor

    constructor(canvasID) {

        // Capture canvas element
        if (!canvasID)
        {
            console.error("No canvas ID provided in Diagram constructor.");
            return;
        }
        this.canvas = new SVG(canvasID).size(500, 500);
        this.canvas.mousedown(function canvasMouseDown(event) {
            tryAddClass(event);
        })

        // Set environment variables
        this.selectedElement = null;
        this.draggingEnabled = false;

    }


    // ----------
    // Selection functions

    // ----------
    // clearSelection

    clearSelection()
    {
        if (this.selectedElement != null && document.querySelector("#diagram-canvas .selected"))
            document.querySelector("#diagram-canvas .selected").classList.remove("selected");
        document.querySelector("#info-panel").style.display = "none"
        document.querySelector("#class-info").style.display = "none"
        document.querySelector("#relationship-info").style.display = "none"
        document.getElementById("function-list").innerHTML = '';
        document.getElementById("variable-list").innerHTML = '';
        this.selectedElement = null;
    }

    // ----------
    // changeSelection

    changeSelection(element)
    {
        this.clearSelection();

        element.addClass("selected");
        document.querySelector("#info-panel").style.display = "block"
        if (currentUIState === UI_STATES.SELECT)
        {
            if (element.hasClass("uml-class"))
            {
                document.querySelector("#class-info").style.display = "block"
                document.querySelector("#class-id").innerHTML = element.id()
                document.querySelector("#relationship-info").style.display = "none"

                var attrDict= JSON.parse(element.attr("data-attributes"));

                for (let [key, value] of Object.entries(attrDict))
                {
                    if ( key != "[x]" && key != "[y]")
                    {
                        // This attribute is a function if the second char of the key is an 'F'
                        if (key.substring(1,2) == "F")
                        {
                            var deserialDict = this.deserializeFunction(key, value);

                            var funcVisibility = deserialDict["visibility"];
                            var funcType = deserialDict["return-type"];
                            var funcName = deserialDict["name"];
                            var funcParamStr = deserialDict["param-str"];

                            addMemberFunction(funcVisibility, funcType, funcName, funcParamStr);
                        }
                        // This attribute is a variable if the second char of the key is an 'V'
                        else if (key.substring(1,2) == "V")
                        {
                            var deserialDict = this.deserializeVariable(key, value);

                            var varVisibility = deserialDict["visibility"];
                            var varType = deserialDict["type"];
                            var varName = deserialDict["name"];

                            addMemberVariable(varVisibility, varType, varName);
                        }
                    }
                }

            }
            else
            {
                document.querySelector("#class-info").style.display = "none"
                document.querySelector("#relationship-info").style.display = "block"
                document.querySelector("#relationship-id").innerHTML = element.id()
            }
        }
        else
        {
            document.querySelector("#info-panel").style.display = "none"
            document.querySelector("#class-info").style.display = "none"
            document.querySelector("#relationship-info").display = "none"
        }
        this.selectedElement = element;
    }

    // ----------
    // deserializeFunction

    deserializeFunction(attrKey, attrValue) {
        var resultDict = {};

        resultDict["name"] = attrKey.substring(3, attrKey.length - 1);

        attrValue = attrValue.substring(1, attrValue.length -1);
        var splitArray = attrValue.split("][");

        resultDict["visibility"] = splitArray[0];
        resultDict["return-type"] = splitArray[1];

        var paramsString = "";
        for (var i = 2; i < splitArray.length; i += 2){
            paramsString += splitArray[i] + " " + splitArray[i + 1] + ", ";
        }
        // Fixes fencepost issue: extra ", " at the end
        paramsString = paramsString.trimRight(", ");

        resultDict["param-str"] = paramsString;

        return resultDict;
    }

    // ----------
    // deserializeVariable

    deserializeVariable(attrKey, attrValue) {
        var resultDict = {};

        resultDict["name"] = attrKey.substring(3, attrKey.length - 1);

        attrValue = attrValue.substring(1, attrValue.length -1);
        var splitArray = attrValue.split("][");

        resultDict["visibility"] = splitArray[0];
        resultDict["type"] = splitArray[1];

        return resultDict;
    }


    // ----------
    // Element builder functions

    // ----------
    // buildClassElement

    buildClassElement(className, classAttr) {

        // Build element on the canvas with appropriate ID and classification
        var element = this.canvas.nested().id(className).addClass("uml-class");

        element.attr('data-attributes', JSON.stringify(classAttr))

        // Add body and text
        var rect = element.rect(1, 1);
        var text_OfClassName = element.text(className).move(10, 10);

        var width = text_OfClassName.bbox().width + 20;
        var height = text_OfClassName.bbox().height + 20;
        rect.width(width);
        rect.height(height);

        // Place element at the appropriate coordinates, if in the attributes
        if (classAttr["[x]"] && classAttr["[y]"])
        {
            element.move(classAttr["[x]"], classAttr["[y]"]);
        }

        // Hook element in to click event handler
        element.mousedown(function classMouseDown(event) {
            classElementClicked(this);
        });

        // Hook drag end event to handler
        element.on("dragend", function classDragEnd(event) {
            classElementDragged(this);
        });

    }

    // ----------
    // updateClassAttr

    updateClassAttr(className, classAttr) {
        var element = SVG.get(className);

        if (element.attr('data-attributes') != JSON.stringify(classAttr))
        {
            element.attr('data-attributes', JSON.stringify(classAttr));
        }
    }


    // ----------
    // buildRelationshipElement

    buildRelationshipElement(relationshipID, relationshipAttr) {

        // Get class names from relationship ID
        var names = relationshipID.slice(1, -1).split(",");
        var classNameA = names[0];
        var classNameB = names[1];

        // Draw connector to the canvas
        var classAElem = SVG.get(classNameA);
        var classBElem = SVG.get(classNameB);
        var connector = classAElem.connectable({"sourceAttach": "perifery",
                                                "targetAttach": "perifery",
                                                "type": "curved"},
                                               classBElem).connector;

	//var endpointA = connector.pointAt(0);
	//var endpointB = connector.connector.pointAt(connector.connector.length());
        //var indicatorA = connector.parent().text("1").move(endpointA.x,endpointA.y);
	//var indicatorB = connector.text("1asefasesf").move(endpointB.x(),endpointB.y());
	//classAElem.add(indicatorA);

        // Give the connector an ID and classify it properly
        connector.id(relationshipID).addClass("uml-relationship");

        // Hook element in to click event handler
        connector.mousedown(function relationshipMouseDown() {
            relationshipElementClicked(this);
        });

    }

    // ----------
    // setDragging

    setDragging(enable) {

        // Set global dragging flag
        this.draggingEnabled = enable;

        // "this" is shadowed by a reference to the element in the "each" loop
        var me = this;

        // Set dragging behavior of every UML class
        this.canvas.each(function setDraggingCanvasEach(i, children) {
            if (this.hasClass("uml-class")) {

                // Enable dragging
                if (enable && typeof this.fixed !== "function")
                {
                    this.draggy({
                        minX: 0,
                        minY: 0,
                        maxX: me.canvas.width() - this.bbox().width,
                        maxY: me.canvas.height() - this.bbox().height
                    });
                }
                else if (!enable && typeof this.fixed === "function")
                {
                    this.fixed();
                }
            }
        });

    }

    // ----------
    // update

    update(toSelect = "") {

        // "this" is shadowed by a reference to the promise in the callbacks
        var me = this;

        // Get the classes in the diagram
        pywebview.api.getAllClasses().then(function getClasses(response) {

            var classes = response;

            // Get the relationships in the diagram
            pywebview.api.getAllRelationships().then(function getRelationships(response) {

                var relationships = response;

                // Clear the current selection
                me.clearSelection()

                // Remove elements from the canvas that are no longer in the diagram
                me.canvas.each(function updateCanvasEach(i, children) {
                    if (!(this.id() in classes) || !(this.id() in relationships))
                    {
                        this.remove();
                    }
                });

                // Add any new classes to the canvas
                for (let [key, value] of Object.entries(classes))
                {
                    if (!SVG.get(key))
                    {
                        me.buildClassElement(key, value);
                    }
                    me.updateClassAttr(key, value);
                }

                // Add any new relationships to the diagram
                for (let [key, value] of Object.entries(relationships))
                {
                    if (!SVG.get(key))
                    {
                        me.buildRelationshipElement(key, value);
                    }
                }

                // Make sure that newly-created diagram elements are appropriately draggable/fixed
                me.setDragging(me.draggingEnabled);

                // Attempt to select an element post-update if specified
                if (toSelect !== "" && SVG.get(toSelect))
                {
                    me.changeSelection(SVG.get(toSelect));
                }

            });

        });

    }

}
