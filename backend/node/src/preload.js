// secure, minimal preload
const { contextBridge } = require("electron");
contextBridge.exposeInMainWorld("api", {
  getAppVersion: () => require("electron").app.getVersion()
});
