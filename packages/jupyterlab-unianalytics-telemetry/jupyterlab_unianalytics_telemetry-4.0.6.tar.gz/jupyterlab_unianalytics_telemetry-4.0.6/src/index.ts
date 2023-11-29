import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  LabShell
} from '@jupyterlab/application';
import { FocusExtension } from './extensions/FocusExtension';
import { ExecutionExtension } from './extensions/ExecutionExtension';
import { AlterationExtension } from './extensions/AlterationExtension';
import { InstanceInitializer } from './extensions/InstanceInitializer';
import { CellMappingExtension } from './extensions/CellMappingExtension';
import { PLUGIN_ID } from './utils/constants';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { NotebookPanel } from '@jupyterlab/notebook';
import { compareVersions } from './utils/utils';

import { LabIcon } from '@jupyterlab/ui-components';
// to register the svg icon to reuse it in the settings (through schema/settings.json > jupyter.lab.setting-icon)
import schemaStr from '../style/icons/dataCollection_cropped.svg';
import { PanelManager } from './websocket/PanelManager';
import { CompatibilityManager } from './utils/compatibility';

export const schemaIcon = new LabIcon({
  name: `${PLUGIN_ID}:schema-icon`,
  svgstr: schemaStr
});

const activate = (
  app: JupyterFrontEnd,
  settingRegistry: ISettingRegistry
): void => {
  console.log(`JupyterLab extension ${PLUGIN_ID} is activated!`);

  const targetVersion = '3.1.0';
  const appNumbers = app.version.match(/[0-9]+/g);

  if (appNumbers && compareVersions(app.version, targetVersion) >= 0) {
    const jupyterVersion = parseInt(appNumbers[0]);

    CompatibilityManager.setJupyterVersion(jupyterVersion);

    // // adds an instance_id to the notebook
    app.docRegistry.addWidgetExtension('Notebook', new InstanceInitializer());

    // // updates the notebook metadata to track the current-to-original notebook cell id mapping
    app.docRegistry.addWidgetExtension('Notebook', new CellMappingExtension());

    settingRegistry
      .load(`${PLUGIN_ID}:settings`)
      .then((settings: ISettingRegistry.ISettings) => {
        const labShell = app.shell as LabShell;

        // FocusExtension implements the opt-in dialog box so it should be registered first
        settingRegistry
          .load(`${PLUGIN_ID}:dialogShownSettings`)
          .then((dialogShownSettings: ISettingRegistry.ISettings) => {
            // notebook widget extension with notebook ON/OFF + cell ON/OFF messaging
            app.docRegistry.addWidgetExtension(
              'Notebook',
              new FocusExtension(labShell, settings, dialogShownSettings)
            );

            // notebook widget extension with cell insertion/deletion messaging
            app.docRegistry.addWidgetExtension(
              'Notebook',
              new AlterationExtension(settings)
            );

            // to retrieve execution start/finish times, activate the independent setting that write the cell execution info to the cell metadata
            settingRegistry
              .load('@jupyterlab/notebook-extension:tracker')
              .then((nbTrackerSettings: ISettingRegistry.ISettings) => {
                nbTrackerSettings.set('recordTiming', true).then(() => {
                  // notebook widget extension with code and markdown cell execution messaging
                  app.docRegistry.addWidgetExtension(
                    'Notebook',
                    new ExecutionExtension(settings)
                  );

                  const panelManager = new PanelManager(settings);

                  // update the panel when the active widget changes
                  if (labShell) {
                    labShell.currentChanged.connect(() =>
                      onConnect(labShell, panelManager)
                    );
                  }

                  // connect to current widget
                  void app.restored.then(() => {
                    onConnect(labShell, panelManager);
                  });
                });
              })
              .catch(error =>
                console.log(
                  `${PLUGIN_ID}: Could not force cell execution metadata recording: ${error}`
                )
              );
          });
      })
      .catch(error =>
        console.log(`${PLUGIN_ID}: Could not load settings, error: ${error}`)
      );
  } else {
    console.log(`Use a more recent version of JupyterLab (>=${targetVersion})`);
  }
};

function onConnect(labShell: LabShell, panelManager: PanelManager) {
  const widget = labShell.currentWidget;
  if (!widget) {
    return;
  }
  // only proceed if the new widget is a notebook panel
  if (!(widget instanceof NotebookPanel)) {
    // if the previously used widget is still available, stick with it.
    // otherwise, set the current panel to null.
    if (panelManager.panel && panelManager.panel.isDisposed) {
      panelManager.panel = null;
    }
    return;
  }
  const notebookPanel = widget as NotebookPanel;
  panelManager.panel = notebookPanel;
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: `${PLUGIN_ID}:plugin`,
  autoStart: true,
  requires: [ISettingRegistry],
  activate: activate
};

export default plugin;
