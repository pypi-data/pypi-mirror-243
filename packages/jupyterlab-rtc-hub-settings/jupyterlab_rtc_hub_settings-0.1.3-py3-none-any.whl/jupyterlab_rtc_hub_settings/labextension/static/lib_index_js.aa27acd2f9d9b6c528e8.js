"use strict";
(self["webpackChunkjupyterlab_rtc_hub_settings"] = self["webpackChunkjupyterlab_rtc_hub_settings"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-rtc-hub-settings', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _sidebar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./sidebar */ "./lib/sidebar.js");


/**
 * Initialization data for the jupyterlab_rtc_hub_settings extension.
 */
const plugin = {
    id: 'jupyterlab_rtc_hub_settings:plugin',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, labShell) => {
        console.log('JupyterLab extension jupyterlab_rtc_hub_settings is activated!');
        // Create the sharing settings sidebar panel
        const sidebar = new _sidebar__WEBPACK_IMPORTED_MODULE_1__.SharingSettingsSidebar();
        sidebar.id = 'rtc-hub-settings-labextension:plugin';
        sidebar.title.iconClass =
            'rtc-hub-settings-SharingSettingsLogo jp-SideBar-tabIcon';
        sidebar.title.caption = 'Sharing settings';
        // Register sidebar panel with JupyterLab
        labShell.add(sidebar, 'left', { rank: 600 });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/sidebar.js":
/*!************************!*\
  !*** ./lib/sidebar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SharingSettingsSidebar: () => (/* binding */ SharingSettingsSidebar)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _tableWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tableWidget */ "./lib/tableWidget.js");
/* harmony import */ var _toolbarWidget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./toolbarWidget */ "./lib/toolbarWidget.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);







/**
 * Sidebar widget for displaying RTC sharing settings.
 */
class SharingSettingsSidebar extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this._users = [];
        this._valueChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this.addClass('rtc-hub-settings-SharingSettingsSidebar');
        // Define widget layout
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout());
        // Add Toolbar widget
        const toolbar = new _toolbarWidget__WEBPACK_IMPORTED_MODULE_4__.ToolbarWidget(() => {
            this._getUsers();
        });
        layout.addWidget(toolbar);
        // Add Users table widget
        const table = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.UseSignal, { signal: this._valueChanged, initialArgs: this._users }, (_, oa) => (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_tableWidget__WEBPACK_IMPORTED_MODULE_5__.UsersTableWidget, { ar: oa === undefined ? [] : oa, updateUsers: arg0 => this._updateUsers(arg0), refreshUsers: () => this._getUsers() }))));
        table.addClass('rtc-hub-settings-SharingSettingsSidebar-table-div');
        layout.addWidget(table);
    }
    async _getUsers() {
        // Return results of API request
        (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('users').then(response => {
            // Update internal variable
            this._users = response;
            // Send signal for table widget to update data
            this._valueChanged.emit(this._users);
        });
    }
    async _updateUsers(users) {
        // Send updated list of users statuses
        (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('users', {
            method: 'POST',
            body: JSON.stringify(users)
        }).then(response => {
            // Update internal variable
            this._users = response;
            // Send signal for table widget to update data
            this._valueChanged.emit(this._users);
        });
    }
}


/***/ }),

/***/ "./lib/tableWidget.js":
/*!****************************!*\
  !*** ./lib/tableWidget.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   UsersTableWidget: () => (/* binding */ UsersTableWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

// Class for table of users
class UsersTableWidget extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.updateUser = (name) => {
            const props = this.props;
            const index = props.ar.findIndex((user) => user.name === name);
            props.ar[index].shared = !props.ar[index].shared;
            props.updateUsers(props.ar);
        };
        props.refreshUsers();
    }
    render() {
        const tableRows = this.props.ar.map((user) => {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tr", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null, user.name),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "checkbox", checked: user.shared, onChange: () => this.updateUser(user.name) }))));
        });
        // Assemble headers and rows in the full table
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("table", { className: "rtc-hub-settings-SharingSettingsSidebar-table" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tbody", null, tableRows))));
    }
}


/***/ }),

/***/ "./lib/toolbarWidget.js":
/*!******************************!*\
  !*** ./lib/toolbarWidget.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ToolbarWidget: () => (/* binding */ ToolbarWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);



class ToolbarWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor(refresh) {
        super();
        this.addClass('rtc-hub-settings-Toolbar-layout');
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.PanelLayout());
        const header = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node: document.createElement('div') });
        header.node.textContent = 'Collaboration Sharing';
        layout.addWidget(header);
        const spacer = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node: document.createElement('span') });
        spacer.addClass('rtc-hub-settings-Toolbar-spacer');
        layout.addWidget(spacer);
        // Search button
        const refreshButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.refreshIcon,
            onClick: refresh
        });
        layout.addWidget(refreshButton);
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.aa27acd2f9d9b6c528e8.js.map