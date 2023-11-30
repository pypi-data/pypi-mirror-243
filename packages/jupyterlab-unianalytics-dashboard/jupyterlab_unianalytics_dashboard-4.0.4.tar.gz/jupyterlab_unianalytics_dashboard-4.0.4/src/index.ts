import {
  ILabShell,
  ILayoutRestorer,
  JupyterFrontEndPlugin,
  JupyterFrontEnd
} from '@jupyterlab/application';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

//importing bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';
import { APP_ID, BACKEND_API_URL, PLUGIN_ID } from './utils/constants';
import { compareVersions } from './utils/utils';
import { activateUploadNotebookPlugin } from './plugins/uploadNotebook';
import { activateDashboardPlugins } from './plugins/dashboards';
import { CompatibilityManager } from './utils/compatibility';
import { getUserIdFromEnv } from './utils/utils';

export const DASHBOARD_USER_ID = crypto.randomUUID();

const activate = (
  app: JupyterFrontEnd,
  factory: IFileBrowserFactory,
  restorer: ILayoutRestorer,
  labShell: ILabShell,
  rendermime: IRenderMimeRegistry,
  settingRegistry: ISettingRegistry
): void => {
  console.log(`JupyterLab extension ${APP_ID} is activated!`);

  const targetVersion = '3.1.0';
  const appNumbers = app.version.match(/[0-9]+/g);

  if (appNumbers && compareVersions(app.version, targetVersion) >= 0) {
    const jupyterVersion = parseInt(appNumbers[0]);

    CompatibilityManager.setJupyterVersion(jupyterVersion).then(() => {
      // read the userId from the environment variables, userId is '' if not defined
      getUserIdFromEnv(app, 'JUPYTERHUB_USER')
        .then((userId: string) => {
          // authenticate the user and only activate the plugins if the user is logged in
          fetch(`${BACKEND_API_URL}/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Unianalytics-User-Id': userId
            },
            credentials: 'include'
          })
            .then(loginResponse => {
              if (loginResponse.ok) {
                loginResponse
                  .json()
                  .then(loginJSON => {
                    if (loginJSON.status === 'logged_in') {
                      activateUploadNotebookPlugin(app, factory);

                      activateDashboardPlugins(
                        app,
                        restorer,
                        labShell,
                        settingRegistry,
                        rendermime
                      );

                      return;
                    } else {
                      console.log(`${APP_ID}: User not authenticated`);
                    }
                  })
                  .catch(error =>
                    console.log(`${APP_ID}: Authentication error, ${error}`)
                  );
              } else {
                console.log(`${APP_ID}: Unauthorized user`);
              }
            })
            .catch(error =>
              console.log(`${APP_ID}: Authentication error, ${error}`)
            );
        })
        .catch(error =>
          console.log(`${APP_ID}: Failed to access the userId, ${error}`)
        );
    });
  } else {
    console.log(
      `${APP_ID}: Use a more recent version of JupyterLab (>=${targetVersion})`
    );
  }
};

const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [
    IFileBrowserFactory,
    ILayoutRestorer,
    ILabShell,
    IRenderMimeRegistry,
    ISettingRegistry
  ],
  optional: [],
  activate: activate
};

export default plugin;
