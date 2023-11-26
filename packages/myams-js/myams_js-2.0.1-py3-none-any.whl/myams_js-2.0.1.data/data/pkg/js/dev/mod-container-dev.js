(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports);
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports);
    global.modContainer = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.container = void 0;
  /* global MyAMS */
  /**
   * MyAMS container management
   */

  const $ = MyAMS.$;
  const container = _exports.container = {
    /**
     * Switch attribute of container element
     *
     * @param action
     */
    switchElementAttribute: action => {
      return function (link, params) {
        MyAMS.require('ajax', 'alert', 'i18n').then(() => {
          const cell = link.parents('td').first(),
            icon = $('i', cell),
            row = cell.parents('tr'),
            table = row.parents('table'),
            col = $(`thead th:nth-child(${cell.index() + 1})`, table);
          let location = link.data('ams-location') || col.data('ams-location') || row.data('ams-location') || table.data('ams-location') || '';
          if (location) {
            location += '/';
          }
          const updateTarget = link.data('ams-update-target') || col.data('ams-update-target') || row.data('ams-update-target') || table.data('ams-update-target') || 'switch-element-attribute.json',
            objectName = row.data('ams-element-name'),
            hint = icon.attr('data-original-title') || icon.attr('title');
          icon.tooltip('hide').replaceWith('<i class="fas fa-spinner fa-spin"></i>');
          MyAMS.ajax.post(location + updateTarget, {
            object_name: objectName,
            attribute_name: col.data('ams-attribute-name')
          }).then((result, status, xhr) => {
            let icon = $('i', cell);
            if (result.status === 'success') {
              if (result.state) {
                icon.replaceWith(`<i class="${col.data('ams-icon-on')}"></i>`);
              } else {
                icon.replaceWith(`<i class="${col.data('ams-icon-off')}"></i>`);
              }
              if (hint) {
                icon = $('i', cell);
                icon.addClass('hint').attr('data-original-title', hint);
              }
              if (result.handle_json) {
                MyAMS.ajax.handleJSON(result);
              }
            } else {
              MyAMS.ajax.handleJSON(result);
            }
          });
        });
      };
    },
    /**
     * Delete element from container
     *
     * @param action
     * @returns {(function(*, *): void)|*}
     */
    deleteElement: action => {
      return function (link, params) {
        MyAMS.require('ajax', 'alert', 'i18n').then(() => {
          MyAMS.alert.bigBox({
            status: 'danger',
            icon: 'fas fa-bell',
            title: MyAMS.i18n.WARNING,
            message: MyAMS.i18n.CONFIRM_REMOVE,
            successLabel: MyAMS.i18n.CONFIRM,
            cancelLabel: MyAMS.i18n.BTN_CANCEL
          }).then(status => {
            if (status !== 'success') {
              return;
            }
            const cell = link.parents('td'),
              row = cell.parents('tr'),
              table = row.parents('table'),
              col = $(`thead th:nth-child(${cell.index() + 1})`, table);
            let location = link.data('ams-location') || col.data('ams-location') || row.data('ams-location') || table.data('ams-location') || '';
            if (location) {
              location += '/';
            }
            const deleteTarget = link.data('ams-delete-target') || col.data('ams-delete-target') || row.data('ams-delete-target') || table.data('ams-delete-target') || 'delete-element.json',
              objectName = row.data('ams-element-name');
            MyAMS.ajax.post(location + deleteTarget, {
              'object_name': objectName
            }).then((result, status, xhr) => {
              if (result.status === 'success') {
                if (table.hasClass('datatable')) {
                  table.DataTable().row(row).remove().draw();
                } else {
                  row.remove();
                }
                if (result.handle_json) {
                  MyAMS.ajax.handleJSON(result);
                }
              } else {
                MyAMS.ajax.handleJSON(result);
              }
            });
          });
        });
      };
    }
  };

  /**
   * Global module initialization
   */
  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('container');
    } else {
      MyAMS.container = container;
      console.debug("MyAMS: container module loaded...");
    }
  }
});
//# sourceMappingURL=mod-container-dev.js.map
