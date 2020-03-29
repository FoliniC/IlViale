var collapseClass = "TreeView-Collapse";
var expandClass = "TreeView-Expand";
var showClass = "TreeView-Show";
var hideClass = "TreeView-Hide";
function CanHaveClass_CssFriendlyAdapters(element)
{
    return ((element != null) && (element.className != null));
}

function HasAnyClass_CssFriendlyAdapters(element)
{
    return (CanHaveClass_CssFriendlyAdapters(element) && (element.className.length > 0));
}

function HasClass_CssFriendlyAdapters(element, specificClass)
{
    return (HasAnyClass_CssFriendlyAdapters(element) && (element.className.indexOf(specificClass) > -1));
}

function AddClass_CssFriendlyAdapters(element, classToAdd)
{
    if (HasAnyClass_CssFriendlyAdapters(element))
    {
        if (!HasClass_CssFriendlyAdapters(element, classToAdd))
        {
            element.className = element.className + " " + classToAdd;
        }
    }
    else if (CanHaveClass_CssFriendlyAdapters(element))
    {
        element.className = classToAdd;
    }
}

function AddClassUpward_CssFriendlyAdapters(startElement, stopParentClass, classToAdd)
{
    var elementOrParent = startElement;
    while ((elementOrParent != null) && (!HasClass_CssFriendlyAdapters(elementOrParent, topmostClass)))
    {
        AddClass_CssFriendlyAdapters(elementOrParent, classToAdd);
        elementOrParent = elementOrParent.parentNode;
    }    
}

function SwapClass_CssFriendlyAdapters(element, oldClass, newClass)
{
    if (HasAnyClass_CssFriendlyAdapters(element))
    {
        element.className = element.className.replace(new RegExp(oldClass, "gi"), newClass);
    }
}

function SwapOrAddClass_CssFriendlyAdapters(element, oldClass, newClass)
{
    if (HasClass_CssFriendlyAdapters(element, oldClass))
    {
        SwapClass_CssFriendlyAdapters(element, oldClass, newClass);
    }
    else
    {
        AddClass_CssFriendlyAdapters(element, newClass);
    }
}

function RemoveClass_CssFriendlyAdapters(element, classToRemove)
{
    SwapClass_CssFriendlyAdapters(element, classToRemove, "");
}

function RemoveClassUpward_CssFriendlyAdapters(startElement, stopParentClass, classToRemove)
{
    var elementOrParent = startElement;
    while ((elementOrParent != null) && (!HasClass_CssFriendlyAdapters(elementOrParent, topmostClass)))
    {
        RemoveClass_CssFriendlyAdapters(elementOrParent, classToRemove);
        elementOrParent = elementOrParent.parentNode;
    }    
}

function IsEnterKey()
{
    var retVal = false;
    var keycode = 0;
    if ((typeof(window.event) != "undefined") && (window.event != null))
    {
        keycode = window.event.keyCode;
    }
    else if ((typeof(e) != "undefined") && (e != null))
    {
        keycode = e.which;
    }
    if (keycode == 13)
    {
        retVal = true;
    }
    return retVal;
}
function IsExpanded_TreeView(element) {
    return (HasClass_CssFriendlyAdapters(element, collapseClass));
}

function TogglePlusMinus_TreeView(element, showPlus) {
    if (HasAnyClass_CssFriendlyAdapters(element)) {
        var showPlusLocal = IsExpanded_TreeView(element);
        if ((typeof (showPlus) != "undefined") && (showPlus != null)) {
            showPlusLocal = showPlus;
        }
        var oldClass = showPlusLocal ? collapseClass : expandClass;
        var newClass = showPlusLocal ? expandClass : collapseClass;
        SwapClass_CssFriendlyAdapters(element, oldClass, newClass);
    }
}

function ToggleChildrenDisplay_TreeView(element, collapse) {
    if ((element != null) && (element.parentNode != null) && (element.parentNode.getElementsByTagName != null)) {
        var childrenToHide = element.parentNode.getElementsByTagName("ul");
        var oldClass = collapse ? showClass : hideClass;
        var newClass = collapse ? hideClass : showClass;
        for (var i = 0; i < childrenToHide.length; i++) {
            if ((childrenToHide[i].parentNode != null) && (childrenToHide[i].parentNode == element.parentNode)) {
                SwapOrAddClass_CssFriendlyAdapters(childrenToHide[i], oldClass, newClass);
            }
        }
    }
}

function ExpandCollapse_TreeView(sourceElement) {
    if (HasAnyClass_CssFriendlyAdapters(sourceElement)) {
        var expanded = IsExpanded_TreeView(sourceElement);
        TogglePlusMinus_TreeView(sourceElement, expanded);
        ToggleChildrenDisplay_TreeView(sourceElement, expanded);
    }
}

function GetViewState_TreeView(id) {
    var retStr = "";
    if ((typeof (id) != "undefined") && (id != null) && (document.getElementById(id) != null)) {
        var topUL = document.getElementById(id);
        retStr = ComposeViewState_TreeView(topUL, "");
    }
    return retStr;
}

function ComposeViewState_TreeView(element, state) {
    var child = element.firstChild;
    var bConsiderChildren = true;

    //  The following line must be changed if you alter the TreeView adapters generation of
    //  markup such that the first child within the LI no longer is the expand/collapse <span>.
    if ((element.tagName == "LI") && (child != null)) {
        var expandCollapseSPAN = null;
        var currentChild = child;
        while (currentChild != null) {
            if ((currentChild.tagName == "SPAN") &&
                (currentChild.className != null) &&
                ((currentChild.className.indexOf(collapseClass) > -1) ||
                    (currentChild.className.indexOf(expandClass) > -1))) {
                expandCollapseSPAN = currentChild;
                break;
            }
            currentChild = currentChild.nextSibling;
        }

        if (expandCollapseSPAN != null) {
            if (expandCollapseSPAN.className.indexOf(collapseClass) > -1) {
                //  If the "collapse" class is currently being used then the "collapse" icon is, presumably, being shown.
                //  In other words, the node itself is actually expanded at the present moment (which is why you now
                //  have the option of collapsing it.  So we mark it as an "expanded" node for purposes of the view state
                //  we are now accumulating.
                state += "e";
            }
            else if (expandCollapseSPAN.className.indexOf(expandClass) > -1) {
                //  This part of the tree is collapsed so we don't need to consider its children.
                bConsiderChildren = false;
                state += "n";
            }
        }
    }

    if (bConsiderChildren && (child != null)) {
        state = ComposeViewState_TreeView(child, state);
    }

    if (element.nextSibling != null) {
        state = ComposeViewState_TreeView(element.nextSibling, state);
    }

    return state;
}