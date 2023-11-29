"""Convert a set of waveforms into the dataset object."""
from pathlib import Path


from dandelion_data_schema.utils import load_dicom_folder

# assumes data is in a folder in the base repo
DATA_FOLDER = Path(__file__).parent.parent / 'data/luna16'
OUTPUT_FOLDER = Path(__file__).parent.parent / 'data/dicom_json_dataset'

def main():
    # set folders for input/output
    data_folder = DATA_FOLDER
    output_folder = OUTPUT_FOLDER
    output_folder.mkdir(exist_ok=True)

    # get list of directories in the data folder
    # assuming DICOM files stored in a folder
    for dicom_folder in data_folder.glob('**/'):
        # skip current dir
        if dicom_folder == data_folder:
            continue
        record = load_dicom_folder(dicom_folder)

        # save the record to json
        record_name = dicom_folder.name
        output_filename = output_folder / f'{record_name}.json'

        json_str = record.model_dump_json(indent=2)
        with open(output_filename, 'w') as fp:
            fp.write(json_str)

if __name__ == '__main__':
    main()