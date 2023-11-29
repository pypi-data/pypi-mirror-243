const LOCAL_DEV = false;

export let BACKEND_API_URL: string, WEBSOCKET_API_URL: string;
if (LOCAL_DEV) {
  BACKEND_API_URL = 'http://localhost:5000/send/';
  WEBSOCKET_API_URL = 'ws://localhost:1337/ws';
} else {
  BACKEND_API_URL = 'https://api.unianalytics.ch/send/';
  WEBSOCKET_API_URL =
    'wss://ax5pzl8bwk.execute-api.eu-north-1.amazonaws.com/production/';
}

export const PLUGIN_ID = 'jupyterlab_unianalytics_telemetry';

export const MAX_PAYLOAD_SIZE = 1048576; // 1*1024*1024 => 1Mb

export const POST_TOKEN = '407b1e36627f49f28fe51d06233d9765';

export const EXTENSION_SETTING_NAME = 'SendExtension';

export const UNIANALYTICS_COOKIE_NAME = 'unianalytics-notebook-user-ids';

// notebook metadata field names
const SELECTOR_ID = 'unianalytics';
export namespace Selectors {
  export const notebookId = `${SELECTOR_ID}_notebook_id`;

  export const instanceId = `${SELECTOR_ID}_instance_id`;

  export const cellMapping = `${SELECTOR_ID}_cell_mapping`;
}

export namespace CommandIDs {
  export const dashboardOpenChat = `${PLUGIN_ID}:unianalytics-open-chat`;
}
