interface IProcess {
    env: {
        API_LOCATION: string,
        NODE_ENV: string
    }
}

declare const process: IProcess;
declare const tinymce: any;
