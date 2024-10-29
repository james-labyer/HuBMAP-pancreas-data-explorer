
var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.dsLink = function (props) {
    if (props.value === " ") {
        return " "
    } else return React.createElement(window.dash_core_components.Link, {
        children: "View data",
        href: props.value,
    });
}