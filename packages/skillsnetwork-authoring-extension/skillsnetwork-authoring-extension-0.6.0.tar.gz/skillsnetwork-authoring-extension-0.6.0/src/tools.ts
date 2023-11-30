/* eslint-disable @typescript-eslint/ban-types */
import { AxiosError } from 'axios';
import { Cell, ICellModel } from '@jupyterlab/cells';
import {
  INotebookModel,
  NotebookPanel
} from '@jupyterlab/notebook';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { ContentsManager, Contents } from '@jupyterlab/services';
import * as nbformat from '@jupyterlab/nbformat';
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { Globals } from './config';
import { axiosHandler, getLabModel, awbAxiosHandler, getIndependentLabModel} from './handler';

export interface ICellData {
  cell_type: string;
  id: string;
  metadata: {};
  outputs: [];
  source: string[];
}
export interface IPynbRaw {
  cells: ICellData[];
  metadata: {};
  nbformat: number;
  nbformat_minor: number;
}

/**
 * Extracts the relevant data from the cells of the notebook
 *
 * @param cell Cell model
 * @returns ICellData object
 */
export const getCellContents = (cell: Cell<ICellModel>): ICellData => {
  const cellData: ICellData = {
    cell_type: cell.model.type,
    id: cell.model.id,
    metadata: {},
    outputs: [],
    source: [cell.model.value.text]
  };
  return cellData;
};

/**
 * Extracts the relevant data from the cells of the notebook but omit ID
 *
 * @param cell Cell model
 * @returns ICellData object without ID
 */
export const getCellContentsOmitID = (cell: Cell<ICellModel>): ICellData => {
  const cellData: ICellData = {
    cell_type: cell.model.type,
    id: "",
    metadata: {},
    outputs: [],
    source: [cell.model.value.text]
  };
  return cellData;
};

/**
 * Gets the raw data (cell models and content, notebook configurations) from the .ipynb file
 *
 * @param panel Notebook panel
 * @param context Notebook context
 */
export const getFileContents = (
  panel: NotebookPanel,
  context: DocumentRegistry.IContext<INotebookModel>
): string => {
  // Cell types: "code" | "markdown" | "raw"
  const allCells: any[] = [];
  panel.content.widgets.forEach((cell: Cell<ICellModel>) => {
    const cellData = getCellContents(cell);
    allCells.push(cellData);
  });

  // Get the configs from the notebook model
  const config_meta = context.model.metadata.toJSON();
  const config_nbmajor = context.model.nbformat;
  const config_nbminor = context.model.nbformatMinor;

  // Put all data into IPynbRaw object
  const rawFile: IPynbRaw = {
    cells: allCells,
    metadata: config_meta,
    nbformat: config_nbmajor,
    nbformat_minor: config_nbminor
  };
  return JSON.stringify(rawFile, null, 2);
};

/**
 * Updates the file with its commit ID
 *
 * @param panel Notebook panel
 * @param context Notebook context
 */
export async function updateLabCommitID(
  panel: NotebookPanel,
  context: DocumentRegistry.IContext<INotebookModel>,
) : Promise<void> {
  const fileCells : string = await getFileCellContentsOmitID(panel, context)
  const commitID = await generateHash(fileCells);

  await context.ready;

  context.model.metadata.set(Globals.PREV_PUB_HASH, commitID);

  // Save the notebook to persist the changes
  context.save().then(() => {
    console.log("Notebook saved with updated metadata.");
  }).catch(err => {
    console.error("Failed to save notebook:", err);
  });
}

/**
 * Defines the expected structure of lab content.
 */
interface LabContent {
  metadata?: {
    [key: string]: string | object | undefined;
  };
  content?: {
    metadata?: {
      [key: string]: string | object | undefined;
    };
  };
}

/**
 * Updates the file with its commit ID
 *
 * @param panel Notebook panel
 * @param context Notebook context
 */
export function getLabCommitID(labContent: LabContent) : string {
  if (typeof(labContent) === 'string'){
    labContent = JSON.parse(labContent);
  }
  // check if labContent has the expected structure
  if (
    typeof(labContent) !== "object" || 
    labContent === null || 
    (!("metadata" in labContent) && !("content" in labContent))
    ) {
    console.error("Lab content is of unknown type: ", typeof(labContent), "\n Value: \n", labContent);
    return "";
  } 
  
  // Attempt to retrive commitID from either metadata or content.metadata
  const commitID = labContent.metadata?.[Globals.PREV_PUB_HASH]?.toString() ??
    labContent.content?.metadata?.[Globals.PREV_PUB_HASH]?.toString() ??
    "";

  return commitID;
}

/**
 * Gets the raw data (cell models and content, notebook configurations) from the .ipynb file
 *
 * @param panel Notebook panel
 * @param context Notebook context
 */
export const getFileCellContentsOmitID = (
  panel: NotebookPanel,
  context: DocumentRegistry.IContext<INotebookModel>
): string => {
  // Cell types: "code" | "markdown" | "raw"
  const allCells: any[] = [];
  panel.content.widgets.forEach((cell: Cell<ICellModel>) => {
    const cellData = getCellContentsOmitID(cell);
    allCells.push(cellData);
  });

  return JSON.stringify(allCells, null, 2);
};



export const openIndependentLab = async (awb_token: string, docManager: IDocumentManager, contentsManager: ContentsManager): Promise<NotebookPanel> => {
  let {labFilename, body: instructions_content} = await getIndependentLabModel(awbAxiosHandler(awb_token), awb_token);

  await checkAndBackupSaveFile(labFilename, instructions_content, contentsManager, docManager);

  // Set the publish button to only show for the lab with title labFilename
  Globals.SHOW_PUBLISH_BUTTON_FOR = labFilename;
  // Set the publish button to only work for the lab with title labFilename
  Globals.TOKENS.set(labFilename, awb_token);

  const prevFile: Contents.IModel | null = await getFile(`./${labFilename}`, contentsManager);
  let nbPanel: NotebookPanel | undefined;
  if (!prevFile) {
    nbPanel = docManager.createNew(labFilename, 'notebook', { name:  Globals.PY_KERNEL_NAME}) as NotebookPanel;
    if (nbPanel === undefined) {
      throw Error('Error loading lab')
    }
    await loadLabContents(nbPanel, instructions_content as unknown as nbformat.INotebookContent);
  } else {
    nbPanel = docManager.openOrReveal(labFilename) as NotebookPanel;
  }

  return nbPanel;
}

/**
 * Renames a file to filename.backup.ipynb and overwrites any files with the same name.
 * 
 * @param {string} labFilename - Path to string.
 * @param {LabContent} instructions_content - Lab instructions
 * @param {ContentsManager} contentsManager - The JupyterLab contents manager.
 * @returns {Promise<void>} - Returns nothing
 */
async function checkAndBackupSaveFile(labFilename: string, instructions_content: LabContent, contentsManager: ContentsManager, docManager: IDocumentManager): Promise<void> {
  const prevFile: Contents.IModel | null = await getFile(`./${labFilename}`, contentsManager);
  if (prevFile) {
    const currCommitID = getLabCommitID(instructions_content); 
    const prevCommitID = getLabCommitID(prevFile); 
    if (currCommitID !== prevCommitID) {
      await convertFileToBackup(prevFile, contentsManager, docManager);
      await showDialog({
        title: 'Your Lab was Updated',
        body: `The newest published version of "${labFilename}" is loaded. Your previous version has been backed up under "${labFilename}${Globals.BACKUP_EXT}.ipynb"`,
        buttons: [Dialog.okButton({ label: 'Dismiss' })]
      });
    }
  }
}


export const openLab = async (token: string, docManager: IDocumentManager, contentsManager: ContentsManager): Promise<NotebookPanel> => {
  let {instructions_file_path, body: instructions_content} = await getLabModel(axiosHandler(token))
  const labFilename = getLabFileName(instructions_file_path);
  await checkAndBackupSaveFile(labFilename, instructions_content, contentsManager, docManager);

  // Set the publish button to only show for the lab with title labFilename
  Globals.SHOW_PUBLISH_BUTTON_FOR = labFilename;
  // Set the publish button to only work for the lab with title labFilename
  Globals.TOKENS.set(labFilename, token);

  const prevFile: Contents.IModel | null = await getFile(`./${labFilename}`, contentsManager);
  let nbPanel: NotebookPanel | undefined;
  if (!prevFile) {
    nbPanel = docManager.createNew(labFilename, 'notebook', { name:  Globals.PY_KERNEL_NAME}) as NotebookPanel;
    if (nbPanel === undefined) {
      throw Error('Error loading lab')
    }
    await loadLabContents(nbPanel, JSON.parse(instructions_content) as unknown as nbformat.INotebookContent);
  } else {
    nbPanel = docManager.openOrReveal(labFilename) as NotebookPanel;
  }
  
  return nbPanel;
}

export const loadLabContents = async (widget: NotebookPanel, notebook_content : nbformat.INotebookContent, author_env?: string): Promise<void> => {
  // Wait for widget to initalize correctly before making changes
  await widget.context.ready;

  if (author_env !== 'local') {    
    if (widget.context && widget.context.model) {
      // Load content
      widget.context.model.fromJSON(notebook_content);
      // Save content 
      try {

        // TODO: Minor Bug that can confuse user - after loading and saving, 
        // user is still prompted to save because JLabs updates the saved ipynb's metadata 
        await widget.context.save();
      } catch(error) {
        console.error("Error saving notebook:", error);
      }
    } else {
      console.error('Notebook model is not initialized.');
    }
  }
};

export const getLabFileName = (lab_filepath: any): string => {
  let labFilePath = lab_filepath ?? Globals.DEFAULT_LAB_NAME;
  // Extract filename from filepath
  // TODO: This is required as the createNew method will not automatically create the parent directories
  return labFilePath.replace(/^.*[\\\/]/, '');
}

/**
 * Renames a file to filename.backup.ipynb and overwrites any files with the same name.
 * 
 * @param {string} path - path to string.
 * @param {ContentsManager} contentsManager - The JupyterLab contents manager.
 * @returns {Promise<IModel | null>} - Returns the file or null
 */
async function getFile(path: string, contentsManager: ContentsManager) : Promise<Contents.IModel | null> {
  try {
    return await contentsManager.get(path);
  } catch (error) {
    if (error instanceof Error) {
      
      const axiosError = error as AxiosError;
      
      // Check if the error is because the file doesn't exist
      if (axiosError.response && axiosError.response.status !== 404) {
        // If the error is not a 404 error, log it and throw it
        console.error("Error checking for existent backup file: ", error);
        throw error;
      } else {
        return null;
      }
    } else {
      // If not an error object, throw it and handle appropriately outside

      console.error("Unexpected error occured: ", error);
      throw error;
    }
  }
}

/**
 * Function that saves and close open widgets
 *
 * @param docManager - The JupyterLab document manager.
 * @param oldPath - The old path of the file.
 * @param newPath - The new path of the file.
 */
async function saveAndCloseOpenFiles(docManager: IDocumentManager, path: string): Promise<void> {
  const widget = docManager.findWidget(path);
  if (widget) {
    try {
      // Save the content of the widget
      if(widget.context.model.dirty){
        await widget.context.save();
      }
    } catch (error) {
      console.error("Error saving widget content:", error);
      // Handle error appropriately
    }

    // Close the widget
    widget.close();
  }
}

/**
 * Takes a file and renames it filename.backup and overwrite any files with the same name
 * 
 * @param {Contents.IModel} file - The file model to rename
 * @param {IContents.Manager} contentsManager - The JupyterLab contents manager.
 * @returns {Promise<void>} - returns after file is renamed
 */
async function convertFileToBackup(file: Contents.IModel, contentsManager: ContentsManager, docManager: IDocumentManager) : Promise<void> {
  const prevPath = file.path;
  const fileExt = prevPath.split('.').pop();

  // removes the last portion of the string, separated by the last dot
  const fileNameWithoutExt = prevPath.replace(/\.[^/.]+$/, "");
  
  const newPath = `${fileNameWithoutExt}${Globals.BACKUP_EXT}.${fileExt}`;
  const prevFile = await getFile(newPath, contentsManager);
  
  if (prevFile) {
    try {
      await contentsManager.delete(newPath);
    } catch (error) {
      console.error("Unexpected error occured: ", error);
    }
  }

  try {
    // Saving and closing opened files to remove the sn-publish button
    await saveAndCloseOpenFiles(docManager, prevPath);
    await contentsManager.rename(prevPath, newPath);
  } catch (error) {
    console.error("Unexpected error occured: ", error);
  }
}

export async function generateHash(data : string ) : Promise<string> {
  const encoder = new TextEncoder();
  const dataBuffer = encoder.encode(data);

  // Use the Web Crypto API to compute the SHA-256 hash of the binary data.
  const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);

  return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
}

// eslint-disable-next-line @typescript-eslint/quotes
export const DEFAULT_CONTENT: nbformat.INotebookContent = {
  cells: [
    {
      cell_type: 'code',
      id: 'c852569f-bf26-4994-88e7-3b94874d3853',
      metadata: {},
      source: ['print("hello world again")']
    },
    {
      cell_type: 'markdown',
      id: '5a2dc856-763a-4f12-b675-481ed971178a',
      metadata: {},
      source: ['this is markdown']
    },
    {
      cell_type: 'raw',
      id: '492a02e8-ec75-49f7-8560-b30256bca6af',
      metadata: {},
      source: ['this is raw']
    }
  ],
  metadata: {
    kernelspec: {
      display_name: 'Python 3 (ipykernel)',
      language: 'python',
      name: 'python3'
    },
    language_info: {
      codemirror_mode: { name: 'ipython', version: 3 },
      file_extension: '.py',
      mimetype: 'text/x-python',
      name: 'python',
      nbconvert_exporter: 'python',
      pygments_lexer: 'ipython3',
      version: '3.10.4'
    }
  },
  nbformat: 4,
  nbformat_minor: 5
};
