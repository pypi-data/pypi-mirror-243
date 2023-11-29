import { NotebookPanel } from '@jupyterlab/notebook';
import { isNotebookValid } from '../utils/utils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { WebsocketManager } from './WebsocketManager';

export class PanelManager {
  constructor(settings: ISettingRegistry.ISettings) {
    this._panel = null;

    this._websocketManager = new WebsocketManager(settings);
  }

  get panel(): NotebookPanel | null {
    return this._panel;
  }

  set panel(value: NotebookPanel | null) {
    if (value && this._panel && this._panel === value) {
      return;
    }

    if (this._panel) {
      this._panel.disposed.disconnect(this._onPanelDisposed, this);
    }

    // remove the websocket connection if there's one
    this._websocketManager.terminateSocketConnection();

    this._panel = value;

    if (this._panel) {
      this._panel.disposed.connect(this._onPanelDisposed, this);
    }

    // if there is no panel, return...
    if (!this._panel) {
      return;
    }

    // to make sure the panel hasn't changed by the time the context is ready
    const scopeId = crypto.randomUUID();
    this._ongoingContextId = scopeId;
    // wait for the panel session context to be ready for the metadata to be available
    this._panel.sessionContext.ready.then(() => {
      if (
        this._ongoingContextId === scopeId &&
        this._panel &&
        !this._panel.isDisposed
      ) {
        // check if notebook is tagged
        const notebookTags = isNotebookValid(this._panel);
        if (notebookTags) {
          // notebookTags is { notebookId, instanceId }
          this._websocketManager.establishSocketConnection(notebookTags);
        }
      }
    });
  }

  private _onPanelDisposed(_panel: NotebookPanel) {
    // when the panel is disposed, dispose from the panel (calling the _panel setter)
    this.panel = null;
  }

  private _panel: NotebookPanel | null;
  private _ongoingContextId = '';
  private _websocketManager: WebsocketManager;
}
