import { IChartForExport } from "@kanaries/graphic-walker/dist/interfaces";
export declare function usePythonCode(props: {
    sourceCode: string;
    specList: IChartForExport[];
    version: string;
}): {
    pyCode: string;
};
