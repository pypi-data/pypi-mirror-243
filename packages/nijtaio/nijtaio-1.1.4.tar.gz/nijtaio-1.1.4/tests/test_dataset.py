"""Test the creation of datasets objects from different inputs."""
import datasets
import nijtaio


def test_create_dataset_from_one_file():
    """Test the creation of a dataset from a single file."""
    dataset = nijtaio._create_dataset('samples/e0003.wav')
    assert isinstance(dataset, datasets.DatasetDict)
    assert dataset['train'].num_rows == 1


def test_create_dataset_from_a_list_of_files():
    """Test the creation of a dataset from a list of files."""
    dataset = nijtaio._create_dataset(['samples/e0003.wav'])
    assert isinstance(dataset, datasets.DatasetDict)
    assert dataset['train'].num_rows == 1


def test_create_dataset_from_a_dir():
    """Test the creation of a dataset from a directory."""
    dataset: datasets.DatasetDict = nijtaio._create_dataset('samples/')
    assert isinstance(dataset, datasets.DatasetDict)
    assert dataset['train'].num_rows == 1
