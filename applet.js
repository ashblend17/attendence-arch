const Applet = imports.ui.applet;
const Main = imports.ui.main;
const PopupMenu = imports.ui.popupMenu;
const Lang = imports.lang;
const Util = imports.misc.util;

function AttendenceApplet(metadata, orientation, panel_height, instanceId) {
  this._init(metadata, orientation, panel_height, instanceId);
}

AttendenceApplet.prototype = {
    __proto__: Applet.TextApplet.prototype,
  
    _init: function(metadata, orientation, panel_height, instanceId) {
      this._data = {};
      Applet.TextApplet.prototype._init.call(this, orientation, panel_height, instanceId);
      this.metadata = metadata;
      //add icon to applet firefox
      // this.set_applet_icon_name('firefox');
      //add label to applet
      this.set_applet_label('LMS');

      

      this._call_lms();
      this.menu = new Applet.AppletPopupMenu(this, orientation);
      this.menuManager = new PopupMenu.PopupMenuManager(this);
      this.menuManager.addMenu(this.menu);


    },
    
    //function to async call lms.py
    _call_lms: function() {
      Util.spawn_async(['python3', this.metadata.path + '/lms.py'], Lang.bind(this, function(result) {
        this._data = JSON.parse(result);

      }));
    },


    on_applet_clicked: function(event) {
      // if menu open close
      if (this.menu.isOpen) {
        this.menu.close();
        return;
      }
      this._call_lms()
      this.menu.removeAll();

      this.log('clicked');
      // loop over the data and create a menu item for each
      //loop over each key of the data and add key value to menu
      for (let key in this._data) {
        let item = new PopupMenu.PopupMenuItem(key + ': ' + this._data[key]);
        this.menu.addMenuItem(item);
      }
      //show the menu
      this.menu.open();

    },

    log: function(message) {
      //using error for visibility
      global.logError('[' + this.metadata.uuid + '] ' + message);

    },
    
}

function main(metadata, orientation, panel_height, instanceId) {
    return new AttendenceApplet(metadata, orientation, panel_height, instanceId);
  }
  