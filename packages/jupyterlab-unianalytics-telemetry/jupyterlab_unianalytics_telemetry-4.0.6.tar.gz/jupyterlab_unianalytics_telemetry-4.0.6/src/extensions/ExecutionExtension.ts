import { DocumentRegistry } from '@jupyterlab/docregistry';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import {
  INotebookModel,
  NotebookPanel,
  NotebookActions,
  Notebook
} from '@jupyterlab/notebook';
import { JSONExt, JSONObject } from '@lumino/coreutils';
import { IDisposable } from '@lumino/disposable';
import { Signal } from '@lumino/signaling';
import { Cell, CodeCell, MarkdownCell } from '@jupyterlab/cells';
import { processCellOutput } from '../utils/utils';
import { EXTENSION_SETTING_NAME } from '../utils/constants';
import { postCodeExec, postMarkdownExec } from '../api';
import { Selectors } from '../utils/constants';
import { isNotebookValid } from '../utils/utils';
import { CompatibilityManager } from '../utils/compatibility';

export class ExecutionExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  constructor(settings: ISettingRegistry.ISettings) {
    this._settings = settings;
  }

  createNew(panel: NotebookPanel) {
    return new ExecutionDisposable(panel, this._settings);
  }

  private _settings: ISettingRegistry.ISettings;
}

class ExecutionDisposable implements IDisposable {
  constructor(panel: NotebookPanel, settings: ISettingRegistry.ISettings) {
    this._panel = panel;

    this._updateSettings(settings);
    settings.changed.connect(this._updateSettings.bind(this));

    panel.context.ready.then(() => {
      const notebookTags = isNotebookValid(panel);
      if (notebookTags) {
        this._notebookId = notebookTags.notebookId;
        this._instanceId = notebookTags.instanceId;

        // connect to cell execution
        NotebookActions.executed.connect(this._onCellExecuted, this);

        panel.disposed.connect(() =>
          NotebookActions.executed.disconnect(this._onCellExecuted, this)
        );
      }
    });
  }

  private _updateSettings(settings: ISettingRegistry.ISettings) {
    this._isSettingEnabled = settings.get(EXTENSION_SETTING_NAME)
      .composite as boolean;
  }

  private _onCellExecuted(
    sender: any,
    args: { notebook: Notebook; cell: Cell }
  ) {
    if (this._isSettingEnabled) {
      const { notebook, cell } = args;

      // only track the executions of the current panel instance
      if (notebook !== this._panel.content) {
        return;
      }
      if (cell instanceof CodeCell) {
        const executionMetadata = CompatibilityManager.getMetadataComp(
          cell.model,
          'execution'
        ) as JSONObject;
        if (executionMetadata && JSONExt.isObject(executionMetadata)) {
          const startTimeStr = (executionMetadata[
            'shell.execute_reply.started'
          ] || executionMetadata['iopub.execute_input']) as string | null;
          const endTimeStr = executionMetadata['shell.execute_reply'] as
            | string
            | null;
          const executionAborted =
            endTimeStr && !executionMetadata['iopub.execute_input'];

          if (!executionAborted) {
            if (endTimeStr && startTimeStr) {
              const outputs = cell.model.outputs.toJSON();
              const notebookModel = this._panel.model;
              const { status, cell_output_length } = processCellOutput(outputs);
              const orig_cell_id: string | undefined =
                CompatibilityManager.getMetadataComp(
                  notebookModel,
                  Selectors.cellMapping
                )?.find(([key]: [key: string]) => key === cell.model.id)?.[1];

              if (orig_cell_id) {
                postCodeExec({
                  notebook_id: this._notebookId as string,
                  instance_id: this._instanceId as string,
                  language_mimetype:
                    CompatibilityManager.getMetadataComp(
                      notebookModel,
                      'language_info'
                    )['mimetype'] || 'text/plain',
                  cell_id: cell.model.id,
                  orig_cell_id: orig_cell_id,
                  t_start: startTimeStr,
                  t_finish: endTimeStr,
                  status: status,
                  cell_input: cell.model.sharedModel.getSource(),
                  cell_output_model: outputs,
                  cell_output_length: cell_output_length
                });
              }
            }
          }
        }
      } else if (cell instanceof MarkdownCell) {
        const orig_cell_id: string | undefined =
          CompatibilityManager.getMetadataComp(
            this._panel.model,
            Selectors.cellMapping
          )?.find(([key]: [key: string]) => key === cell.model.id)?.[1];

        if (orig_cell_id) {
          postMarkdownExec({
            notebook_id: this._notebookId as string,
            instance_id: this._instanceId as string,
            cell_id: cell.model.id,
            orig_cell_id: orig_cell_id,
            time: new Date().toISOString(),
            cell_content: cell.model.sharedModel.getSource()
          });
        }
      }
    }
  }

  get isDisposed(): boolean {
    return this._isDisposed;
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }

    this._isDisposed = true;
    this._notebookId = null;
    this._instanceId = null;

    Signal.clearData(this);
  }

  private _panel: NotebookPanel;
  private _isDisposed = false;
  private _notebookId: string | null = null;
  private _instanceId: string | null = null;
  private _isSettingEnabled = false;
}
