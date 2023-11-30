const LOCAL_DEV = false;

export let BACKEND_API_URL: string, WEBSOCKET_API_URL: string;
if (LOCAL_DEV) {
  BACKEND_API_URL = 'http://localhost:5000';
  WEBSOCKET_API_URL = 'ws://localhost:1337/ws';
} else {
  BACKEND_API_URL = 'https://api.unianalytics.ch';
  WEBSOCKET_API_URL =
    'wss://ax5pzl8bwk.execute-api.eu-north-1.amazonaws.com/production/';
}

// adapt the app ids in the schema/*.json if this value is changed
export const APP_ID = 'jupyterlab_unianalytics_dashboard';
// A plugin id has to be of the form APP_ID:<schema name without .json>
export const PLUGIN_ID = `${APP_ID}:plugin`;

export const STORAGE_KEY = `@jupyterlab/${APP_ID}:sidedashboard`;

export const TOC_DASHBOARD_RENDER_TIMEOUT = 1000;

export namespace CommandIDs {
  export const dashboardOpenVisu = `${APP_ID}:dashboard-open-visu`;

  export const uploadNotebook = `${APP_ID}:dashboard-upload-notebook`;

  export const copyDownloadLink = `${APP_ID}:dashboard-copy-download-link`;
}

export const visuIconClass = 'jp-icon3';

export const notebookSelector =
  '.jp-DirListing-item[data-file-type="notebook"]';

// notebook metadata field names
const SELECTOR_ID = 'unianalytics';
export namespace Selectors {
  export const notebookId = `${SELECTOR_ID}_notebook_id`;

  export const instanceId = `${SELECTOR_ID}_instance_id`;

  export const cellMapping = `${SELECTOR_ID}_cell_mapping`;
}
