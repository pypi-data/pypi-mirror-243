import { Signal } from '@lumino/signaling';
import { IDisposable } from '@lumino/disposable';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { Cell, ICellModel } from '@jupyterlab/cells';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { postNotebookClick, postCellClick } from '../api';
import { LabShell } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { EXTENSION_SETTING_NAME, Selectors } from '../utils/constants';
import { isNotebookValid } from '../utils/utils';
import { CompatibilityManager } from '../utils/compatibility';
import { Dialog, showDialog } from '@jupyterlab/apputils';

type ClickType = 'OFF' | 'ON';

export class FocusExtension implements DocumentRegistry.WidgetExtension {
  constructor(
    labShell: LabShell,
    settings: ISettingRegistry.ISettings,
    dialogShownSettings: ISettingRegistry.ISettings
  ) {
    this._labShell = labShell;
    this._settings = settings;
    this._dialogShownSettings = dialogShownSettings;
  }

  createNew(panel: NotebookPanel): IDisposable {
    return new FocusDisposable(
      panel,
      this._labShell,
      this._settings,
      this._dialogShownSettings
    );
  }

  private _labShell: LabShell;
  private _settings: ISettingRegistry.ISettings;
  private _dialogShownSettings: ISettingRegistry.ISettings;
}

class FocusDisposable implements IDisposable {
  constructor(
    panel: NotebookPanel,
    labShell: LabShell,
    settings: ISettingRegistry.ISettings,
    dialogShownSettings: ISettingRegistry.ISettings
  ) {
    this._panel = panel;

    this._updateSettings(settings);
    settings.changed.connect(this._updateSettings.bind(this));

    panel.context.ready.then(() => {
      const notebookTags = isNotebookValid(panel);
      if (notebookTags) {
        // prompt the user with a dialog box to enable/disable the extension (opt-in)
        this.showConsentDialogPromise(settings, dialogShownSettings).then(
          () => {
            if (panel && !panel.isDisposed) {
              this._notebookId = notebookTags.notebookId;
              this._instanceId = notebookTags.instanceId;

              // call it a first time after the panel is ready to send missed start-up signals
              this._onCellChanged(panel.content, panel.content.activeCell);
              this._onNotebookChanged(labShell);

              // connect to active cell changes
              panel.content.activeCellChanged.connect(
                this._onCellChanged,
                this
              );

              // connect to panel changes
              labShell.currentChanged.connect(this._onNotebookChanged, this);

              // panel.content is disposed before panel itself, so release the associated connection before
              panel.content.disposed.connect(this._onContentDisposed, this);
            }
          }
        );
      }
    });
  }

  private async showConsentDialogPromise(
    settings: ISettingRegistry.ISettings,
    dialogShownSettings: ISettingRegistry.ISettings
  ) {
    // setting only used to persist over sessions if the Dialog box has ever been shown
    const dialogShown = dialogShownSettings.get('DialogShown')
      .composite as boolean;

    // simply go through if the consent box has been show before
    if (dialogShown) {
      return;
    } else {
      const result = await showDialog({
        title: 'Unianalytics Data',
        // to disable the user from clicking away or pressing ESC to cancel the Dialog box
        hasClose: false,
        body: 'Enable anonymous collection of interaction data in specific notebooks to make it easier for your teacher(s) to support your learning?',
        buttons: [
          Dialog.okButton({ label: 'Yes' }),
          Dialog.cancelButton({ label: 'No' })
        ]
      });

      // update the setting to indicate that the dialog has been shown and should not be show again
      await dialogShownSettings.set('DialogShown', true);

      let isEnabled = false;
      if (result.button.accept) {
        // user clicked 'Yes', enable the data collection
        await settings.set(EXTENSION_SETTING_NAME, true);
        isEnabled = true;
      } else {
        // user clicked 'No', disable the data collection
        await settings.set(EXTENSION_SETTING_NAME, false);
        isEnabled = false;
      }
      // setting update might happen after the first cell and notebook clicks are sent, so call the update directly
      this._isSettingEnabled = isEnabled;
    }
  }

  private _updateSettings(settings: ISettingRegistry.ISettings) {
    this._isSettingEnabled = settings.get(EXTENSION_SETTING_NAME)
      .composite as boolean;
  }

  private _onContentDisposed = (content: Notebook) => {
    content.activeCellChanged.disconnect(this._onCellChanged, this);
    // directly release the content.disposed connection
    content.disposed.disconnect(this._onContentDisposed, this);
  };

  private _onCellChanged = (
    content: Notebook,
    activeCell: Cell<ICellModel> | null
  ) => {
    this._sendCellClick('OFF');

    // change both the id of the last active cell and the corresponding orig cell id
    this._setActiveCellAndOrigCellId(activeCell);

    if (this._focusON) {
      this._sendCellClick('ON');
    }
  };

  private _setActiveCellAndOrigCellId = (
    activeCell: Cell<ICellModel> | null
  ) => {
    this._lastActiveCellId = activeCell?.model.sharedModel.getId();
    if (this._lastActiveCellId) {
      this._lastOrigCellId = CompatibilityManager.getMetadataComp(
        this._panel?.model,
        Selectors.cellMapping
      )?.find(([key]: [key: string]) => key === this._lastActiveCellId)?.[1];
    } else {
      this._lastOrigCellId = null;
    }
  };

  private _onNotebookChanged = (_labShell: LabShell) => {
    if (_labShell.currentWidget === this._panel) {
      this._isActive = true;
      // send ON message only if it's still active by the time the panel is ready (and if it's not already focused on)

      if (!this.isDisposed) {
        if (this._isActive && !this._focusON) {
          this._sendNotebookClick('ON');
          this._sendCellClick('ON');
          this._focusON = true;
        }
      }
    } else {
      // check if there was focus on that notebook
      if (this._focusON) {
        this._sendNotebookClick('OFF');
        this._sendCellClick('OFF');
      }
      this._focusON = false;
      this._isActive = false;
    }
  };

  private _sendCellClick = (clickType: ClickType) => {
    if (this._lastActiveCellId && this._isSettingEnabled) {
      let cellDurationSec: number | null = null;
      if (clickType === 'ON') {
        this._cellStart = new Date();
        cellDurationSec = null;
      } else {
        const cellEnd = new Date();
        cellDurationSec =
          (cellEnd.getTime() - this._cellStart.getTime()) / 1000;
      }

      if (this._lastOrigCellId) {
        postCellClick({
          notebook_id: this._notebookId as string,
          instance_id: this._instanceId as string,
          cell_id: this._lastActiveCellId,
          orig_cell_id: this._lastOrigCellId,
          click_type: clickType,
          time: new Date().toISOString(),
          click_duration: cellDurationSec
        });
      }
    }
  };

  private _sendNotebookClick = (clickType: ClickType) => {
    if (this._isSettingEnabled) {
      let notebookDurationSec: number | null = null;
      if (clickType === 'ON') {
        this._notebookStart = new Date();
        notebookDurationSec = null;
      } else {
        const notebookEnd = new Date();
        notebookDurationSec =
          (notebookEnd.getTime() - this._notebookStart.getTime()) / 1000;
      }

      postNotebookClick({
        notebook_id: this._notebookId as string,
        instance_id: this._instanceId as string,
        click_type: clickType,
        time: new Date().toISOString(),
        click_duration: notebookDurationSec
      });
    }
  };

  get isDisposed(): boolean {
    return this._isDisposed;
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }

    if (this._focusON) {
      this._sendNotebookClick('OFF');
      this._sendCellClick('OFF');
    }

    this._focusON = false;
    this._isActive = false;
    this._isDisposed = true;
    this._panel = null;
    this._notebookId = null;
    this._instanceId = null;
    this._lastActiveCellId = null;

    Signal.clearData(this);
  }

  private _focusON = false;
  private _isActive = false;
  private _isDisposed = false;
  private _panel: NotebookPanel | null;
  private _isSettingEnabled = false;
  private _notebookId: string | null = null;
  private _instanceId: string | null = null;
  private _lastActiveCellId: string | null | undefined = null;
  private _lastOrigCellId: string | null | undefined = null;

  private _notebookStart: Date = new Date();
  private _cellStart: Date = new Date();
}
